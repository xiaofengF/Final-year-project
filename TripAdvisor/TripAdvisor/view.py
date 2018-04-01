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

	try:
		if query[len(query) - 1] == '>':
			flag = query.find('<')
			option = int(query[flag + 1:len(query) - 1])
		if option:
			query = query[:flag]
	except ValueError:
		pass

	r = Parser()
	# get the answer from NLG system
	(data, question_type) = r.get_data(query)
	answer = ""

	if data == None or question_type == None:
		return HttpResponse("Sorry I don't know what you mean.")

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
	elif question_type == "3":
		for i in xrange(len(data)):
			restaurants.append(data[i])

	# 0: id 1: name 2:address 3: phone 4: price 5,6: postcode 7: rank 8: feature
	if question_type == "1":
		# descriptive question
		if len(restaurants) > 1:
			if option:
				return HttpResponse(nlg.generate_long_sentence(restaurants[option - 1][1], restaurants[option - 1][2], restaurants[option - 1][3], restaurants[option - 1][4], restaurants[option - 1][7], restaurants[option - 1][8], 1))
			
			rest_name = restaurants[0][1]
			answer = "There are " + str(len(restaurants)) + " <b>" + rest_name + "</b> in London. Which one do you mean?<br>"
			for i in xrange(len(restaurants)):
				answer = answer + str(i + 1) + ". " + rest_name + " in " + restaurants[i][2] + "<br>"
		else:
			answer = nlg.generate_long_sentence(restaurants[0][1], restaurants[0][2], restaurants[0][3], restaurants[0][4], restaurants[0][7], restaurants[0][8], 1)
	elif question_type == "2":
		# list question
		if option:
			return HttpResponse(nlg.generate_long_sentence(restaurants[option - 1][1], restaurants[option - 1][2], restaurants[option - 1][3], restaurants[option - 1][4], restaurants[option - 1][7], restaurants[option - 1][8], 1))
		
		restaurants_number = 20;
		if len(restaurants) < 20:
			restaurants_number = len(restaurants)

		answer = "There are results that match your search:<br>"
		for i in xrange(20):
			answer = answer + str(i + 1) + ". " + restaurants[i][1] + "<br>"
	elif question_type == "3":
		# location question


		if len(restaurants) > 1:
			if option:
				return HttpResponse(nlg.generate_long_sentence(restaurants[option - 1][1], restaurants[option - 1][2], restaurants[option - 1][3], restaurants[option - 1][4], restaurants[option - 1][7], restaurants[option - 1][8], 3))
			
			rest_name = restaurants[0][1]
			answer = "There are " + str(len(restaurants)) + " <b>" + rest_name + "</b> in London. Which one do you mean?<br>"
			for i in xrange(len(restaurants)):
				answer = answer + str(i + 1) + ". " + rest_name + " in " + restaurants[i][2] + "<br>"
		else:
			answer = nlg.generate_long_sentence(restaurants[0][1], restaurants[0][2], restaurants[0][3], restaurants[0][4], restaurants[0][7], restaurants[0][8], 3)


	# elif question_type == "4":
	# 	# Yes or No question

	# elif question_type == "5":
	# 	# detail question

	# answer = nlg.generate_long_sentence('burger king', 'abcabc', '07715562605', '£££', 33, 'fast food')
	return HttpResponse(answer)

