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
        self.centroids = self.initialize_centroids()
        self.clusters = []
    def initialize_centroids(self):
        centroids = self.data.copy()
        np.random.shuffle(centroids)
        return centroids[:self.k]
    def closest_centroids(self, data):
        dist = []
        #Cari jarak terpendek dari data ke centroid, return centroid ke berapa
        for j in self.centroids:
            dist.append(euclideanDistance(data, j, data.shape[0]))
        return np.argmin(dist, axis=0)
    def clustering(self):
        for j in range(self.k):
            self.clusters.append([])
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
    dataSeed= data[:,:7]
    k=3
    
    obj = kMeans(dataSeed, k)
    clusters = obj.clustering()  
    newCentroids = obj.update_centroids()
    
    for i in range(k):
        print("cluster %d" % i)
        print(len(clusters[i]))
    #print(clusters[0])
    #print("\n\n\n")
   # print(newCentroids)
    

main()