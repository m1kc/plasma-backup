from interfaces import Strategy

import os


class StrategyNoop(Strategy):
	"""
	StrategyNoop creates an empty file.
	"""

	def can_execute(self):
		return True

	def execute(self):
		fd = os.open(self.outputPath, os.O_CREAT | os.O_WRONLY)
		os.close(fd)
		return
