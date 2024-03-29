#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 15:08:46 2019

@author: janne
"""

from setuptools import setup

setup(name='mesa_reader',
    version='0.3.0',
    description='tools for interacting with output from MESA star',
    url='http://github.com/wmwolf/py_mesa_reader',
    author='William M. Wolf',
    author_email='wolfey6@gmail.com',
    license='MIT',
    packages=['mesa_reader'],
    install_requires=['numpy'])