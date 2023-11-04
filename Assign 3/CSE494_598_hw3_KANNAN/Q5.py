with open('5_compute_LF_mapping/Submissions/testcases/test_1.txt','r') as input_data:
    items = [line for line in input_data.readlines()]

d = [i for i in items[0]]
s = [i for i in range(len(d))]
#print(d,s)
n = len(d)
for i in range(n):
    for j in range(0, n - i - 1):
        if d[j] > d[j + 1]:
            d[j], d[j + 1] = d[j + 1], d[j]
            s[j], s[j + 1] = s[j + 1], s[j]
#print(d,s,items[1])
for i in range(len(s)):
    if s[i] == int(items[1]):
        ans = (i)
        break
#print(ans)
with open('5_compute_LF_mapping/Submissions/outputs/output_1.txt','w') as output_data:
    output_data.write(str(ans))
