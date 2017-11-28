#!/usr/bin/env python3
from decider import Decider

def main():
	config = {
		'strategy': 'btrfs-snapshot',
		'policy': {
			'daily': 5,
			'weekly': 3,
			'monthly': 2,
		},
	}
	em = None #em = FilesystemEntryManager()
	d = Decider(em, config['policy'])
	d.execute()
	print("OK, exiting.")


if __name__ == '__main__':
	main()
