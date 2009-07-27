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
from problems.models import AnswerForm
import problems.models

# problem-specific imports
import random

class Problem(problems.models.Problem):
	"""
	:Subject: Intermediate Algebra
	:Chapter: Ch 01: Algebra, Mathematical Models and Problem Solving
	:Section: Solving Linear Equations
	:Keywords: - linear equations
	           - solving equations
	:Text Title: MAP Intermediate Algebra
	:Text Edition: 1
	:Text Author: Yoshiwara
	:Text Section: Lesson 1
	:Problem: 1
	:Author: Yoshiwara
	:Institution: Los Angeles Pierce College
	:Date: 2009
	"""
	requestDict = None
	def __init__(self):
		var('y')
		
		# calculate some values
		b = random.randint(2, 5)
		r = random.randint(1, 9)
		a = b + r
		c = random.randint(1, 9)
		ans = random.randint(1, 9)
		d = (r + c) * ans
		
		self.f = Eq(a*y - b*y, d - c*y)
	
	def __str__(self, standAlone=False):
		"""
		Generate the appropriate forms and return a rendered html template.
		"""
		answerForm = AnswerForm(self.requestDict, answer=forms.IntegerField(required=False))
		return render_to_string('example_library/foo.html', {'MEDIA_PATH_PREFIX': settings.MEDIA_PATH_PREFIX,
		                                                     'problem': printing.latex(self.f),
		                                                     'answerForm': answerForm,
		                                                     'standAlone': standAlone,})
	
	def is_correct(self, answer):
		return super(Problem, self).is_correct(function=self.f, solveFor=y, answer=answer['answer'])

# are we running this standalone, rather than as a module?
def main():
	print Problem().__str__(standAlone=True)
	return

if __name__ == '__main__' or __name__ == '__console__':
	import sys
	sys.exit(main())
