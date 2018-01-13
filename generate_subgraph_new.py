import re
import textwrap

output_path = "./output/dhry_sg/"

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


def generate_graph(count, signature, file_name):
  signature_split = signature.split(".")
  N = len(signature_split)-1
  labels = [int(signature_split[i]) for i in range(N)]
  signature_str = signature_split[N];
  #output nodes
  with open(output_path+file_name, "w") as output_file:
    for i in range(N):
      output_file.write("n{0} {1} {2}\n".format(i+1, i, opcode[str(labels[i])]))

  #output edges
  adj_matrix = textwrap.wrap(signature_str, N)
  edge_num = 0
  with open(output_path+file_name, "a") as output_file:
    output_file.write("EDGES\n")
    for i in range(len(adj_matrix)):
      for j in range(len(adj_matrix[i])):
        if adj_matrix[i][j] == "1":
          edge_num+=1
          output_file.write("e{0} n{1} n{2}\n".format(edge_num, i+1, j+1))
  print(adj_matrix)

sg_tuples = []
FILE_COUNT = 0
with open("signatures.dump", "r") as in_sg_str:
  for line in in_sg_str:
    sg_data = line.split()
    sg_tuples.append((int(sg_data[0]), sg_data[1]))
  
  sg_tuples.sort(key=lambda tup:tup[0], reverse=True)
  for sg_tuple in sg_tuples:
    generate_graph(sg_tuple[0], sg_tuple[1], str(FILE_COUNT))
    FILE_COUNT+=1
  
