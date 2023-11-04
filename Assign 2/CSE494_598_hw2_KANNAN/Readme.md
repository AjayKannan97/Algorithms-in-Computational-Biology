Motif Search Algorithms

There are 3 code files. Create folders rand_output and gibbs_output.

Run the code and it will be saved in rand_output (Q1) and gibbs_output (Q2). The third question saved in main folder itself. 

		Run - python Q1.py Q2.py Q3.py

Comparisons of the Randomized Motif Search and Gibbs Sampler.

The RMS is a much faster algorithm than Gibbs. So, taking this into consideration, the number of algorithm runs is different for the two algorithms. For RMS, it is run for 1000, 10000 and 100000 each iteration of the infinite loop until the best score is achieved. Also for Gibbs, 1000, 2000 and 10000, and the implementation is run for 30 times. The result shows that RMS is consistent when run for many iterations considering each iteration has an infinite loop until the condition is satisfied. Whereas Gibbs is run for 30*N, increase the number of iterations within the main loop. Still Gibbs is slower. Also the implementation of randomised motif search is such that every iteration it is improved and compared before it's checked with the best score. In Gibbs, the best motif is chosen and compared with the overall best motif, making the search much slower than RMS. This shows that RMS has a higher learning rate than Gibbs Sampler and it's more uniform.









