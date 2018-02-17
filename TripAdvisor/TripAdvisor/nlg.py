# coding: utf8
import random
import os
def generate_long_sentence(name, address, phone, price, rank, feature):
	if name == 'unknown':
		return ""
	sentences = []
	path = os.path.abspath('.')
	print path
	# rank sentence
	if rank == 1:
		sentences.append(generate_sentence('highest', path+'/TripAdvisor/rank.txt'))
	elif rank < 2000:
		sentences.append(generate_sentence('high', path+'/TripAdvisor/rank.txt'))
	elif rank >= 2000:
		sentences.append(generate_sentence('low', path+'/TripAdvisor/rank.txt'))
	# price sentence
	if price == '££££':
		sentences.append(generate_sentence('expensive', path+'/TripAdvisor/price.txt'))
	elif price != None:
		sentences.append(generate_sentence('cheap', path+'/TripAdvisor/price.txt'))
	# phone, address and feature
	if phone != None:
		sentences.append(generate_sentence('none', path+'/TripAdvisor/phone.txt'))
	if address != None:
		sentences.append(generate_sentence('none', path+'/TripAdvisor/address.txt'))
	if feature != None:
		sentences.append(generate_sentence('none', path+'/TripAdvisor/feature.txt'))

	# replace keywords

	
	# glue


	return '.'.join(sentences)

def generate_sentence(CAT, TXT_FILE):
	answer = read_expressions('sentence', CAT, TXT_FILE)
	generated_sentence = list_to_string(break_down(answer), "")
	return generated_sentence

def list_to_string(sentence, string):
	for item in sentence:
		if type(item) == list:
			string = list_to_string(item, string)
		else:
			if string != "":
				string = string + ' ' + item
			else:
				string = item
	return string

def break_down(answer):
	if type(answer) == list:
		and_or = 0
		temp = []

		for i in xrange(len(answer)):
			if answer[i] == '|':
				and_or = 1
				continue
			# part of the sentence
			part = answer[i]
			# have more than one choice
			if type(part) == list:
				temp.append(break_down(part))
			else:
				temp.append(part)
		if and_or == 1:
			return temp[random.randint(0, len(temp) - 1)]
		else:
			return temp


def read_expressions(position, CAT, TXT_FILE):
	file = open(TXT_FILE)
	while 1:
		line = file.readline()
		# end of the file
		if not line:
			break
		# change format
		index = line.find('->')
		left = split_to_part(line[:index].split(), CAT)
		right = split_to_part(line[index + 2:].split(), CAT)
		sentence = [] 
		temp = []
		# recursion
		if left == []:
			return sentence
		elif left[0] == position:
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
							s = read_expressions(e, CAT, TXT_FILE)
							if s != []:
								# print s
								sentence.append(s)	
							else:
								sentence.append(['UNKNOWN'])							
					else:
						# one non-terminal
						s = read_expressions(expression, CAT, TXT_FILE)
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
					temp.append('|')
					temp.append(sentence)
					sentence = temp
			return sentence
	file.close()
	return []

def split_to_part(items, CAT):
	formed = []
	temp = []
	for i in xrange(len(items)):
		if items[i] == '|':
			# more than 1 options
			part1 = [formed, '|']
			part2 = split_to_part(items[i+1:], CAT)
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
				 formed.append(split2(items[i], 1, CAT))
			else:
				temp = split2(items[i], 2, CAT)
		elif ']' in items[i]:
			temp.append(split2(items[i], 4, CAT))
			formed.append(temp)
		else:
			if items[i].split('=') == [items[i]]:
				# print items[i]
				formed.append(items[i])
				# print formed
				continue
			temp.append(split2(items[i], 3, CAT))
	return formed
			

def split2(item, t, CAT):
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

# generate_long_sentence('burger king', 'abcabc', '07715562605', '£££', 33, 'fast food')

