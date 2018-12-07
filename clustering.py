import random
import pprint
from csv import reader
import math
import numpy as np
from matplotlib import pyplot as plt

class kMeans:
    def __init__(self, dataset, k):
        self.data = dataset
        self.k = k
        self.centroids = self.initialize_centroids(self.data, self.k)
        self.clusters = list()
    def initialize_centroids(data, k):
        centroids = data.copy()
        np.random.shuffle(centroids)
        return centroids[:k]
    def closest_centroids(self, data):
        dist = []
        #Cari jarak terpendek dari data ke centroid, return centroid ke berapa
        for j in self.centroids:
            dist.add(euclideanDistance(data, j, data.shape[1]))
        return np.argmin(dist, axis=0)
    def clustering(self):
        for i in self.data:
            index = self.closest_centroids(i)
            self.clusters[index].append(i)
        return self.clusters
    def update_centroids(self):
        return np.mean(self.clusters, axis=0)
            
        
        
        
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
    dataSeed=data[:,:7]
    print('data :', data[0][3])
    

main()