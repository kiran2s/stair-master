from random import randint
import random
import sys
import os

posOrNeg = [-1, 1]

'''
# upper and lower bounds for torque values
upperBound = 1000
lowerBound = -1000

# fps and simulation duration
fps = 10
simDuration = 10
signalLength = fps * simDuration
'''

# how many and how much can it change
numSimulations = 60
mutationRange = 100

yvalsFilename = sys.argv[1]

cwd = os.getcwd()
yvalsPathname = cwd + "/" + yvalsFilename

# Parse yvals/fitness values
yvals = {}
f_index = 0
f_in = open(yvalsPathname, 'r')
for line in f_in:
	yval = line.strip()
	yvals[float(yval)] = f_index
	f_index += 1
f_in.close()

# Get the top 4 fitness values and their corresponding indices
print yvalsFilename
bestIndices = []
sortedYvals = yvals.keys()
sortedYvals.sort(reverse=True)
i = 0
while i < 4:
	yval = sortedYvals[i]
	bestIndices.append(yvals[yval])
	print str(yval) + " " + str(yvals[yval])
	i += 1

if (len(sys.argv) < 3):
	print "1 argument passed in"
	sys.exit()

# Get all signals
signalsFilename = sys.argv[2]
signals = []
signalsPathname = cwd + "/" + signalsFilename
f_in = open(signalsPathname, 'r')
for line in f_in:
	signal = line.strip()
	signals.append(signal.split(","))
f_in.close()

# Extract the best signals
numSignalSetsToExtract = 4
if (len(sys.argv) == 4):
	numSignalSetsToExtract = int(sys.argv[3])

currSignalSet = 0
bestSignals = []
for i in bestIndices:
	if currSignalSet < numSignalSetsToExtract:
		signalBaseIndex = i*8
		bestSignals.append(signals[signalBaseIndex:signalBaseIndex+8])
		currSignalSet += 1

# Mutate best signals and write them to files
currentSignal = ""
outputFilename = "outputSignals"
i = 0
for signals in bestSignals:
	with open(outputFilename + str(i) + ".txt", 'w') as f_out:
		j = 0
		while j < numSimulations:
			for signal in signals:
				for force in signal:
					mutatedForce = (random.choice(posOrNeg) * randint(0, mutationRange)) + float(force)
					currentSignal += str(mutatedForce) + ","
				f_out.write(currentSignal[:-1] + "\n")
				currentSignal = ""
			j += 1
	i += 1

'''
# Write the best signals to a file
with open("outputSignals.txt", 'w') as f_out:
	for signals in bestSignals:
		for signal in signals:
			f_out.write(str(signal))
			f_out.write('\n')
		f_out.write('\n')
'''
