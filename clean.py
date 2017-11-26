import os.path
import time
import datetime
import math
import sys
import copy

DEBUG_LEVEL = 1
input_file_name = "../build/release/run/crafty_edge_dump/list"
output_file_name = "./test/dhry_interval/"

opcode = {"0": "iOpInvalid",
          "1": "iRALU",
          "2": "iAALU",
          "3": "iBALU_LBRANCH", 
          "4": "iBALU_RBRANCH",
          "5": "iBALU_LJUMP",
          "6": "iBALU_RJUMP", 
          "7": "iBALU_LCALL", 
          "8": "iBALU_RCALL",
          "9": "iBALU_RET",
         "10": "iLALU_LD",
         "11": "iSALU_ST",
         "12": "iSALU_LL",
         "13": "iSALU_SC",
         "14": "iSALU_ADDR",
         "15": "iCALU_FPMULT",
         "16": "iCALU_FPDIV",
         "17": "iCALU_FPALU",
         "18": "iCALU_MULT",
         "19": "iCALU_DIV",
         "20": "iMAX"}

interval_size = 100000
counter = 0
graph = {}
depths = {}
labels = {}

def get_timestamp():
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  return st

def debug(d, msg):
  if (d<=DEBUG_LEVEL):
    print("{0} ({1})".format(msg, get_timestamp()))

def dump_to_vis(G, filename):
  with open(filename, "w") as outfile:
    outfile.write("{0} 0 0\n".format(len(G)))
    edges_num = 0
    for node, node_deps in G.items():
      outfile.write("n{0} {1} {2}\n".format(node, depths[node], opcode[str(labels[node])]))
      edges_num += len(node_deps)
    
    outfile.write("{0}\n".format(edges_num))
    i=0
    for node, node_deps in G.items():
      for node_dep in node_deps:
        outfile.write("e{0} n{1} n{2}\n".format(i, node, node_dep))
        i+=1

    if i==edges_num:
      print("Good")

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
  gr = {}
  for node, node_deps in G.items():
    temp_node_deps = node_deps[:]
    for node_dep in node_deps:
      if node_dep not in G:
        temp_node_deps.remove(node_dep)
      elif node_dep==node:
        temp_node_deps.remove(node_dep)

    gr[node] = temp_node_deps[:]

  return copy.deepcopy(gr)

def clean_redundant(G):
  gr = {}
  for node, node_deps in G.items():
    temp_node_deps = node_deps[:]
    #if has 2 edges remove the redundant edge (if exists)
    if len(node_deps)==2:
      depth1 = depths[node_deps[0]]
      depth2 = depths[node_deps[1]]
      if depth1>depth2:
        if connected(G, node_deps[0], node_deps[1], depth2):
          temp_node_deps.remove(node_deps[1])
      elif depth1<depth2:
        if connected(G, node_deps[1], node_deps[0], depth1):
          temp_node_deps.remove(node_deps[0])

    gr[node] = temp_node_deps

  return copy.deepcopy(gr)

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
      if v1 not in graph:
        graph[v1] = [v2]
      else:
        graph[v1].append(v2)

      if v1 not in depths:
        depths[v1] = depth
        labels[v1] = label

      edges_processed+=1


      if edges_processed%interval==0:
        print("Graph size={0}".format(len(graph)))
        graph = clean_unreachable(graph)
        dump_to_vis(graph, output_file_name+"before")
        graph = clean_redundant(graph)
        dump_to_vis(graph, output_file_name+"after")
        graph = {}
        depths = {}
        exit(0)
  i+=1
