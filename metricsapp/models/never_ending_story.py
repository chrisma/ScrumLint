from .base import SprintMetric
from ..settings import conf
import json
from django.utils import timezone


class NeverEndingStory(SprintMetric):
	def _calculate_score(self, sprint=conf.sprints[-1]):
		UPPER_BOUND = 10
		LOWER_BOUND = 0.2
		
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		amount = len(results[sprint]['rows'])
		score = 100 - ((amount ** 2)*2)
		return score if score > 0 else 0

	def run(self):
		self.results = self._process(self._run_query())
		self.last_query = timezone.now()
		self.save()

	def _process(self, query_data):
		data = super()._process(query_data)
		results = {}
		for sprint in conf.sprints:
			results[sprint] = {'rows':[], 'columns':data['columns']}
			for row in data['rows']:
				if (sprint in row[-1]) and (row[-1].index(sprint) != len(row[-1])-1):
					results[sprint]['rows'] += [row]
		return results
