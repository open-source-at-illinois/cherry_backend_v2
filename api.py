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
