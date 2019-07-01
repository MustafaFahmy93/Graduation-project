import json
from lidar import *
import time
start = time.time()

objects = []
depthList = []
with open('000705.json') as json_file:
    data = json.load(json_file)
    for p in data :
        # print( p['topleft'])

        x1 = p['topleft']['x']

        x2 = p['bottomright']['x']

        depth = object_depth(x1, x2)

        objects.append(p['label'])

        depthList.append(depth)


print(objects)
print(depthList)
end = time.time()
print(end - start)
