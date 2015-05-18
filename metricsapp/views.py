from django.shortcuts import render
from .models import Metric
from .settings import conf

def group_by(queryset, attrib):
	result = []
	for element in queryset:
		group = getattr(element, attrib).all()
		for ele in group:
			match = [r for r in result if r.get(attrib) == ele]
			if match:
				for m in match:
					m['items'].append(element)
			else:
				result.append({attrib:ele, 'items':[element]})
	return result

def index(request, sprint_index):
	sprint_index = int(sprint_index)
	sprint = conf.sprints[sprint_index-1]
	all_metrics = Metric.objects.select_subclasses()
	categories_list = group_by(all_metrics, 'categories')
	for cat in categories_list:
		cat['items'] = [{'obj': m, 'result': m.get_results(sprint)} for m in cat['items']]
	# metrics_list = [{'obj': m, 'result': m.get_results(sprint)} for m in all_metrics]
	sprint_scores = [Metric.rate(all_metrics, s) for s in conf.sprints[:sprint_index]]

	context = {	
		# 'metrics_list': metrics_list, 
		'categories_list': categories_list, 
		'current_sprint': sprint,
		'sprint_list': conf.sprints,
		'current_sprint_score': Metric.rate(all_metrics, sprint),
		'chart_overall_labels': list(conf.sprints[:sprint_index]),
		'chart_overall_data': sprint_scores,
	}
	
	return render(request, 'metricsapp/index.html', context)
