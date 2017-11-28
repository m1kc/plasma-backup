class EntryManager(object):
	"""
	EntryManager manages existing backups. Mostly, deletes them.
	"""
	def __init__(self):
		super(EntryManager, self).__init__()

	def list(self): raise NotImplementedError()
	def remove(self, entry): raise NotImplementedError()


class GenericDecider(object):
	"""
	GenericDecider reads list of backups and removes extra (obsolete, outdated)
	ones. This interface defines a single method, execute().
	"""
	def __init__(self, entry_manager, policy):
		super(GenericDecider, self).__init__()
		self.em = entry_manager
		self.policy = policy

	def execute(self): raise NotImplementedError()
