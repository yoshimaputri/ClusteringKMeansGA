import K_means
import numpy as np
import random
from operator import itemgetter
from sklearn.decomposition import IncrementalPCA
import matplotlib.pyplot as plt

def createPopulation():
	c = []
	gen = []
	for i in range(k):
		c.append(i*70)
		gen.append([])
	for x in range(0, 70): #populasi size = 70
		cluster.chromosome = []
		for y in range(k):
			gen[y] = [cluster.data[i][c[y]] for i in range(1, len(cluster.data))]
			cluster.chromosome.append(gen[y])
		cluster.populasi.append(cluster.chromosome)
		for z in range(k):
			c[z]+=1

def crossOver(prob):
	parent = []
	cluster.populasi = []
	crossOverRate = 0.3
	totChild = 0
	
	for i in range(len(prob)):
		R = random.uniform(0,1)
		if R < crossOverRate:
			parent.append(prob[i])
	for i in range(len(parent)):
		for j in range(i+1, len(parent)):
			os1 = []
			os2 = []
			x = parent[i]
			y = parent[j]
			os1.append(x[0])
			os1.append(y[1])
			os1.append(y[2])
			os2.append(y[0])
			os2.append(x[1])
			os2.append(x[2])
			cluster.populasi.append(os1)
			cluster.populasi.append(os2)
			totChild+=2
	# print("totChild: ", totChild)
	return totChild

def mutation(nP, cluster): #
	# Mutation changes a single gene in each offspring randomly.
	length = len(cluster.__dict__['populasi'])
	# print("chromosomes", cluster.__dict__['populasi'][length-1][2][3])
	for idx in range(nP):
		# The random value to be added to the gene.
		for i in range(length):
			random_value = np.random.uniform(0.0, 1.0)
			cluster.__dict__['populasi'][i][idx][3] + random_value

	return cluster
	
def getCentroidPop(i):
	cluster.centroids = cluster.populasi[i]

k = 3
fitness = []
cluster = K_means.Kmeans('seeds.txt', k)

#------------------------- POPULATION, CHROMOSOME, CLUSTERING -------------------------#
createPopulation()

for i in range(0, 70):
	getCentroidPop(i) # ngambil centroid d masing2 populasi
	cluster.clustering()
	centroid, SSE, acc = cluster.groupData()
	result = centroid, SSE, acc
	fitness.append(result)
	# per chromosome->centroid punya fitness function
	# print("SSE chromosome: %.2f" % SSE)
	# print("Acc chromosome: %.2f" % acc)

#--------------------------------- SELECTION ----------------------------------#
sortedFitness = sorted(fitness, key=itemgetter(2), reverse=True) # sorting akurasi
totF = 0
for count in range(0,70):
	totF += sortedFitness[count][1]
# print("totF: ", totF)

probChromosome = []
for i in range(0,70):
	probChromosome.append((sortedFitness[i][0], sortedFitness[i][1]/totF*100))
# print("probChromosome", probChromosome)

#---------------------- NEW GENERATION || FROM CROSS OVER || MUTATION -----------------------#
newGen = []
for i in range(0, 70):
	R = random.uniform(0, 1)
	if R > probChromosome[i][1] and R < probChromosome[i+1][1]:
		newGen.append(probChromosome[i+1][0])
	else:
		newGen.append(probChromosome[i][0])

jmlOS = crossOver(newGen)
newGeneration = []
generasiKe = 0

cluster = mutation(k, cluster)

for i in range(2):
	f = []
	newGeneration = []
	# newGeneration = mutation(k, )
	for i in range(0, jmlOS):
		getCentroidPop(i)
		cluster.clustering()
		centroid, SSE, acc = cluster.groupData()
		result = centroid, SSE, acc
		f.append(result)
		newGeneration.append(centroid)
	generasiKe+=1

	jmlOS = crossOver(newGeneration)
	newGeneration = []
	sortedFitness = sorted(f, key=itemgetter(2), reverse=True)
	# print("Generasi ke-%d" % generasiKe)
cluster.centroids = sortedFitness[0][0]
cluster.clustering()
centroid, SSE, acc = cluster.groupData()

#--------------------------------- GENERATE SCATTER ----------------------------------#
datased = []
clustered = []
for i in range(210):
	datased.append([])
	clustered.append(int(cluster.data[0][i])) # cluster predict

# print("data",datased)
for j in range(210):
	for i in range(7):
		datased[j].append(cluster.data[i+1][j])

print("Best Centroid :\n", np.array(centroid))
print("Accuracy :", acc)
print("SSE :", SSE)
# print("cluster", cluster)

X = datased
ipca = IncrementalPCA(n_components=2)
ipca.fit(X)
pca = ipca.transform(X)

C = np.array(centroid)
ipca2 = IncrementalPCA(n_components=2)
ipca2.fit(C)
pca2 = ipca2.transform(C)

fig, axs = plt.subplots(1, 1, figsize=(5,5))
for i in range(k):
	color = "#%06x" % random.randint(0, 0xFFFFFF)
	for j in range(len(clustered)):
		if (clustered[j] == i+1):
			x = pca[j,0]
			y = pca[j,1]
			axs.scatter(x,y,color=color,marker=">")
	axs.scatter(pca2[i,0], pca2[i,1], marker="o")
plt.show()