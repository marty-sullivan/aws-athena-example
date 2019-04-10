import matplotlib
matplotlib.use('agg')

import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from boto3.session import Session
from datetime import datetime
from mpl_toolkits.basemap import Basemap
from os import environ, remove
from PIL import Image
from pyproj import Proj

# NDFD CONUS Projection
p = Proj('+units=m +a=6371200.0 +b=6371200.0 +lon_0=265.0 +proj=lcc +lat_2=25.0 +lat_1=25.0 +lat_0=25.0')
offset_x, offset_y = p(238.445999, 20.191999)

# Square KM offset
square_km = float(environ['SQUARE_KM'])
km_offset = int(round(square_km / 2.5 / 2))

fontsize = 1 if float(environ['SQUARE_KM']) > 75 else 4

aws = Session()
athena = aws.client('athena')
s3 = aws.resource('s3')
bucket = s3.Bucket(environ['OUTPUT_BUCKET'])

class QueryIncompleteException(Exception):
  pass

class QueryFailedException(Exception):
  pass

QUERY_TEMPLATE = '''SELECT
  concat(name,' (', unit, ')') as description,
  date_format(
    date_add(
      'second', 
      CAST(TRUNCATE(CAST(projected_hour AS REAL) * 3600) AS BIGINT), 
      from_unixtime(CAST(reference_time AS BIGINT), 'UTC')
    ) AT TIME ZONE '{TimeZone}',
    '%Y-%m-%d %T %a'
  ) AS forecast_time,
  array_agg(lat) AS latitudes,
  array_agg(lon) AS longitudes,
  array_agg(ROUND(CAST(value AS DECIMAL(6,3)))) AS vals
FROM {LatestTable}
JOIN {CoordinatesTable}
  ON  {LatestTable}.area={CoordinatesTable}.area 
  AND {LatestTable}.x={CoordinatesTable}.x 
  AND {LatestTable}.y={CoordinatesTable}.y
JOIN {ElementsTable}
  ON {LatestTable}.element={ElementsTable}.element
WHERE 
  status='opnl'
  AND {LatestTable}.area='conus'
  AND {LatestTable}.element='{NdfdElement}'
  AND {CoordinatesTable}.x BETWEEN {MinX} AND {MaxX}
  AND {CoordinatesTable}.y BETWEEN {MinY} AND {MaxY}
GROUP BY 
  concat(name,' (', unit, ')'),
  date_format(
    date_add(
      'second', 
      CAST(TRUNCATE(CAST(projected_hour AS REAL) * 3600) AS BIGINT), 
      from_unixtime(CAST(reference_time AS BIGINT), 'UTC')
    ) AT TIME ZONE '{TimeZone}',
    '%Y-%m-%d %T %a'
  )
ORDER BY
  forecast_time
'''

def lambda_handler(event, context):
  if not event or 'QueryStatus' not in event:
    event = execute_query(event)
  
  else:
    query_execution = athena.get_query_execution(
      QueryExecutionId=event['QueryExecutionId'],
    )['QueryExecution']

    event['QueryStatus'] = query_execution['Status']['State']
    
    if event['QueryStatus'] not in ['SUCCEEDED', 'FAILED']:
      raise QueryIncompleteException('QueryIncompleteException')
    
    if event['QueryStatus'] in ['FAILED']:
      raise QueryFailedException('QueryFailedException')
      
    create_map(event)
    
  return event
  
def execute_query(event):
  grid_x, grid_y = p(environ['CENTER_LONGITUDE'], environ['CENTER_LATITUDE'])
  x = int(round((grid_x - offset_x) / 2539.703))
  y = int(round((grid_y - offset_y) / 2539.703))
  
  query_string = QUERY_TEMPLATE.format(
    CoordinatesTable=environ['COORDINATES_TABLE'],
    ElementsTable=environ['ELEMENTS_TABLE'],
    LatestTable=environ['LATEST_TABLE'],
    TimeZone=environ['TIMEZONE'],
    NdfdElement=environ['NDFD_ELEMENT'],
    MaxX=x + km_offset,
    MaxY=y + km_offset,
    MinX=x - km_offset,
    MinY=y - km_offset,
  )
  
  event['QueryExecutionId'] = athena.start_query_execution(
    QueryString=query_string,
    QueryExecutionContext=dict(
      Database=environ['NDFD_DATABASE'],
    ),
    ResultConfiguration=dict(
      OutputLocation=datetime.utcnow().strftime('s3://{0}/results/%Y-%m-%d-%H-%M-%S'.format(environ['OUTPUT_BUCKET'])),
    ),
  )['QueryExecutionId']
  
  event['QueryStatus'] = 'QUEUED'
  
  return event

def create_map(event):
  timesteps = { }
  global_lons = None
  global_lats = None
  desc = None
  cbar = None
  max_val = float('-inf')
  min_val = float('inf')
    
  resp = athena.get_query_results(
    QueryExecutionId=event['QueryExecutionId'],
  )
  
  while resp:
    for row in resp['ResultSet']['Rows']:
      dataset = { }
      row = row['Data']
      
      if row[0]['VarCharValue'] == 'description':
        continue
      
      timestep = row[1]['VarCharValue']
      desc = row[0]['VarCharValue'] if not desc else desc
      dataset['lats'] = json.loads(row[2]['VarCharValue'])
      dataset['lons'] = json.loads(row[3]['VarCharValue'])
      dataset['vals'] = json.loads(row[4]['VarCharValue'])
      timesteps[timestep] = dataset
      
      global_lons = dataset['lons'] if not global_lons else global_lons
      global_lats = dataset['lats'] if not global_lats else global_lats
      max_val = max(dataset['vals']) if max(dataset['vals']) > max_val else max_val
      min_val = min(dataset['vals']) if min(dataset['vals']) < min_val else min_val
    
    resp = athena.query_results(
      QueryExecutionId=event['QueryExecutionId'],
      NextToken=resp['NextToken']
    ) if 'NextToken' in resp else None
  
  img_num = 0
  fig, ax = plt.subplots()
  
  llcrnrx, llcrnry = p(min(global_lons), min(global_lats))
  urcrnrx, urcrnry = p(max(global_lons), max(global_lats))
  
  m = Basemap(
    resolution='h',
    projection='lcc',
    rsphere=6371200.0,
    lon_0=265.0,
    lat_0=25.0,
    lat_1=25.0,
    lat_2=25.0,
    llcrnrx=llcrnrx - 5000,
    llcrnry=llcrnry - 5000,
    urcrnrx=urcrnrx + 5000,
    urcrnry=urcrnry + 5000,
    ax=ax,
  )
  
  m.fillcontinents(color='white', lake_color='aqua')
  m.drawcoastlines()
  m.drawrivers(color='blue')
  m.drawcounties(linewidth=0.5, zorder=15)
  
  for timestep, dataset in timesteps.items():
    ax.set_title('{0} {1}'.format(desc, timestep), fontdict=dict(fontfamily='monospace'))
    x, y = m(dataset['lons'], dataset['lats'])
    
    try: 
      levels = list(np.linspace(min_val, max_val, num=25))
      contours = plt.tricontourf(x, y, dataset['vals'], levels=levels, cmap=plt.cm.jet, alpha=0.5, antialiased=True, zorder=20)
      
      if not cbar:
        cbar = fig.colorbar(contours, orientation='vertical', format='%.1f', pad=0.02)
    
    except:
      contours = None
    
    digits = []
    for i in range(len(dataset['vals'])):
      px, py = m(dataset['lons'][i], dataset['lats'][i])
      digit = plt.text(px, py, dataset['vals'][i], fontsize=fontsize, ha='center', va='center')
      digits.append(digit)
    
    plt.savefig('/tmp/{0:03d}.png'.format(img_num), bbox_inches='tight', dpi=300)
    img_num += 1
    
    for digit in digits:
      digit.remove()
      
    if contours:
      for c in contours.collections:
        c.remove()
  
  frames = []
  
  for i in range(img_num):
    frames.append(Image.open('/tmp/{0:03d}.png'.format(i)))
  
  frames[0].save('/tmp/out.gif', save_all=True, append_images=frames[1:], duration=750, loop=0)
  
  for i in range(img_num):
    remove('/tmp/{0:03d}.png'.format(i))
    
  bucket.upload_file(
    Filename='/tmp/out.gif',
    Key='{0}.gif'.format(environ['NDFD_ELEMENT']),
    ExtraArgs=dict(
      ACL='public-read',
      #CacheControl=
      ContentType='image/gif',
    ),
  )
  
  remove('/tmp/out.gif')
  