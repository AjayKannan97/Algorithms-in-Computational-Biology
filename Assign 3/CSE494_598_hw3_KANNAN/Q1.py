from driver import global_alignment
import pandas as pd
#Submissions/testcases/test_1.txt
#Debugging/inputs/input_1.txt
scoring_matrix = pd.read_table('BLOSUM62.txt', sep = '  ', engine = 'python')

with open("1_global_alignment_with_a_fixed_indel_penalty/Submissions/testcases/test_1.txt",'r') as input_data:
    items = []
    for line in input_data.readlines():
        if '>Seq' not in line:
            items.append(line.strip('\n'))

#print(items)
alignment = global_alignment(items[0],items[1], scoring_matrix, 5)

with open("1_global_alignment_with_a_fixed_indel_penalty/Submissions/outputs/output_1.txt",'w') as output_data:
    for line in alignment:
        output_data.write(str(line)+'\n')