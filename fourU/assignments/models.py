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

class Problem(models.Model):
	file = models.FilePathField(path=settings.PROBLEM_DIRECTORY, recursive=True, match=".*\.py")
	total = models.FloatField(null=True)

class ProblemGrade(models.Model):
	score = models.FloatField()
	answer = models.TextField(null=True)
	problem = models.ForeignKey('Problem')

class Assignment(models.Model):
	startDate = models.DateTimeField()
	endDate = models.DateTimeField()
	total = models.FloatField(null=True)
	problems = models.ManyToManyField('Problem')

class AssignmentGrade(models.Model):
	score = models.FloatField(null=True)
	isTaken = models.BooleanField()
	assignment = models.ForeignKey('Assignment')
