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
	def __init__(self):
		# calculate some values
		b = random.randint(2, 5)
		r = random.randint(1, 9)
		a = b + r
		c = random.randint(1, 9)
		ans = random.randint(1, 9)
		d = (r + c) * ans
		
		super(Problem, self).__init__(a=a, b=b, c=c, d=d, ans=ans)
	
	def __str__(self, queryDict=None):
		"""
		Generate the appropriate forms and return a rendered html template.
		"""
		answerForm = AnswerForm(queryDict, answer=forms.CharField(required=False))
		return render_to_string('example_library/foo.html', {'MEDIA_PATH_PREFIX': settings.MEDIA_PATH_PREFIX,
		                                                     'problem1': self,
		                                                     'answerForm': answerForm})
	
	def is_correct(self, answer):
		# longer, more explicit, way
		#def check(a, b):
		#	"""
		#	Return True if `b` is a correct answer, as compared to `a`
		#	"""
		#	# TODO: this needs to be a better example, preferably something you'd actually use
		#	return cmp(a, b) == 0
		
		# compare answer using check(), instead of default
		#return super(Problem, self).is_correct(answer, check)
		
		# shorter, but slightly more confusing, way
		return super(Problem, self).is_correct(answer, lambda a, b: cmp(a, b) == 0)

# are we running this standalone, rather than as a module?
def main():
	print Problem()
	return

if __name__ == '__main__' or __name__ == '__console__':
	import sys
	sys.exit(main())
