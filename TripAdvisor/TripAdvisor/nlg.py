# coding: utf8
import random
import os

def generate_long_sentence(name, address, phone, price, rank, feature, question_type):
	sentences = []
	path = os.path.abspath('.')

	if type(question_type) == str:
		name = "this restaurant"
		if question_type == "phone":
			sentence = generate_phone_sentence(phone, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)
			else:
				sentence = "This restaurant doesn't have contact information"
		elif question_type == "speciality":
			sentence = generate_feature_sentence(feature, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)
			else:
				sentence = "This restaurant doesn't have feature information"
			sentences.append(sentence)
		elif question_type == "price":
			sentence = generate_price_sentence(price, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)
			else:
				sentence = "This restaurant doesn't have price information"
			sentences.append(sentence)
	else:	
		if question_type == 1:
			name = name.title()
			# rank sentence
			sentence = generate_rank_sentence(rank, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)
			# price sentence
			sentence = generate_price_sentence(price, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)
			# phone, address and feature
			sentence = generate_phone_sentence(phone, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)

			sentence = generate_address_sentence(address, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)

			sentence = generate_feature_sentence(feature, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)
		elif question_type == 3:
			name = "this restaurant"
			sentence = generate_address_sentence(address, name, path)
			if sentence != "ERROR":
				sentences.append(sentence)
		else:
			return "ERROR"

	temp_sentence = '.'.join(sentences)
	# Capitalize the first word
	temp_sentence = temp_sentence[0].upper() + temp_sentence[1:]
	# Capitalize all first words in sentences and put space between every sentence.
	pos = temp_sentence.find(".")
	while pos != -1:
		temp_sentence = temp_sentence[:pos + 1] + " " +  temp_sentence[pos + 1].upper() + temp_sentence[pos+2:]
		if temp_sentence[pos + 1:].find(".") == -1:
			break
		pos = temp_sentence[pos + 1:].find(".") + pos + 1

	temp_sentence = temp_sentence[:len(temp_sentence)] + '.'

	return temp_sentence

def generate_price_sentence(price, name, path):
	print "price:",price
	if price == '$$$$':
		sentence = generate_sentence('expensive', path+'/TripAdvisor/price.txt')
	elif price != '':
		sentence = generate_sentence('cheap', path+'/TripAdvisor/price.txt')
	else:
		return "ERROR"
	sentence = sentence.replace('NAME', name)
	if sentence.find("PRICE") != -1:
		if price == '$':
			sentence = sentence.replace("PRICE", "£1 - £10")
		elif price == '$$ - $$$':
			sentence = sentence.replace("PRICE", "£11 - £30")
		elif price == '$$$$':
			sentence = sentence.replace("PRICE", "more than £30")
		else:
			return "ERROR"
	return sentence

def generate_rank_sentence(rank, name, path):
	if rank == 1:
		sentence = generate_sentence('highest', path+'/TripAdvisor/rank.txt')
	elif rank < 2000:
		sentence = generate_sentence('high', path+'/TripAdvisor/rank.txt')
	elif rank >= 2000:
		sentence = generate_sentence('low', path+'/TripAdvisor/rank.txt')
	else:
		return "ERROR"
	sentence = sentence.replace('NAME', name)
	if sentence.find("RANK") != -1:
		sentence = sentence.replace("RANK", "#" + str(rank))
	return sentence

def generate_phone_sentence(phone, name, path):
	if phone != '+ Add phone number' or None:
		# "none": whatever the input
		sentence = generate_sentence('none', path+'/TripAdvisor/phone.txt')
	else:
		return "ERROR"
	sentence = sentence.replace('NAME', name)
	if sentence.find("PHONE") != -1:
		sentence = sentence.replace("PHONE", phone)
	return sentence

def generate_address_sentence(address, name, path):
	if address != None:
		# "none": whatever the input
		sentence = generate_sentence('none', path+'/TripAdvisor/address.txt')
	else:
		return "ERROR"
	sentence = sentence.replace('NAME', name)
	if sentence.find("ADDRESS") != -1:
		sentence = sentence.replace("ADDRESS", address)
	return sentence

def generate_feature_sentence(feature, name, path):
	if feature != None:
		# "none": whatever the input
		sentence = generate_sentence('none', path+'/TripAdvisor/feature.txt')
	else:
		return "ERROR"
	sentence = sentence.replace('NAME', name)
	if sentence.find("FEATURE") != -1:
		sentence = sentence.replace("FEATURE", feature)
	return sentence

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

