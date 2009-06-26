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
from django.contrib.auth.models import User, UserManager
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.db.models import signals

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

class CustomUser(User):
	"""
	A custom class that inherits from ``django.contrib.auth.models.User``.
	
	``permamentAddress`` and ``temporaryAddress``: ``Address``s
	"""
	# use UserManager to get the create_user method, etc.
	objects = UserManager()
	
	permanentAddress = models.ForeignKey('Address', related_name="user_permanent_address", null=True)
	temporaryAddress = models.ForeignKey('Address', related_name="user_temporary_address", null=True)

class CustomUserModelBackend(ModelBackend):
	"""
	A custom authentication backend to acomodate the ``CustomUser`` class.
	"""
	def authenticate(self, username=None, password=None):
		try:
			user = self.user_class.objects.get(username=username)
			if user.check_password(password):
				return user
		except self.user_class.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return self.user_class.objects.get(pk=user_id)
		except self.user_class.DoesNotExist:
			return None

	@property
	def user_class(self):
		if not hasattr(self, '_user_class'):
			self._user_class = CustomUser
			if not self._user_class:
				raise ImproperlyConfigured('Could not get custom user model')
		return self._user_class

def create_customuser_for_user(sender, **kwargs):
	"""
	Create a matching CustomUser for a User
	"""
	if kwargs['created']:
		p = CustomUser()
		p.__dict__.update(kwargs['instance'].__dict__)
		p.save()

# when we have a User created, we want to convert them into a CustomUser
signals.post_save.connect(create_customuser_for_user, sender=User)
