from django.shortcuts import render
from .models import Metric
from .settings import conf

def index(request, sprint):
	sprint = conf.sprints[int(sprint)-1]
	metrics_list = [{'obj': m, 'result': m.get_results(sprint)} for m in Metric.objects.select_subclasses()] 
	context = {'metrics_list': metrics_list, 'current_sprint': sprint}
	return render(request, 'metricsapp/index.html', context)
