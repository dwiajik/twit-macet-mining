f = open('Indonesian_Manually_Tagged_Corpus.tsv', 'r')
text = f.read()

text = text.replace('\n', ' ').replace('\t', '/')
text = text.replace('  ', '\n')
print(text)
with open('Indonesian_Manually_Tagged_Corpus.txt', 'a') as f:
	f.write(text)
