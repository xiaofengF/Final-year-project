CAT = 'price'
TXT_FILE = "reg_exp.txt"

def generate_sentence(start):
	answer = read_expressions(start)
	for a in answer:
		print '******'
		for i in a:
			print i

def read_expressions(position):
	file = open(TXT_FILE)
	while 1:
		line = file.readline()
		# end of the file
		if not line:
			break
		# change format
		index = line.find('->')
		left = split_to_part(line[:index].split())
		right = split_to_part(line[index + 2:].split())
		sentence = [] 
		temp = []
		# recursion
		if left[0] == position:
			if type(right[0]) != list:
				# terminal found
				return right
			else:
				for expression in right:
					if expression == '|':
						# divide options into different lists
						temp.append(sentence)
						sentence = []
					# branch of the tree
					if type(expression[0]) == list:
						# more than one non-terminal
						for e in expression:
							s = read_expressions(e)
							if s != []:
								# print s
								sentence.append(s)	
							else:
								sentence.append(['UNKNOWN'])							
					else:
						# one non-terminal
						s = read_expressions(expression)
						if s == [] and expression != '|':
							# terminal found
							sentence = expression
							for e in expression:
								if type(e) == list:
									sentence = ['UNKNOWN']
									break
							# print sentence
						elif s != []:
							# terminal found
							sentence.append(s)

				if temp != []:
					# divide options into different lists
					temp.append(sentence)
					sentence = temp
			return sentence
	file.close()
	return []

def split_to_part(items):
	formed = []
	temp = []
	for i in xrange(len(items)):
		if items[i] == '|':
			# more than 1 options
			part1 = [formed, '|']
			part2 = split_to_part(items[i+1:])
			if type(part2[0]) == list:
				for p in part2:
					part1.append(p)
				return part1
			else:
				part1.append(part2)
				return part1

		if '[' in items[i]:
			# nonterminal
			if items[i][len(items[i]) - 1] == ']':
				# only one condition part
				 formed.append(split2(items[i], 1))
			else:
				temp = split2(items[i], 2)
		elif ']' in items[i]:
			temp.append(split2(items[i], 4))
			formed.append(temp)
		else:
			if items[i].split('=') == [items[i]]:
				# print items[i]
				formed.append(items[i])
				# print formed
				continue
			temp.append(split2(items[i], 3))
	return formed
			

def split2(item, t):
	if t == 1 or t == 2:
		part = item.split('[')
		title = part[0]
		subpart = part[1].split('=')
		con = subpart[0]
		if t == 1:
			con1 = subpart[1][:len(subpart[1]) - 1]
		else:
			con1 = subpart[1]
		if con1 == '?':
			con1 = CAT
		return [title, [con, con1]]
	elif t == 3 or t == 4:
		part = item.split('=')
		con = part[0]
		if t == 3:
			con1 = part[1]
		else:
			con1 = part[1][:len(part[1]) - 1]
		if con1 == '?':
			con1 = CAT
		return [con, con1]
	else:
		print "Wrong input!"
		return None

generate_sentence('sentence')
