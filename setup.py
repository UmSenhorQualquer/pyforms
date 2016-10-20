#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

version = ''
with open('pyforms/__init__.py', 'r') as fd: version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                                                                      fd.read(), re.MULTILINE).group(1)
if not version: raise RuntimeError('Cannot find version information')

requirements = [
	"pyopengl >= 3.1.0",
	"visvis >= 1.9.1",
	"numpy >= 1.6.1",
	"matplotlib",
	"pysettings >= 0.1"
]

setup(

	name='PyForms',
	version=version,
	description="""Pyforms is a Python 2.7 and 3.0 framework to develop GUI application,
		which promotes modular software design and code reusability with minimal effort.""",
	author='Ricardo Ribeiro',
	author_email='ricardojvr@gmail.com',
	license='MIT',

	download_urlname='https://github.com/UmSenhorQualquer/pyforms',
	url='https://github.com/UmSenhorQualquer/pyforms',

	packages=[
		'pyforms',
		'pyforms.utils',
		'pyforms.terminal',
		'pyforms.terminal.Controls',
		'pyforms.gui',
		'pyforms.gui.dialogs',
		'pyforms.gui.Controls',
		'pyforms.gui.Controls.ControlEventTimeline',
		'pyforms.gui.Controls.ControlEventsGraph',
		'pyforms.gui.Controls.ControlPlayer'],
	package_data={'pyforms': [
		'gui/Controls/uipics/*.png',
		'gui/mainWindow.ui', 'gui/Controls/*.ui', 'gui/Controls/ControlPlayer/*.ui',
		'gui/Controls/ControlEventTimeline/*.ui']
	},

	# install_requires=[requirements],
)
