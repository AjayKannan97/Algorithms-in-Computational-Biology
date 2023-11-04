import numpy as np
#/Debugging/inputs/input_1.txt
#/Submissions/testcases/test_1.txt
f = open("4_BW_Learning_for_HMM/Submissions/testcases/test_1.txt",'r')
data = f.read().strip().split()
#probabilitiesint(data)
def init_params(data): 
    N = int(data[0])
    x = data[2]
    line = [i for i in range(len(data)) if '--------' == data[i]]
    e_var = data[line[1]+1:line[2]]
    states = data[line[2]+1:line[3]]
    transition = np.zeros((len(states), len(states)))
    emission = np.zeros((len(states), len(e_var)))
    return N, x, line, e_var, states, transition, emission

def add_values(states, e_var, data, transition, emission, line):
    for i in range(len(states)):
        p = line[3]+len(states)+2+i*(len(states)+1)
        q = line[3]+len(states)+1+(i+1)*(len(states)+1)
        transition[i, :] = [float(d) for d in data[p:q]]
        p = line[4]+len(e_var)+2+i*(len(e_var)+1)
        q = line[4]+len(e_var)+1+(i+1)*(len(e_var)+1)
        emission[i, :] = [float(d) for d in data[p:q]]
    return transition, emission

def calc_prob(n,l,f,b,sum_prob):
    probabilities1 = np.zeros((l, n))
    for i in range(n):
        for k in range(l):
            probabilities1[k, i] = f[i][k]*b[i][k]/sum_prob
    
    probabilities2 = np.zeros((l, l, n-1))
    for k1 in range(l):
        for k2 in range(l):
            for i in range(n-1):
                a = transition[k1, k2]
                e = emission[k2, x_array[i+1]]
                z = f[i][k1]*a*e*b[i+1][k2]
                probabilities2[k1, k2, i] = z/sum_prob
    return probabilities1, probabilities2

def soft(n,l,f,b,x_array,transition, emission):
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

def new_prob(n,l,probabilities1,probabilities2,transition,emission):
    for k1 in range(l):
        for k2 in range(l):
            transition[k1, k2] = sum(probabilities2[k1, k2, :])
    for k in range(l):
        for i in range(n):
            emission[k, x_array[i]] += probabilities1[k, i]
    return transition, emission


def soft_est(x_array, transition, emission, e_var):
    n = len(x_array)
    l = transition.shape[0]
    f = [[0 for j in range(l)] for i in range(n)]
    b = [[0 for j in range(l)] for i in range(n)]
    
    f, b, sum_prob = soft(n,l,f,b,x_array,transition, emission)
    probabilities1, probabilities2 = calc_prob(n,l,f,b,sum_prob)
    
    n_alpha = len(e_var)
    n = len(x_array)
    l = probabilities2.shape[0]
    transition = np.zeros((l, l))
    emission = np.zeros((l, n_alpha))
    transition, emission = new_prob(n,l,probabilities1,probabilities2,transition,emission)
    return transition, emission

N, x, line, e_var, states, transition, emission = init_params(data)
transition, emission = add_values(states, e_var, data, transition, emission, line)
l = transition.shape[0]
x_line = {e_var[i]:i for i in range(len(e_var))}
x_array = [x_line[x[i]] for i in range(len(x))]
for i in range(N):
    transition, emission = soft_est(x_array, transition, emission, e_var)
    for i in range(l):
        s1 = sum(transition[i,:])
        if 0 == s1:
            transition[i,:] += 1/l
        else:
            transition[i,:] /= s1
        s2 = sum(emission[i,:])
        if 0 == s2:
            emission[i,:] += 1/len(e_var)
        else:
            emission[i,:] /= s2

f = open("output_q4_Ajay_Kannan.txt","w")
f.write(" ".join(states)+"\n")
for s in range(len(states)):
    data = states[s] 
    for k in range(len(states)):
        data += " " + str(transition[s][k])
    f.write(str(data)+"\n")
f.write("--------\n")
f.write(" ".join(e_var)+"\n")
for s in range(len(states)):
    data = states[s] 
    for k in range(len(e_var)):
        data += " " + str(emission[s][k])
    f.write(str(data)+"\n")
f.close()