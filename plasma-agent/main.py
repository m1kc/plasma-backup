#!/usr/bin/env python3

from noop import StrategyNoop
from btrfs import StrategyBtrfsSnapshot
from tar import StrategySimpleTar

import os
import subprocess
import json
import sys
from datetime import datetime


CONFIG_PATH = '/etc/plasma-agent.json'

STRATEGIES = {
	'noop': StrategyNoop,
	'btrfs-snapshot': StrategyBtrfsSnapshot,
	'tar': StrategySimpleTar,
}

target_strategy = None
target_folders = None
temp_path = None
options = None

ssh_host = None
ssh_login = None
remote_folder = None


def main():
	splash()

	config = load_config()

	target_strategy = config['strategy']
	target_folders = config['folders']
	temp_path = config['tempfile']
	options = config['options']

	ssh_host = config['ssh']['host']
	ssh_login = config['ssh']['login']
	remote_folder = config['remoteFolder']

	# Make the backup

	strategy = STRATEGIES[target_strategy](target_folders, temp_path, options)
	if not strategy.can_execute():
		raise OSError("Cannot execute strategy")

	try:
		os.stat(temp_path)
		print("Deleting previous backup")
		os.remove(temp_path)
	except FileNotFoundError:
		pass

	print("Executing strategy:", target_strategy)
	err = strategy.execute()
	if err != None:
		print("Failed to execute strategy:", err)
		sys.exit(1)

	# Upload file

	d = datetime.now()
	stamp = get_stamp(d)
	filename = "%d%s%s-%s%s-%s.tar" % (
		d.year, str(d.month).zfill(2), str(d.day).zfill(2),
		str(d.hour).zfill(2), str(d.minute).zfill(2),
		stamp
	)

	scpArg = "%s@%s:%s/%s" % (ssh_login, ssh_host, remote_folder, filename)
	print("Uploading file to", scpArg)
	result = subprocess.run(["scp", temp_path, scpArg])
	if result.returncode != 0:
		print("Upload failed")
		sys.exit(1)

	print("Lauching plasma-rotate on remote host")
	sshArg = "%s@%s" % (ssh_login, ssh_host)
	result = subprocess.run(["ssh", sshArg, "plasma-rotate", remote_folder])
	if result.returncode != 0:
		print("WARNING: plasma-rotate failed, old backups were not deleted")
		sys.exit(1)

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
	print("- https://github.com/m1kc/plasma-backup")
	print("- licensed under GNU GPL v3")
	print("")
	print("THIS SOFTWARE IS STILL EXPERIMENTAL.")
	print("USE AT YOUR OWN RISK.")
	print("")


if __name__ == '__main__':
	main()
