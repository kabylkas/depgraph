import random
import os.path
import datetime
import time
import hashlib

#define for processing
DEBUG_LEVEL = 2
input_file_name = "./input/dhry/dump"
output_file_name = "./output/dhry"

#helper functions
def get_timestamp():
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  return st

def debug(d, msg):
  if (d<=DEBUG_LEVEL):
    print("{0} ({1})".format(msg, get_timestamp()))

def is_real_edge(G, v1, v2):
  for node in G[str(v1)]:
    if node[0]==v2:
      return node[1]

observe = [0,0,0,0]
tokens = {}
labels = {}
graph_tokens = {}
graph_id = {}
def traverse(G, u, depth):
  if u in observe:
    return
  if (depth==len(observe)-1):
    #debug(2, "{0}".format(observe))
    observe[depth] = u
    temp = observe[:]
    temp.sort()
    token = "-".join([str(node) for node in temp])
    if token not in tokens:
      tokens[token] = True
      real_edges = []
      for node in temp:
        if str(node) in G:
          for neighbor in G[str(node)]:
            if neighbor[0] in temp and neighbor[1]:
              real_edges.append((node, neighbor[0]))

      subgraph = [(node, labels[str(node)]) for node in temp]
      subgraph.sort(key=lambda tup: tup[1])
      w,h = len(observe), len(observe)
      subgraph_mat = [["." for x in range(w)] for y in range(h)]
      for v1,v2 in real_edges:
        i=0
        found_i = False
        found_j = False
        for i in range(0, len(subgraph)):
          if subgraph[i][0] == v1:
            found_i = True
            break
        j=0
        for j in range(0, len(subgraph)):
          if subgraph[j][0] == v2:
            found_j = True
            break
        if found_i and found_j:
          subgraph_mat[i][j] = "+"

      subgraph_arr = "".join(["("+str(subgraph[i][1])+")" for i in range(len(subgraph))])
      for y in range(h):
        subgraph_arr += "".join([subgraph_mat[y][x] for x in range(w)])
      
      if subgraph_arr not in graph_tokens:
        graph_tokens[subgraph_arr] = 1
      else:
        graph_tokens[subgraph_arr] += 1
     
      #decide how many individual nodes within specific subgraph show up in
      #graph
      if subgraph_arr not in graph_id:
        graph_id[subgraph_arr] = []
        for u in observe:
          graph_id[subgraph_arr].append(u)
      else:
        for u in observe:
          if u not in graph_id[subgraph_arr]:
            graph_id[subgraph_arr].append(u)

    return
  else:
    observe[depth] = u
    if str(u) in G:
      for v in G[str(u)]:
        traverse(G, v[0], depth+1)

graph = {}
for i in range(0,5):
  fileName = input_file_name+str(i)
  if (os.path.exists(fileName)):
    debug(1,"Reading file: {0}".format(fileName))
    with open(fileName, "r") as infile:
      for line in infile:
        nodes = line.split()
        v1 = int(nodes[0])
        #if (v1 == 0):
          #continue

        label = int(nodes[1])
        for j in range(2, len(nodes)):
          v2 = int(nodes[j])
          #if (v2 == 0):
            #continue

          if str(v1) not in graph:
            graph[str(v1)] = [(v2,True)]
          else:
            graph[str(v1)].append((v2,True))

          if str(v2) not in graph:
            graph[str(v2)] = [(v1,False)]
          else:
            graph[str(v2)].append((v1,False))

        if str(v1) not in labels:
          labels[str(v1)] = label

#extract subgraph of particular depth
depth=2
start = get_timestamp()
print(start)
graph_size = 0
for key, value in graph.items():
  graph_size += 1
  subgraph_edges = []
  subgraph_nodes = [int(key)]
  visited = []
  for d in range(depth):
    deeper_subgraph_nodes = []
    for node in subgraph_nodes:
      visited.append(node)
      for deeper_node in graph[str(node)]:
        if (deeper_node[0] not in visited):
          if (node<deeper_node[0]):
            subgraph_edges.append((node,deeper_node[0]))
          else:
            subgraph_edges.append((deeper_node[0],node))
          deeper_subgraph_nodes.append(deeper_node[0])
    subgraph_nodes = deeper_subgraph_nodes

  #build sub-graph for traversal from the edge list
  subgraph_inst = {}
  for edge in subgraph_edges:
    v1, v2 = int(edge[0]), int(edge[1])
    real_edge = is_real_edge(graph, v1,v2)
    if str(v1) not in subgraph_inst:
      subgraph_inst[str(v1)] = [(v2,real_edge)]
    else:
      subgraph_inst[str(v1)].append((v2,real_edge))

    if str(v2) not in subgraph_inst:
      subgraph_inst[str(v2)] = [(v1,not real_edge)]
    else:
      subgraph_inst[str(v2)].append((v1,not real_edge))

  subgraph_size = len(subgraph_inst)
  debug(1, "Start traversal from  node with id = {0}. Subgraph size = {1}\n{2}\n\n".format(key, subgraph_size, value))

  for k, v in subgraph_inst.items():
    traverse(subgraph_inst, int(k), 0)


end = get_timestamp()
print(end)

debug(1, "Calculating occurrence percentage of subgraphs")
graph_token_tuple = []
total = 0
total_nodes = 0
for key, value in graph_tokens.items():
  graph_token_tuple.append([key, value,0., len(graph_id[key])])
  total += value
  total_nodes+=len(graph_id[key])

debug(1, "Sorting subgraphs")
graph_token_tuple.sort(key=lambda tup: tup[3], reverse=True)

fileName = output_file_name
debug(1, "Dumping subgraphs to files to {0}".format(fileName))
with open(fileName+"/one","w") as one, open(fileName+"/two","w") as two,\
        open(fileName+"/three","w") as three, open(fileName+"/four","w") as four:
    for a in graph_token_tuple:
      a[2]=(float(a[1])/float(total))*100
      one.write("{0}\n".format(a[0]))
      two.write("{0}\n".format(a[1]))
      three.write("{0}\n".format(a[2]))
      four.write("{0}\n".format(a[3]))

debug(1, "Graph size = {0}".format(graph_size))
debug(1, "Start time = {0}".format(start))
debug(1, "End time = {0}".format(end))
