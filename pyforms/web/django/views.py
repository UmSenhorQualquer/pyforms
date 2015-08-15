from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.views.decorators.cache 			import never_cache
from django.views.decorators.csrf 			import csrf_exempt
import json, simplejson, os
from django.contrib.staticfiles.views import serve

@never_cache
@csrf_exempt
def updateapplicationform(request, application):
	module 				= settings.PYFORMS_APPLICATIONS.createInstance(application)
	module.httpRequest 	= request

	module.loadSerializedForm( json.loads(request.body) )
	
	result 				= module.serializeForm()

	return HttpResponse(simplejson.dumps(result), "application/json")

@never_cache
@csrf_exempt
def pyformsjs(request): 
	filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pyforms.js')
	abspath = open(filename,'r')
	response = HttpResponse(content=abspath.read())
	response['Content-Type']= 'text/javascript'
	response['Content-Disposition'] = 'attachment; filename=pyforms.js'
	return response