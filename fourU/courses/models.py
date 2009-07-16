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
from users.models import CustomUser, PERMISSION_LEVEL_CHOICES

class Course(models.Model):
	"""
	``name``
	"""
	name = models.CharField(max_length=255,)
	slug = models.SlugField(unique=True,)

class Section(models.Model):
	"""
	``number``: e.g. 01 if section is CSC 101-01
	
	``course``: the ``Course`` that this section is associated with
	"""
	number = models.IntegerField()
	course = models.ForeignKey('Course')

class SectionEnrollment(models.Model):
	"""
	``user``: the ``CustomUser`` enrolled in this section
	
	``permissionLevel``: a string indicating the level of permissions this user has for this section;
	should be one of ``PERMISSION_LEVEL_CHOICES``
	
	``section``: the section this user is enrolled in
	"""
	user = models.ForeignKey(CustomUser)
	permissionLevel = models.CharField(max_length=30, choices=PERMISSION_LEVEL_CHOICES)
	section = models.ForeignKey(Section)
