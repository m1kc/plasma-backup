#!/usr/bin/env python3

from decider import Decider
from entry_manager import EntryManagerFilesystem

import json
import sys
import os.path


FILENAME = 'plasma-rotate.json'

TEST_PATH = '/home/m1kc/work/Still-experimental/plasma/tdtdtdtdtd'

def main():
	print("Plasma 1.0")
	print("- written by m1kc")
	print("- https://github.com/m1kc/plasma")
	print("- licensed under GNU GPL v3")
	print("")
	print("THIS SOFTWARE IS STILL EXPERIMENTAL.")
	print("USE AT YOUR OWN RISK.")
	print("")

	path = sys.argv[1]

	print("Rotating entries in:", path)

	config = load_json(os.path.join(path, FILENAME))
	em = EntryManagerFilesystem(path)
	d = Decider(em, config['policy'])

	print("Entries exist:", len(em.list()))
	d.execute()

	print("Everything's fine, exiting.")


def load_json(filename):
	with open(filename) as f:
		s = f.read()
		config = json.loads(s)
		print("Loaded config from", filename)
		return config


if __name__ == '__main__':
	main()
