from random import randint
from collections import Counter
import numpy as np
from scipy import stats

def HammingDistance(str1, str2):
    i = 0
    count = 0
 
    while(i < len(str1)):
        if(str1[i] != str2[i]):
            count += 1
        i += 1
    return count

def score(motifs):
    score = 0
    for i in range(len(motifs[0])):
        motif = ''.join([motifs[j][i] for j in range(len(motifs))])
        score += min([HammingDistance(motif, seq*len(motif)) for seq in 'ACGT'])
    return score

def profile_most_probable_kmer(dna, k, prof):
    nuc_loc = {nucleotide:index for index,nucleotide in enumerate('ACGT')}
    max_prob = [-1, None]
    for i in range(len(dna)-k+1):
        current_prob = 1
        for j, nucleotide in enumerate(dna[i:i+k]):
            current_prob *= prof[j][nuc_loc[nucleotide]]
        if current_prob > max_prob[0]:
            max_prob = [current_prob, dna[i:i+k]]
    return max_prob[1]

def profile_with_pseudocounts(motifs,k):
    prof = []
    for i in range(len(motifs[0])):
        freq = Counter([motifs[j][i] for j in range(len(motifs))])
        for j in ['A','C','G','T']:
            if j not in freq:
                freq[j] = 1
            else:
                freq[j] += 1
        t = []
        g = sum(freq.values())
        for i in ['A','C','G','T']:
            t.append(freq[i] / g)
        prof.append(t)
    return prof

def consensus(motifs):
	con_motif = ""
	for i in range(len(motifs[0])):
		s = [motifs[j][i] for j in range(len(motifs))]
		con_motif += (stats.mode(s)[0][0])

	return con_motif


def randomized_motif_search(dna,k,t):
    rand_ints = [randint(0,len(dna[0])-k) for a in range(t)]
    motifs = [dna[i][r:r+k] for i,r in enumerate(rand_ints)]
    best_score = [score(motifs), motifs]
    while True:
        prof = profile_with_pseudocounts(motifs,k)
        motifs = [profile_most_probable_kmer(seq,k,prof) for seq in dna]
        current_score = score(motifs)
        if current_score < best_score[0]:
            best_score = [current_score, motifs]
        else:
            return best_score
        
def gibbs_sampler(dna,k,t,N):
    rand_ints = [randint(0,len(dna[0])-k) for a in range(t)]
    motifs = [dna[i][r:r+k] for i,r in enumerate(rand_ints)]
    best_score = [score(motifs), motifs]
    for i in range(N):
        r = randint(0,t-1)
        current_profile = profile_with_pseudocounts([motif for index, motif in enumerate(motifs) if index!=r],k)
        motifs = [profile_most_probable_kmer(dna[index],k,current_profile) if index == r else motif for index,motif in enumerate(motifs)]
        current_score = score(motifs)
        if current_score < best_score[0]:
            best_score = [current_score, motifs]

    return best_score

def rms(k,t,N,dna_list):
    best_motifs = [k*t, None]
    for repeat in range(N):
        current_motifs = randomized_motif_search(dna_list,k,t)
        if current_motifs[0] < best_motifs[0]:
            best_motifs = current_motifs

    return (best_motifs)

def gibbs(k,t,N,dna_list):
    best_motifs = [k*t, None]
    for repeat in range(30):
        current_motifs = gibbs_sampler(dna_list,k,t,N)
        if current_motifs[0] < best_motifs[0]:
            best_motifs = current_motifs

    return (best_motifs)
    

