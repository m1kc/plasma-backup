from interfaces import Strategy

import os
import subprocess

import logging; log = logging.getLogger(__name__)


class StrategySimpleTar(Strategy):
	"""
	StrategySimpleTar compresses targets with UNIX tar.
	"""

	def can_execute(self):
		result = subprocess.run(["which", "tar"])
		return (result.returncode == 0)

	def execute(self):
		log.info("Creating tar archive: %s", self.outputPath)
		args = ['tar', '--create', '--file', self.outputPath] + self.targetFolders
		# args = ['tar', '--create', '--file', self.outputPath, '-v'] + self.targetFolders
		result = subprocess.run(args)
		if result.returncode == 0:
			return None
		else:
			return "tar error"
