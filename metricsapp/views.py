from django.shortcuts import render
from .models import Metric
from .settings import conf

def index(request, sprint_index):
	sprint_index = int(sprint_index)
	sprint = conf.sprints[sprint_index-1]
	all_metrics = Metric.objects.select_subclasses()
	metrics_list = [{'obj': m, 'result': m.get_results(sprint)} for m in all_metrics]
	sprint_scores = [Metric.rate(all_metrics, s) for s in conf.sprints[:sprint_index]]

	context = {	
		'metrics_list': metrics_list, 
		'current_sprint': sprint,
		'sprint_list': conf.sprints,
		'current_sprint_score': Metric.rate(all_metrics, sprint),
		'chart_overall_labels': list(conf.sprints[:sprint_index]),
		'chart_overall_data': sprint_scores,
	}
	
	return render(request, 'metricsapp/index.html', context)
