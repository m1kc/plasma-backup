#!/usr/bin/env python3
from decider import Decider
from entry_manager import EntryManagerFilesystem

def main():
	print("Plasma 1.0")
	print("- written by m1kc")
	print("- https://github.com/m1kc/plasma")
	print("- licensed under GNU GPL v3")
	print("")
	print("THIS SOFTWARE IS STILL EXPERIMENTAL.")
	print("USE AT YOUR OWN RISK.")
	print("")

	config = {
		'policy': {
			'daily': 5,
			'weekly': 3,
			'monthly': 2,
		},
		'path': '/home/m1kc/work/Still-experimental/plasma-rotate/tdtdtdtdtd',
	}
	em = EntryManagerFilesystem(config['path'])
	d = Decider(em, config['policy'])

	print("Scanning", config['path'], '...')
	print("Entries exist:", len(em.list()))
	d.execute()

	print("Everything's fine, exiting.")


if __name__ == '__main__':
	main()
