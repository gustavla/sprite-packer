
# Frameworks
import os
import ConfigParser
from os.path import basename, dirname, join
import fnmatch
from PIL import Image

# Project
from sprite import Sprite
from algorithm import ALGORITHMS

# Import all algorithm files here, so that they are registered
import naive
import simple

ERROR = 0
MESSAGE = 1

class Packer(object):
	def __init__(self, config_file_path):
		self.config_file_path = config_file_path
		self.settings = {}
		self.error = ""
		pass	


	def load_settings(self, config_file_path = None):
		"""Loads the config file"""
		if config_file_path is not None:
			self.config_file_path = config_file_path

		parser = ConfigParser.ConfigParser()
		try:
			config_file = open(self.config_file_path)	
		except IOError:
			self.error = "Could not open config file {0}".format(self.config_file_path)
			return False
		else:
			parser.readfp(config_file)



		cat = "sprite-packer"
		try:
			self.settings['input_path'] = parser.get(cat, "input")
			self.settings['output_path'] = parser.get(cat, "output")
			width = int(parser.get(cat, "width"))
			height = int(parser.get(cat, "height"))	
			if width <= 0 or height <= 0:
				self.error = "Invalid size ({0}, {1})".format(width, height)
			else:
				self.settings['size'] = (width, height)	

			padding = int(parser.get(cat, "padding"))
			if padding < 0:
				self.error = "Invalid padding {0}".format(padding)
			else:
				self.settings['padding'] = padding

			self.settings['algorithm'] = parser.get(cat, "algorithm")
			if self.settings['algorithm'] not in ALGORITHMS:
				self.error = "Could not find algorithm '{0}'".format(self.settings['algorithm'])
				return

		except ConfigParser.NoSectionError, e:
			self.error = e 
			return False
		except ConfigParser.NoOptionError, e:
			self.error = e 
			return False
		except Exception, e:
			self.error = e	
			return False

		return True

	def error_msg(self):
		return self.error

	def pack(self, sprites):
		"""This function create a packing, but it doesn't save the file"""

		# First check if any sprites are bigger than the output sprite, this will be an immediate no-go
		for sprite in sprites:
			if sprite.width > self.settings['size'][0] or sprite.height > self.settings['size'][1]:
				self.error = "Image ({0}) is bigger than output texture sprite".format(sprite.name) 
				return False

		# Instantiate algorithm
		algo = ALGORITHMS[self.settings['algorithm']]()

		if not algo.pack(self.settings, sprites):
			self.error = algo.error
			return False	
		else:		
			return True

	def matching_file_paths(self):
		"""Returns a list of files that matches the input patter"""	
		input_path = self.settings['input_path']
		directory = dirname(input_path)
		pattern = basename(input_path)

		files = []
		try:
			for f in os.listdir(directory):
				if fnmatch.fnmatch(f, pattern):
					files.append(join(directory, f)) 
		except OSError, e:
			self.error = "No such directory '{0}'".format(directory)	

		return files

	def load_sprite(self, file_path):
		"""Calls Sprite() and checks all that it can throw"""
		try:
			sprite = Sprite(file_path)				
		except IOError:
			self.error = "Could not open file '{0}'".format(file_path)
			return None	
		else:
			return sprite

	def save_files(self, sprites):
		im = Image.new("RGBA", self.settings['size'])
			
		for sprite in sprites:
			if sprite.position[0] != -1:
				if sprite.rotated:
					im.paste(sprite.image.rotate(90), sprite.position)
				else:
					im.paste(sprite.image, sprite.position)
		
		im.save(self.settings['output_path'])

		return True

	def run(self):
		# We just won't do anything with the messages
		self.run_with_messages()
	
	def run_with_messages(self):
		"""
		This does everything (load config, packs and saves sprite/plist files) and 
		yields strings with messages of progress
		"""

		yield MESSAGE, "Reading config '{0}'".format(self.config_file_path)

		if not self.load_settings():
			yield ERROR, "CONFIG ERROR: {0}".format(self.error_msg())	
			return

		yield MESSAGE, "Loading image files:"
		yield MESSAGE, dirname(self.settings['input_path'])

		file_paths = self.matching_file_paths()		
		if not file_paths:
			yield ERROR, "FILE ERROR: No sprites matched '{0}'".format(self.settings['input_path'])
			return
	
		sprites = []
		for file_path in file_paths:
			sprite = self.load_sprite(file_path)
			if sprite:
				yield MESSAGE, "  {0} ({1}x{2})".format(sprite.name, sprite.size[0], sprite.size[1])
				sprites.append(sprite)
			else:
				yield ERROR, "FILE ERROR: {0}".format(self.error_msg())
				return
						

		yield MESSAGE, "Using packing algorithm '{0}' to generate packing".format(self.settings['algorithm'])

		if not self.pack(sprites):
			yield ERROR, "ALGORITHM ERROR: {0}".format(self.error_msg())
			# Keep going so the user can take a look at the output sprite

		yield MESSAGE, "Saving sprite '{0}'".format(self.settings['output_path'])

		if not self.save_files(sprites):
			yield ERROR, "SAVE ERROR: {0}".format(self.error_msg())
			return

		yield MESSAGE, "Saving plist file '{0}'".format(self.settings['plist_path'])

		if not self.save_plist(sprites):
			yield ERROR, "PLIST ERROR: {0}".format(self.error_msg())
			return 

		yield MESSAGE, "Done."
		

if __name__ == '__main__':
	from shell import main
	main(sys.argv[1:])
