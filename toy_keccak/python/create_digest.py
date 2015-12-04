import sys
import toy_keccak
import binascii

# Set up I/O
input_file = open(sys.argv[1], 'r')
output_file = open(sys.argv[2], 'w') 

print "Running hashes"

for line in input_file:

	# Read message
	msg = bytearray(binascii.unhexlify(line.strip('\n\r')))

	# Run through SHA-3
	test = toy_keccak.SHA3_X(msg, 16)
	
	# Write to file
	output_file.write(binascii.hexlify(test).upper() + '\n')
