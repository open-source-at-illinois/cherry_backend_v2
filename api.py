# This file will outline the routes that can be called / accessed with the API
# Written in python using flask to perform API calls

import importlib
from flask import Flask, jsonify
# Grab the course data from the data.py processing script
from data import parse_courses, number_of_courses, number_of_pages, get_course_by_num_instructor
# moduleName = input('utils')
# importlib.import_module(utils)

app = Flask(__name__)

# sort courses by gpa
@app.route('/2021/courses_by_gpa/<page_number>')
def courses_by_gpa(page_number):
   try:
      course_list = parse_courses(page_number, '', '', '', 'GPA').to_json(orient='records')
      return course_list
   except AttributeError:  # should probably find a better way to do this, could hide actual AttributeErrors 
      return 'Bad request!', 400

# sort courses by name
@app.route('/2021/courses_by_name/<page_number>')
def courses_by_name(page_number):
   try:   
      course_list = parse_courses(page_number, '', '', '', 'Course Name').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

# sort courses by size
@app.route('/2021/courses_by_size/<page_number>')
def courses_by_size(page_number):
   try:
      course_list = parse_courses(page_number, '', '', '', 'size').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

# get courses in a dept (currently gets any matches)
@app.route('/2021/courses_by_dept/<dept>/<page_number>')
def courses_by_dept(dept, page_number):
   try:
      course_list = parse_courses(page_number, '', dept, '', 'Course Name').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

# get courses by name (currently gets any matches)
@app.route('/2021/course_by_name/<name>/<page_number>')
def course_by_name(name, page_number):
   try:   
      course_list = parse_courses(page_number, '', '', name, 'Course Name').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

# get courses by number (currently gets any matches)
@app.route('/2021/course_by_number/<num>/<page_number>')
def course_by_number(num, page_number):
   try:   
      course_list = get_course_by_num_instructor(page_number, num, '', 'Course Name').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

# get courses by instructor (currently gets any matches)
@app.route('/2021/course_by_instructor/<instructor>/<page_number>')
def course_by_instructor(instructor, page_number):
   try:   
      course_list = get_course_by_num_instructor(page_number, '', instructor, 'Course Name').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

@app.route('/2021/number_of_courses')
def json_number_of_courses():
   return jsonify(number_of_courses())

@app.route('/2021/number_of_pages')
def json_number_of_pages():
   return jsonify(number_of_pages())

# Notes on the data

# 'GPA' and 'size' columns incomplete...
# Some duplicate and random columns
# Outdated courses


#TODO:

# Create a route that will display information about a specific course when you get it

# Create a route that will display specific information about courses in a department (DONE)

# Create a route that will filter courses based on total size (DONE?)

# Create a route that will retrieve courses taught by a specific instructor (Next)

# Create a route that will display all the geneds

# Create a route that will display a gened of a specific category

# Create a route that will filter by department + gpa

# Create a route to search by course number (DONE)

# Create a route to filter/search by class type

# Sort all the different routes into seperate files