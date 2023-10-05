# This file contains the data processing side for the CSV file, transforming it into arrays for the API

import math
import pandas as pd

# course_data = pd.read_csv('courses_2021_desc.csv')
course_data = pd.read_csv('courses_2021_desc.csv')

def parse_courses(page, geneds, depts, query, sort_order):
    if len(geneds) == 0:
        pass

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
    
