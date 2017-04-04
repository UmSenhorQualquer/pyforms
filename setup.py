#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
#import re

#version = ''
#with open('pyforms/__init__.py', 'r') as fd: version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
#                                                                      fd.read(), re.MULTILINE).group(1)
#if not version: raise RuntimeError('Cannot find version information')

setup(

	name='PyForms',
	version='2.0.0.beta',
	description="""Pyforms is a Python 2.7 and 3.4 framework to develop GUI application,
		which promotes modular software design and code reusability with minimal effort.""",
	author='Ricardo Ribeiro',
	author_email='ricardojvr@gmail.com',
	license='MIT',
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
)
