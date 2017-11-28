#!/usr/bin/env python3

from noop import StrategyNoop

def main():
	print("Plasma 1.0")
	print("- written by m1kc")
	print("- https://github.com/m1kc/plasma")
	print("- licensed under GNU GPL v3")
	print("")
	print("THIS SOFTWARE IS STILL EXPERIMENTAL.")
	print("USE AT YOUR OWN RISK.")
	print("")

	target_strategy = StrategyNoop
	targetFolders = ['/home/m1kc/work/Still-experimental/plasma/plasma-agent']
	outputPath = ['/home/m1kc/work/Still-experimental/plasma/tdtdtdtdtd/last-backup.supertar']
	options = {}

	strategy = target_strategy(targetFolders, outputPath, options)
	if not strategy.can_execute():
		raise OSError("Cannot execute strategy")

	print("Executing the strategy...")
	strategy.execute()

	print("Everything's fine, exiting.")


if __name__ == '__main__':
	main()
