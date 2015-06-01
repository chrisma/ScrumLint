from .base import SprintMetric
from ..settings import conf
import json

class DailyUserStoryThroughput(SprintMetric):
	def _calculate_score(self, sprint, team):
		SCORE_COLUMN = 'USperDev'
		UPPER_BOUND = 10
		LOWER_BOUND = 0.2
		
		value = self.get_value(sprint, team, SCORE_COLUMN)
		if value is None:
			value = 0
		
		if value > UPPER_BOUND or value < LOWER_BOUND:
			return 25
		r = 80 + (value*5)
		return r if r<=100 else 100
