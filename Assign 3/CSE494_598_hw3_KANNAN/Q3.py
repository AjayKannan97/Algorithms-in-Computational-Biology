from driver import make_Bwm
#Submissions/testcases/test_1.txt
with open('3_compute_BWT_of_a_string/Submissions/testcases/test_1.txt','r') as input_data:
    items = input_data.readlines()
#print(items[0])
ans = make_Bwm(items[0])
with open('3_compute_BWT_of_a_string/Submissions/outputs/output_1.txt','w') as output_data:
    output_data.write(str(ans))