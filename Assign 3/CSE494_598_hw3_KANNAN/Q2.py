from driver import local_alignment
import pandas as pd
#Submissions/testcases/test_1.txt
#Debugging/inputs/input_1.txt
with open("2_local_alignment_with_affine_gap_penalty/Submissions/testcases/test_1.txt",'r') as input_data:
    items = []
    for line in input_data.readlines():
        if '>Seq' not in line:
            items.append(line.strip('\n'))

scoring_matrix = pd.read_table('BLOSUM62.txt', sep = '  ', engine = 'python')
alignment = local_alignment(items[0], items[1], scoring_matrix, 11, 1)
#print(alignment)
with open("2_local_alignment_with_affine_gap_penalty/Submissions/outputs/output_1.txt",'w') as output_data:
    for line in alignment:
        output_data.write(str(line)+'\n')