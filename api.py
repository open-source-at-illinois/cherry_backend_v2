# This file will outline the routes that can be called / accessed with the API
# Written in python using flask to perform API calls

import importlib
from flask import Flask
# Grab the course data from the data.py processing script
from data import course_data
moduleName = input('utils')
importlib.import_module(utils)

app = Flask(__name__)

in_memory_datastore = {
   "COBOL" : {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
   "ALGOL" : {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
   "APL" : {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
}

@app.route('/programming_languages/<programming_language_name>')
def get_programming_language(programming_language_name):
   return in_memory_datastore[programming_language_name]
