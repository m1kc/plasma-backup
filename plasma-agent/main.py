#!/usr/bin/env python3

from noop import StrategyNoop
from btrfs import StrategyBtrfsSnapshot
from tar import StrategySimpleTar

import os
import subprocess
import json
from datetime import datetime


CONFIG_PATH = '/etc/plasma-agent.json'

STRATEGIES = {
	'noop': StrategyNoop,
	'btrfs-snapshot': StrategyBtrfsSnapshot,
	'tar': StrategySimpleTar,
}

target_strategy = None
targetFolders = None
tempPath = None
options = None

sshHost = None
sshUsername = None
remoteFolder = None


def main():
	splash()

	config = load_config()

	target_strategy = config['strategy']
	targetFolders = config['folders']
	tempPath = config['tempfile']
	options = config['options']

	sshHost = config['ssh']['host']
	sshUsername = config['ssh']['login']
	remoteFolder = config['remoteFolder']

	# Make the backup

	strategy = STRATEGIES[target_strategy](targetFolders, tempPath, options)
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

	# Upload file

	d = datetime.now()
	stamp = get_stamp(d)
	filename = "%d%s%s-%s%s-%s.tar" % (
		d.year, str(d.month).zfill(2), str(d.day).zfill(2),
		str(d.hour).zfill(2), str(d.minute).zfill(2),
		stamp
	)

	scpArg = "%s@%s:%s/%s" % (sshUsername, sshHost, remoteFolder, filename)
	print("Uploading file to", scpArg)
	result = subprocess.run(["scp", tempPath, scpArg])

	print("Lauching plasma-rotate on remote host")
	sshArg = "%s@%s" % (sshUsername, sshHost)
	result = subprocess.run(["ssh", sshArg, "plasma-rotate", remoteFolder])

	# Glad it's done
	print("Everything's fine, exiting.")


def load_config():
	with open(CONFIG_PATH) as f:
		s = f.read()
		config = json.loads(s)
		print("Loaded config from", CONFIG_PATH)
		return config


def get_stamp(date):
	ret = 'daily'
	if date.isoweekday() == 1:
		ret = 'weekly'
	if date.day == 1:
		ret = 'monthly'
	return ret


def splash():
	print("Plasma 1.0")
	print("- written by m1kc")
	print("- https://github.com/m1kc/plasma")
	print("- licensed under GNU GPL v3")
	print("")
	print("THIS SOFTWARE IS STILL EXPERIMENTAL.")
	print("USE AT YOUR OWN RISK.")
	print("")


if __name__ == '__main__':
	main()
