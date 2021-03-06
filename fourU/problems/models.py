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

from django import forms
from sympy import *

def integer(object):
	try:
		return int(object)
	except:
		return None

class Problem(object):
	"""
	A generic wrapper of things useful in displaying and grading a math problem.
	Intended to be subclassed.
	"""
	def __init__(self, **kwargs):
		# add any given keywords arguments as instance variables
		for arg in kwargs:
			vars(self)[arg] = kwargs[arg]
	
	def is_correct(self, answer, function, solveFor):
		return integer(answer) in solve(function, solveFor)

class AnswerForm(forms.Form):
	"""
	A form with a variable number of fields.
	"""
	def __init__(self, queryDict, **kwargs):
		"""
		Create the form, with any number of named keyword arguments as fields.
		For instance, to create a character field referenced by the name `answer`,
		pass in `answer=forms.CharField()`
		"""
		# we have to make sure to call Form's __init__(), since it sets some variables we override
		#super(AnswerForm, self).__init__(queryDict)
		forms.Form.__init__(self, queryDict, prefix="answer")
		
		# add any given keyword arguments as instance variables
		# because the form fields aren't _really_ instance variables,
		# we can't declare them like we do in Problem.__init__()
		# self.fields is a magically-generated dictionary in forms.BaseForm
		for arg in kwargs:
			self.fields[arg] = kwargs[arg]
