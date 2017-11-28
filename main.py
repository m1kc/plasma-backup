#!/usr/bin/env python3
from decider import Decider

def main():
	policy = None # {}
	em = None #em = FilesystemEntryManager()
	d = Decider(em, policy)
	d.execute()
	print("OK, exiting.")


if __name__ == '__main__':
	main()
