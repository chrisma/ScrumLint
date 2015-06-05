from .base import SprintMetric

class MonsterStories(SprintMetric):
	def _calculate_score(self, sprint, team):
		SCORE_COLUMN = 'IssueCount'
		
		value = self.get_value(sprint, team, SCORE_COLUMN)
		if value is None:
			value = 0

		# 11 incidents gets you a 50 rating
		r = 100-(value*8)
		return 0 if r<0 else r
