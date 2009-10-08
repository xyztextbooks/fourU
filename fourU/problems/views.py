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

def wysiwym_to_html(line, answers):
	"""
	Convert our WYSIWYM syntax into HTML, with the help of some meta-information.
	
	Some initial data:
	>>> answers = {u'answer-1': {u'type': u'radio'}, u'answer-2': {u'type': u'fill-in'}}
	
	Variable names are prefixed with a hash (#), and are only substituted
	when enclosed in [% %]:
	
	>>> wysiwym_to_html('Problem #1: [% #a + #b = #sum %]', answers)
	'Problem #1: <span class="math"> a + b = sum </span>'
	
	Any mathematical expressions inside [% %] are assumed to be typeset in TeX,
	and will be converted to standard symbols.
	Currently, this is done by jsMath in the user's browser, so this function
	should leave things alone.
	
	# commenting this out for now, since doctests doesn't like the \r
	# this is the expected behavior, though, so manual testing should work
	#>>> wysiwym_to_html('[% \root n \of {x^n+y^n}\quad %]', answers)
	#'<span class="math"> \root n \\of {x^n+y^n}\\quad </span>'
	
	Answer boxes are indicated by double square brackets around 'answer_xx',
	where 'xx' indicates a unique integer identifying the particular answer:
	
	>>> wysiwym_to_html('The [[answer_1]] of 15 and 20 is [[answer_2]].', answers)
	'The <input type="radio" id="answer_1" /> of 15 and 20 is <input type="radio" id="answer_2" />.'
	
	Square braces may, in the future, be used to indicate the presence of elements
	other than answer boxes.  Therefore, we must not assume an answer box upon
	seeing '[['.
	
	>>> wysiwym_to_html('[[This]] is not an answer.', answers)
	'[[This]] is not an answer.'
	
	The entire problem text will be wrapped in an html paragraph (<p></p>).
	Blank lines will end the current paragraph and begin a new one.
	
	>>> wysiwym_to_html('', answers)
	'</p><p>'
	>>> wysiwym_to_html('  ', answers)
	'</p><p>'
	>>> wysiwym_to_html("\t", answers)
	'</p><p>'
	
	Four spaces at the end of a line produces a line break.
	
	>>> wysiwym_to_html('Lorem ipsum dolor sit amet.    ', answers)
	'Lorem ipsum dolor sit amet.<br />'
	"""
	# end paragraph and begin a new one on blank lines
	if search(r'^[\s]*$', line):
		line = '</p><p>'
	# four spaces at the end of a line gives a line break
	elif search(r'[\s]{4}$', line):
		line = sub(r'[\s]{4}$', '<br />', line)
	
	# replace [[answer_xx]] with an appropriate input box
	if search(r'\[\[answer_(.*?)\]\]', line):
		answerNum = search(r'\[\[answer_(.*?)\]\]', line).group(1)
		type = answers['answer-%s' % answerNum]['type']
		if type == 'fill-in':
			try:
				size = ' size="%s"' % answers['answer-%s' % answerNum]['size']
			except:
				size = ''
			replacement = r'<input type="text"' + size + ' id="answer_\1" />'
		elif type == 'radio':
			replacement = r'<input type="radio" id="answer_\1" />'
		else:
			replacement = ''
		
		line = sub(r'\[\[answer_(.*?)\]\]', replacement, line)
	# strip hash marks from the beginning of variable names
	if search(r'#([\w_]+)', line):
		line = sub(r'#([\w_]+)', r'\1', line)
	# tell jsMath to parse TeX inside [% %]
	if search(r'\[%(.*)%\]', line):
		line = sub(r'\[%(.*)%\]', r'<span class="math">\1</span>', line)
	
	return line

def preview_problem(request):
	"""
	Take in a problem text and some JSON, and combine them to create an html preview.
	"""
	try:
		raw = request.POST['problem']
	except:
		raw = ''
	try:
		answers = simplejson.loads(request.POST['answers'])
	except:
		answers = {}
	converted = ['<p>',]
	
	for line in raw.split('\n'):
		converted.append(wysiwym_to_html(line, answers))
	converted.append('</p>')
	
	return HttpResponse(simplejson.dumps({'problem': '\n'.join(converted)}), mimetype='application/json')

if __name__ in ("__main__", "__console__"):
	# the doctests aren't identified properly when using iPython or
	# code.InteractiveConsole (which "manage.py problem" uses)
	# see http://stackoverflow.com/questions/1336980/running-doctests-through-ipython-and-pseduo-consoles
	import doctest, problems.views
	doctest.testmod(problems.views, verbose=True)
