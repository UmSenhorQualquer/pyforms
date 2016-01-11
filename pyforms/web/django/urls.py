from django.conf.urls 			import patterns, url
from pyforms.web.django.views 	import updateapplicationform, pyformsjs, chartjs

urlpatterns = patterns('',
	url(r'^update/(?P<application>\w+)/', updateapplicationform),
	url(r'^pyforms.js', pyformsjs),
	url(r'^chart.js', 	chartjs),
)