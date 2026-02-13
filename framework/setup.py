#!/usr/bin/env python

# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

from shieldnetdefend import __version__

from setuptools import setup, find_namespace_packages

setup(name='shieldnetdefend',
      version=__version__,
      description='ShieldnetDefend control with Python',
      url='https://github.com/shieldnetdefend',
      author='ShieldnetDefend',
      author_email='hello@shieldnetdefend.com',
      license='GPLv2',
      packages=find_namespace_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_data={'shieldnetdefend': ['core/shieldnetdefend.json',
                              'core/cluster/cluster.json', 'rbac/default/*.yaml']},
      include_package_data=True,
      install_requires=[],
      zip_safe=False,
      )
