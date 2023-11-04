from driver import rms, gibbs, consensus

k, t, = 15, 10

with open('motif_dataset.txt') as input_data:
	dna_list = [line.strip() for line in input_data.readlines()]

d = []
for i in [1000,10000,100000]:
	motifs = rms(k,t,i,dna_list)
	d.append("RMS Output - K = " + str(i) + " score : "+str(motifs[0]) + "  Consensus : " + consensus(motifs[1]))
	print(d[-1])

for i in [1000,2000,10000]:
	motifs = gibbs(k,t,i,dna_list)
	d.append("Gibbs Output - K = " + str(i) + " score : "+str(motifs[0]) + "  Consensus : " + consensus(motifs[1]))
	print(d[-1])

with open("motif_dataset_output.txt","w") as txt_file:
    for line in d:
        txt_file.write("".join(line) + "\n")
