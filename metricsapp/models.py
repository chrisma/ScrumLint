import json
from django.db import models
from django.utils import timezone
from metricsapp.data import result_data
from jsonfield import JSONField
from model_utils.managers import InheritanceManager

from metricsapp.settings import conf

class Metric(models.Model):

	@classmethod
	def rate(cls, list_of_metrics, sprint):
		rating = 0
		max_rating = 0
		for metric in list_of_metrics:
			metric_results = metric.get_results(sprint)
			rating += metric_results['score'] * metric.severity
			max_rating += 100 * metric.severity
		return (rating/max_rating)*100

	#Enables returning subclasses via select_subclasses()
	objects = InheritanceManager()

	name = models.CharField(max_length=50)
	description = models.CharField(max_length=2000)
	explanation = models.TextField(blank=True)
	query = models.CharField(max_length=2000)
	endpoint = models.CharField(max_length=200)
	results = JSONField(null=True)
	last_query = models.DateTimeField(null=True, blank=True)
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
		return result_data[self.name]

	def _process(self, query_data):
		data = query_data['results'][0]
		result = {}
		result['rows'] = []
		for row in data['data']:
			result['rows'].append(row['row'])
		result['columns'] = data['columns']
		return result

	def _calculate_score(self, *args, **kwargs):
		return 50*self.severity

	def run(self):
		self.results = self._process(self._run_query())
		self.last_query = timezone.now()
		self.save()

	def score_rating(self, score):
		if score >= 75:
			return 'good'
		if score <= 25:
			return 'bad'
		return 'ok'

	def get_results(self, *args, **kwargs):
		score = self._calculate_score()
		rating = self.score_rating(score)
		return {'data':self.results, 'score':score, 'rating':rating}


class SprintMetric(Metric):
	def _run_query(self, sprint):
		return result_data[self.name + ' ' + sprint]

	def run(self):
		results = {}
		for sprint in conf.sprints:
			results[sprint] = self._process(self._run_query(sprint))
		self.results = results
		self.last_query = timezone.now()
		self.save()

	def get_results(self, sprint=conf.sprints[-1], *args, **kwargs):
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		score = self._calculate_score(sprint)
		rating = self.score_rating(score)
		return {'data':results[sprint], 'score':score, 'rating':rating}

class DailyUserStoryThroughput(SprintMetric):
	def _calculate_score(self, sprint=conf.sprints[-1]):
		SCORE_COLUMN = 'USperDev'
		UPPER_BOUND = 10
		LOWER_BOUND = 0.2
		
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		results = results[sprint]
		
		score_index = results['columns'].index(SCORE_COLUMN)
		value = results['rows'][0][score_index]
		
		if value > UPPER_BOUND or value < LOWER_BOUND:
			return 25
		r = 80 + (value*5)
		return r if r<=100 else 100

class JustInTimeDevelopment(SprintMetric):
	def _calculate_score(self, sprint=conf.sprints[-1]):
		SCORE_COLUMN = 'Percentage'
		UPPER_BOUND = 0.3
		
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		results = results[sprint]
		
		score_index = results['columns'].index(SCORE_COLUMN)
		value = results['rows'][0][score_index]

		if value > UPPER_BOUND:
			return 20
		r = 100 - (value*300)
		return r if r >= 0 else 0