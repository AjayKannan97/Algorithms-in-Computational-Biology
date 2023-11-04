from driver import gibbs

for i in range(1,5):
	with open('gibbs_testcases/test_'+str(i)+'.txt') as input_data:
		k,t,N = map(int, input_data.readline().split())
		dna_list = [line.strip() for line in input_data.readlines()]
	motifs = gibbs(k,t,N,dna_list)
	print("Writing Output "+str(i))#+ ": " + str(len(motifs)))
	with open("gibbs_output/output_"+str(i)+".txt","w") as txt_file:
		for line in motifs[1]:
			txt_file.write("".join(line) + "\n")

print("All files written!")