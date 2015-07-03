#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import os
import subprocess



class BioradWriter:

	"""
		Encapsulation of ImageJ's (http://rsb.info.nih.gov/ij/) 'Biorad Writer' plugin to enable
		the transformation of TIFF images into PIC format directly from the command line.
	"""

	# Configuration parameters
	# NB: Keep the trailing slashes
	imageJDir = '/home/admin/imagej/'
	javaDir = imageJDir + 'jdk/bin/'
	bioradWriterConfigFile = 'biorad_writer_config.txt'

	@staticmethod
	def __update_config_file(outputFileName):
		try:
			with open(BioradWriter.imageJDir + BioradWriter.bioradWriterConfigFile, 'w') as f:
				f.write(os.getcwd() + "/output/\n");
				f.write(outputFileName);		
	    	except (IOError) as e:
	    		raise e

	@staticmethod
	def convert(inputFileName, outputFileName='', 
		imageJDir='/home/admin/imagej/', 
		javaDir='/home/admin/imagej/jdk/bin/', 
		bioradWriterConfigFile='biorad_writer_config.txt' ):
		
		if not outputFileName:
			outputFileName = os.path.splitext(inputFileName)[0] + '.PIC'

		BioradWriter.__update_config_file(outputFileName)
		execStr = 'cd ' + BioradWriter.imageJDir + ";"
		execStr += BioradWriter.javaDir + 'java -cp ' + BioradWriter.imageJDir + 'ij.jar ij.ImageJ -batch ' + BioradWriter.imageJDir + 'macro.ijm ' + inputFileName + ';'
		execStr += 'cd -'
		subprocess.call(execStr, shell=True)
