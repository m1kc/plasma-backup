from interfaces import Strategy

import subprocess

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
			print("Deleting existing snapshot")
			result = subprocess.run(["btrfs", "subvolume", "delete", "--commit-after", "/@snapshot"])
		except:
			pass

		result = subprocess.run(["btrfs", "subvolume", "snapshot", "-r", "/@snapshot", "/"])

		folders = list(map(lambda x: "/@snapshot"+x, self.targetFolders))
		args = ['tar', '--create', '--file', self.outputPath] + folders
		# args = ['tar', '--create', '--file', self.outputPath, '-v'] + folders
		result = subprocess.run(args)
		#return (result.returncode == 0)

		try:
			result = subprocess.run(["btrfs", "subvolume", "delete", "--commit-after", "/@snapshot"])
		except:
			print("StrategyBtrfsSnapshot: failed to delete snapshot, proceeding anyway")
