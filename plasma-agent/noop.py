from interfaces import Strategy

class StrategyNoop(Strategy):
	"""
	StrategyNoop does nothing.
	"""

	def can_execute(self):
		return True

	def execute(self):
		return
