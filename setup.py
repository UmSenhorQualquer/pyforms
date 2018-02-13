#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

version = ''
with open('pyforms/__init__.py', 'r') as fd: version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
																 fd.read(), re.MULTILINE).group(1)

if not version: raise RuntimeError('Cannot find version information')

setup(
	name='PyForms',
	version=version,
	description="""Pyforms is a Python 2.7 and 3.4 framework to develop GUI applications based on pyqt""",
	author='Ricardo Ribeiro',
	author_email='ricardojvr@gmail.com',
	license='MIT',
	url='https://github.com/UmSenhorQualquer/pyforms',
	install_requires=[
		'anyqt',
		'pyqt5',
		'pyopengl',
		'QScintilla',
		'visvis',
		'matplotlib',
		'python-dateutil',
		'numpy'
	],
	packages=find_packages(),
	package_data={'pyforms': [
		'gui/controls/uipics/*.png',
		'gui/mainWindow.ui', 'gui/controls/*.ui', 'gui/controls/control_player/*.ui',
		'gui/controls/control_event_timeline/*.ui']
	},
)
