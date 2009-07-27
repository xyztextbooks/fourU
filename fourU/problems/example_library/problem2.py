# -*- coding: utf-8 -*-

# imports common to all problems
from __future__ import division
from sympy import *
from django.conf import settings
from django.template.loader import render_to_string
from django import forms
from problems.models import AnswerForm, integer
import problems.models

import random

class Problem(problems.models.Problem):
	requestDict = None
	def __init__(self):
		a = b = 1;
		while a >= b:
			a = random.randint(2, 7)
			b = random.randint(4, 9)
		c = random.randint(3, 4)
		
		self.fraction = Rational(a, b)
		self.num = c * a
		self.denom = c * b
	
	def __str__(self, standAlone=False):
		"""
		Generate the appropriate forms and return a rendered html template.
		"""
		answerForm = AnswerForm(self.requestDict, answer=forms.IntegerField(required=False))
		return render_to_string('example_library/problem2.html', {'MEDIA_PATH_PREFIX': settings.MEDIA_PATH_PREFIX,
		                                                          'fraction': printing.latex(self.fraction),
		                                                          'denom': self.denom,
		                                                          'answerForm': answerForm,
		                                                          'standAlone': standAlone,})
	
	def is_correct(self, answer):
		try:
			return integer(answer['answer']) == self.num
		except KeyError:
			return False

# are we running this standalone, rather than as a module?
def main():
	print Problem().__str__(standAlone=True)
	return

if __name__ == '__main__' or __name__ == '__console__':
	import sys
	sys.exit(main())

