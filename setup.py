#!/usr/bin/env python

from distutils.core import setup

from packer.packer import Packer

version = Packer.version_str()

setup(name='sprite-packer',
    version=version,
    author="Gustav Larsson",
    author_email="gustav.m.larsson@gmail.com",
    url="http://github.com/gustavla/sprite-packer",
    description="Texture Packer for use with cocos2d",
	install_requires=['PIL'],
#    long_description="Tool for evaluating and analysing eye movement classification algorithms."
    packages=['packer'],
	scripts=['scripts/sprite-packer'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
	],
)
