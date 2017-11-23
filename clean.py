import os.path
import time
import datetime
import math
import sys

DEBUG_LEVEL = 1
input_file_name = "../build/release/run/crafty_edge_dump/list"
output_file_name = "./test/crafty"

interval_size = 100000
counter = 0
graph = {}
depths = {}

def get_timestamp():
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  return st

def debug(d, msg):
  if (d<=DEBUG_LEVEL):
    print("{0} ({1})".format(msg, get_timestamp()))

def connected(G, v1, v2, d_furthest):
  node_deps = G[v1]
  for node_dep in node_deps:
    #print(node_deps)
    if node_dep in G:
      for deep_node_dep in G[node_dep]:
        if depths[deep_node_dep]<=d_furthest:
          if deep_node_dep == v2:
            return True
        else:
          if deep_node_dep not in node_deps:
            node_deps.append(deep_node_dep)
        

  return False

def clean_unreachable(G):
  for node, node_deps in G.items():
    temp_node_deps = node_deps
    for node_dep in node_deps:
      if node_dep not in G:
        temp_node_deps.remove(node_dep)
      elif node_dep==node:
        temp_node_deps.remove(node_dep)

    if len(temp_node_deps) == 0:
      print("Complete delete")
      del G[node]
    else:
      G[node] = temp_node_deps

def clean_redundant(G):
  for node, node_deps in G.items():
    #if has 2 edges remove the redundant edge (if exists)
    if len(node_deps)==2:
      depth1 = depths[node_deps[0]]
      depth2 = depths[node_deps[1]]
      temp_node_deps = node_deps
      if depth1>depth2:
        if connected(G, node_deps[0], node_deps[1], depth2):
          temp_node_deps.remove(node_deps[1])
      elif depth1<depth2:
        if connected(G, node_deps[1], node_deps[0], depth1):
          temp_node_deps.remove(node_deps[0])

      if len(temp_node_deps) == 0:
        del G[node]
      else:
        G[node] = temp_node_deps

  return G

def check(G):
  for node, node_deps in G.items():
    if node not in depths:
      print("WHAT!?")

if os.path.isfile(output_file_name):
  os.remove(output_file_name)

interval = 5000
interval_count = []
i=0
graph = {}
edges_processed = 0
interval_count = 0
while os.path.isfile(input_file_name+str(i)):
  with open(input_file_name+str(i), "r") as infile:
    for line in infile:
      nodes = line.split()
      v1, label, depth, v2 = int(nodes[0]),int(nodes[1]),int(nodes[2]),int(nodes[3])
      if v1==2902:
        print("here")
      if v1 not in graph:
        graph[v1] = [v2]
      else:
        graph[v1].append(v2)

      if v1 not in depths:
        depths[v1] = depth

      edges_processed+=1


      if edges_processed%interval==0:
        clean_unreachable(graph)
        check(graph)
        clean_redundant(graph)
        graph = {}
        depths = {}
        #exit(0)
  i+=1
