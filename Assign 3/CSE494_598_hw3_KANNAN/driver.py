from numpy import unravel_index, zeros
import numpy as np

def create_counter(last):
    d={}
    count_matrix_head = []
    for char in sorted(last):
        if char not in count_matrix_head:
            count_matrix_head.append(char)
        else:
            continue
    #print(count_matrix_head)
    ret_mat = []
    for char in last:
        if char not in d:
            d[char] = 0
        d[char] += 1
        ret_mat.append([d[c] if c in d else 0 for c in count_matrix_head])
    return(ret_mat)
     

def BWM_matching(first, last, pattern_reversed, LtoF, Count):
    top, bottom = 0, len(last) - 1
    letters = list(set(last))
    letters.sort()
    while top <= bottom:
        if pattern_reversed:
            s = pattern_reversed[0]
            pattern_reversed = pattern_reversed[1:]
            s_index = letters.index(s)
            top_i, bottom_i = top, bottom
            #print(np.shape(Count))
            for i in range(len(Count)):
                if Count[s_index][i] != 0:
                    top_i = Count[s_index][i]
                    break
            bottom_i = Count[s_index][bottom]
           
            top = last.index(s) + Count[s_index][top_i]
            bottom = last.index(s) + Count[s_index][bottom_i]
#             if s in last[top:bottom+1]:
#                 lastColumn_top2bottom = last[top:bottom+1]
#                 topIndex = lastColumn_top2bottom.index(s)
#                 joined_lastColumn_top2bottom = ''.join(lastColumn_top2bottom)
#                 bottomIndex = joined_lastColumn_top2bottom.rfind(s)
#                 print(topIndex,bottomIndex)
#                 top = LtoF[topIndex]
#                 bottom = LtoF[bottomIndex]
#             else:
#                 print("p-correct")
#                 return 0
        else:
            #print("correct")
            return bottom - top + 1
    #print("incorrect")
    return 0

def length_of_patterns(string,last):
    last = list(last)
    first = sorted(last)
    string = string.split()
    nums = [i for i in range(len(list(first)))]
    x = []
    for i in range(len(first)):
        for j in range(len(first)):
            if last[i] == first[j]:
                first[j] = '.'
                x.append(j)
                break
    #print(nums)
    first = sorted(last)
    #print(first)
    #print(last)
    #print(x)
    #print()
    Count_matrix = create_counter(last)
    Count_matrix = np.transpose(Count_matrix)
    patterns_length = []
    for word in string:
        word = list(word)
        word.reverse()
        #print(np.shape(Count_matrix))
        patterns_length.append(BWM_matching(first,last,word,x,Count_matrix))
    return(patterns_length)


def global_alignment(s1, s2, b_matrix, indel):
    score_matrix = [[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)]
    reverse_array = [[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)]
    rs1, rs2 = s1, s2

    for i in range(1, len(s1)+1):
        score_matrix[i][0] = (-i)*indel
    for j in range(1, len(s2)+1):
        score_matrix[0][j] = (-j)*indel

    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            score_map = {score_matrix[i-1][j] - indel:0, 
                        score_matrix[i][j-1] - indel:1, 
                        score_matrix[i-1][j-1] + int(b_matrix[s1[i-1]][s2[j-1]]):2}
            score_matrix[i][j] = max(score_map.keys())
            reverse_array[i][j] = score_map[score_matrix[i][j]]

    row, col = len(s1), len(s2)
    max_score = score_matrix[row][col]

    while row*col != 0:
        if reverse_array[row][col] == 0:
            row -= 1
            rs2 = rs2[:col]+'-'+rs2[col:]
        elif reverse_array[row][col] == 1:
            col -= 1
            rs1 = rs1[:row]+'-'+rs1[row:]
        else:
            row -= 1
            col -= 1

    return [max_score,rs1,rs2]

def calc_p(match, i, j, gap, extend, f = False):
    if f:
        return gap if match[i][j-1] else extend
    else:
        return gap if match[i-1][j] else extend


def local_alignment(s1, s2, b_matrix, gap, extend):
    score_matrix = np.array([[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)])
    reverse_array = np.array([[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)])
    match = [[False for j in range(len(s2))] for i in range(len(s1))]
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                match[i-1][j-1] = True
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            bscore = int(b_matrix[s1[i-1]][s2[j-1]])
            score_map = {score_matrix[i-1][j] - calc_p(match, i-1, j-1, gap, extend):0,
                         score_matrix[i][j-1] - calc_p(match, i-1, j-1, gap, extend, f=True):1,
                         score_matrix[i-1][j-1] + bscore:2,
                         0:3}
            score_matrix[i][j] = max(score_map.keys())
            reverse_array[i][j] = score_map[score_matrix[i][j]]

    i, j = np.unravel_index(np.argmax(score_matrix, axis=None), score_matrix.shape)
    max_score = score_matrix[i][j]
    s1, s1 = s1[:i], s2[:j]
    while reverse_array[i][j] != 3 and i*j != 0:
        if reverse_array[i][j] == 0:
            i -= 1
            s1 = s1[:j] + '-' + s1[j:]
        elif reverse_array[i][j] == 1:
            j -= 1
            s1 = s1[:i] + '-' + s1[i:]
        elif reverse_array[i][j] == 2:
            i -= 1
            j -= 1

    return [max_score,s1[i:],s1[j:]]

def make_Bwm(t):
    s = t * 2
    t_array = [ s[i:i+len(t)] for i in range(len(t)) ]
    t_array = sorted(t_array)
    return ''.join(map(lambda x: x[-1], t_array))

def rank_Bwt(s):
    d = dict()
    ranks = []
    for c in s:
        if c not in d:
            d[c] = 0
        ranks.append(d[c])
        d[c] += 1
    return ranks, d


def reverse_Bwt(bw):
    ranks, d = rank_Bwt(bw)
    first = {}
    dic = 0
    for c, count in sorted(d.items()):
        first[c] = (dic, dic + count)
        dic += count
    row = 0 
    t = '$' 
    while bw[row] != '$':
        c = bw[row]
        t = c + t 
        row = first[c][0] + ranks[row]
    return t

