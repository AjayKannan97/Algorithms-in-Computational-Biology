import numpy as np
#/Debugging/inputs/input_1.txt
#/Submissions/testcases/test_1.txt
f = open("3_Soft_Decoding/Submissions/testcases/test_1.txt","r")
data = f.read().strip().split()

def init_params(data): 
    x = data[0]
    line = [i for i in range(len(data)) if '--------' == data[i]]
    e_var = data[line[0]+1:line[1]]
    states = data[line[1]+1:line[2]]
    transition = np.zeros((len(states), len(states)))
    emission = np.zeros((len(states), len(e_var)))
    return x, line, e_var, states, transition, emission

def add_values(states, e_var, data, transition, emission, line):
    for i in range(len(states)):
        p = line[2]+len(states)+2+i*(len(states)+1)
        q = line[2]+len(states)+1+(i+1)*(len(states)+1)
        transition[i, :] = [float(d) for d in data[p:q]]
        p = line[3]+len(e_var)+2+i*(len(e_var)+1)
        q = line[3]+len(e_var)+1+(i+1)*(len(e_var)+1)
        emission[i, :] = [float(d) for d in data[p:q]]
    return transition, emission

def calc_prob(n, l, f, b, sum_prob):
    probabilities = np.zeros((n, l))
    for i in range(n):
        for k in range(l):
            probabilities[i, k] = f[i][k]*b[i][k]/sum_prob
    return probabilities

def soft(n,l,x_array, transition, emission):
    f = [[0 for j in range(l)] for i in range(n)]
    b = [[0 for j in range(l)] for i in range(n)]
    for k in range(l):
        f[0][k] = emission[k, x_array[0]]/l
        b[n-1][k] = 1
    for i in range(1, n):
        for k in range(l):
            d = []
            for j in range(l):
                d.append(f[i-1][j]*transition[j, k]*emission[k, x_array[i]])
            f[i][k] = sum(d)
    for i in range(n-2, -1, -1):
        for k in range(l):
            d = []
            for j in range(l):
                d.append(b[i+1][j]*transition[k, j]*emission[j, x_array[i+1]])
            b[i][k] = sum(d)
    sum_prob = sum(f[n-1])
    return f, b, sum_prob


x, line, e_var, states, transition, emission = init_params(data)
transition, emission = add_values(states, e_var, data, transition, emission, line)
n = len(x)
l = transition.shape[0]
t = {e_var[i]:i for i in range(len(e_var))}
x_array = [t[x[i]] for i in range(n)]
f, b, sum_prob = soft(n,l,x_array, transition, emission)
probabilities = calc_prob(n, l, f, b, sum_prob)

f = open("output_q3_Ajay_Kannan.txt","w")
f.write(" ".join(states)+"\n")
for s in range(len(probabilities)):
    data = str(probabilities[s][0]) + " " + str(probabilities[s][1])
    f.write(str(data)+"\n")
f.close()
