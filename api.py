# This file will outline the routes that can be called / accessed with the API
# Written in python using flask to perform API calls

import importlib
from flask import Flask, jsonify, request
# Grab the course data from the data.py processing script
from data import parse_courses, number_of_courses, number_of_pages
# moduleName = input('utils')
# importlib.import_module(utils)

app = Flask(__name__)

# Multiple queries
# Example: http://127.0.0.1:8080/2021/courses?page=0&name=intro&geneds=NWC&geneds=HA&dept=REL
@app.route('/2021/courses')
def courses_from_parameters():
   page_number = request.args.get('page', default=0, type=int)
   course_name = request.args.get('name', default='', type=str)
   geneds = request.args.getlist('geneds', type=str)
   dept = request.args.getlist('dept', type=str)
   try:
      course_list = parse_courses(page_number, geneds, dept, course_name, 'Course Name').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

@app.route('/2021/courses_by_gpa/<page_number>')
def courses_by_gpa(page_number):
   try:
      course_list = parse_courses(page_number, '', '', '', 'GPA').to_json(orient='records')
      return course_list
   except AttributeError:  # should probably find a better way to do this, could hide actual AttributeErrors 
      return 'Bad request!', 400

@app.route('/2021/courses_by_name/<page_number>')
def courses_by_name(page_number):
   try:   
      course_list = parse_courses(page_number, '', '', '', 'Course Name').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

@app.route('/2021/courses_by_size/<page_number>')
def courses_by_size(page_number):
   try:
      course_list = parse_courses(page_number, '', '', '', 'size').to_json(orient='records')
      return course_list
   except AttributeError:
      return 'Bad request!', 400

@app.route('/2021/number_of_courses')
def json_number_of_courses():
   return jsonify(number_of_courses())

@app.route('/2021/number_of_pages')
def json_number_of_pages():
   return jsonify(number_of_pages())

#TODO:

# Create a route that will display information about a specific course when you get it

# Create a route that will display specific information about courses in a department

# Create a route that will filter courses based on total size

# Create a route that will retrieve courses taught by a specific instructor

# Create a route that will display all the geneds

# Create a route that will display a gened of a specific category

# Create a route that will filter by department + gpa

# Sort all the different routes into seperate files