from driver import length_of_patterns

with open("6_BWM_algo/Submissions/testcases/test_1.txt",'r') as input_data:
    items = []
    for line in input_data.readlines():
        items.append(line.strip('\n'))

ans = length_of_patterns(items[1],items[0])

with open("6_BWM_algo/Submissions/outputs/output_1.txt",'w') as output_data:
    for i in ans:
        output_data.write(str(i)+' ')