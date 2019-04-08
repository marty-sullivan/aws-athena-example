#!/usr/bin/env python3

import matplotlib
matplotlib.use('agg')

import csv
import json
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from os import remove
from PIL import Image

timesteps = { }
lons = None
lats = None
max_val = float('-inf')
min_val = float('inf')

with open('./cornell_temp.csv') as dataset_file:
  dataset_csv = csv.DictReader(dataset_file)
  #img_num = 0
  
  for row in dataset_csv:
    vals = json.loads(row['vals'])
    
    timesteps[row['forecast_time']] = dict(
      lons=json.loads(row['longitudes']),
      lats=json.loads(row['latitudes']),
      vals=vals,
    )
    
    lons = json.loads(row['longitudes']) if not lons else lons
    lats = json.loads(row['latitudes']) if not lats else lats
    min_val = min(vals) if min(vals) < min_val else min_val
    max_val = max(vals) if max(vals) > max_val else max_val
    
img_num = 0
fig, ax = plt.subplots()
cax = fig.add_axes([0.72, 0.12, 0.02, 0.75])

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

for timestep, dataset in timesteps.items():
  x, y = m(dataset['lons'], dataset['lats'])
  levels = list(numpy.linspace(min_val, max_val, num=25))
  mymap = ax.tricontourf(x, y, dataset['vals'], levels=levels, cmap=plt.cm.jet, alpha=0.5, antialiased=True, zorder=20)
  fig.colorbar(mymap, cax=cax, orientation='vertical', format='%.1f')
  txt = fig.text(0.35, 0.135, timestep, bbox=dict(facecolor='white'))
  
  
  digits = []
  # for i in range(0, len(dataset['vals']), 25):
  for i in range(len(dataset['vals'])):
    px, py = m(dataset['lons'][i], dataset['lats'][i])
    digits.append(ax.text(px, py, dataset['vals'][i], fontsize=3, ha='center', va='center'))
  
  plt.savefig('{0:03d}.png'.format(img_num), bbox_inches='tight', dpi=300)
  img_num += 1
  
  txt.remove()
  
  for i in digits:
    i.remove()
  
  for i in mymap.collections:
    i.remove()

frames = []

for i in range(img_num):
  frames.append(Image.open('{0:03d}.png'.format(i)))
  
frames[0].save('temp.gif', save_all=True, append_images=frames[1:], duration=500, loop=0)
  
for i in range(img_num):
  remove('{0:03d}.png'.format(i))
  