# This file contains the data processing side for the CSV file, transforming it into arrays for the API

from flask import request
import math
import pandas as pd

# course_data = pd.read_csv('courses_2021_desc.csv')
course_data = pd.read_csv('courses_2021_desc.csv')

# This is a very messy function
# What it tries to do is extract course data based on a number of variables
# Geneds: If you put in a gened requirement it will filter on that requirement
# Depts: It will get courses for specific departments
# Query: If you input a search query it will return that course
# Sort Order: Orders how you want the data to be filtered
def parse_courses(page, geneds, depts, query, sort_order):

    if(int(page) < 0):
        return (0, [])
        
    # sort courses by sort_order

    try:
        course_list = course_data[['Course Name', 'GPA', 'Course Number', 'geneds', 'dept', 'size']]

        for gened in geneds:
            course_list = course_list[course_list['geneds'].apply(lambda x: gened in x)]

        if query and len(query):
            course_list = course_list[course_list['Course Name'].apply(lambda x: query.lower() in x.lower())]

        if depts:
            course_list = course_list[course_list['dept'].apply(lambda x: x in depts)]


        course_list = course_list.sort_values(by=[sort_order], ascending=False)

        total = len(course_list)

        course_list = course_list.iloc[int(page)*100:int(page)*100+100]
        return course_list
    except KeyError:
        return (0, [])
    
def number_of_courses():
    return len(course_data.index)

def number_of_pages():
    return math.ceil(number_of_courses()/100)

def fetch_courses_by_instructor():
    # validate that professor is passed
    if not request.get_json()["instructor"]:
        return 'Bad request!', 400
    else:
        instructor = request.get_json()["instructor"]

    # load page, geneds, and sort_order if given
    page = 0 if "page" not in request.get_json() else request.get_json()["page"]
    geneds = [] if "geneds" not in request.get_json() else request.get_json()["geneds"]
    sort_order = "" if "sort_order" not in request.get_json() else request.get_json()["sort_order"]

    
    course_list = course_data[['Course Name', 'GPA', 'Course Number', 'geneds', 'dept', 'size', "Primary Instructor", "Instructor"]]
    try:
        # load instructor's classes
        course_list = course_list[
            course_list['Instructor'].str.contains(instructor, na=False)
            ]
        
        # load geneds
        for gened in geneds:
                course_list = course_list[course_list['geneds'].apply(lambda x: gened in x)]

        # sort
        if sort_order != "":
            course_list = course_list.sort_values(by=[sort_order], ascending=False)

        return course_list[['Course Name', 'GPA', 'Course Number', 'geneds', 'dept', 'size']].to_json(orient="records")
    except KeyError:
        return 'Bad request! Key Error', 400



#TODO:

# Completely Change this file

# Use it as an interface between an SQL / MySQL database instead of calling pandas to read from a csv

# In its currrent state we want better filtering and searching methods so we can set it up easier