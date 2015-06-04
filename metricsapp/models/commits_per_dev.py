from .base import SprintMetric

class CommitsPerDev(SprintMetric):
	def _calculate_score(self, sprint, team):
		SCORE_COLUMN = 'CommitsperDev'
		
		value = self.get_value(sprint, team, SCORE_COLUMN)
		if value is None:
			value = 0
		
		# >12 commits gets you 100
		r = value*8.5
		return r if r<100 else 100
