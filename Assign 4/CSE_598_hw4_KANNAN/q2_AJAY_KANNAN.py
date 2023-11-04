import numpy as np
#/Debugging/inputs/input_1.txt
#/Submissions/testcases/test_1.txt
f = open("2_Parameter_Estimation_via_Viterbi_Learning/Submissions/testcases/test_1.txt",'r')
data = f.read().strip().split()
#print(data)

def init_params(data):
    N = int(data[0])
    x = data[2]
    line = [i for i in range(len(data)) if '--------' == data[i]]
    e_var = data[line[1]+1:line[2]]
    states = data[line[2]+1:line[3]]
    transition = np.zeros((len(states), len(states)))
    emission = np.zeros((len(states), len(e_var)))
    return N, x, line, e_var, states, transition, emission

def add_values(states, e_var, data, transition, emission):
    for i in range(len(states)):
        p = line[3]+len(states)+2+i*(len(states)+1)
        q = line[3]+len(states)+1+(i+1)*(len(states)+1)
        transition[i, :] = [float(d) for d in data[p:q]]
        p = line[4]+len(e_var)+2+i*(len(e_var)+1)
        q = line[4]+len(e_var)+1+(i+1)*(len(e_var)+1)
        emission[i, :] = [float(d) for d in data[p:q]]
    return transition, emission

def make_path(matrix_max,b,n):
    path_array = [matrix_max]
    for i in range(n-1, 0, -1):
        matrix_max = b[i][matrix_max]
        path_array.insert(0, matrix_max)
    return path_array

def make_matrix(x_array, transition, emission):
    n, l = len(x_array), transition.shape[0]
    matrix = [[1. for i in range(l)] for i in range(n)]
    b = [[None for i in range(l)] for i in range(n)]
    for k in range(l):
        matrix[0][k] = emission[k, x_array[0]]/l
    for i in range(1, n):
        for k in range(l):
            currmatrix = [ ]
            for j in range(l):
                currmatrix.append(matrix[i-1][j] * transition[j, k] * emission[k, x_array[i]])
            line = np.argmax(currmatrix)
            b[i][k] = line
            matrix[i][k] = currmatrix[line]
    matrix_max = np.argmax(matrix[n-1])
    path_array = make_path(matrix_max,b,n)
    return path_array

def reiterate(x_array, transition, emission, path_array):
    n, l = emission.shape
    for i in range(len(path_array)-1):
        transition[path_array[i], path_array[i+1]] += 1
    for i in range(len(x_array)):
        emission[path_array[i], x_array[i]] += 1
    for i in range(n):
        s1 = sum(transition[i,:])
        if 0 == s1:
            transition[i,:] += 1/n
        else:
            transition[i,:] /= s1
        s2 = sum(emission[i,:])
        if 0 == s2:
            emission[i,:] += 1/l
        else:
            emission[i,:] /= s2
    return transition, emission

def estimate(N, x, e_var, transition, emission, line):
    for iteration in range(N): 
        x_line = {e_var[i] : i for i in range(len(e_var))}
        x_array = [x_line[x[i]] for i in range(len(x))]
        path_array = make_matrix(x_array, transition, emission)
        transition = np.zeros_like(transition)
        emission = np.zeros_like(emission)
        transition, emission = reiterate(x_array, transition, emission, path_array)
    return transition, emission

N, x, line, e_var, states, transition, emission = init_params(data)
transition, emission = add_values(states, e_var, data, transition, emission)
transition, emission = estimate(N, x, e_var, transition, emission, line)

f = open("output_q2_Ajay_Kannan.txt","w")
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
