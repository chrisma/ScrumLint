from .base import SprintMetric
from ..settings import conf
import json

class JustInTimeDevelopment(SprintMetric):
	def _calculate_score(self, sprint, team):
		SCORE_COLUMN = 'Percentage'
		UPPER_BOUND = 0.3
		
		value = self.get_value(sprint, team, SCORE_COLUMN)
		if value is None:
			value = 0

		if value > UPPER_BOUND:
			return 20
		r = 100 - (value*300)
		return r if r >= 0 else 0
