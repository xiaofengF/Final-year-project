# -*- coding: utf-8 -*-
from django.shortcuts import loader, render
from django.http import HttpResponse
from parser import Parser
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	return render(request, 'index.html')

def getData(request):
	r = Parser()
	query = request.GET['query']
	query = query.encode('utf-8')
	data = r.get_data(query)
	if data == None:
		data = "Sorry I don't know what you mean." 
	return HttpResponse(data)


