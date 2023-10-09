# This file contains the data processing side for the CSV file, transforming it into arrays for the API

import math
import pandas as pd
import numpy as np

# course_data = pd.read_csv('courses_2021_desc.csv')
course_data = pd.read_csv('courses_2021_desc.csv')
course_data.replace(np.nan, '')
course_data.fillna("", inplace=True)

# This is a very messy function
# What it tries to do is extract course data based on a number of variables
# Geneds: If you put in a gened requirement it will filter on that requirement
# Depts: It will get courses for specific departments
# Query: If you input a search query it will return that course
# Sort Order: Orders how you want the data to be filtered
def search(**kwargs):
    output = course_data[['Course Name', 'GPA', 'Course Number', 'geneds', 'dept', 'size', 'Instructor']]
    for key, value in kwargs.items():
        key = key.replace("_", " ")
        output = output[output[key].str.contains(value)]
    return output


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

#TODO:

# Completely Change this file

# Use it as an interface between an SQL / MySQL database instead of calling pandas to read from a csv

# In its currrent state we want better filtering and searching methods so we can set it up easier