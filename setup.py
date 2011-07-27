#!/usr/bin/env python

from distutils.core import setup

setup(name='sprite-packer',
    version='0.1.0git',
    author="Gustav Larsson",
    author_email="gustav.m.larsson@gmail.com",
    url="http://github.com/gustavla/sprite-packer",
    description="Texture Packer for use with cocos2d",
	install_requires=['PIL'],
#    long_description="Tool for evaluating and analysing eye movement classification algorithms."
    packages=['packer'],
	scripts=['scripts/sprite-packer'],
)
