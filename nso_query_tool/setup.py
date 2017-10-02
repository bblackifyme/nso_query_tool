#!/usr/bin/env python

from distutils.core import setup

setup(name='nso_query_tool',
      version='1.0',
      description='Python Library to enable SQL like queries against the NSO cDB',
      author='Brandon Black',
      author_email='branblac@cisco.com',
      url='https://wwwin-gitlab-sjc.cisco.com/branblac/nso_query_tool',
      packages=['requests', 'json', 'unittest'],
     )
