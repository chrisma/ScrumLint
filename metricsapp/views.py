from django.shortcuts import render
from .models import Metric, Category
from .settings import conf

from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest

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

# Obligatory comment on how the author is aware of
# the code's shortcomings, but blames this on the
# lack of time
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
		metrics_data = []
		for metric in cat['items']:
			previous_scores = [metric.summary(s,team)['score'] for s in conf.sprints[:sprint_index]]
			metrics_data.append( (metric, metric.summary(sprint, team), previous_scores) )
		cat['metrics'] = metrics_data
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

	selected_team_names = request.GET.getlist('team', [])
	all_teams = conf.teams
	if selected_team_names:
		current_teams = [t for t in all_teams if t['name'] in selected_team_names]
	else:
		current_teams = all_teams

	# Line chart of ScrumLint score over sprints of selected teams
	all_metrics = Metric.objects.filter(active=True).select_subclasses()
	line_chart_data = []
	for team in current_teams:
		scores = [Metric.rate(all_metrics, s, team) for s in conf.sprints[:sprint_index]]
		line_chart_data.append( (team, scores) )

	# Radar chart of categories for each team
	categories = [c for c in Category.objects.all() if not c.is_empty()]
	radar_chart_data = []
	for team in current_teams:
		cat_scores = [c.rate(sprint, team) for c in categories]
		radar_chart_data.append( (team, cat_scores ) )
	category_names = [c.name for c in categories]

	# Line charts of individual metrics over sprints of selected teams
	metrics_chart_data = []
	for metric in all_metrics:
		team_scores = []
		for team in current_teams:
			metrics_scores = [metric.summary(s,team)['score'] for s in conf.sprints[:sprint_index]]
			team_scores.append( (team, metrics_scores) )
		metrics_chart_data.append( (metric, team_scores) )

	context = {
		'sprint_list': conf.sprints,
		'current_sprint': sprint,
		'current_sprint_index': sprint_index,
		'team_list': all_teams,
		'current_parameters': request.GET.urlencode(),
		'selected_teams': current_teams,
		'line_chart_data': line_chart_data,
		'line_chart_labels': list(conf.sprints[:sprint_index]),
		'radar_chart_data': radar_chart_data,
		'radar_chart_labels': category_names,
		'metrics_chart_data': metrics_chart_data,
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
		print('Malformed request')
		message = '400 - Malformed request.'
		return HttpResponseBadRequest(message)
	metric.active = False
	metric.save()
	return JsonResponse({'success': True})
