import collections

class DigestCounter(dict):
	def __missing__(self, key):
		return 0

output_file = open("collisions.txt", 'w')

digests = DigestCounter()

sorted_digests = collections.defaultdict(list)

print "Finding duplicates"

digests_file = open("output.txt", 'r')

digs = []
for line in digests_file:
	digs.append(line.strip('\n\r'))

messages_file = open("input.txt", 'r')

msgs = []
for line in messages_file:
	msgs.append(line.strip('\n\r'))

for i in range(len(msgs)):
	msg = msgs[i]
	dig = digs[i]

	digests[dig] += 1
	sorted_digests[dig].append(msg)

collisions = collections.defaultdict(list)

for key in sorted_digests.keys():
	values = sorted_digests[key]

	if digests[key] > 1:
		collisions[key] = values
		output_file.write(key + ": " + str(values) + '\n')

print "Total Collisions: " + str(len(collisions.keys()))