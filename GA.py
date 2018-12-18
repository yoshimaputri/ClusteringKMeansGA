import kmeans
from operator import itemgetter
import random

def make_populasi():
	c1 = 0
	c2 = 70
	c3 = 140

	for x in range(0, 70): #population sizenya 70
		cluster.chromosome = []
		
		genotipe1 = [cluster.data[i][c1] for i in range(1, len(cluster.data))]
		genotipe2 = [cluster.data[i][c2] for i in range(1, len(cluster.data))]
		genotipe3 = [cluster.data[i][c3] for i in range(1, len(cluster.data))]

		cluster.chromosome.append(genotipe1)
		cluster.chromosome.append(genotipe2)
		cluster.chromosome.append(genotipe3)
		cluster.populasi.append(cluster.chromosome)
		# print(len(cluster.populasi))				
		c1+=1
		c2+=1
		c3+=1
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

cluster = kmeans.KMeans('seeds.txt', 3)
print(type(cluster))
make_populasi()
fitness = []
for i in range(0, 70):
	evaluasi_populasi(i)
	cluster.kClustering()
	centroid, sse, akurasi = cluster.pengelompokanData()
	eval = centroid, sse, akurasi
	fitness.append(eval)
	# print("Data fitness: ", fitness)
	#print("Data cluster: ", cluster.data)
	#print("Chromosome: ", centroid)
	print("SSE chromosome: %.2f" % sse)
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
		centroid, sse, akurasi = cluster.pengelompokanData()
		eval = centroid, sse, akurasi
		#print("Centroid di sini: ", centroid)
		fitness.append(eval)
		newGeneration.append(centroid)
		#print("Data cluster: ", cluster.data)
		#print("Chromosome: ", centroid)
		#print("SSE chromosome: %.2f" % sse)
		#print("AKurasi chromosome: %.2f" % akurasi)
	generasi+=1
	#print("New Geneartion iter: ", newGeneration)
	jumlahOffspring = cross_over2(newGeneration)
	newGeneration = []
	#print("fitness: ", fitness)
	sortedFitness = sorted(fitness, key=itemgetter(2), reverse=True)
	#print("sortedFitness: ", sortedFitness)
	#print("Generasi ke-%d" % generasi)
cluster.centroids = sortedFitness[0][0]
cluster.kClustering()
centroid, sse, akurasi = cluster.pengelompokanData()
print("Centroid terbaik: \n", centroid)
print("Akurasi: ", akurasi)
print("SSE: ", sse)
# print("cluster", cluster)


