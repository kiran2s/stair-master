from random import randint
import random
import os

posOrNeg = [-1, 1]

# upper and lower bounds for torque values
upperBound = 6000
lowerBound = -6000

numSignals = 1000
changeRange = 1000

cwd = os.getcwd()
inputSignal = cwd + "/initialSignals.txt"
outputSignal = cwd + "/nextGenSignals.txt"

currentSignal = ""
currentY = 0

# open out file
with open(outputSignal, "w") as f_out:
	with open(inputSignal, "r") as f_in:
		signal = f_in.readline().split(",")

		i = 0
		while i < numSignals:

			j = 0
			while j < len(signal):
				nextY = (random.choice(posOrNeg) * randint(0, changeRange)) + int(signal[j])
				if nextY >= lowerBound and nextY <= upperBound:
					currentSignal += str(nextY) + "," 
					j += 1

			f_out.write(currentSignal[:-1] + "\n")
			currentSignal = ""
			i += 1