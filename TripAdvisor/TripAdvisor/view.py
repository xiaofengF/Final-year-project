from django.shortcuts import loader, render
from django.http import HttpResponse
from parser import Parser
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	if request.POST.get('enter'):
		r = Parser()
		query = "Provide me the feature information of Barrafina."
		data = r.get_data(query)
		return render_to_response('index.html', {'data':data})
	else:
		return render_to_response('index.html')

	# if(request.GET.get('btn')):
	# 	r = Parser()
	# 	query = "Provide me the feature information of Barrafina."
	# 	data = r.get_data(query)
	# 	return render_to_response('index.html', {'data':data})
	# else:
	# 	return render_to_response('index.html')
