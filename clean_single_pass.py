import os.path
import time
import datetime
import math
import sys
import copy


DEBUG_LEVEL = 1
#input_file_name = "../build/release/run/crafty_edge_dump/list"
input_file_name = "./test/list"
output_file_name = "./test/dhry_interval/"

opcode = {"0": ("iOpInvalid", 0),
          "1": ("iRALU", 1),
          "2": ("iAALU", 1),
          "3": ("iBALU_LBRANCH", 2), 
          "4": ("iBALU_RBRANCH", 2),
          "5": ("iBALU_LJUMP", 2),
          "6": ("iBALU_RJUMP", 2), 
          "7": ("iBALU_LCALL", 2), 
          "8": ("iBALU_RCALL", 2),
          "9": ("iBALU_RET", 2),
         "10": ("iLALU_LD", 20),
         "11": ("iSALU_ST", 2),
         "12": ("iSALU_LL", 2),
         "13": ("iSALU_SC", 2),
         "14": ("iSALU_ADDR", 2),
         "15": ("iCALU_FPMULT", 2),
         "16": ("iCALU_FPDIV", 2),
         "17": ("iCALU_FPALU", 2),
         "18": ("iCALU_MULT", 2),
         "19": ("iCALU_DIV", 2),
         "20": ("iMAX", 2)}


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

def clean_redundant(G, rev_G, path=[]):
  for node, node_deps in G.items():
    q = [node]
    while q:
      v1=q.pop(0)
      if v1 not in path and v1!=0:
        path=path+[v1]
        #latency calculation
        max_latency = 0
        max_v2 = 0
        for v2 in rev_G[v1]:
          latency = graph_latency[v1]+graph_latency[v2]
          if latency>max_latency:
            max_latency = latency
            max_v2 = v2
        graph_latency[v1] = max_latency

        if len(rev_G[v1])>1:
          print(">>", max_v2)
          for v2 in rev_G[v1]:
            print(v2)
            if v2!=max_v2:
              killed_edges[str(v1)+"-"+str(v2)] = True
        q=q+G[v1]
        
              
                

  print(graph_latency)
  print(killed_edges)
  return path


if os.path.isfile(output_file_name):
  os.remove(output_file_name)

interval = 10
interval_count = []
i=0
graph = {}
rev_graph = {}
graph_latency = {}
killed_edges = {}

edges_processed = 0
interval_count = 0
while os.path.isfile(input_file_name+str(i)):
  with open(input_file_name+str(i), "r") as infile:
    for line in infile:
      nodes = line.split()
      v1, label, depth, v2 = int(nodes[0]),int(nodes[1]),int(nodes[2]),int(nodes[3])

      if v1 not in graph:
        graph[v1] = []
        rev_graph[v1] = []
        graph_latency[v1] = 0
      if v2 not in graph:
        graph[v2] = []
        rev_graph[v2] = []
        graph_latency[v2] = 0

      graph[v2].append(v1)
      rev_graph[v1].append(v2)

      if v1 not in depths:
        depths[v1] = depth
        labels[v1] = label


      edges_processed+=1


      if edges_processed%interval==0:
        for v, deps in graph.items():
          if v!=0:
            graph_latency[v] = opcode[str(labels[v])][1]

        #graph = clean_unreachable(graph)
        #dump_to_vis(graph, output_file_name+"before")
        print(graph_latency)
        path = clean_redundant(graph, rev_graph)
        print(graph_latency)
        #dump_to_vis(graph, output_file_name+"after")
        graph = {}
        depths = {}
        exit(0)
