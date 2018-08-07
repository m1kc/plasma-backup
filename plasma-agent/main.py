#!/usr/bin/env python3

from noop import StrategyNoop
from btrfs import StrategyBtrfsSnapshot
from tar import StrategySimpleTar

import os
import subprocess
import json
import sys
from datetime import datetime

import logging; log = logging.getLogger(__name__)


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
	logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(name)s: %(message)s')
	splash()

	config = load_config()

	target_strategy = config['strategy']
	target_folders = config['folders']
	temp_path = config['tempfile']
	options = config['options']

	ssh_host = config['ssh']['host']
	ssh_login = config['ssh']['login']
	remote_folder = config['remoteFolder']

	execute_before = config['executeBefore']
	execute_after = config['executeAfter']

	# Pick up strategy
	strategy = STRATEGIES[target_strategy](target_folders, temp_path, options)
	log.debug('Checking if we can use this strategy: %s', target_strategy)
	if not strategy.can_execute():
		raise OSError("Cannot execute strategy")

	# Execute pre-commands, cancel operation if any fails
	for cmd in execute_before:
		log.info("Executing pre-command: %s", cmd)
		subprocess.run(cmd, check=True, shell=True)

	# Make the backup

	try:
		log.debug('Checking for previous backup')
		os.stat(temp_path)
		log.info('Deleting previous backup')
		os.remove(temp_path)
	except FileNotFoundError:
		pass

	log.info("Starting backup (using strategy: %s)", target_strategy)
	err = strategy.execute()
	if err != None:
		log.error("Failed to execute strategy: %s", err)
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
	log.info("Uploading file to %s", scpArg)
	result = subprocess.run(["scp", temp_path, scpArg])
	if result.returncode != 0:
		log.error("Upload failed")
		sys.exit(1)

	log.info("Launching plasma-rotate on remote host")
	sshArg = "%s@%s" % (ssh_login, ssh_host)
	result = subprocess.run(["ssh", sshArg, "plasma-rotate", remote_folder])
	if result.returncode != 0:
		log.warning("plasma-rotate failed, old backups were not deleted")
		sys.exit(1)

	# Execute pre-commands, cancel operation if any fails
	for cmd in execute_after:
		log.info("Executing post-command: %s", cmd)
		try:
			subprocess.run(cmd, check=True, shell=True)
		except:
			log.warning("Command failed, continuing anyway")

	# Glad it's done
	log.info("Everything's fine, exiting.")


def load_config():
	with open(CONFIG_PATH) as f:
		s = f.read()
		config = json.loads(s)
		log.debug("Loaded config from %s", CONFIG_PATH)
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
