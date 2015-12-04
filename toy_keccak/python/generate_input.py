import itertools

output_file = open("input.txt", 'w')

chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

length = 4

print "Generating inputs"

words = [''.join(i) for  i in itertools.product(chars, repeat = length)]

for word in words:
	output_file.write(word + '\n')