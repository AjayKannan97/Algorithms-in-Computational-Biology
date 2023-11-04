import numpy as np
#1_Viterbi_Algo/Debugging/inputs/input_1.txt
#1_Viterbi_Algo/Submissions/testcases/test_1.txt
f = open("1_Viterbi_Algo/Submissions/testcases/test_1.txt",'r')
s = f.read().strip().split()

def init_params(s):
	obs = s[0]
	line = [i for i in range(len(s)) if '--------' == s[i]]
	e_var = s[line[0]+1:line[1]]
	states = s[line[1]+1:line[2]]
	transition = np.zeros((len(states), len(states)))
	emission = np.zeros((len(states), len(e_var)))
	return obs, line, e_var, states, transition, emission

def add_values(s, states, line, e_var, transition, emission):
	for i in range(len(states)):
		p = line[2]+len(states)+2+i*(len(states)+1)
		q = line[2]+len(states)+1+(i+1)*(len(states)+1)
		transition[i, :] = [float(d) for d in s[p:q]]
		p = line[3]+len(e_var)+2+i*(len(e_var)+1)
		q = line[3]+len(e_var)+1+(i+1)*(len(e_var)+1)
		emission[i, :] = [float(d) for d in s[p:q]]
	return transition, emission

def make_dict(e_var, states, transition, emission):
	d_transition, d_emission = {}, {}
	for i in range(len(transition)):
		d = {}
		for j in range(len(transition[i])):
			d[states[j]] = transition[i][j]
		d_transition[states[i]] = d
	for i in range(len(emission)):
		d = {}
		for j in range(len(emission[i])):
			d[e_var[j]] = emission[i][j]
		d_emission[states[i]] = d
	return d_transition, d_emission

def add_prob(states, obs, d_emission):
	p = {}
	for i in states:
		p[i] = d_emission[i][obs[0]]
	return p

def prob_calc(obs, states, d_transition, d_emission):
	dict = { s:[] for s in states} 
	probabilities = add_prob(states, obs, d_emission)
	
	for i in range(1, len(obs)):
		last_p = probabilities
		probabilities = {}
		for curr in states:
			combinations = []
			for max_i in states:
				a = last_p[max_i]
				b = d_transition[max_i][curr]
				c = d_emission[curr][obs[i]]
				combinations.append([a*b*c, max_i])
			[maxp, max_i] = max(combinations)
			probabilities[curr] = maxp
			dict[curr].append(max_i)

	return dict,probabilities

def Viterbi(dict, p, states):
	maxp = -1
	max_dict = None
	for s in states:
		dict[s].append(s)
		if p[s] > maxp:
			max_dict = dict[s]
			maxp = p[s]
	return max_dict


obs, line, e_var, states, transition, emission = init_params(s)
transition, emission = add_values(s, states, line, e_var, transition, emission)
d_transition, d_emission = make_dict(e_var, states, transition, emission)
dict, probabilities = prob_calc(obs, states,  d_transition, d_emission)
string = Viterbi(dict,probabilities, states)
string = ''.join(string)
f = open("output_q1_Ajay_Kannan.txt",'w')
f.write(string)
f.close()

