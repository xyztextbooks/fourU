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

from sympy import Rational, Basic
# importing _methods is a bit risky, as it implies that it may change or move at
# any time; we'll have to keep an eye on this
from sympy.core.numbers import _parse_rational as parse_rational
from sympy.core.numbers import igcd as greatest_common_divisor

class Fraction(Rational):
	"""
	Represents a fraction.  Keeps track of numerator and denominator given it,
	rather than reducing, like sympy's Rational, from which this derives.
	
	>>> fraction = Fraction(6, 4)
	>>> fraction
	6/4
	>>> fraction.p
	6
	>>> fraction.q
	4
	
	>>> fraction3 = Fraction(2, 4)
	>>> fraction3
	2/4
	>>> fraction3.p
	2
	>>> fraction3.q
	4
	
	>>> fraction4 = Fraction(2, 2)
	>>> fraction4
	2/2
	>>> fraction4.p
	2
	>>> fraction4.q
	2
	
	Fraction can also be initialized with a string in standard fraction notation.
	
	>>> fraction2 = Fraction("6/4")
	>>> fraction2
	6/4
	>>> fraction2.p
	6
	>>> fraction2.q
	4
	
	We can print it out in nice LaTeX:
	
	>>> from sympy import printing
	>>> printing.latex(fraction)
	'$\\\\frac{6}{4}$'
	"""
	def __new__(cls, num, denom=None):
		obj = Basic.__new__(cls)
		if denom is None:
			if isinstance(num, str):
				obj.p, obj.q = parse_rational(num)
		else:
			obj.p = num
			obj.q = denom
		return obj
	
	def reduce(self):
		"""
		Try to reduce this Fraction, and return a new Fraction of the result.
		
		>>> fraction = Fraction(6, 4)
		>>> fraction
		6/4
		>>> reduced = fraction.reduce()
		>>> reduced
		3/2
		>>> stillReduced = reduced.reduce()
		>>> stillReduced
		3/2
		
		A reduced Fraction should be equivalent to a Rational seeded with the
		same values.
		
		>>> reduced == Rational(6, 4)
		True
		"""
		p = self.p
		q = self.q
		n = greatest_common_divisor(abs(p), q)
		# if we aren't already reduced, divide out the GCD from both parts
		if n > 1:
			p //= n
			q //= n
		return Fraction(p, q)

if __name__ in ("__main__", "__console__"):
	# the doctests aren't identified properly when using iPython or
	# code.InteractiveConsole (which "manage.py problem" uses)
	# see http://stackoverflow.com/questions/1336980/running-doctests-through-ipython-and-pseduo-consoles
	import doctest, problems.utils
	doctest.testmod(problems.utils, verbose=True)
