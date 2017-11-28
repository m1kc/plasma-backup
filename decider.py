from datetime import date, timedelta
import unittest


class EntryManager(object):
	def __init__(self):
		super(EntryManager, self).__init__()

	def list(self):
		raise NotImplementedError()

	def remove(self, entry):
		raise NotImplementedError()


class Decider(object):
	"""
	Decider reads entries and removes extra ones.
	"""
	def __init__(self, entry_manager, policy):
		super(Decider, self).__init__()
		self.em = entry_manager
		self.policy = policy

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


class TestDecider(unittest.TestCase):
	def test_year(self):
		"""
		Adds a new backup every day of 2015, checks list of backups
		2nd of each month.
		"""
		em = EntryManagerMock()
		decider = Decider(em, {
			'monthly': 2,
			'weekly': 3,
			'daily': 5,
		})
		expected_results = {
			1: [
				'20150101-2330-monthly',
				'20150102-2330-daily',
			],
			2: [
				'20150101-2330-monthly',
				'20150119-2330-weekly',
				'20150126-2330-weekly',
				'20150127-2330-daily',
				'20150128-2330-daily',
				'20150129-2330-daily',
				'20150130-2330-daily',
				'20150131-2330-daily',
				'20150201-2330-monthly',
				'20150202-2330-weekly',
			],
			3: [
				'20150201-2330-monthly',
				'20150216-2330-weekly',
				'20150223-2330-weekly',
				'20150224-2330-daily',
				'20150225-2330-daily',
				'20150226-2330-daily',
				'20150227-2330-daily',
				'20150228-2330-daily',
				'20150301-2330-monthly',
				'20150302-2330-weekly',
			],
			4: [
				'20150301-2330-monthly',
				'20150316-2330-weekly',
				'20150323-2330-weekly',
				'20150327-2330-daily',
				'20150328-2330-daily',
				'20150329-2330-daily',
				'20150330-2330-weekly',
				'20150331-2330-daily',
				'20150401-2330-monthly',
				'20150402-2330-daily',
			],
			5: [
				'20150401-2330-monthly',
				'20150413-2330-weekly',
				'20150420-2330-weekly',
				'20150426-2330-daily',
				'20150427-2330-weekly',
				'20150428-2330-daily',
				'20150429-2330-daily',
				'20150430-2330-daily',
				'20150501-2330-monthly',
				'20150502-2330-daily',
			],
			6: [
				'20150501-2330-monthly',
				'20150511-2330-weekly',
				'20150518-2330-weekly',
				'20150525-2330-weekly',
				'20150528-2330-daily',
				'20150529-2330-daily',
				'20150530-2330-daily',
				'20150531-2330-daily',
				'20150601-2330-monthly',
				'20150602-2330-daily',
			],
			7: [
				'20150601-2330-monthly',
				'20150615-2330-weekly',
				'20150622-2330-weekly',
				'20150626-2330-daily',
				'20150627-2330-daily',
				'20150628-2330-daily',
				'20150629-2330-weekly',
				'20150630-2330-daily',
				'20150701-2330-monthly',
				'20150702-2330-daily',
			],
			8: [
				'20150701-2330-monthly',
				'20150713-2330-weekly',
				'20150720-2330-weekly',
				'20150727-2330-weekly',
				'20150728-2330-daily',
				'20150729-2330-daily',
				'20150730-2330-daily',
				'20150731-2330-daily',
				'20150801-2330-monthly',
				'20150802-2330-daily',
			],
			9: [
				'20150801-2330-monthly',
				'20150817-2330-weekly',
				'20150824-2330-weekly',
				'20150827-2330-daily',
				'20150828-2330-daily',
				'20150829-2330-daily',
				'20150830-2330-daily',
				'20150831-2330-weekly',
				'20150901-2330-monthly',
				'20150902-2330-daily',
			],
			10: [
				'20150901-2330-monthly',
				'20150914-2330-weekly',
				'20150921-2330-weekly',
				'20150926-2330-daily',
				'20150927-2330-daily',
				'20150928-2330-weekly',
				'20150929-2330-daily',
				'20150930-2330-daily',
				'20151001-2330-monthly',
				'20151002-2330-daily',
			],
			11: [
				'20151001-2330-monthly',
				'20151019-2330-weekly',
				'20151026-2330-weekly',
				'20151027-2330-daily',
				'20151028-2330-daily',
				'20151029-2330-daily',
				'20151030-2330-daily',
				'20151031-2330-daily',
				'20151101-2330-monthly',
				'20151102-2330-weekly',
			],
			12: [
				'20151101-2330-monthly',
				'20151116-2330-weekly',
				'20151123-2330-weekly',
				'20151126-2330-daily',
				'20151127-2330-daily',
				'20151128-2330-daily',
				'20151129-2330-daily',
				'20151130-2330-weekly',
				'20151201-2330-monthly',
				'20151202-2330-daily',
			],
		}
		d = date(2015, 1, 1)
		while True:
			#print('-->', d)
			# add entry
			stamp = 'daily'
			if d.isoweekday() == 1: stamp = 'weekly'
			if d.day == 1: stamp = 'monthly'
			stamp = str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2) + '-2330-' + stamp
			em.add(stamp)
			decider.execute()

			# if we're on checkpoint, compare
			if d.day == 2:
				self.assertEqual(em.list(), expected_results[d.month])

			# ok, go next
			d += timedelta(days=1)
			if d > date(2015, 12, 31):
				break


class EntryManagerMock(EntryManager):
	def __init__(self):
		super(EntryManagerMock, self).__init__()
		self.entries = []

	def add(self, x):
		# print('added', x)
		self.entries += [x]

	def list(self):
		return self.entries

	def remove(self, target):
		# print('removed', target)
		self.entries.remove(target)
