from django.shortcuts import render
from .models import Metric, Category
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

def index(request, sprint_index, team_name):
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
		chart_radar_labels.append(cat['categories'].name)
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
