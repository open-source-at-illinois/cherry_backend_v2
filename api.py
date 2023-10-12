# This file will outline the routes that can be called / accessed with the API
# Written in python using flask to perform API calls

import importlib
from flask import Flask, jsonify, request
# Grab the course data from the data.py processing script
from data import parse_courses_by_criteria_dictionary
# moduleName = input('utils')
# importlib.import_module(utils)

app = Flask(__name__)

# General route for filtering courses based on passed json
# Supported JSON/Dictionary keys and explected value types copied from parse_courses_by_criteria_dictionary
'''
gened_keys = ('gened', 'geneds') # TYPE: List of Strings
gened_match_all_keys = ('match all geneds', 'all geneds', 'match all') # TYPE: Boolean
department_keys = ('department', 'departments', 'dept', 'depts') # TYPE: List of Strings
primary_instructor_keys = ('primary instructor', 'pi', 'instructor', 'instructor name') # TYPE: String
max_gpa_keys = ('max gpa', 'gpa max') # TYPE: Float
min_gpa_keys = ('min gpa', 'gpa min') # TYPE: Float
course_number_keys = ('course number', 'cnum', 'number') # TYPE: Integer
course_name_keys = ('course name', 'cname', 'name') # TYPE: String
max_course_level_keys = ('max course level', 'course level max', 'max cl', 'cl max') # TYPE: Integer (Hundreds)
min_course_level_keys = ('min course level', 'course level min', 'min cl', 'cl min') # TYPE: Integer (Hundreds)
course_level_keys = ('course level', 'cl') # TYPE: Integer (Hundreds)
min_class_size_keys = ('min class size', 'class size min', 'min cs', 'cs min') # TYPE: Integer
max_class_size_keys = ('max class size', 'class size max', 'max cs', 'cs max') # TYPE: Integer

sort_by_keys = ('sort by', 'by') # TYPE: String --> Can be: ('Course Name', 'dept', 'Number', 'size', 'GPA')
#   * 'GPA' will be default if not given by criteria_dictionary or invalid string provided
sort_ascending_keys = ('sort ascending', 'ascending', 'ascend', 'order ascending', 'ascending order') # TYPE: Boolean
#   * False will be default if not given by criteria_dictionary
'''
@app.route('/2021/query_course_list/<page_number>')
def courses_by_json(page_number):
   try:
      course_data = {}
      criteria_dictionary = request.get_json()

      if type(criteria_dictionary) is dict:
         course_data = parse_courses_by_criteria_dictionary(criteria_dictionary, int(page_number))

      return jsonify({
         'course data' : course_data[0].to_dict('index'), # Dictionary of courses with str(index) as keys
         'courses returned' : course_data[1],
         'total courses' : course_data[2], # Total courses matching criterion
         'highest page' : course_data[3], # Highest page for displaying courses
         'returned page' : course_data[4] # Page requested and returned
      })
   except AttributeError:
      return 'Bad request!', 400


### DEPRECATED ROUTES ###
# However, I updated all of them to use the parse_courses_by_criteria_dictionary method for compatibility with overhauled data.py
# All courses sorted by GPA
@app.route('/2021/courses_by_gpa/<page_number>')
def courses_by_gpa(page_number):
   try:
      course_data = {}
      criteria_dictionary = {
         'sort by' : 'GPA'
      }

      course_data = parse_courses_by_criteria_dictionary(criteria_dictionary, int(page_number))

      return jsonify({
         'course data' : course_data[0].to_dict('index'), # Dictionary of courses with str(index) as keys
         'courses returned' : course_data[1],
         'total courses' : course_data[2], # Total courses matching criterion
         'highest page' : course_data[3], # Highest page for displaying courses
         'returned page' : course_data[4] # Page requested and returned
      })
   except AttributeError:  # should probably find a better way to do this, could hide actual AttributeErrors 
      return 'Bad request!', 400


# All courses sorted by name
@app.route('/2021/courses_by_name/<page_number>')
def courses_by_name(page_number):
   try:
      course_data = {}
      criteria_dictionary = {
         'sort by' : 'Course Name'
      }

      course_data = parse_courses_by_criteria_dictionary(criteria_dictionary, int(page_number))

      return jsonify({
         'course data' : course_data[0].to_dict('index'), # Dictionary of courses with str(index) as keys
         'courses returned' : course_data[1],
         'total courses' : course_data[2], # Total courses matching criterion
         'highest page' : course_data[3], # Highest page for displaying courses
         'returned page' : course_data[4] # Page requested and returned
      })
   except AttributeError:
      return 'Bad request!', 400


# All courses sorted by size
@app.route('/2021/courses_by_size/<page_number>')
def courses_by_size(page_number):
   try:
      course_data = {}
      criteria_dictionary = {
         'sort by' : 'size'
      }

      course_data = parse_courses_by_criteria_dictionary(criteria_dictionary, int(page_number))

      return jsonify({
         'course data' : course_data[0].to_dict('index'), # Dictionary of courses with str(index) as keys
         'courses returned' : course_data[1],
         'total courses' : course_data[2], # Total courses matching criterion
         'highest page' : course_data[3], # Highest page for displaying courses
         'returned page' : course_data[4] # Page requested and returned
      })
   except AttributeError:
      return 'Bad request!', 400


#TODO:

# Create a route that will display information about a specific course when you get it

# Create a route that will display specific information about courses in a department

# Create a route that will display all the geneds