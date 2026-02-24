#!/usr/bin/env python

# Copyright (C) 2015, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import re

def _get_version():
    with open('wazuh/__init__.py', 'r') as f:
        match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE)
        return match.group(1) if match else '0.0.0'

from setuptools import setup, find_namespace_packages

setup(name='wazuh',
      version=_get_version(),
      description='Wazuh control with Python',
      url='https://github.com/wazuh',
      author='Wazuh',
      author_email='hello@wazuh.com',
      license='GPLv2',
      packages=find_namespace_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_data={'wazuh': ['core/wazuh.json',
                              'core/cluster/cluster.json', 'rbac/default/*.yaml']},
      include_package_data=True,
      install_requires=[],
      zip_safe=False,
      )
