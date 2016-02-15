import sys
import os

lines = [line.rstrip('\n').rstrip('\r') for line in open(sys.argv[1])]

for line in lines:
	if line[:1].isnumeric():
		with open(os.path.dirname(__file__) + sys.argv[1] + '-clean.txt', 'a') as f:
			f.write(line + "\r\n")
