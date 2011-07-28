
# Framework
import sys
from optparse import OptionParser

# Project 
from packer import Packer, ERROR, MESSAGE

def main():
	examples = []
	examples.append(("-n test.cfg", "creates empty config file"))
	examples.append(("-v sprite.cfg", "runs sprite.cfg with messages"))

	ex_str = "\n".join(["  %prog {0:<18}{1}".format(tup[0], tup[1]) for tup in examples])

	usage = "Usage: %prog [options] <config file> [<config file> ...]\n\nExamples:\n{0}".format(ex_str)
	parser = OptionParser(usage=usage, version="%prog {0}".format(Packer.version_str()))
	parser.add_option("-v", "--verbose", action="store_true", help="print messages to stdout", dest="verbose")
	parser.add_option("-n", "--new-config", action="store_true", help="creates an empty config file; recommended way of creating a new sprite.", dest="newcfg")
	#parser.add_option("--hd", action="store_true", help="works only with -n, creates an empty config file perfect for generating ", dest="create-cfg")

	(options, args) = parser.parse_args()

	if args:
		for arg in args:	
			packer = Packer(arg)

			if options.newcfg:
				packer.create_cfg(arg)
			else:
				for etype_and_msg in packer.run_with_messages():
					etype, msg = etype_and_msg
					if etype == ERROR:
						sys.stderr.write(msg + "\n")
					elif etype == MESSAGE and options.verbose:
						print msg	

				if packer.error_msg():
					sys.exit(1)
