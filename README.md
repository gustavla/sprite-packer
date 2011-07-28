# sprite-packer

Texture Packer for in Python, for use with cocos2d.

## Features

Not much yet, so far:

 * Sprite packing with a choice of two extremely basic algorithms
 * Generates plist for cocos2d
 * Algorithms can choose to rotate sprite (one algorithm does this already)

## Installation

    [sudo] python setup.py install

## Usage

The sprite is definied in a config file. To get started, create an empty config file:

    sprite-packer -n test.cfg

Now, edit this, save it and run

    sprite-packer test.cfg

Your sprite and plist will be generated.

## Requirements

 * Python 2 (2.5 or newer)
 * [PIL](http://www.pythonware.com/products/pil/)

## Copyright

Copyright (c)
