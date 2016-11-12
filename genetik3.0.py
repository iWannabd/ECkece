import random as r
nodes = "ABCFED "

ketetanggan = {
	'S':
	{
	'A':6,
	'B':14,
	'C':10,
	'D':100000,
	'E':100000,
	'F':100000,
	'G':100000
	},
	'A':
	{
	'S':6,
	'B':6,
	'C':100000,
	'D':24,
	'E':100000,
	'F':100000,
	'G':100000
	},
	'B':
	{
	'A':6,
	'S':14,
	'C':4,
	'D':100000,
	'E':15,
	'F':100000,
	'G':100000
	},
	'C':
	{
	'A':100000,
	'B':4,
	'S':10,
	'D':100000,
	'E':100000,
	'F':18,
	'G':100000
	},
	'D':
	{
	'A':24,
	'B':100000,
	'C':100000,
	'S':100000,
	'E':4,
	'F':100000,
	'G':9
	},
	'E':
	{
	'A':100000,
	'B':15,
	'C':100000,
	'D':4,
	'S':100000,
	'F':4,
	'G':9
	},
	'F':
	{
	'A':100000,
	'B':100000,
	'C':18,
	'D':100000,
	'E':4,
	'S':100000,
	'G':9
	},
	'G':
	{
	'A':100000,
	'B':100000,
	'C':100000,
	'D':9,
	'E':9,
	'F':9,
	'S':100000
	},
}

keteta = {
	'S':
	{
	'A':6,
	'B':14,
	'C':10
	},
	'A':
	{
	'S':6,
	'B':6,
	'D':24,
	},
	'B':
	{
	'A':6,
	'S':14,
	'C':4,
	'E':15,
	},
	'C':
	{
	'B':4,
	'S':10,
	'F':18,
	},
	'D':
	{
	'A':24,
	'E':4,
	'G':9
	},
	'E':
	{
	'B':15,
	'D':4,
	'F':4,
	'G':9
	},
	'F':
	{
	'C':18,
	'E':4,
	'G':9
	},
	'G':
	{
	'D':9,
	'E':9,
	'F':9,
	},
}

class Individu:
	def __init__(self, arg):
		self.n = len(arg)
		self.kromosom = arg
		self.hitungFitness()

	def spaceremoval(self):
		# fungsi ini menghilangkan karakter spasi dalam kromosom
		# fungsi ini digunakan untuk menghitung total waktu tempuh
		nospace = []
		for i in self.kromosom:
			if i != ' ':
				nospace.append(i)
		return nospace

	def hitungRute(self):
		#fungsi ini digunakan untuk menentukan rute yang bisa dilalui oleh simpul-simpul dalam kromosom
		rute = ['S'] + self.spaceremoval() + ['G']
		bisa = ['S']
		j = 1
		i = 0
		while rute[j-1]!='G':
			while j<len(rute):
				if (rute[i] in keteta[rute[j]]) and (rute[j] not in bisa):
					i = j
					bisa.append(rute[j])
				j += 1	
		self.rute = bisa
		return bisa

	def hitungFitness(self):
		#fungsi ini digunakan untuk menghitung nilai fitness
		waktutempuh = 0
		rute = self.hitungRute()
		for i in range(len(rute)-1):
			waktutempuh += keteta[rute[i]][rute[i+1]]
		if rute[len(rute)-1]!='G':
			waktutempuh += 100
		self.fitness = float(1.0/waktutempuh)
		return float(1.0/waktutempuh)


def listprobabi(populasi):
	#fungsi ini digunakan sebagai pembantu dalam proses seleksi orangtua menggunakan metode roda rolet
	fitnseses = [a.fitness for a in populasi]
	totalfitness = float(sum(fitnseses))
	probs = [p/totalfitness for p in fitnseses]
	return [sum(probs[:i+1]) for i in range(len(probs))]

def rodaPutar(populasi,n):
	# n adalah jumlahindv
	# fungsi ini mengembalikan individu terpilih berdasarkan metode roda rolet
	terpilih = []
	popula = populasi[:]
	for nn in xrange(n):
		listprob = listprobabi(popula)
		pr = r.uniform(0,1)
		for i in xrange(len(popula)):
			if pr <= listprob[i]:
				terpilih.append(popula.pop(i))
				break
	return terpilih

def generateKromosom(n):
	#fungsi ini digunakan untuk membangkitkan kromosom acak
	# n adalah jumlah gen
	kromosom = []
	for i in range(n):
		kromosom.append(nodes[r.randint(0,len(nodes)-1)])
	return kromosom

def generatePopulasi(n,m):
	#digunakan untuk menginisiasi populasi awal saat program pertama dijalankan
	#n adalah jumlah individu dalam populasi
	#m adalah jumlah gen dalam individu
	pop = []
	for i in range(n):
		pop.append(Individu(generateKromosom(m)))
	return pop

def crossOver(ind1,ind2):
	#digunakan untuk melakukan proses crossover dengan satu titik poting
	a = ind1.kromosom
	b = ind2.kromosom
	x = r.randint(0,len(a)) #penentuan titik potong
	aa = a[:x]+b[x:]
	bb = b[:x]+a[x:]
	return Individu(aa),Individu(bb)

def mutasi(individu):
	#mutasi dilakukan dengan cara mengganti salah satu gen dengan simpul acak
	kromo = individu.kromosom
	pr = float(1.0/len(kromo)) #penentuan probabilitas terjadinya mutasi
	p = r.uniform(0,1)
	if (p<pr):
		i = r.randint(0,len(kromo)-1) #pentuan gen mana yang akan diganti
		kromo[i] = nodes[r.randint(0,len(nodes)-1)]
	return Individu(kromo)

def elitelit(populasi,n):
	#digunakan untuk menjaga kromosom terbaik dalam populasi
	#n adalah jumlah kromsom elit
	terbail = []
	populasi = sorted(populasi,key=lambda x:x.fitness,reverse=True)
	return populasi[:n]


nindv = 30 #jumalh individu dalam populasi
nelit = 2 #jumlah kromosom elit
generasi = 0
populasi = generatePopulasi(nindv,23)

while generasi<100:
	populasi = rodaPutar(populasi,nindv)
	newgen = []
	for i in xrange(0,nindv/2):
		newgen += crossOver(populasi[2*i],populasi[(2*i)+1])
	newgen = [mutasi(d) for d in populasi]
	newgen = sorted(newgen,key = lambda x:x.fitness,reverse=True)
	populasi = elitelit(populasi[:],nelit) + newgen[:-nelit]
	print "generasi ke",generasi
	print populasi[0].rute, populasi[0].fitness
	generasi += 1



