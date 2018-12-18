# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 19:21:08 2018

@author: PC
"""
import numpy as np
from sklearn.decomposition import IncrementalPCA
import matplotlib.pyplot as plt
import random
import copy

def loadDataset(filename):
    ds = np.loadtxt(filename, delimiter='\t')
    return ds

def euclid(v1, v2): 
    dist = 0
    for i in range(len(v1)):
        dist += pow((v1[i]-v2[i]), 2)
    return (np.sqrt(dist))

def normalize(data):
    return (data-data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

def init_centroids(dataset, k):
    centroids = copy.deepcopy(dataset)
    np.random.shuffle(centroids)
    np.random.shuffle(centroids)
    np.random.shuffle(centroids)
    return centroids[:k]

def compute_new_centroids(clusters):
    return np.mean(clusters, axis=0)

def compute_sse(k, clusters, datas, centroids):
    sum = 0
    for i in range(k):
            cluster = [datas[j] for j in range(len(datas)) if clusters[j] == i]
            for c in cluster:
                sum += euclid(c, centroids[i])**2
    return sum
        
def kmeans(dataset, centroid):
    k           = len(centroid)
    convergence = False
    datas       = copy.deepcopy(dataset)
    iterasi     = 0
    sse         = 0
    
    while not convergence:
        iterasi     += 1        
        clusters    = [] 
        cluster     = []
        
        oldCentroid = copy.deepcopy(centroid)
        for data in datas:
            dist        = []
            for i, center in enumerate(centroid):
                dist.append(euclid(data, center))
            n = np.argmin(dist, axis=0)
            clusters.append(n)
        
        #cluster    = [ datas[j] for j in range(len(datas)) if clusters[j]==i ]
        #UPDATE THE VALUE OF CENTROIDS
        #clusters = np.asarray(clusters)
        for i in range(k):
            cluster = [datas[j] for j in range(len(datas)) if clusters[j] == i]

        for i in range(k):
            centroid[i] = compute_new_centroids(cluster[i])
            
        sse = compute_sse(k, clusters, datas, centroids)
        print("SSE = %.3f" % sse)
        
        clusters.clear()
        err = euclid(centroid, oldCentroid)
        count = 0
        for i in range(len(err)):
            if(err[i]==0):
                count += 1
        if(count==len(err)):
            convergence = True
        
    return clusters, centroid

def init_population(npop):
    chromosomes     = []
    chromosome      = []
    for i in range(npop):
        genes           = []
        for i in range(0, 7, +1):
            gen = float('%.2f' % random.uniform(0.0, 1.0))
            genes.append(gen)
        chromosome.append(genes)
    chromosomes.append(chromosome)
    return chromosomes

def calcFitness (errors):
    fitnessScores = []
    totalError = sum(errors)
    i = 0
    # fitness scores are a fraction of the total error
    for error in errors:
        fitnessScores.append (float(errors[i])/float(totalError))
        i += 1
    return fitnessScores

def selection(fitnessScores):
    # sort chromosomes after ranking selection
    fitnessScores = sorted(generation, reverse=True, key=lambda elem: elem.fitness)
    return generation

#def perform_GA(npop, nM, nC, iterasi, data, generationCount, k):
    

if __name__ == '__main__':
    dataset = loadDataset('seeds.txt')
    dataset = dataset[:,:7]
    dataset = normalize(dataset)
    
    k           = int(input('k? '))
    population  = int(input('Jumlah Initial Population? '))
    nC          = float(input('Persentase Crossover? '))
    nM          = float(input('Persentase Mutasi? '))
    iterasi     = int(input('Jumlah Iterasi? '))
    
    #INITIALIZE POPULATION
    init_generation     = init_population(population)
    generation          = 0
    
    centroids           = init_centroids(dataset, k)
    clusters, centroid  = kmeans(dataset, centroids)
    
    while generation != iterasi:
        
        generation      += 1
    
    