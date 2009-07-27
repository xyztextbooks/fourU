# -*- coding: utf-8 -*-

################################################################################
# Copyright (C) 2009 XYZ Textbooks                                             #
#                                                                              #
# This file is part of fourU.                                                  #
#                                                                              #
# This program is free software; you can redistribute it and/or modify it under#
# the terms of either: (a) the GNU General Public License as published by the  #
# Free Software Foundation; either version 3, or (at your option) any later    #
# version, or (b) the MIT License which comes with this package.               #
#                                                                              #
# fourU is distributed in the hope that it will be useful,                     #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See either the         #
# GNU General Public License or the MIT License for more details.              #
################################################################################

import os
from django.core.management.base import LabelCommand
from optparse import make_option
from django.conf import settings
	
problemBlock = '''\
# -*- coding: utf-8 -*-

# imports common to all problems
from __future__ import division
from sympy import *
from django.conf import settings
from django.template.loader import render_to_string
from django import forms
from problems.models import AnswerForm, integer
import problems.models

class Problem(problems.models.Problem):
	"""
	:Subject: 
	:Chapter: 
	:Section: 
	:Keywords: 
	:Text Title: 
	:Text Edition: 
	:Text Author: 
	:Text Section: 
	:Problem: 
	:Author: 
	:Institution: 
	:Date: 
	"""
	requestDict = None
	def __init__(self):
		pass
	
	def __str__(self, standAlone=False):
		"""
		Generate the appropriate forms and return a rendered html template.
		"""
		answerForm = AnswerForm(self.requestDict, answer=forms.IntegerField(required=False))
		return render_to_string('%s', {'MEDIA_PATH_PREFIX': settings.MEDIA_PATH_PREFIX,
		                                                     'problem': printing.latex(self.f),
		                                                     'answerForm': answerForm,
		                                                     'standAlone': standAlone,})
	
	def is_correct(self, answer):
		pass

# are we running this standalone, rather than as a module?
def main():
	print Problem().__str__(standAlone=True)
	return

if __name__ == '__main__' or __name__ == '__console__':
	import sys
	sys.exit(main())

'''

class Command(LabelCommand):
	help = "Creates a template problem file.  Makes directories as needed."
	
	def handle_label(self, problem, **options):
		filepath = os.path.join(settings.PROBLEM_DIRECTORY, problem + ".py")
		try:
			file = open(filepath, "w")
		except IOError:
			library = os.path.split(filepath)[0]
			os.makedirs(library)
			file = open(filepath, "w")
		file.write(problemBlock % (problem + ".html"))
		file.close()
