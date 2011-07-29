
# Frameworks
import os
import ConfigParser
from os.path import basename, dirname, join
import fnmatch
from PIL import Image
import plistlib

# Project
from sprite import Sprite
from algorithms.algorithm import ALGORITHMS

# Import all algorithm files here, so that they are registered
import algorithms.naive
import algorithms.simple

ERROR = 0
MESSAGE = 1

VERSION = (0, 1, 0)
RELEASE = False # This will add a 'git' to the version name, indicated it's not an actual release

def plist_encode(value):
    if isinstance(value, tuple) or isinstance(value, tuple):
        # Notice, a double {{ escapes it, so this is essentially "{%s}" using old syntax
        return "{{{0}}}".format(",".join(["{0}".format(plist_encode(x)) for x in value]))
    elif isinstance(value, bool):
        return ['YES', 'NO'][int(value)]
    else:
        return str(value)

class Packer(object):
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config_directory = dirname(config_file_path)
        self.settings = {}
        self.error = None 
        pass    

    @classmethod
    def version_str(cls):
        '''This is the version for the whole sprite-packer. Possibly awkward place.'''
        global VERSION
        global RELEASE  
        rel_str = ""
        if not RELEASE:
            rel_str = "git"
        return ".".join(["{0:d}".format(x) for x in VERSION]) + rel_str

    def load_settings(self, config_file_path = None):
        """Loads the config file"""
        if config_file_path is not None:
            self.config_file_path = config_file_path

        parser = ConfigParser.ConfigParser()
        try:
            parser.read(self.config_file_path)
        except IOError:
            self.error = "Could not open config file {0}".format(self.config_file_path)
            return False

        cat = "settings"

        items = []  

        try:
            items = dict(parser.items(cat))
        except ConfigParser.NoSectionError, e:
            self.error = str(e) 
            return False
        except ValueError, e:
            self.error = str(e)
            return False

        required = ['input', 'output-sprite', 'output-plist', 'width', 'height', 'padding', 'algorithm']

        for r in required:
            if r not in items:
                self.error = "Option '{0}' required".format(r)
                return False

        self.settings['input_path'] = items["input"]
        self.settings['output_path'] = items["output-sprite"]
        self.settings['plist_path'] = items["output-plist"]
        width = int(items["width"])
        height = int(items["height"])   
        if width <= 0 or height <= 0:
            self.error = "Invalid size ({0}, {1})".format(width, height)
        else:
            self.settings['size'] = (width, height) 

        padding = int(items["padding"])
        if padding < 0:
            self.error = "Invalid padding {0}".format(padding)
        else:
            self.settings['padding'] = padding

        self.settings['algorithm'] = items["algorithm"]
        if self.settings['algorithm'] not in ALGORITHMS:
            self.error = "Could not find algorithm '{0}'".format(self.settings['algorithm'])
            return

        if 'scale' in items:
            self.settings['scale'] = float(items['scale'])
        else:
            self.settings['scale'] = 1.0

        if 'source-pixels-to-points' in items:
            self.settings['source-pixels-to-points'] = float(items['source-pixels-to-points'])
        else:
            self.settings['source-pixels-to-points'] = 1.0

        return True

    def create_cfg(self, file_path):
        '''Creates an example config file'''
        config = ConfigParser.RawConfigParser()
        cat = 'settings'
        config.add_section(cat)
        config.set(cat, 'input', 'sprites/*.png')
        config.set(cat, 'output-sprite', 'sprite.png')
        config.set(cat, 'output-plist', 'sprite.plist')
        config.set(cat, 'width', '1024')
        config.set(cat, 'height', '1024')
        config.set(cat, 'aglorithm', 'simple')  

        with open(file_path, 'wb') as configfile:
            config.write(configfile)

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
            dire = os.path.join(self.config_directory, directory)
            for f in os.listdir(dire):
                if fnmatch.fnmatch(f, pattern):
                    files.append(os.path.join(dire, f)) 
        except OSError, e:
            self.error = "No such directory '{0}'".format(directory)    

        return files

    def load_sprite(self, file_path):
        """Calls Sprite() and checks all that it can throw"""
        try:
            sprite = Sprite(file_path)              
            sprite.scale = self.settings['scale']
            sprite.source_pixels_to_points = self.settings['source-pixels-to-points']
        except IOError:
            self.error = "Could not open file '{0}'".format(file_path)
            return None 
        else:
            return sprite

    def save_sprite(self, sprites):
        im = Image.new("RGBA", self.settings['size'])
            
        for sprite in sprites:
            if sprite.position[0] != -1:
                spr = sprite.image

                if sprite.rotated:
                    spr = spr.rotate(-90)
                if sprite.scale != 1.0:
                    spr = spr.resize(sprite.size, Image.ANTIALIAS)  

                im.paste(spr, sprite.position)
        
        im.save(os.path.join(self.config_directory, self.settings['output_path']))

        return True

    def save_plist(self, sprites, file_path):
        '''Saves a plist file that can be used by cocos2d'''
        
        texformat = 2
        frames = {}
        for sprite in sprites:
            if texformat == 0:
                # Format 0
                # (rotation not supported)
                frames[sprite.name] = {
                    'width': sprite.point_size[0],
                    'height': sprite.point_size[1],
                    'offsetX': 0,
                    'offsetY': 0,   
                    'originalWidth': sprite.size[0],
                    'originalHeight': sprite.size[1],
                    'x': sprite.position[0],
                    'y': sprite.position[1],
                }
            elif 1 <= texformat <= 2:
                # Format 2
                frames[sprite.name] = {
                    'frame': plist_encode( (sprite.position, sprite.unrotated_size) ),
                    'offset': plist_encode( (0, 0) ),
                    'sourceColorRect': plist_encode( ((0, 0), sprite.unrotated_size) ),
                    'sourceSize': plist_encode(sprite.unrotated_size),
                }
                if texformat == 2:
                    frames[sprite.name]['rotated'] = sprite.rotated
            elif texformat == 3:
                # Format 3
                frames[sprite.name] = {
                    'spriteSize': plist_encode(sprite.unrotated_size),
                    'spriteOffset': plist_encode(sprite.position),
                    'spriteSourceSize': plist_encode(sprite.unrotated_size),
                    'textureRect': plist_encode((sprite.position, sprite.unrotated_size)),
                    'textureRotated': sprite.rotated,
                }


        metadata = {}
        metadata['format'] = texformat
        #metadata['realTextureFileName'] = basename(file_path)
        metadata['size'] = plist_encode(self.settings['size'])
        metadata['textureFileName'] = basename(basename(self.settings['output_path']))

        texture = {'height': self.settings['size'][0], 'width': self.settings['size'][1]}
        

        pl = {'frames': frames, 'metadata': metadata, 'texture': texture}
            
        try:
            plistlib.writePlist(pl, os.path.join(self.config_directory, file_path))
        except TypeError, e:
            self.error = e
            return False

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

        if not self.save_sprite(sprites):
            yield ERROR, "SAVE ERROR: {0}".format(self.error_msg())
            return

        yield MESSAGE, "Saving plist file '{0}'".format(self.settings['plist_path'])

        if not self.save_plist(sprites, self.settings['plist_path']):
            yield ERROR, "PLIST ERROR: {0}".format(self.error_msg())
            return 

        yield MESSAGE, "Done."
        

if __name__ == '__main__':
    from shell import main
    main(sys.argv[1:])
