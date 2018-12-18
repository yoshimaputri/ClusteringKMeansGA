import random
import math

def normalize(col):
	hasil = []
	for c in range(len(col)):
		hasil.append((col[c] - min(col)) / (max(col) - min(col)))
	return hasil

class Kmeans:
	def __init__(self, dataset, k):
		self.k = k
		self.populasi = []
		self.chromosome = []
		self.centroids = []
		self.SSE = 0
		# self.data = {}
		self.jmlData = 0
		self.iter = 0
		self.col = 8 #atribut
		with open(dataset) as file:
			row = file.readlines()
			file.close()

		self.data = [[] for i in range(self.col)]
		
		for line in row[:]:
			fitur = line.split('\t')
			flag = 0
			count = 0
			for col in range(self.col):
				if flag == 0:
					self.data[col].append(fitur[7]) # kalo udah fitur ke 7, berhenti
					flag = 1
				else:
					self.data[col].append(float(fitur[count]))
					count +=1
		# inisialisasi member cluster
		self.memberCluster = [0 for x in range(len(self.data[1]))]
		# normalisasi data
		for i in range(1, self.col):
			self.data[i] = normalize(self.data[i])

		random.seed()
		c = []
		# ngambil data random dr rentang per kelas
		c.append(random.sample(range(0,70),1))
		c.append(random.sample(range(71,140),1))
		c.append(random.sample(range(141,210),1))

		# init centroid
		self.centroids = [[self.data[i][r] for i in range(1, len(self.data))] for r in random.sample(range(len(self.data[0])), self.k)]
		# print("init centroids", self.centroids)

	def minDistance(self, i): # min distance per data with centroid
		MIN = 9999
		numCluster = 0
		for centroid in range(self.k):
			jarak = self.euclid(i, centroid)
			if jarak < MIN:
				MIN = jarak
				numCluster = centroid
		if numCluster != self.memberCluster[i]:
			self.jmlData += 1
		self.SSE += (MIN**2)

		return numCluster

	def clusterData(self): # naruh data ke cluster
		self.jmlData = 0
		self.SSE = 0
		self.memberCluster = [self.minDistance(i) for i in range(len(self.data[1]))]
		# print("member of cluster ke-", self.memberCluster)

	def euclid(self, i, j):
		dist = 0
		for k in range(1, self.col):
			dist += (self.data[k][i] - self.centroids[j][k-1])**2
		return math.sqrt(dist)

	def clustering(self):
		konvergen = False
		while not konvergen:
			self.iter += 1
			self.clusterData()
			# print("jumlah data berubah", self.jmlData)
			if float(self.jmlData)/len(self.memberCluster) < 0.01:
				konvergen = True
		# print("jumlah iterasi: ", self.iter)

	def groupData(self):
		acc = []
		allMember = 0
		for centroid in range(len(self.centroids)):
			cluster1 = cluster2 = cluster3 = 0
			for nama in [self.data[0][i] for i in range(len(self.data[0])) if self.memberCluster[i] == centroid]:
				if nama == "1\n":
					cluster1 += 1
				elif nama == "2\n":
					cluster2 += 1
				elif nama == "3\n":
					cluster3 += 1
			allMember = cluster1+cluster2+cluster3
			maximum = max(cluster1, cluster2, cluster3)
			acc.append(float(maximum)/float(allMember))
		resAcc = 0
		for i in range(0, len(acc)):
			resAcc += acc[i]
		self.acc = (resAcc / 3.0) * 100
		# print("centroids now", self.centroids)
		return self.centroids, self.SSE, self.acc