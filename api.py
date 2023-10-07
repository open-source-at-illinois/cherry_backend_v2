# This file will outline the routes that can be called / accessed with the API
# Written in python using flask to perform API calls

import importlib
from flask import Flask, jsonify
# Grab the course data from the data.py processing script
from data import parse_courses, number_of_courses, number_of_pages
# moduleName = input('utils')
# importlib.import_module(utils)

app = Flask(__name__)

@app.route('/2021/courses_by_gpa/<page_number>')
def courses_by_gpa(page_number):
   return parse_courses(page_number, '', '', '', 'gpa').to_json(orient='records')

@app.route('/2021/courses_by_name/<page_number>')
def courses_by_name(page_number):
   return parse_courses(page_number, '', '', '', 'Course Name').to_json(orient='records')

@app.route('/2021/courses_by_size/<page_number>')
def courses_by_size(page_number):
   return parse_courses(page_number, '', '', '', 'size').to_json(orient='records')

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