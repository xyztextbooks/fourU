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
from django.shortcuts import render_to_response

from courses.models import Course, Section
from assignments.models import Assignment, Problem, ProblemGrade

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
	
	data = {}
	
	if request.method == 'GET':
		grade = ProblemGrade(problem=problem, user=request.user)
		problemInstance = problem.instance
	
	if request.method == 'POST':
		# pull the ProblemGrade out of the session, or from the database if necessary
		try:
			grade = request.session.get('grade', ProblemGrade.objects.get(user=request.user))
		# and if we haven't created one yet (first time viewing this problem), then create a new one
		except:
			grade = ProblemGrade(problem=problem, user=request.user)
		try:
			problemInstance = request.session['problemInstance']
			# give the problemInstance back the values submitted, if any
			problemInstance.requestDict = request.POST
		except:
			problemInstance = problem.instance
		
		# catch exceptions raised by is_correct(), which may use a comparison function not in our tests
		try:
			answers = {}
			for key, value in request.POST.iteritems():
				if key[:7] == "answer-":
					answers[key[7:]] = value
			
			if problemInstance.is_correct(answers):
				data['message'] = 'Hooray, you got it right!'
			else:
				data['message'] = ':( try again'
		except:
			raise # maybe do something else?
		# only count the attempt if we didn't encounter a problem checking the answer
		else:
			# don't save the problem in the database if we aren't logged in
			if request.user.is_authenticated():
				grade.attempts += 1
				grade.save()
	
	problem.instance = problemInstance
	request.session['problemInstance'] = problemInstance
	request.session['grade'] = grade
	
	data['problem'] = problem
	return render_to_response('assignments/problem_detail.html', data)
