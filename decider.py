from interfaces import GenericDecider

class Decider(GenericDecider):
	def _get_group(self, label):
		ret = []
		src = self.em.list()
		for i in src:
			if i.endswith(label):
				ret += [i]
		return ret

	def _process_group(self, label):
		entries = self._get_group(label)
		target = self.policy[label]
		if len(entries) > target:
			for i in range(target):
				entries.pop()
			for i in entries:
				self.em.remove(i)

	def execute(self):
		self._process_group('monthly')
		self._process_group('weekly')
		self._process_group('daily')
