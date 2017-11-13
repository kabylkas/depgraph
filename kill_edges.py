import os.path
import time
import datetime

DEBUG_LEVEL = 2
input_file_name = "../build/release/run/edge_list/list"
output_file_name = "./output/dhry"

interval_size = 100000
counter = 0
graph = {}
labels = {}

def get_timestamp():
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  return st

def debug(d, msg):
  if (d<=DEBUG_LEVEL):
    print("{0} ({1})".format(msg, get_timestamp()))

def process(G):
  killed = 0
  for key, value in G.items():
    for v in value:
      if str(v) not in G:
        killed += 1

  debug(1, "{0} nodes proccessed. Killed edges = {1}".format(len(G), killed))

for i in range(0,5):
  fileName = input_file_name+str(i)
  if (os.path.exists(fileName)):
    debug(1,"Reading file: {0}".format(fileName))
    with open(fileName, "r") as infile:
      for line in infile:
        nodes = line.split()
        v1, label, v2 = int(nodes[0]), int(nodes[1]), int(nodes[2])

        if str(v1) not in graph:
          graph[str(v1)] = [v2]
        else:
          graph[str(v1)].append(v2)

        if str(v1) not in labels:
          labels[str(v1)] = label
        
        counter+=1
        if (counter%interval_size == 0):
          process(graph)
          counter = 0
          graph = {}
          labels = {}
