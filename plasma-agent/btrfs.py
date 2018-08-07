from interfaces import Strategy

import subprocess
import os

import logging; log = logging.getLogger(__name__)


class StrategyBtrfsSnapshot(Strategy):
	"""
	StrategyBtrfsSnapshot makes a read-only btrfs snapshot before archiving
	files to ensure consistent FS state.

	PLEASE NOTE: this strategy assumes btrfs root filesystem and that all
	important stuff lies within it (i.e. no target folders cross filesystem
	boundaries). If that's not the case, DON'T USE IT, IT WON'T WORK
	AS YOU EXPECT. Use StrategySimpleTar instead.
	"""

	def can_execute(self):
		result = subprocess.run(["btrfs", "fi", "df", "/"])
		return (result.returncode == 0)

	def execute(self):
		try:
			os.stat("/@snapshot")
			log.info("Deleting existing snapshot")
			result = subprocess.run(["btrfs", "subvolume", "delete", "--commit-after", "/@snapshot"])
			if result.returncode != 0:
				return "Failed to delete existing snapshot"
		except:
			pass

		log.info("Creating read-only snapshot at /@snapshot")
		result = subprocess.run(["btrfs", "subvolume", "snapshot", "-r", "/", "/@snapshot"])
		if result.returncode != 0:
			return "Failed to create snapshot"

		log.info("Running tar")
		folders = list(map(lambda x: "/@snapshot"+x, self.targetFolders))
		args = ['tar', '--create', '--file', self.outputPath] + folders
		# args = ['tar', '--create', '--file', self.outputPath, '-v'] + folders
		result = subprocess.run(args)
		#return (result.returncode == 0)

		log.info("Removing snapshot")
		result = subprocess.run(["btrfs", "subvolume", "delete", "--commit-after", "/@snapshot"])
		if result.returncode != 0:
			log.warning("Failed to delete snapshot, leaving it at /@snapshot")
