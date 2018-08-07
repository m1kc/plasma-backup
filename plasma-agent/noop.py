from interfaces import Strategy

import os

import logging; log = logging.getLogger(__name__)


class StrategyNoop(Strategy):
	"""
	StrategyNoop creates an empty file.
	"""

	def can_execute(self):
		return True

	def execute(self):
		log.debug("Creating empty file %s", self.outputPath)
		fd = os.open(self.outputPath, os.O_CREAT | os.O_WRONLY)
		os.close(fd)
		return
