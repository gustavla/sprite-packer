
from PIL import Image
from os.path import basename

class Sprite(object):
    '''A reference of a sprite, with all the information needed for the packing algorithm,
    i.e. without any actual image data, just the size.'''

    def __init__(self, file_path):
        self.file_path = file_path
        self.image = Image.open(file_path)
        self.name = basename(file_path) 
        self.unrotated_source_size = self.image.size
        self.position = (-1, -1) # The algorithms should set this value
        self.rotated = False
        self.scale = 1.0
        self.source_pixels_to_points = 1.0

    @property
    def unrotated_size(self):
        s = (int(round(self.unrotated_source_size[0]*self.scale)), int(round(self.unrotated_source_size[1]*self.scale)))
        return s

    @property
    def source_size(self):
        s = self.unrotated_source_size
        if self.rotated:
            return tuple(s[::-1])
        else:
            return s

    @property 
    def point_size(self):
        def arr(x):
            return int(round(x*self.source_pixels_to_points/self.scale))
        s = map(arr, self.size)
        return tuple(s)

    @property
    def size(self):
        s = (int(round(self.source_size[0]*self.scale)), int(round(self.source_size[1]*self.scale)))
        return s

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
            return self.size[1]
