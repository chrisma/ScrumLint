from django.shortcuts import render
from .models import Metric, Category
from .settings import conf

from django.http import JsonResponse, HttpResponseNotAllowed

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

def index(request, sprint_index=None, team_name=None):
	if team_name is None:
		team_name = conf.teams[0]["name"]
	if sprint_index is None:
		sprint_index = len(conf.sprints)
	team = [team for team in conf.teams if team["name"] == team_name][0]
	sprint_index = int(sprint_index)
	sprint = conf.sprints[sprint_index-1]
	all_metrics = Metric.objects.filter(active=True).select_subclasses()
	categories_list = group_by(all_metrics, 'categories')
	chart_radar_labels = []
	chart_radar_data = []
	for cat in categories_list:
		cat['metrics'] = [(m, m.summary(sprint, team)) for m in cat['items']]
		score = cat['categories'].rate(sprint, team)
		cat['score'] = score
		chart_radar_data.append(score)
		chart_radar_labels.append(str(cat['categories'].name))
	sprint_scores = [Metric.rate(all_metrics, s, team) for s in conf.sprints[:sprint_index]]

	context = {	
		'categories_list': categories_list, 
		'current_sprint': sprint,
		'current_sprint_index': sprint_index,
		'sprint_list': conf.sprints,
		'current_team': team,
		'team_list': conf.teams,
		'current_sprint_score': Metric.rate(all_metrics, sprint, team),
		'chart_overall_labels': list(conf.sprints[:sprint_index]),
		'chart_overall_data': sprint_scores,
		'chart_radar_data': chart_radar_data,
		'chart_radar_labels': chart_radar_labels
	}
	
	return render(request, 'metricsapp/index.html', context)

def compare(request, sprint_index=None):
	if sprint_index is None:
		sprint_index = len(conf.sprints)
	sprint_index = int(sprint_index)
	sprint = conf.sprints[sprint_index-1]
	all_metrics = Metric.objects.filter(active=True).select_subclasses()
	metric_list = []
	for team in conf.teams:
		scores = [Metric.rate(all_metrics, s, team) for s in conf.sprints[:sprint_index]]
		metric_list.append( (team, scores) )

	context = {
		'sprint_list': conf.sprints,
		'current_sprint': sprint,
		'line_chart_labels': list(conf.sprints[:sprint_index]),
		'metric_list': metric_list,
	}
	return render(request, 'metricsapp/compare.html', context)


from django.views.decorators.csrf import csrf_exempt
# See https://docs.djangoproject.com/en/1.8/ref/csrf/
# for the proper way to handle CSRF & POST
@csrf_exempt
def deactivate(request):
	# request.POST can be {} on POST request
	if request.method != "POST":
		message = '405 - Method Not Allowed. Only POST is supported.'
		# first constructor parameter is the list of _allowed_ methods
		return HttpResponseNotAllowed(['POST'], message)
	try:
		metric_id = request.POST['metric_id']
		# Don't have to select_subclasses() here,
		# active is defined on the base model.
		metric = Metric.objects.get(id=metric_id)
	except (ValueError, Metric.DoesNotExist):
		return JsonResponse({'success': False})
	metric.active = False
	metric.save()
	return JsonResponse({'success': True})
