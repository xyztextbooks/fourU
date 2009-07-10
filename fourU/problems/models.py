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

class Problem(object):
	def __init__(self, **kwargs):
		# add any given keywords arguments as instance variables
		for arg in kwargs:
			vars(self)[arg] = kwargs[arg]
	
	def is_correct(self, answer, compare=None, decrementGrade=True):
		# TODO: decrement number of tries and/or increment number of attempts
		if decrementGrade:
			self.attempts += 1
		
		if compare:
			return compare(self.answer, answer)
		else:
			return self.answer == answer

class AnswerForm(forms.Form):
	def __init__(self, queryDict, **kwargs):
		# we have to make sure to call Form's __init__(), since it sets some variables we override
		#super(AnswerForm, self).__init__(queryDict)
		forms.Form.__init__(self, queryDict)
		
		# add any given keyword arguments as instance variables
		# because the form fields aren't _really_ instance variables,
		# we can't declare them like we do in Problem.__init__()
		# self.fields is a magically-generated dictionary in forms.BaseForm
		for arg in kwargs:
			self.fields[arg] = kwargs[arg]
