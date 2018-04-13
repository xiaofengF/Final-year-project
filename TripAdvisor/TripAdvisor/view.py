# -*- coding: utf-8 -*-
from django.shortcuts import loader, render
from django.http import HttpResponse
from parser import Parser
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import nlg

@csrf_exempt

def index(request):
	return render(request, 'index.html')

def getData(request):
	query = (request.GET['query']).encode('utf-8')
	option = 0

	# get the option of the user
	try:
		if query[len(query) - 1] == '>':
			flag = query.find('<')
			option = int(query[flag + 1:len(query) - 1])
		if option:
			query = query[:flag]
	except ValueError:
		pass

	parser = Parser()
	# get the data from NLP system
	(data, question_type) = parser.get_data(query)

	answer = ""
	name = ""
	if type(question_type) == list:
		name = question_type[1]
		question_type = question_type[0]

	if data == None or question_type == None:
		return HttpResponse("Sorry I don't know what you mean.")

	print data

	if question_type == "4":
		# Yes or No question
		if len(data):
			answer = "Yes"
		else:
			answer = "No"

	# change format
	restaurants = []
	if question_type == "1" or question_type == "2":
		tag = data[0][2]
		restaurant = list(data[0])
		for i in xrange(1, len(data)):
			# add the feature to the restaurant
			if data[i][2] == tag:
				restaurant[8] = restaurant[8] + ", " + data[i][8]
				# reach the end of the loop
				if i == len(data) - 1:
					restaurants.append(restaurant)
			else:
				# next restaurant
				restaurants.append(restaurant)
				restaurant = list(data[i])
				tag = data[i][2]
	else: 
		for i in xrange(len(data)):
			restaurants.append(data[i])

	if question_type == "1":
		# descriptive question
		if len(restaurants) > 1:
			if option:
				return HttpResponse(nlg.generate_long_sentence(restaurants[option - 1][1], restaurants[option - 1][2], restaurants[option - 1][3], restaurants[option - 1][4], restaurants[option - 1][7], restaurants[option - 1][8], 1))
			
			rest_name = restaurants[0][1]
			answer = "There are " + str(len(restaurants)) + " <b>" + rest_name + "</b> in London. Which one do you mean?<br>"
			for i in xrange(len(restaurants)):
				answer = answer + str(i + 1) + ". " + rest_name + " on " + restaurants[i][2] + "<br>"
		else:
			answer = nlg.generate_long_sentence(restaurants[0][1], restaurants[0][2], restaurants[0][3], restaurants[0][4], restaurants[0][7], restaurants[0][8], 1)
	elif question_type == "2":
		# list question
		if option:
			return HttpResponse(nlg.generate_long_sentence(restaurants[option - 1][1], restaurants[option - 1][2], restaurants[option - 1][3], restaurants[option - 1][4], restaurants[option - 1][7], restaurants[option - 1][8], 1))
		
		restaurants_number = 20;
		if len(restaurants) < 20:
			restaurants_number = len(restaurants)

		answer = "There are results that match your question:<br>"
		for i in xrange(20):
			answer = answer + str(i + 1) + ". " + restaurants[i][1] + "<br>"
	elif question_type == "3":
		# location question
		if len(restaurants) > 1:
			answer = "This restaurant has " + str(len(restaurants)) +  " locations in London.<br>"
			for i in xrange(len(restaurants)):
				answer = answer + str(i + 1) + ". " + restaurants[i][0] + "<br>"
		else:
			answer = nlg.generate_long_sentence(None, restaurants[0][0], None, None, None, None, 3)
	elif question_type == "speciality":
		# speciality question
			feature = restaurants[0][0]
			for i in xrange(1, len(restaurants)):
				feature = feature + ", " + restaurants[i][0]
			print feature
			answer = nlg.generate_long_sentence(None, None, None, None, None, feature, "speciality")
	elif question_type == "phone" or question_type == "price":
		# phone question
		if option:
			if question_type == "phone":
				return HttpResponse(nlg.generate_long_sentence(None, None, restaurants[option - 1][0], None, None, None, "phone"))
			else:
				return HttpResponse(nlg.generate_long_sentence(None, None, None, restaurants[option - 1][0], None, None, "price"))
		if len(restaurants) > 1:
			answer = "There are " + str(len(restaurants)) + " <b>" + name + "</b> in London. Which one do you mean?<br>"
			for i in xrange(len(restaurants)):
				answer = answer + str(i + 1) + ". " + name + " on " + restaurants[i][1] + "<br>"
		else:
			if question_type == "phone":
				answer = nlg.generate_long_sentence(None, None, restaurants[0][0], None, None, None, "phone")
			else:
				answer = nlg.generate_long_sentence(None, None, None, restaurants[0][0], None, None, "price")
	return HttpResponse(answer)

