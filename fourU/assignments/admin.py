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

from django.contrib import admin
from fourU.assignments.models import Problem, ProblemGrade, Assignment, AssignmentGrade

class AssignmentAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	list_display = ('name', 'course_and_section', 'startDate', 'endDate')

class AssignmentGradeAdmin(admin.ModelAdmin):
	list_display = ('assignment', 'section', 'score')

class ProblemGradeAdmin(admin.ModelAdmin):
	list_display = ('user', 'problem', 'score', 'attempts')


admin.site.register(Problem)
admin.site.register(ProblemGrade, ProblemGradeAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(AssignmentGrade, AssignmentGradeAdmin)
