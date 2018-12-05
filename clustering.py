import csv
import math
import operator
import numpy as np
 
def loadDataset(filename, p, split, trainSet=[] , testSet=[]):
	with open(filename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		np.random.shuffle(dataset)
		for x in range(len(dataset)-1):
			for y in range(8):
				dataset[x][y] = float(dataset[x][y])
			if x >= p and x < min(p+split, len(dataset)-1):
				testSet.append(dataset[x])
			else:
				trainSet.append(dataset[x])


	
def main():
	
	
main()