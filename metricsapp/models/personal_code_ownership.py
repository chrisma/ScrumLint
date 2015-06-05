from .base import SprintMetric

class PersonalCodeOwnership(SprintMetric):
	def _calculate_score(self, sprint, team):
		data = self._result_getter(sprint, team)
		amount = len(data['rows'])

		# 11 incidents gets you a 50 rating
		r = 100-(amount*4.84)
		return 0 if r<0 else r
