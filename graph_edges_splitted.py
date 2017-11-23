import random
import os.path
import datetime
import time
import hashlib
import sys
import getopt

#define for processing
DEBUG_LEVEL = 2

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
depths = {}
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

def process(graph):
  #extract subgraph of particular depth
  depth=2
  graph_size = 0
  degree = 0
  for key, value in graph.items():
    graph_size += 1
    subgraph_edges = []
    subgraph_nodes = [int(key)]
    visited = []
    degrees = {}
    max_degree = 0
    for d in range(depth):
      deeper_subgraph_nodes = []
      for node in subgraph_nodes:
        visited.append(node)
        for deeper_node in graph[str(node)]:
          if (deeper_node[0] not in visited):
            v1=0
            v2=0
            if (node<deeper_node[0]):
              v1 = node
              v2 = deeper_node[0]
            else:
              v2 = node
              v1 = deeper_node[0]
            subgraph_edges.append((v1,v2))
            if v1 not in degrees:
              degrees[v1] = 1
            else:
              degrees[v1] += 1

            if v2 not in degrees:
              degrees[v2] = 1
            else:
              degrees[v2] += 1

            if degrees[v1] > max_degree:
              max_degree = degrees[v1]
            if degrees[v1] > max_degree:
              max_degree = degrees[v2]
            deeper_subgraph_nodes.append(deeper_node[0])
      subgraph_nodes = deeper_subgraph_nodes

    skip = False
    if max_degree != degree:
      degree = max_degree
    else:
      skip = True

    if not skip:
      #build sub-graph for traversal from the edge list
      subgraph_inst = {}
      for edge in subgraph_edges:
        v1, v2 = int(edge[0]), int(edge[1])
        if str(v1) not in labels or str(v2) not in labels:
          continue

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
      #debug(1, "Start traversal from  node with id = {0}. Subgraph size = {1}\n{2}\n\n".format(key, subgraph_size, value))
      for k, v in subgraph_inst.items():
        traverse(subgraph_inst, int(k), 0)

def connected(G, v1, v2, d_furthest):
  node_deps = G[v1]
  for node_dep in node_deps:
    if node_dep[1]:
      for deep_node_dep in G[str(node_dep[0])]:
        if deep_node_dep[1]:
          if depth[deep_node_dep[0]]<=d_furthest:
            if deep_node_dep[0] == v2:
              return True
          else:
            if deep_node_dep not in node_deps:
              node_deps.append(deep_node_dep)
            

  return False
def clean(G):
  for node, node_deps in G.items():
    #clean from not reachable nodes
    #also get real edges
    real_nodes = []
    for node_dep in node_deps:
      if str(node_dep[0]) not in G:
        node_deps.remove(node_dep)
        break

      if node_dep[1]:
        real_nodes.append(node_dep[0])
        if len(real_nodes)==2:
          break
    #if has 2 edges remove the redundant edge (if exists)
    if len(real_nodes)==2:
      depth1 = depths[real_nodes[0]]
      depth2 = depths[real_nodes[1]]
      if depth1>depth2:
        if connected(real_nodes[0], real_nodes[1], depth2):
          node_deps.remove((real_nodes[1], True))
      elif depth1<depth2:
        if connected(real_nodes[1], real_nodes[0], depth1):
          node_deps.remove((real_nodes[0], True))

  return G
    

#=====================================================================================================
#process the arguments
if len(sys.argv)<5:
  print("Usage: {0} inputPath outputPath rangeA rangeB".format(sys.argv[0]))
  exit(1)
else:
  input_file_name = sys.argv[1]
  output_file_name = sys.argv[2]
  print(input_file_name)
  print(output_file_name)
  files_ind = [k for k in range(int(sys.argv[3]), int(sys.argv[4]))]
  print(files_ind)

start = get_timestamp()
print(start)
graph = {}
interval = 5000
i=0
k=0
edges_processed = 0
for i in files_ind:
  if os.path.isfile(input_file_name+str(i)):
    with open(input_file_name+str(i), "r") as infile:
      debug(1, "Processing file: {0}".format(input_file_name+str(i)))
      for line in infile:
        nodes = line.split()
        v1, label, depth, v2 = int(nodes[0]),int(nodes[1]),int(nodes[2]),int(nodes[3])


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
          depths[str(v1)] = depth

        edges_processed+=1
        if edges_processed%interval==0:
          k+=1
          #debug(2, "{1} Processing interval with graph size={0}... Token count = {2}".format(len(graph),k,len(graph_tokens)))
          #process(graph)
          print(len(graph))
          graph = clean(graph)
          print(len(graph))
          exit(0)
          graph = {}
          labels = {}
          depths = {}
if len(graph)>0:
  process(graph)


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

debug(1, "Start time = {0}".format(start))
debug(1, "End time = {0}".format(end))
#get the graph size
