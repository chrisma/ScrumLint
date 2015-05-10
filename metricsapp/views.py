from django.shortcuts import render
from .models import Metric
from .settings import conf

def index(request, sprint):
	sprint = conf.sprints[int(sprint)-1]
	all_metrics = Metric.objects.select_subclasses()
	metrics_list = [{'obj': m, 'result': m.get_results(sprint)} for m in all_metrics] 
	context = {	'metrics_list': metrics_list, 
				'current_sprint': sprint,
				'sprint_list': conf.sprints,
				'current_sprint_score': Metric.rate(all_metrics, sprint)}
	return render(request, 'metricsapp/index.html', context)
