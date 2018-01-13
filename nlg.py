
class PREP(object):
	def getPREP(self):
		return 'of'

class V(object):
	def __init__(self, cat, subcat, tense, num):
		self.cat = cat
		self.subcat = subcat
		self.tense = tense
		self.num = num

	def getV(self):
		# V[CAT=feature SUBCAT=trans TENSE=pres, NUM=sg] -> 'serves' | 'provides'
		if self.cat == 'feature' and self.subcat == 'trans' and self.tense == 'pres' and self.num == 'sg':
			return ['serves', 'provides']
		# V[CAT=price SUBCAT=trans TENSE=pres, NUM=sg] -> 'will cost you' | 'will spend you'
		elif self.cat == 'price' and self.subcat == 'trans' and self.tense == 'pres' and self.num =='sg':
			return ['will cost you', 'will spend you']
		# V[CAT=ALL SUBCAT=predicate TENSE=pres, NUM=sg] -> 'is'
		elif self.subcat == 'predicate' and self.tense == 'pres' and self.num == 'sg':
			return ['is']
		else:
			return []

class N(object):
	def __init__(self, cat, subcat):
		self.cat = cat
		self.subcat = subcat

	def getN(self):
		# N[CAT=rank SUBCAT=obj] -> '#rank'
		if self.cat == 'rank' and self.subcat == 'obj':
			return ['RANK']
		# N[CAT=price SUBCAT=obj] -> 'cheap' | 'expensive'
		elif self.cat == 'price' and self.subcat == 'obj':
			return ['cheap', 'expensive']
		# N[CAT=phone SUBCAT=obj] -> 'REST PHONE'
		elif self.cat == 'phone' and self.subcat == 'obj':
			return ['PHONE']
		# N[CAT=address SUBCAT=obj] -> 'REST ADDRESS'
		elif self.cat == 'address' and self.subcat == 'obj':
			return ['ADDRESS']
		# N[CAT=sub SUBCAT=obj] -> '#rank restaurant in London' | 'cheap' | 'expensive'
		elif self.cat == 'sub' and self.subcat == 'obj':
			return ['RANK restaurant in London', 'cheap', 'expensive']
		# N[CAT=feature SUBCAT=obj] -> 'REST FEATURE'
		elif self.cat == 'feature' and self.subcat == 'obj':
			return ['FEATURE']
		# N[CAT=rank SUBCAT=obj1] -> 'the rank'
		elif self.cat == 'rank' and self.subcat == 'obj1':
			return ['the rank']
		# N[CAT=price SUBCAT=obj1] -> 'the price' | 'the cost'
		elif self.cat == 'price' and self.subcat == 'obj1':
			return ['the price', 'the cost']
		# N[CAT=phone SUBCAT=obj1] -> 'the phone number'
		elif self.cat == 'phone' and self.subcat == 'obj1':
			return ['the phone number']
		# N[CAT=address SUBCAT=obj1] -> 'the address'
		elif self.cat == 'address' and self.subcat == 'obj1':
			return ['the address']
		# N[CAT=feature SUBCAT=obj1] -> 'the feature'
		elif self.cat == 'feature' and self.subcat == 'obj1':
			return ['the feature']
		# N[CAT=price SUBCAT=obj2] -> 'REST PRICE'
		elif self.cat == 'price' and self.subcat == 'obj2':
			return ['PRICE']
		# N[CAT=feature SUBCAT=obj2] -> 'REST FEATURE'
		elif self.cat == 'feature' and self.subcat == 'obj2':
			return ['FEATURE']
		# N[CAT=ALL SUBCAT=sub] -> 'the restaurant' | 'REST NAME'
		elif self.subcat == 'sub':
			return ['the restaurant', 'NAME']
		else:
			return []

class VP(object):
	def __init__(self, cat, tense, num):
		self.cat = cat
		self.tense = tense
		self.num = num
		
	def getVP(self):
		result = []
		result1 = []
		v = V(self.cat,'predicate', self.tense, self.num)
		n = N(self.cat, 'obj')
		vData = v.getV()
		nData = n.getN()
		# VP[CAT=? TENSE=?, NUM=?n] -> V[SUBCAT=predicate TENSE=pres, NUM=sg] N[CAT=?, SUBCAT=obj]
		if vData != [] and nData != []:
			for verb in vData:
				for noun in nData:
					result.append(verb + ' ' + noun)

		v1 = V(self.cat, 'trans', self.tense, self.num)
		n1 = N(self.cat, 'obj2')
		v1Data = v1.getV()
		n1Data = n1.getN()
		# VP[CAT=? TENSE=?, NUM=?n] -> V[CAT=?] N[CAT=? SUBCAT=obj2]
		if v1Data != [] and n1Data != []:
			for verb in v1Data:
				for noun in n1Data:
					result1.append(verb + ' ' + noun)

		if result == []:
			return result1
		elif result1 == []:
			return result
		else:
			return [result, result1]


class NP(object):
	def __init__(self, cat):
		self.cat = cat

	def getNP(self):
		if self.cat == 'sub':
			# NP[CAT='sub'] -> N[SUBCAT='sub']
			n = N(self.cat, 'sub')
			return n.getN()
		else:
			n = N(self.cat, 'obj1')
			p = PREP()
			n1 = N(self.cat, 'sub')
			result = []
			# NP[CAT=?] -> N[CAT=? SUBCAT='obj1'] PREP N[CAT=? SUBCAT='sub'] | N[CAT=? SUBCAT='obj1']
			for noun in n.getN():
				for noun1 in n1.getN():
					result.append(noun + ' ' + p.getPREP() + ' ' + noun1)
			return [result, n.getN()]

np = NP('price')
vp = VP('price', 'pres', 'sg')

result = np.getNP()
print 'result of np', result
result1 = vp.getVP()
print 'result of vp', result1

