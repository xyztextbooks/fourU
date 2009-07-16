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

from django.views.generic.list_detail import object_list, object_detail

from courses.models import Course, Section
from assignments.models import Assignment, Problem

def course_detail(request, courseSlug):
	"""
	Display information about a course, including its sections.
	"""
	course = Course.objects.get(slug=courseSlug)
	sections = Section.objects.filter(course__slug=courseSlug)
	return object_list(request, sections, extra_context={'course': course})

def section_detail(request, courseSlug, sectionSlug):
	"""
	Display information about a section, including its assignments.
	"""
	section = Section.objects.filter(course__slug=courseSlug).get(number=sectionSlug)
	assignments = section.assignment_set.all()
	return object_list(request, assignments, extra_context={'course': section.course,
	                                                        'section': section,})

def assignment_detail(request, courseSlug, sectionSlug, assignmentSlug):
	"""
	Display information about an assignment, including its problems.
	"""
	section = Section.objects.filter(course__slug=courseSlug).get(number=sectionSlug)
	assignment = section.assignment_set.get(slug=assignmentSlug)
	problems = assignment.problems.all()
	return object_list(request, problems, extra_context={'course': section.course,
	                                                     'section': section,
	                                                     'assignment': assignment,})

def problem_detail(request, courseSlug, sectionSlug, assignmentSlug, problemNum):
	"""
	Display a problem.
	"""
	section = Section.objects.filter(course__slug=courseSlug).get(number=sectionSlug)
	assignment = section.assignment_set.get(slug=assignmentSlug)
	problem = assignment.problems.get(number=problemNum)
	return object_detail(request, Problem.objects.all(), problem.id)
