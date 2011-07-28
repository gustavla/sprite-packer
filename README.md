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

## Xcode integration

 * In Xcode 4, click your project target and select the 'Build Phases'.
 * Click 'Add Build Phase'.
 * Move this up above 'Compile Sources' and below 'Target Dependencies'.
 * You can let the shell be '/bin/sh'.
 * Enter the following:

    exec sprite-packer path/to/config.cfg

I had some problems with this though, because it seems that Xcode loads its PATH from a different place. You could either fix this somehow or be lazy like me and just use absolutes to find the right stuff (I also had to add 'exec /path/to/python' to get it to run my macports python). 

The config path is relative to your projects top-most folder (the one that houses the .xcodeproj folder). To double check where this is, add this to the shell script: 

    echo $PWD
