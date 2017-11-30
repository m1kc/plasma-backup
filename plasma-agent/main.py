#!/usr/bin/env python3

from noop import StrategyNoop
from btrfs import StrategyBtrfsSnapshot
from tar import StrategySimpleTar

import os
import subprocess
from datetime import datetime


def main():
	print("Plasma 1.0")
	print("- written by m1kc")
	print("- https://github.com/m1kc/plasma")
	print("- licensed under GNU GPL v3")
	print("")
	print("THIS SOFTWARE IS STILL EXPERIMENTAL.")
	print("USE AT YOUR OWN RISK.")
	print("")

	strategies = {
		'noop': StrategyNoop,
		'btrfs-snapshot': StrategyBtrfsSnapshot,
		'tar': StrategySimpleTar,
	}

	target_strategy = 'tar'
	targetFolders = ['/home/m1kc/work/Still-experimental/plasma/plasma-agent']
	tempPath = '/home/m1kc/work/Still-experimental/plasma/tdtdtdtdtd/last-backup.supertar'
	options = {}

	sshHost = 'localhost'
	sshUsername = 'm1kc'
	remoteFolder = '/home/m1kc/work/Still-experimental/plasma/tdtdtdtdtd'

	strategy = strategies[target_strategy](targetFolders, tempPath, options)
	if not strategy.can_execute():
		raise OSError("Cannot execute strategy")

	try:
		os.stat(tempPath)
		print("Deleting previous backup")
		os.remove(tempPath)
	except FileNotFoundError:
		pass

	print("Executing strategy:", target_strategy)
	strategy.execute()

	d = datetime.now()
	stamp = 'daily'
	if d.isoweekday() == 1: stamp = 'weekly'
	if d.day == 1: stamp = 'monthly'
	filename = "%d%s%s-%s%s-%s.tar" % (
		d.year, str(d.month).zfill(2), str(d.day).zfill(2),
		str(d.hour).zfill(2), str(d.minute).zfill(2),
		stamp
	)

	scpArg = "%s@%s:%s/%s" % (sshUsername, sshHost, remoteFolder, filename)
	print("Uploading file to", scpArg)
	result = subprocess.run(["scp", tempPath, scpArg])

	print("Everything's fine, exiting.")


if __name__ == '__main__':
	main()
