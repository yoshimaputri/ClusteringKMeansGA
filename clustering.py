import random
import pprint
from csv import reader
import math
import numpy as np
 
def loadDataset(filename):
	ds = np.loadtxt(filename, delimiter='\t')
	return ds

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def main():
	data = loadDataset('seeds.txt')
	print('data :', data[0][3])

main()