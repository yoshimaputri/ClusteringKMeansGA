import K_means
from operator import itemgetter
import random
from sklearn.decomposition import IncrementalPCA
import matplotlib.pyplot as plt
import numpy as np

def createPopulation():
	c = []
	gen = []
	for i in range(k):
		c.append(i*70)
		gen.append([])
	for x in range(0, 70): #populasi , size = 70
		cluster.chromosome = []
		for y in range(k):
			gen[y] = [cluster.data[i][c[y]] for i in range(1, len(cluster.data))]
			cluster.chromosome.append(gen[y])

		cluster.populasi.append(cluster.chromosome)
		for z in range(k):
			c[z]+=1
	# print("Populasi: ", cluster.populasi)

def cross_over2(ProbabilityChromosomes):
	parent = []
	crossOverRate = 0.25
	jumlahChild = 0
	del cluster.populasi[:]
	for i in range(len(ProbabilityChromosomes)):
		R = random.uniform(0,1)
		if R < crossOverRate:
			parent.append(ProbabilityChromosomes[i])
	#print("Parent Chrom: ", parent)
	for i in range(len(parent)):
		for j in range(i+1, len(parent)):
			offspring1 = []
			offspring2 = []

			mother = parent[i]
			#print("Mother: ", mother)
			father = parent[j]
			#print("Father: ", father)
			offspring1.append(mother[0])
			offspring1.append(father[1])
			offspring1.append(father[2])

			offspring2.append(father[0])
			offspring2.append(mother[1])
			offspring2.append(mother[2])
			#child1 = mother[0] + father[1] + father[2]
			#child2 = father[0] + mother[1] + mother[2]
			#print("child1: ", offspring1)
			#print("child2: ", offspring2)
			cluster.populasi.append(offspring1)
			cluster.populasi.append(offspring2)
			jumlahChild+=2
	#print("jumlahChild: ", jumlahChild)
	return jumlahChild
	
def evaluasi_populasi(i):
	cluster.centroids = cluster.populasi[i]

k = 3
cluster = K_means.Kmeans('seeds.txt', k)
# print(type(cluster))
createPopulation()
fitness = []
for i in range(0, 70):
	evaluasi_populasi(i)
	cluster.kClustering()
	centroid, sse, akurasi = cluster.groupData()
	eval = centroid, sse, akurasi
	fitness.append(eval)
	# print("Data fitness: ", fitness)
	#print("Data cluster: ", cluster.data)
	#print("Chromosome: ", centroid)
	# print("SSE chromosome: %.2f" % sse)
	#print("AKurasi chromosome: %.2f" % akurasi)
#print("fitness: ", fitness)
sortedFitness = sorted(fitness, key=itemgetter(2), reverse=True) #sort pake akurasi (2)
#print("sortedFitness: ", sortedFitness)

#Proses seleksi
TotalFitness = 0
for count in range(0,70):
	TotalFitness += sortedFitness[count][1]
#print("TotalFitness: ", TotalFitness) 

ProbabilityChromosomes = []
jumlah = 0
for count in range(0,70):
	ProbabilityChromosomes.append((sortedFitness[count][0],sortedFitness[count][1]/TotalFitness*100))

newGeneration1 = []
for i in range(0, 70):
	R = random.uniform(0, 1)
	if R > ProbabilityChromosomes[i][1] and R < ProbabilityChromosomes[i+1][1]:
		newGeneration1.append(ProbabilityChromosomes[i+1][0])
	else:
		newGeneration1.append(ProbabilityChromosomes[i][0])

#print("Probality Chrom: ", ProbabilityChromosomes)
#print("newGeneration1: ", newGeneration1)

jumlahOffspring = cross_over2(newGeneration1)
newGeneration = []
generasi = 0

for i in range(2):
	fitness = []
	newGeneration = []
	for i in range(0, jumlahOffspring):
		evaluasi_populasi(i)
		cluster.kClustering()
		centroid, sse, akurasi = cluster.groupData()
		eval = centroid, sse, akurasi
		fitness.append(eval)
		newGeneration.append(centroid)
		#print("SSE chromosome: %.2f" % sse)
		#print("AKurasi chromosome: %.2f" % akurasi)
	generasi+=1
	#print("New Geneartion iter: ", newGeneration)
	jumlahOffspring = cross_over2(newGeneration)
	newGeneration = []
	sortedFitness = sorted(fitness, key=itemgetter(2), reverse=True)
	#print("sortedFitness: ", sortedFitness)
	print("Generasi ke-%d" % generasi)

cluster.centroids = sortedFitness[0][0]
cluster.kClustering()
centroid, sse, akurasi = cluster.groupData()

datased = []
clustered = []
for i in range(210):
	datased.append([])
	clustered.append(int(cluster.data[0][i])) # cluster predict

# print("data",datased)
for j in range(210):
	for i in range(7):
		datased[j].append(cluster.data[i+1][j])

# print("data", datased)
print("Centroid terbaik: \n", centroid)
print("Akurasi: ", akurasi)
print("SSE: ", sse)
# print("cluster", cluster)

X = datased
ipca = IncrementalPCA(n_components=2)
ipca.fit(X)
pca = ipca.transform(X)

C = np.array(centroid)
ipca2 = IncrementalPCA(n_components=2)
ipca2.fit(C)
pca2 = ipca2.transform(C)
# cluster[0][0]
fig, axs = plt.subplots(1, 1, figsize=(5,5))
for i in range(k):
	color = "#%06x" % random.randint(0, 0xFFFFFF)
	for j in range(len(clustered)):
		# ke = cluster[i][j]
		if (clustered[j] == i+1):
			x = pca[j,0]
			y = pca[j,1]
			axs.scatter(x,y,color=color,marker=">")
	axs.scatter(pca2[i,0], pca2[i,1], marker="o")
plt.show()