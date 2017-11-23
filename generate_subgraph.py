import re

input_path = "./output/dhry/" 
output_path = "./output/dhry_subgraphs/"

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

def generate_graph(subgraph_str, x, o, o_n, coverage, total_nodes):
  b = subgraph_str.split(")(")
  labels = [0 for i in range(len(b))]
  sg_str = ""
  for i in range(len(b)):
    if i==0:
      labels[i] = opcode[str(int(b[i].split("(")[1]))]
    elif i==len(b)-1:
      temp = b[i].split(")")
      labels[i] = opcode[str(int(temp[0]))]
      sg_str = temp[1].split("'")[0]
    else:
      labels[i] = opcode[str(int(b[i]))]
  n = len(labels)
  #generate nodes
  nodes = []
  with open(output_path+"{0}.sg".format(x), "w") as outfile:
    outfile.write("{0} {1} {2} {3}\n".format(n,o,o_n, coverage))
    for i in range(n):
      n_id = "n"+str(i)
      label = labels[i]
      txt_label=""
      outfile.write("{0} {1}\n".format(n_id, label))

    j=-1
    edges = []
    k=0
    for i in range(len(sg_str)):
      if (i%n==0):
        j+=1

      if sg_str[i] == "+":
        e_id = "e"+str(k)
        k+=1
        source = "n"+str(j)
        target = "n"+str(i%n)
        edges.append((e_id, source, target))
      
    outfile.write("{0}\n".format(len(edges)))
    for edge in edges:
      outfile.write("{0} {1} {2}\n".format(edge[0], edge[1], edge[2]))

i=0
with open(input_path+"one", "r") as in_sg_str, \
     open(input_path+"two", "r") as in_occ, \
     open(input_path+"three", "r") as in_occ_perc, \
     open(input_path+"four", "r") as in_coverage:

  in_sg_str = [sg_str for sg_str in in_sg_str]
  in_occ = [occ for occ in in_occ]
  in_occ_perc = [occ_perc for occ_perc in in_occ_perc]
  in_coverage = [int(coverage) for coverage in in_coverage]
  total_nodes = sum(in_coverage)
  for i in range(len(in_sg_str)):
    subgraph_str = in_sg_str[i].replace("\n", "")
    occurance = int(in_occ[i])
    occurance_perc = float(in_occ_perc[i])
    coverage = int(in_coverage[i])

    generate_graph(subgraph_str,i, occurance_perc, occurance, coverage, total_nodes)

    i+=1
