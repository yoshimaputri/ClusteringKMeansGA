import numpy as np
from sklearn.decomposition import IncrementalPCA
import matplotlib.pyplot as plt
import random

def loadDataset(filename):
    ds = np.loadtxt(filename, delimiter='\t')
    return ds

data = loadDataset('seeds.txt')
dataset = data[:,:8]
k=int(input("Masukkan jumlah k-cluster : "))

centroids = dataset.copy()
np.random.shuffle(centroids)
initC = centroids[:k]

def euclid(v1, v2, length): 
    dist = 0
    for i in range(length):
        dist += pow((v1[i]-v2[i]), 2)
    return (np.sqrt(dist))

def new_centroid(cluster, index, new_c):
    i = index
    length = len(cluster[i])
    centro = []
    data_ = []
    for a in range(7):
        centro.append([])
    for x in range(length):
        data_ = dataset[cluster[i][x], :-1]
        for y in range(len(data_)):
            centro[y].append(data_[y])
    for z in range(len(data_)):
        Centro = np.mean(centro[z])
        new_c[index].append(Centro)
    return new_c

def clustering(dataset, centroid):
    cluster = []
    new_c = []
    for i in range(k):
        cluster.append([])
        new_c.append([])
    for i in range(len(dataset)):
        dist = []
        for j in range(len(initC)):
            dist.append(euclid(dataset[i,:-1], centroid[j,:], 7)) # calculate distance all data with centroid
        ind = np.argmin(dist) # get minimum dist to clustering
        cluster[ind].append(i)
    for i in range(k):
        centroid_ = new_centroid(cluster, i, new_c)
    centroid_ = np.array(centroid_)
    return centroid_, np.array(cluster)

# init centroid (k=1)
centroid, cluster = clustering(dataset, initC[:,:-1])

# init centroid (k after 1)
for i in range(k-1):
    centroid, cluster = clustering(dataset, centroid)
    # print(centroid)

# to get x,y from 7 fitur
X = dataset
ipca = IncrementalPCA(n_components=2)
ipca.fit(X)
pca = ipca.transform(X)
# pca[:,0]
# dataset[:,-1:]
C = centroid
ipca2 = IncrementalPCA(n_components=2)
ipca2.fit(C)
pca2 = ipca2.transform(C)

fig, axs = plt.subplots(1, 1, figsize=(5,5))
for i in range(k):
    color = "#%06x" % random.randint(0, 0xFFFFFF)
    for j in range(len(dataset)):
        if (dataset[j,-1:] == i+1):
            x = pca[j,0]
            y = pca[j,1]
            axs.scatter(x,y,color=color,marker=">")
    axs.scatter(pca2[i,0], pca2[i,1], marker="o")
plt.show()