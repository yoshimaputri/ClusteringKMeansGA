import numpy as np
from sklearn.decomposition import IncrementalPCA
import matplotlib.pyplot as plt
import random

def loadDataset(filename):
    ds = np.loadtxt(filename, delimiter='\t')
    return ds

data = loadDataset('seeds.txt')
dataset = data[:,:8]
#k=int(input("Masukkan jumlah k-cluster : "))
k = 3

def normalize(data):
    return (data-data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

datasets = dataset.copy()
datasets = datasets[:,:8]
datasets = normalize(datasets)

#use 3-cluster
cen = []
get = []
cen.append(datasets[0:70])
cen.append(datasets[71:140])
cen.append(datasets[141:210])
for i in range(k):
    np.random.shuffle(cen[i])
    get.append(cen[i][50])
initC = np.array(get)
print(initC)
#truly random
# centroids = datasets.copy()
# np.random.shuffle(centroids)
# initC = centroids[:k]
# initC

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
        data_ = datasets[cluster[i][x], :-1]
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
            dist.append(euclid(datasets[i,:-1], centroid[j,:], 7)) # calculate distance all data with centroid
        ind = np.argmin(dist) # get minimum dist to clustering
        cluster[ind].append(i)
    for i in range(k):
        centroid_ = new_centroid(cluster, i, new_c)
    centroid_ = np.array(centroid_)
    return centroid_, np.array(cluster)

# init centroid (k=1)
centroid, cluster = clustering(datasets, initC[:,:-1])

# init centroid (k after 1)
for i in range(k-1):
    centroid, cluster = clustering(datasets, centroid)
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

#error
true = 0
false = 0
for i in range(len(cluster)):
    lst = []
    for j in range(len(cluster[i])):
        ke = cluster[i][j]
        lst.append(dataset[ke,-1:])
    cls = int(max(lst,key=lst.count))
    print(cls)
    for j in range(len(cluster[i])):
        ke = cluster[i][j]
        if (dataset[ke,-1:] == cls):
            true += 1;
        else:
            false += 1;
print(true, false)
err = ((210)-true)/210*100
acc = true/210*100
print("accuracy", acc)
print("error",err)

fig, axs = plt.subplots(1, 1, figsize=(5,5))
for i in range(k):
    color = "#%06x" % random.randint(0, 0xFFFFFF)
    for j in range(len(cluster[i])):
        ke = cluster[i][j]
        x = pca[ke,0]
        y = pca[ke,1]
        axs.scatter(x,y,color=color,marker=">")
    axs.scatter(pca2[i,0], pca2[i,1], marker="o")
plt.show()
