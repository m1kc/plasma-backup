class Strategy(object):
	"""
	Strategy implements some way of archiving folders on the machine.
	"""
	def __init__(self, targetFolders, outputPath, options):
		super(Strategy, self).__init__()
		self.targetFolders = targetFolders
		self.outputPath = outputPath
		self.options = options

	def can_execute(self):
		"""
		Outputs True if all options are correct and this strategy can be
		executed in this system, False otherwise.
		"""
		raise NotImplementedError()

	def execute(self):
		"""
		Executes the strategy.
		"""
		raise NotImplementedError()
