import os.path
import time
import datetime

DEBUG_LEVEL = 2
input_file_name = "../build/release/run/crafty_edge_dump/list"
#input_file_name = "./input/dhry_edges/dumplist"
output_file_name = "./output/crafty_distances/dist"

def get_timestamp():
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  return st

def debug(d, msg):
  if (d<=DEBUG_LEVEL):
    print("{0} ({1})".format(msg, get_timestamp()))

i=0
graph = {}
while os.path.isfile(input_file_name+str(i)):
  with open(input_file_name+str(i), "r") as infile:
    for line in infile:
      nodes = line.split()
      v1, label, depth, v2 = int(nodes[0]),int(nodes[1]),int(nodes[2]),int(nodes[3])
      if v2 not in graph:
        graph[v2] = v1
      else:
        if graph[v2]<v1:
          graph[v2] = v1
  
  i+=1

hist_ranges = [100]
for i in range(4):
  hist_ranges.append(hist_ranges[i]*10)

buckets = {}
for k, v in graph.items():
  max_reach = v-k
  for hist_range in hist_ranges:
    if hist_range not in buckets:
      buckets[hist_range] = {}
    else:
      bucket_num = int(max_reach/hist_range)
      if bucket_num not in buckets[hist_range]:
        buckets[hist_range][bucket_num] = 1
      else:
        buckets[hist_range][bucket_num] += 1

for k, bucket in buckets.items():
  l = []
  total_count = 0
  with open(output_file_name+str(k), "w") as outfile:
    max_interval = 0
    for interval, count in bucket.items():
      total_count += count
      if max_interval<interval:
        max_interval = interval

    outfile.write("{0}\n".format(total_count))
    for i in range(max_interval):
      if i in bucket:
        outfile.write("{0}\n".format(bucket[i]))
      else:
        outfile.write("0\n")
