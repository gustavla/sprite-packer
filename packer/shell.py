
# Framework
import sys

# Project 
from packer import Packer, ERROR, MESSAGE

def main(arguments):
	if len(arguments) == 1:
		config_path = arguments[0]
		packer = Packer(config_path)

		verbose = True

		for etype_and_msg in packer.run_with_messages():
			etype, msg = etype_and_msg
			if etype == ERROR:
				sys.stderr.write(msg + "\n")
			elif etype == MESSAGE and verbose:
				print msg	

