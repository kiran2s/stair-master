from random import randint
import random
import os

posOrNeg = [-1, 1]

# upper and lower bounds for torque values
upperBound = 2000 
lowerBound = -2000

# fps and simulation duration
fps = 60
simDuration = 20 
signalLength = fps * simDuration

# how many and how much can it change
numSignals = 1000
nextItrRange = 75

cwd = os.getcwd()
output = cwd + "/initialSignals.txt"

currentSignal = ""
currentY = 0

# open out file
with open(output, 'w') as f_out:

	i = 0
	while i < numSignals:
		currentY = randint(lowerBound, upperBound)
		currentSignal += str(currentY) + ","
		
		j = 1
		while j < signalLength:
			nextY = (random.choice(posOrNeg) * randint(0, nextItrRange)) + currentY
			if nextY >= lowerBound and nextY <= upperBound:
				currentSignal += str(nextY) + "," 
				currentY = nextY
				j += 1

		f_out.write(currentSignal[:-1] + "\n")
		currentSignal = ""
		i += 1