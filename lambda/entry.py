import matplotlib
matplotlib.use('agg')

import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from boto3.session import Session
from mpl_toolkits.basemap import Basemap
from os import environ, remove
from PIL import Image

aws = Session()
s3 = aws.resource('s3')
bucket = s3.Bucket(environ['OUTPUT_BUCKET'])

timesteps = { }
lons = None
lats = None
desc = None
max_val = float('-inf')
min_val = float('inf')

with open('{0}/cayuga-temp.csv'.format(environ['LAMBDA_TASK_ROOT'])) as csv_file:
  dataset_csv = csv.DictReader(csv_file)
  
  for row in dataset_csv:
    vals = json.loads(row['vals'])
    
    timesteps[row['forecast_time']] = dict(
      lons = json.loads(row['longitudes']),
      lats = json.loads(row['latitudes']),
      vals = vals,
    )
    
    desc = row['description'] if not desc else desc
    lons = json.loads(row['longitudes']) if not lons else lons
    lats = json.loads(row['latitudes']) if not lats else lats
    min_val = min(vals) if min(vals) < min_val else min_val
    max_val = max(vals) if max(vals) > max_val else max_val

def lambda_handler(event, context):
  img_num = 0
  fig, ax = plt.subplots()
  cax = fig.add_axes([0.77, 0.12, 0.02, 0.75])
  ax.set_title(desc)
  
  m = Basemap(
    resolution='h',
    projection='lcc',
    rsphere=6371200.0,
    lon_0=265.0,
    lat_0=25.0,
    lat_1=25.0,
    lat_2=25.0,
    llcrnrlon=min(lons) - 0.05,
    llcrnrlat=min(lats),
    urcrnrlon=max(lons) + 0.05,
    urcrnrlat=max(lats),
    ax=ax,
  )
  
  m.fillcontinents(color='white', lake_color='aqua')
  m.drawcoastlines()
  m.drawrivers(color='blue')
  m.drawcounties(linewidth=0.5, zorder=15)
  
  for timestep, dataset in timesteps.items():
    x, y = m(lons, lats)
    step_label = fig.text(0.37, 0.135, timestep, bbox=dict(facecolor='white'))
    
    try: 
      levels = list(np.linspace(min(vals), max(vals), num=25))
      contours = ax.tricontourf(x, y, vals, levels=levels, cmap=plt.cm.jet, alpha=0.5, antialiased=True, zorder=20)
      fig.colorbar(contours, cax=cax, orientation='vertical', format='%.1f')
    
    except:
      contours = None
    
    digits = []
    for i in range(len(vals)):
      px, py = m(lons[i], lats[i])
      digit = ax.text(px, py, vals[i], fontsize=3, ha='center', va='center')
      digits.append(digit)
    
    plt.savefig('/tmp/{0:03d}.png'.format(img_num), bbox_inches='tight', dpi=300)
    img_num += 1
    
    step_label.remove()
    
    for digit in digits:
      digit.remove()
      
    if contours:
      for c in contours.collections:
        c.remove()
  
  frames = []
  
  for i in range(img_num):
    frames.append(Image.open('{0:03d}.png'.format(i)))
  
  frames[0].save('/tmp/test.gif', save_all=True, append_images=frames[1:], duration=750, loop=0)
  
  for i in range(img_num):
    remove('{0:03d}.png'.format(i))
    
  bucket.upload_file(
    Filename='/tmp/test.gif',
    Key='test.gif',
    ExtraArgs=dict(
      ACL='public-read',
      #CacheControl=
      ContentType='image/gif',
    ),
  )
  
  remove('/tmp/test.gif')
  