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

class Problem():
	def __init__(self, **kwargs):
		# add any given keywords arguments as instance variables
		for arg in kwargs:
			vars(self)[arg] = kwargs[arg]
	
	def check_answer(self, studentAnswer, compare=None):
		if compare:
			return compare(self.answer, studentAnswer)
		else:
			return self.answer == studentAnswer
