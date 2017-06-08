from random import randint
import random
import os

numSignalsPerSim = 8
signalIndex1 = sys.argv[1]*numSignalsPerSim
signalIndex2 = sys.argv[2]*numSignalsPerSim
signalIndex3 = sys.argv[3]*numSignalsPerSim
signalIndex4 = sys.argv[4]*numSignalsPerSim

posOrNeg = [-1, 1]

# upper and lower bounds for torque values
upperBound = 6000
lowerBound = -6000

numSignals = 1000
changeRange = 1000

cwd = os.getcwd()
inputSignal = cwd + "/initialSignals.txt"
outputSignal = cwd + "/nextGenSignals.txt"
yvalsFile = cmd + "/yvals.txt"

currentSignal = ""
currentY = 0

max4Yvals = []
max4Indices = []
count = 0
for yvalLine in yvalsFile:
    yval = int(yvalLine.strip())
	if count < 4:
		max4Yvals.append(yval)
		max4Indices.append(count)
	else:
		minYval = min(max4Yvals)
		if (yval > minYval):
			ind = max4Yvals.index(minYval)
			max4Yvals[ind] = yval
			max4Indices[ind] = count
	count += 1

with open(yvalsFile, "r") as f_yvals:
	int(yvalsFile.readline().split("\n"))

	

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