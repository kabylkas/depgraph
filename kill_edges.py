import os.path
import time
import datetime
import math

DEBUG_LEVEL = 1
input_file_name = "../build/release/run/crafty_edge_dump/list"
output_file_name = "./output/crafty_killed/crafty"

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
  count = 0
  for node, deps in G.items():
    for dep_nodes in deps:
      if dep_nodes not in G:
        count+=1

  return count

if os.path.isfile(output_file_name):
  os.remove(output_file_name)

intervals = [2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288]
for interval in intervals:
  debug(1, "Processing graph with interval={0}".format(interval))
  interval_count = []
  i=0
  graph = {}
  edges_processed = 0
  killed_edges = 0
  interval_count = 0
  while os.path.isfile(input_file_name+str(i)):
    with open(input_file_name+str(i), "r") as infile:
      for line in infile:
        nodes = line.split()
        v1, label, depth, v2 = int(nodes[0]),int(nodes[1]),int(nodes[2]),int(nodes[3])

        if v1 not in graph:
          graph[v1] = [v2]
        else:
          graph[v1].append(v2)
        edges_processed+=1

        if edges_processed%interval==0:
          killed_edges += process(graph)
          interval_count += 1
          graph = {}
    i+=1
   
  with open(output_file_name, "a") as outfile:
    average=killed_edges/interval_count
    outfile.write("[interval size={0}]Average killed edges per interval = {1} ({2:.2f}%)\n".format(interval, math.floor(average), (killed_edges/edges_processed)*100))

