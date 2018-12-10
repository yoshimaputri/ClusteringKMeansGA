# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 20:05:02 2018

@author: Z A A F
"""

import numpy as np

def loadDataset(filename):
	ds = np.loadtxt(filename, delimiter='\t')
	return ds

def euclidDist(v1, v2, row, col):
    distList = []
    for x in range(row):
        dist = 0
        for y in range(col):
            dist += pow((v1[x][y]-v2[x][y]), 2)
        distList.append(np.sqrt(dist))
    return distList

def euclidean_dist(v1, v2, length):
    dist    = 0
    for x in range(length):
        dist += pow((v1[x]-v2[x]), 2)
    return np.sqrt(dist)

class kMeans:
    def __init__(self, dataset, k):
        self.data = dataset
        self.k = k
        self.centroids = self.initialize_centroids()
        self.clusters = np.zeros(dataset.shape[0])
    def initialize_centroids(self):
        centroids = self.data.copy()
        np.random.shuffle(centroids)
        return centroids[:self.k]
    def closest_centroids(self, data):
        dist = []
        #Cari jarak terpendek dari data ke centroid, return centroid ke berapa
        for j in self.centroids:
            dist.append(euclidean_dist(data, j, data.shape[0]))
        return np.argmin(dist, axis=0)
    def clustering(self):
        error = 0
        #initial centroids
        center = self.centroids
        
        #old centroids
        oldCentroid = np.zeros(center.shape)
        
        #initial error
        err = euclidDist(center, oldCentroid, center.shape[0], center.shape[1])
        stop = 0
        
        while stop != 1:
            #Set Initial Clusters
            for i in range(len(self.data)):
                index = self.closest_centroids(self.data[i])
                self.clusters[i] = index
                
            oldCentroid = np.copy(center)
            
            #find new centroids
            for i in range(self.k):
                avg = [ self.data[j] for j in range(len(self.data)) if self.clusters[j]==i ]
                if avg:
                    center[i] = np.mean(avg, axis = 0)
            #print(center.shape[0])
            #new value of err
            err = euclidDist(center, oldCentroid, center.shape[0], center.shape[1])
            count = 0
            for i in range(len(err)):
                if(err[i]==0):
                    count += 1
            if(count==len(err)):
                stop = 1
        
        #NGITUNG ERRORNYA BELOM SELESE/GATAUUU
        for i in range(self.k):
            d = [euclidean_dist(self.data[j], center[i], center[i].shape[0]) for j in range(len(self.data)) if self.clusters[j]==i]
            error += np.sum(d)
                
        count = {key: 0.0 for key in range(self.k)}
        for i in range(len(self.data)):
            count[self.clusters[i]] += 1
        
        print("error %.5f" % error)
        print(self.k, error/len(self.data), count)
            
        return self.clusters

if __name__ == '__main__':
     data = loadDataset('seeds.txt')
     dataSeed= data[:,:7]
     k = 3
     
     obj = kMeans(dataSeed, k)
     clusters = obj.clustering()
     print(clusters)