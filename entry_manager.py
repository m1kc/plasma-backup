from interfaces import EntryManager

import os


class EntryManagerFilesystem(EntryManager):
	"""
	EntryManagerFilesystem is an implementation of EntryManager that works
	with .tar archives in the given folder.
	"""
	def __init__(self, path):
		super(EntryManagerFilesystem, self).__init__()
		self.path = path

	def list(self):
		src = os.listdir(self.path)
		ret = []
		for i in src:
			if i.endswith('.tar'):
				ret += [i[:-4]]
		ret.sort()
		return ret

	def remove(self, entry):
		filename = os.path.join(self.path, entry+'.tar')
		#print('remove:', filename)
		os.remove(filename)

	def _add(self, entry):
		filename = os.path.join(self.path, entry+'.tar')
		#print('_add:', filename)
		fd = os.open(filename, os.O_CREAT)
		os.close(fd)
