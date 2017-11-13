occurances = []
with open("graph.output.1", "r") as infile:
  for line in infile:
    info = line.split(',')
    occurance = float(info[2].split("]")[0])
    occurance_n = int(info[1])
    occurances.append(occurance_n)

with open("occurances.output", "w") as outfile:
  for occurance in occurances:
    outfile.write("{0}\n".format(occurance))
