import os.path
import time
import datetime

DEBUG_LEVEL = 2
#input_file_name = "./input/dhry/dump"
input_file_name = "/soe/nkabylka/build/release/run/crafty_dump/dump"
output_file_name = "./output/dhry"

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
    if str(value) not in G:
      killed += 1

  debug(1, "{0} nodes proccessed. Killed edges = {1}".format(len(G), killed))

hist_range = 1000
hist = {}
max_bucket = 0
for i in range(0,20000):
  fileName = input_file_name+str(i)
  if (os.path.exists(fileName)):
    debug(1,"Reading file: {0}".format(fileName))
    with open(fileName, "r") as infile:
      for line in infile:
        nodes = line.split()
        if len(nodes) > 2:
          v1 = int(nodes[0])
          last_node = int(nodes[len(nodes)-1])
          distance = last_node-v1 
          bucket = int(distance/hist_range)
          if bucket not in hist:
            hist[bucket] = 1
          else:
            hist[bucket] += 1

          if max_bucket<bucket:
            max_bucket = bucket

with open("distances.txt", "w") as out:
  for i in range(max_bucket):
    j = 0
    if i in hist:
      j = hist[i]
    out.write("{0}\n".format(j))

