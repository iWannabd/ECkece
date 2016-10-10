import math
import random

class Node:
	"""docstring for node"""
	def __init__(self, node,x,y,demand):
		self.x = x
		self.y = y
		self.node = node
		self.demand = demand

	def jarak(self,Object):
		# return Object.x
		ox = Object.x
		oy = Object.y
		return math.sqrt((self.x-ox)**2+(self.y-oy)**2)


nodes = [Node(0,82,76,0),Node(1,96,44,19),Node(2,50,5,21),Node(3,49,8,6),Node(4,13,7,19),Node(5,29,89,7),Node(6,58,30,12),Node(7,84,39,16),Node(8,14,24,6),Node(9,2,39,16),Node(10,3,82,8),Node(11,5,10,14),Node(12,98,52,21),Node(13,84,25,16),Node(14,61,59,3),Node(15,1,65,22),Node(16,88,51,18),Node(17,91,2,19),Node(18,19,32,1),Node(19,93,3,24),Node(20,50,93,8),Node(21,98,14,12),Node(22,5,42,4),Node(23,42,9,8),Node(24,61,62,24),Node(25,9,97,24),Node(26,80,55,2),Node(27,57,69,20),Node(28,23,15,15),Node(29,20,70,2),Node(30,85,60,14),Node(31,98,5,9)]

class Individu(object):
	"""docstring for Individu"""
	def __init__(self,kromosom):
		self.kromosom = kromosom
		self.fitness = self.hitungFitness()

	def totaljarak(self):
		total = 0
		n = len(self.kromosom)-1 #panjang kromosom min satu
		total += nodes[self.kromosom[0]].jarak(nodes[0])
		for i in xrange(0,n):
			total += nodes[self.kromosom[i]].jarak(nodes[self.kromosom[i+1]]) #menjumlah total jarak
		total += nodes[self.kromosom[0]].jarak(nodes[self.kromosom[n]]) #ditambah jarak dari node terahir ke rumah
		return total

	def totalDemand(self):
		total = 0
		for i in self.kromosom:
			total += nodes[i].demand
		return total

	def hitungFitness(self):
		return 1/self.totaljarak()

# menciptakan individu individu random
def randomPopulasi(pk,jp):
	populasi = []
	while (len(populasi)<jp):
		calkro = [] #calon kromosom
		while (len(calkro)<pk-1):
			gen = random.randint(0,len(nodes)-1)
			if gen not in calkro:
				calkro.append(gen)
		ind = Individu(calkro)
		populasi.append(ind)
	return populasi

#daftar peluang kumulatif untuk kemungkinan terpilih
def listprobabi(populasi):
	fitnseses = [a.fitness for a in populasi]
	totalfitness = float(sum(fitnseses))
	probs = [p/totalfitness for p in fitnseses]
	return [sum(probs[:i+1]) for i in range(len(probs))]

#pemilihan orang tua
def rodaPutar(populasi,n):
	# n adalah jumlahindv
	terpilih = []
	popula = populasi[:]
	# print "popula ",[p.kromosom for p in populasi]
	for nn in xrange(n):
		listprob = listprobabi(popula)
		r = random.uniform(0,1)
		for i in xrange(len(popula)):
			if r <= listprob[i]:
				terpilih.append(popula.pop(i))
				break
	return terpilih

def crossOver(indv1,indv2):
	# crossover menggunakan OC
	n = len(indv1.kromosom)
	tp1 = random.randint(0, n)
	tp2 = random.randint(0, n)
	if tp1>tp2:
		tp1,tp2 = tp2,tp1
	#memisahkan yang segmen dan membuat nsegmen yang merupakan urtutan crossover
	segmen1 = indv1.kromosom[tp1:tp2]
	nsegmen1 = indv1.kromosom[tp2:]+indv1.kromosom[:tp1]+segmen1
	segmen2 = indv2.kromosom[tp1:tp2]
	nsegmen2 = indv2.kromosom[tp2:]+indv2.kromosom[:tp1]+segmen2
	#crossing over
	#bikin anak pertama, copy gen dari tp2 sampai ahir
	anak1 = []
	anak1 += segmen1
	# pointer i dan j
	i = tp2
	kk = 0

	while kk<len(nsegmen2) and i<n:
		if nsegmen2[kk] not in segmen1:
			anak1.append(nsegmen2[kk])
			kk += 1
			i += 1
		else:
			kk += 1

	temp = []
	# bikin anak pertama, copy gen dari awal sampai tp1
	while len(temp)<tp1 and kk<len(nsegmen2):
		if nsegmen2[kk] not in segmen1:
			temp.append(nsegmen2[kk])
		kk += 1

	anak1 = temp + anak1
	# bikin anak kedua,copy gene dari tp2 sampai ahir
	anak2 = []
	anak2 += segmen2
	i = tp2
	kk = 0
	while kk<len(nsegmen1) and i<n:
		if nsegmen1[kk] not in segmen2:
			anak2.append(nsegmen1[kk])
			kk += 1
			i += 1
		else:
			kk += 1
	#bikin anak kedia, copy gen dari awal sampai tp1
	temp = []
	while len(temp)<tp1 and kk<len(nsegmen1):
		if nsegmen1[kk] not in segmen2:
			temp.append(nsegmen1[kk])
		kk += 1
	anak2 = temp + anak2

	return Individu(anak1),Individu(anak2)

def mutasi(individu):
	#menghasilkan mutan
	kromo = individu.kromosom
	pm = 1/len(individu.kromosom)
	p = random.uniform(0,1)
	# lakukan mutasi jika random lebh kecil dari permutation rate
	if (p<=pm):
		#permutasi dilakukan dengan cara swaping, posisi
		#penentuan posisi dilakukan random
		t1 = random.randint(0,len(individu.kromosom))
		t2 = random.randint(0,len(individu.kromosom))
		kromo[t1],kromo[t2] = kromo[t2],kromo[t1]
	return Individu(kromo)

panjangkromosom = 12 #panjang kromosom
panjangkromosom += 1
jumlahindv = 10 #jumlah individu dalam populasi
gen = 1
populasi = randomPopulasi(panjangkromosom,jumlahindv)
while True:
	populasi = rodaPutar(populasi,jumlahindv)
	generasibaru = []
	for i in xrange(0,jumlahindv/2):
		generasibaru += crossOver(populasi[2*i],populasi[(2*i)+1])
	#baru lahir langsung dimutasi
	for i in xrange(0,jumlahindv):
		generasibaru[i] = mutasi(generasibaru[i])
	#general replacement
	populasi = generasibaru
	print "generasi ke",gen
	for individu in populasi:
		print individu.kromosom, individu.fitness
	gen += 1






