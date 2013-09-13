#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- mode: python -*-
# vi: set ft=python :

import os
from setuptools import setup, find_packages

DESCRIPTION = 'Easy image thumbnails in Django.'

setup(
    name='django-thumbs',
    version='0.9',
    install_requires=['django'],
    description=DESCRIPTION,
    author='Antonio Melé',
    author_email='antonio.mele@django.es',
    url='https://github.com/zenx/django-thumbs/',
    packages=['django_thumbs'],
)
