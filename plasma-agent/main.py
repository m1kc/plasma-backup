#!/usr/bin/env python3

from noop import StrategyNoop
from btrfs import StrategyBtrfsSnapshot
from tar import StrategySimpleTar

import os


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
	outputPath = '/home/m1kc/work/Still-experimental/plasma/tdtdtdtdtd/last-backup.supertar'
	options = {}

	sshHost = 'localhost'
	sshPort = 22
	sshUsername = 'm1kc'
	remoteFolder = '/home/m1kc/work/Still-experimental/plasma/tdtdtdtdtd/'

	strategy = strategies[target_strategy](targetFolders, outputPath, options)
	if not strategy.can_execute():
		raise OSError("Cannot execute strategy")

	try:
		os.stat(outputPath)
		print("Deleting previous backup")
		os.remove(outputPath)
	except FileNotFoundError:
		pass

	print("Executing strategy:", target_strategy)
	strategy.execute()

	print("Everything's fine, exiting.")


if __name__ == '__main__':
	main()
