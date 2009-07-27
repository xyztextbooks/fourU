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

# imports common to all problems
from __future__ import division
from sympy import *
from django.conf import settings
from django.template.loader import render_to_string
from django import forms
from problems.models import AnswerForm, integer
import problems.models

import random

class Problem(problems.models.Problem):
	requestDict = None
	def __init__(self):
		self.a = random.randint(1, 10)
		self.b = random.randint(1, 10)
		self.sum = self.a + self.b
		
		self.f = "%s + %s = %s" % (self.a, self.b, self.sum)
	
	def __str__(self, standAlone=False):
		"""
		Generate the appropriate forms and return a rendered html template.
		"""
		answerForm = AnswerForm(self.requestDict,
		                        action = forms.CharField(required=False),
		                        arg1 = forms.IntegerField(required=False),
		                        arg2 = forms.IntegerField(required=False),
		                        comparison = forms.CharField(required=False),
		                        answer = forms.IntegerField(required=False))
		return render_to_string('example_library/problem1.html', {'MEDIA_PATH_PREFIX': settings.MEDIA_PATH_PREFIX,
		                                                     'problem': printing.latex(self.f),
		                                                     'answerForm': answerForm,
		                                                     'standAlone': standAlone,})
	
	def is_correct(self, answer):
		try:
			return (answer['action'] == 'sum' and
			        integer(answer['arg1']) == self.a and
			        integer(answer['arg2']) == self.b and
			        answer['comparison'] == 'equal' and
			        integer(answer['answer']) == self.sum)
		except KeyError:
			return False

# are we running this standalone, rather than as a module?
def main():
	print Problem().__str__(standAlone=True)
	return

if __name__ == '__main__' or __name__ == '__console__':
	import sys
	sys.exit(main())
