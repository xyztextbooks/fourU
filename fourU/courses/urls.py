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

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list

from courses.models import Course

urlpatterns = patterns('',
	(r'^$', object_list, {'queryset': Course.objects.all(),}),
	(r'^(?P<courseSlug>[\w-]+)/$', 'courses.views.course_detail'),
	(r'^(?P<courseSlug>[\w-]+)/(?P<sectionSlug>\d+)/$', 'courses.views.section_detail'),
	(r'^(?P<courseSlug>[\w-]+)/(?P<sectionSlug>\d+)/(?P<assignmentSlug>[\w-]+)/$', 'courses.views.assignment_detail'),
	(r'^(?P<courseSlug>[\w-]+)/(?P<sectionSlug>\d+)/(?P<assignmentSlug>[\w-]+)/(?P<problemNum>\d+)/$', 'courses.views.problem_detail'),
)
