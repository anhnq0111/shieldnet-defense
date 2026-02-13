#!/usr/bin/env python

# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from setuptools import setup, find_namespace_packages

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

setup(
    name='api',
    version='4.13.1',
    description="ShieldnetDefend API",
    author_email="hello@shieldnetdefend.com",
    author="ShieldnetDefend",
    url="https://github.com/shieldnetdefend",
    keywords=["ShieldnetDefend API"],
    install_requires=[],
    packages=find_namespace_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    package_data={'': ['spec/spec.yaml']},
    include_package_data=True,
    zip_safe=False,
    license='GPLv2',
    long_description="""\
    The ShieldnetDefend API is an open source RESTful API that allows for interaction with the ShieldnetDefend manager from a web browser, command line tool like cURL or any script or program that can make web requests. The ShieldnetDefend app relies on this heavily and ShieldnetDefend’s goal is to accommodate complete remote management of the ShieldnetDefend infrastructure via the ShieldnetDefend app. Use the API to easily perform everyday actions like adding an agent, restarting the manager(s) or agent(s) or looking up syscheck details.
    """
)
