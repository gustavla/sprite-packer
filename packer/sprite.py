
from PIL import Image
from os.path import basename

class Sprite(object):
	'''A reference of a sprite, with all the information needed for the packing algorithm,
	i.e. without any actual image data, just the size.'''

	def __init__(self, file_path):
		self.file_path = file_path
		self.image = Image.open(file_path)
		self.name = basename(file_path)	
		self.size = self.image.size
		self.position = (-1, -1) # The algorithms should set this value
		self.rotated = False

	@property
	def width(self):
		if self.rotated:
			return self.size[1]
		else:
			return self.size[0]

	@property
	def height(self):
		if self.rotated:
			return self.size[0]
		else:
			return self.size[1]
