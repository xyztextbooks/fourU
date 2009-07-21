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
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField

PERMISSION_LEVEL_CHOICES = (
	('Admin', 'Admin'),
	('Professor', 'Professor'),
	("Teacher's Assistant", 'TeacherAssistant'),
	('Student', 'Student'),
	('Guest', 'Guest'),
)
#PERMISSION_LEVEL_SORT_ORDER = {
#	'Admin': 0,
#	'Professor': 1,
#	'TeacherAssistant': 2,
#	'Student': 3,
#	'Guest': 4,
#}
# same as above, but more flexible
PERMISSION_LEVEL_SORT_ORDER = dict([(level[1], index) for index, level in enumerate(PERMISSION_LEVEL_CHOICES)])

def compare_permissions(one, another):
	return PERMISSION_LEVEL_SORT_ORDER[another] - PERMISSION_LEVEL_SORT_ORDER[one]

class Address(models.Model):
	"""
	A standard street address.
	
	``name``: to whom any mailings should be addressed
	
	``line1`` and ``line2``: street address lines
	
	``city``
	
	``state``
	
	``zipcode``
	"""
	name = models.CharField(max_length=80)
	line1 = models.CharField(max_length=80,blank=True)
	line2 = models.CharField(max_length=80,blank=True)
	city = models.CharField(max_length=50)
	# FIXME: US-specific
	state = USStateField()
	zipcode = models.CharField(max_length=10,blank=True)

class UserProfile(models.Model):
	"""
	Extra information about a user.
	
	``permamentAddress`` and ``temporaryAddress``: ``Address``s
	"""
	user = models.ForeignKey(User, unique=True)
	
	permanentAddress = models.ForeignKey('Address', related_name="user_permanent_address", null=True)
	temporaryAddress = models.ForeignKey('Address', related_name="user_temporary_address", null=True)

