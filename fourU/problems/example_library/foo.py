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

from django.http import HttpResponse
from django.shortcuts import render_to_response
from problems.models import Problem, AnswerForm
from django import forms

import random

def index(request):
	"""
	:Subject: Intermediate Algebra
	:Chapter: Ch 01: Algebra, Mathematical Models and Problem Solving
	:Section: Solving Linear Equations
	:Keywords: - linear equations
	           - solving equations
	:Text Title: MAP Intermedia Algebra
	:Text Edition: 1
	:Text Author: Yoshiwara
	:Text Section: Lesson 1
	:Problem: 1
	:Author: Yoshiwara
	:Institution: Los Angeles Pierce College
	:Date: 2009
	"""
	def check(a, b):
		"""
		Return True if `b` is a correct answer, as compared to `a`
		"""
		# TODO: this needs to be a better example, preferrably something you'd actually use
		return cmp(a, b) == 0
	
	if request.method == 'GET':
		# FIXME: Hacky!  This whole thing needs to be restructured
		global b, r, a, c, ans, d, answer_form, problem1
		
		b = random.randint(2, 5)
		r = random.randint(1, 9)
		a = b + r
		c = random.randint(1, 9)
		ans = random.randint(1, 9)
		d = (r + c) * ans
		
		answer_form = AnswerForm(answer=forms.CharField())
		
		problem1 = Problem(a=a, b=b, c=c, d=d, r=r, answer=ans)
		return render_to_response('example_library/foo.html', {'problem1': problem1, 'answer_form': answer_form})
	else:
		answer_form = AnswerForm(request.POST, answer=forms.CharField())
		studentAnswer = request.POST['answer']
		
		if problem1.check_answer(studentAnswer, check):
			pass
		else:
			return render_to_response('example_library/foo.html', {'problem1': problem1, 'answer_form': answer_form})
