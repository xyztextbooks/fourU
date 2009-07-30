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
from django.contrib import admin
from django.conf import settings
from django.views.generic.list_detail import object_list

from courses.models import Course

admin.autodiscover()

urlpatterns = patterns('',
	(r'^courses/', include('courses.urls')),

	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	import os
	media_dir = os.path.join(os.path.dirname(__file__), 'media/')
	
	urlpatterns += patterns('',
		(r'^media/(.*)$', 'django.views.static.serve', {'document_root': media_dir}),
	)
