import sys

with open(sys.argv[1], 'r') as corpus:
	for line in corpus:
		print(line.strip())
	#print(corpus.readlines()[:1].strip())
