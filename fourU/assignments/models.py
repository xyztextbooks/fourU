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

from django.db import models
from django.conf import settings
from courses.models import SectionEnrollment, Section

class Problem(models.Model):
	"""
	A database representation of one problem, intended to match 1-to-1 with an xxx.py problem file from a library.
	
	``file``: contains the relative path to a problem file from ``settings.PROBLEM_DIRECTORY``;
	can only be of the form \*.py
	
	``total``: the maximum number of points that can be earned for this problem
	"""
	file = models.FilePathField(path=settings.PROBLEM_DIRECTORY, recursive=True, match=".*[^(__){1}]\.py$")
	total = models.FloatField(null=True)
	number = models.PositiveSmallIntegerField()


class ProblemGrade(models.Model):
	"""
	One student's grade on a problem.
	
	``score``: decimal number of points received for this problem
	
	``answer``: textual representation of the student's answer.
	
	``problem``: the ``Problem`` this grade is to
	"""
	score = models.FloatField()
	answer = models.TextField(null=True)
	problem = models.ForeignKey('Problem')

class Assignment(models.Model):
	"""
	An assignment of multiple problems to multiple students
	
	``startDate``: when students are allowed to begin the assignment
	
	``endDate``: the closing date
	
	``total``: the maximum number of points that can be earned for this assignment;
	by default, the summation of the total points for each problem
	
	``problems``: the ``Problem``\s assigned
	
	``section``: the ``Section`` to which this is assigned
	"""
	name = models.CharField(max_length=255, primary_key=True)
	slug = models.SlugField()
	startDate = models.DateTimeField()
	endDate = models.DateTimeField()
	total = models.FloatField(null=True)
	problems = models.ManyToManyField(Problem)
	section = models.ForeignKey(Section)

class AssignmentGrade(models.Model):
	"""
	One student's grade on an assignment.
	
	``score``: decimal number of points received on this assignment
	
	``isTaken``
	
	``assignment``: the ``Assignment`` this grade is to
	
	``section``: a ``SectionEnrollment``
	"""
	score = models.FloatField(null=True)
	isTaken = models.BooleanField()
	assignment = models.ForeignKey(Assignment)
	section = models.ForeignKey(SectionEnrollment)
