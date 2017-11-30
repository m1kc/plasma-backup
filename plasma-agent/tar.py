from interfaces import Strategy

import os
import subprocess


class StrategySimpleTar(Strategy):
	"""
	StrategySimpleTar compresses targets with UNIX tar.
	"""

	def can_execute(self):
		result = subprocess.run(["which", "tar"])
		return (result.returncode == 0)

	def execute(self):
		args = ['tar', '--create', '--file', self.outputPath, '-v'] + self.targetFolders
		result = subprocess.run(args)
		return (result.returncode == 0)