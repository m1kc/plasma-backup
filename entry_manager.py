from interfaces import EntryManager

import os


class Converter(object):
	def __init__(self):
		super(Converter, self).__init__()

	def is_entry(self, x):
		return x.endswith('.tar')

	def from_filename(self, x):
		return x[:-4]

	def to_filename(self, x):
		return x+'.tar'


class EntryManagerFilesystem(EntryManager):
	"""
	EntryManagerFilesystem is an implementation of EntryManager that works
	with .tar archives in the given folder.
	"""
	def __init__(self, path):
		super(EntryManagerFilesystem, self).__init__()
		self.path = path
		self.conv = Converter()

	def list(self):
		src = os.listdir(self.path)
		ret = []
		for i in src:
			if self.conv.is_entry(i):
				ret += [self.conv.from_filename(i)]
		ret.sort()
		return ret

	def remove(self, entry):
		filename = os.path.join(self.path, self.conv.to_filename(entry))
		#print('remove:', filename)
		os.remove(filename)

	def _add(self, entry):
		filename = os.path.join(self.path, self.conv.to_filename(entry))
		#print('_add:', filename)
		fd = os.open(filename, os.O_CREAT)
		os.close(fd)
