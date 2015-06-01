import json
from django.db import models
from django.utils import timezone
from ..data import result_data
from jsonfield import JSONField
from model_utils.managers import InheritanceManager
import requests

from ..settings import conf

class Category(models.Model):
	name = models.CharField(max_length=50)

	def rate(self, sprint, team):
		return Metric.rate(self.metric_set.filter(active=True).select_subclasses(), sprint, team)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)
		verbose_name_plural = "categories"

class Metric(models.Model):

	@classmethod
	def rate(cls, list_of_metrics, sprint, team):
		rating = 0
		max_rating = 0
		for metric in list_of_metrics:
			metric_results = metric.get_results(sprint, team)
			rating += metric_results['score'] * metric.severity
			max_rating += 100 * metric.severity
		result = (rating/max_rating)*100
		return round(result, 2) 

	#Enables returning subclasses via select_subclasses()
	objects = InheritanceManager()

	categories = models.ManyToManyField(Category)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=2000)
	explanation = models.TextField(blank=True)
	query = models.TextField()
	endpoint = models.CharField(max_length=200)
	results = JSONField(null=True)
	last_query = models.DateTimeField(null=True, blank=True)
	active = models.BooleanField(default=True)
	HIGH = 1.5
	NORMAL = 1.0
	LOW = 0.5
	SEVERITY_CHOICES = (
		(HIGH, 'High (1.5x)'),
		(NORMAL, 'Normal (1.0x)'),
		(LOW, 'Low (0.5x)'),
	)
	severity = models.FloatField(choices=SEVERITY_CHOICES,
								default=NORMAL)

	def __str__(self):
		return self.name

	def _run_query(self):
		raise NotImplemented

	def _calculate_score(self, *args, **kwargs):
		raise NotImplemented

	def run(self):
		self.results = self._process(self._run_query())
		self.last_query = timezone.now()
		self.save()

	def score_rating(self, score):
		if score <= 25:
			return 'bad'
		if score >= 80:
			return 'good'
		if score <= 60:
			return 'improvement'
		return 'ok'

	def get_results(self, *args, **kwargs):
		score = self._calculate_score()
		rating = self.score_rating(score)
		return {'data':self.results, 'score':score, 'rating':rating}


class SprintMetric(Metric):
	def _run_query(self, sprint, team):
		url = 'http://192.168.30.196:7478/db/data/transaction/commit'
		payload = {
			"statements" : [ {
				"statement" : self.query.format(
								sprint=sprint,
								team=team['team_name'],
								label=team['label'],
								sprint_list=', '.join(["'"+s+"'" for s in conf.sprints])
							  )
			} ]
		}
		headers = {'Accept': 'application/json; charset=UTF-8', 'Content-Type': 'application/json'}
		r = requests.post(url, data=json.dumps(payload), headers=headers)

		print(sprint, team['name'], r.text[:100])
		data = r.json()
		errors = data.get('errors')
		if errors:
			print('ERROR:', errors)

		return data

	def _process(self, query_data):
		data = query_data['results'][0]
		result = {}
		result['rows'] = []
		for row in data['data']:
			result['rows'].append(row['row'])
		result['columns'] = data['columns']
		return result

	def run(self):
		results = {}
		for sprint in conf.sprints:
			results[sprint] = {}
			for team in conf.teams:
				results[sprint][team['name']] = self._process(self._run_query(sprint, team))
		self.results = results
		self.last_query = timezone.now()
		self.save()

	def _result_getter(self, sprint, team):
		# https://github.com/bradjasper/django-jsonfield/issues/101
		if isinstance(self.results, str):
			results = json.loads(self.results)
		else:
			results = self.results
		return results[sprint][team['name']]

	def get_results(self, sprint, team, *args, **kwargs):
		data = self._result_getter(sprint, team)
		score = self._calculate_score(sprint, team)
		rating = self.score_rating(score)
		return {'data': data, 'score':score, 'rating':rating}

	def get_value(self, sprint, team, column):
		results = self._result_getter(sprint, team)
		try:
			score_index = results['columns'].index(column)
		except ValueError:
			return None
		rows = results['rows']
		if rows:
			value = rows[0][score_index]
		else:
			value = None
		return value