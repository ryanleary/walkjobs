#!/usr/bin/env python

from distutils.core import setup

setup(name='walkjobs',
      version='0.1',
      description='Python job scheduler',
      author='Ryan Leary',
      author_email='ryan@bbn.com',
      packages=['walkjobs', 'walkjobs.graph', 'walkjobs.scheduler', 'walkjobs.job', 'walkjobs.execution'],
      install_requires=['networkx'],
      extras_require = {'grid_engine': ["drmaa"]})