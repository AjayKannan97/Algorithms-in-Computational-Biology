from driver import reverse_Bwt, make_Bwm
#Submissions/testcases/test_1.txt
#Debugging/outputs/output_1.txt
with open('4_compute_original_string_given_BWT/Submissions/testcases/test_1.txt','r') as input_data:
    items = input_data.readlines()
ans = reverse_Bwt(make_Bwm(items[0]))
with open('4_compute_original_string_given_BWT/Submissions/outputs/output_1.txt','w') as output_data:
    output_data.write(str(ans))
#print(ans)