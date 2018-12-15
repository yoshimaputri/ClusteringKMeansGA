import numpy as np

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
	def new_centroid(self, cluster, index, new_c):
		i = index
		length = len(cluster[i])
		centro = []
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
	def clustering(self):
		cluster = []
		new_c = []
		for i in range(k):
		    cluster.append([])
		    new_c.append([])
		for i in range(len(dataset)):
		    dist = []
		    for j in range(len(initC)):
		        dist.append(euclid(dataset[i,:-1], initC[j,:-1], 7)) # calculate distance all data with centroid
		    ind = np.argmin(dist) # get minimum dist to clustering
		    cluster[ind].append(i)
		for i in range(k):
		    centroid_ = new_centroid(cluster, i, new_c)
		print(centroid_)
		
def loadDataset(filename):
	ds = np.loadtxt(filename, delimiter='\t')
	return ds

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return (np.sqrt(distance))
	
def main():
	data = loadDataset('seeds.txt')
	dataSeed = data[:,:8]
	k=3

main()