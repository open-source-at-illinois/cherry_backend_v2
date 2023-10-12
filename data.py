# This file contains the data processing side for the CSV file, transforming it into arrays for the API

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

    try:
        page = int(page)
    except ValueError:
        return (0, []) 

    if(page < 0):
        return (0, [])
        
    # sort courses by sort_order

    try:
        course_list = course_data[['Course Name', 'GPA', 'Course Number', 'geneds', 'dept', 'size']] # What information do we want to return and when?

        for gened in geneds:
            course_list = course_list[course_list['geneds'].apply(lambda x: gened.lower() in x.lower())]

        if query:
            course_list = course_list[course_list['Course Name'].apply(lambda x: query.lower() in x.lower())]

        if depts: # is this going to function as a list like geneds? If so need to iterate through
            course_list = course_list[course_list['dept'].apply(lambda x: depts.lower() in x.lower())] # reverse the lambda to change search substring reqs.. Or do we want exact matches?

        if(sort_order == "Course Name"):
            course_list = course_list.sort_values(by=[sort_order], ascending=True)
        else:
            course_list = course_list.sort_values(by=[sort_order], ascending=False)

        course_list = course_list.iloc[page*100:page*100+100]

        if(course_list.empty):  # Should we have this functionality?
            return (0, [])
            
        return course_list
    except KeyError:
        return (0, [])


# Made a new function so I don't have to modify parameters of every call to parse_courses in api.py...
# Need to name/organize our functions more intuitively rather than combining various parameter searches into one or two functions.
def get_course_by_num_instructor(page, num, instructor, sort_order):

    try:
        page = int(page)
    except ValueError as e:
        return (0, []) 

    if(page < 0):
        return (0, [])

    try:
        course_list = course_data[['Course Name', 'Instructor', 'GPA', 'Course Number', 'geneds', 'dept', 'size']]

        if num:
            course_list = course_list[course_list['Course Number'].apply(lambda x: num.lower() in x.lower())]

        if instructor:
            course_list = course_list[course_list['Instructor'].apply(lambda x: instructor.lower() in x.lower() if pd.notnull(x) else False)] # because some instructor columns missing..

        if(sort_order == "Course Name"):
            course_list = course_list.sort_values(by=[sort_order], ascending=True)
        else:
            course_list = course_list.sort_values(by=[sort_order], ascending=False)

        course_list = course_list.iloc[page*100:page*100+100]

        if(course_list.empty):
            print("empty")
            return (0, [])
            
        return course_list
    except KeyError as e:
        print(e)
        return (0, [])
    
def number_of_courses():
    return len(course_data.index)

def number_of_pages():
    return math.ceil(number_of_courses()/100)

#TODO:

# Completely Change this file

# Use it as an interface between an SQL / MySQL database instead of calling pandas to read from a csv

# In its currrent state we want better filtering and searching methods so we can set it up easier