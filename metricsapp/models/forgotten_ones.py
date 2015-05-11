from .base import SprintMetric
from ..settings import conf
import json

class ForgottenOnes(SprintMetric):
	def _calculate_score(self, sprint=conf.sprints[-1]):
		SCORE_COLUMN = 'Percentage'
		UPPER_BOUND = 0.1
		
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		results = results[sprint]
		
		score_index = results['columns'].index(SCORE_COLUMN)
		value = results['rows'][0][score_index]

		r = 100 - (value*500)
		return r if r >= 0 else 0