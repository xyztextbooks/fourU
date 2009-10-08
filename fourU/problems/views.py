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

from django.utils import simplejson
from django.http import HttpResponse
from re import search, sub

def preview_problem(request):
	try:
		raw = request.POST['problem']
	except:
		raw = ''
	converted = ['<p>',]
	
	for line in raw.split('\n'):
		if search(r'^[\s]*$', line): # blank line?
			line = '</p><p>'
		elif search(r'[\s]{4}$', line):
			line = sub(r'[\s]{4}$', '<br />', line)
		
		if search(r'\[\[(.*?)\]\]', line):
			line = sub(r'\[\[(.*?)\]\]', r'<input type="text" id="\1" />', line)
		if search(r'#([\w_]+)', line):
			line = sub(r'#([\w_]+)', r'\1', line)
		if search(r'\[%(.*)%\]', line):
			line = sub(r'\[%(.*)%\]', r'<span class="math">\1</span>', line)
		converted.append(line)
	converted.append('</p>')
	
	return HttpResponse(simplejson.dumps({'problem': '\n'.join(converted)}), mimetype='application/json')
