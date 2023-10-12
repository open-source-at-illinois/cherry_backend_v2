# This file contains the data processing side for the CSV file, transforming it into arrays for the API

import math
import pandas as pd
import time # For runtime comparisons

# Read course data csv with pandas
raw_data = pd.read_csv('courses_2021_desc.csv')
course_data = raw_data[['dept', 'Number', 'Course Name', 'Number of Credits', 'Primary Instructor', 'GPA', 'geneds','size']]


# RETURN: Filtered Dataframe of courses that satisfy ALL geneds given.
# INPUT geneds: Required field. List of gen-eds in abbreviated, all-caps format of type str.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_all_geneds(geneds: list, data: pd.DataFrame = course_data):
    output_data = data

    for gened in geneds:
        # Every iteration filters out the courses that do not satisfy gened
        output_data = output_data[output_data['geneds'].apply(lambda x: gened in x)]
    
    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# RETURN: Filtered Dataframe of courses that satisfy AT LEAST ONE gened given (with no repeats).
# INPUT geneds: Required field. List of gen-eds in abbreviated, all-caps format of type str.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_geneds(geneds: list, data: pd.DataFrame = course_data):
    output_data = pd.DataFrame(columns = ['dept', 'Number', 'Course Name', 'Number of Credits', 'Primary Instructor', 'GPA', 'geneds','size'])

    for gened in geneds:
        # Every iteration appends classes that satisfy gened from geneds
        # We also have to remove duplicate headers and courses from concatenating
        temp = data[data['geneds'].apply(lambda x: gened in x)]
        output_data = pd.concat([output_data, temp]).drop_duplicates()

    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# RETURN: Filtered Dataframe of courses that are from the given departments.
# INPUT depts: Required field. List of departments in abbreviated, all-caps format of type str.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_departments(depts: list, data: pd.DataFrame = course_data):
    output_data = data[data['dept'].isin(depts)] # Slightly faster than lambda implementation? --> from my limited testing
    
    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# RETURN: Filtered Dataframe of courses that are taught by primary instructors' 
#   whose names contain or match the given words separated by spaces in a string.
# INPUT name: Required field. Instructor name or parts of instructor name separated by spaces to filter by.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_primary_instructor(name: str, data: pd.DataFrame = course_data):
    # Split up first and last name in case that was entered
    # This means if 'Geoffrey Challen' or even 'Geof Chal' is entered, 'Challen, Geoffrey' in the DataFrame will still be found
    names = name.lower().split(" ")

    output_data = data

    for n in names:
        # Ever iteration filters out the courses that don't match the substring of names n
        output_data = output_data[output_data['Primary Instructor'].apply(lambda x: n in str(x).lower())]

    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# RETURN: Filtered Dataframe of courses that have GPAs between minimum and maximum.
# INPUT min: Default is 0.000. Float that represents lower bound gpa of courses returned.
# INPUT max: Default is 4.000. Float that represents upper bound gpa of courses returned.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_gpa(min: float = 0.000, max: float = 4.000, data: pd.DataFrame = course_data):
    # Catch if there is no value and filter the row immediately
    # Then convert to float and compare to min and max
    output_data = data[data['GPA'].apply(lambda x: False if x == '' else float(x) >= min and float(x) <= max)]
    
    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# RETURN: Filtered Dataframe of courses whose course number (NOT DEPT + NUMBER) matches the given integer.
# INPUT number: Required Field. Course number to filter by.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_course_number(number: int, data: pd.DataFrame = course_data):
    # Direct comparison to Number column
    output_data = data[data['Number'] == number]
    
    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# RETURN: Filtered Dataframe of courses whose course name matches the words separated by spaces contained in the given string.
#   * Same implementation as parse_courses_by_primary_instructor.
# INPUT name: Required Field. Course name or parts of name separated by spaces to filter by.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_course_name(name: str, data: pd.DataFrame = course_data):
    # Split up first and last name in case that was entered
    names = name.lower().split(" ")

    output_data = data

    for n in names:
        # Ever iteration filters out the courses that don't match the substring of names n
        output_data = output_data[output_data['Course Name'].apply(lambda x: n in str(x).lower())]
    
    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# RETURN: Filtered Dataframe of courses whose course level matches the range of levels given
#   * Can find course of a specific level by putting in min and max of equal level.
# INPUT min_level: Default 100. Minimum bound of level of the courses returned in hundreds.
# INPUT max_level: Default 700. Maximum bound of level of the courses returned in hundreds.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_course_levels(min_level: int = 100, max_level: int = 700, data: pd.DataFrame = course_data):
    # Catch if there is no value and filter the row immediately
    # Then convert to float and compare to min_level and max_level using floor division
    output_data = data[data['Number'].apply(lambda x: False if x == '' else float(x) // 100 >= min_level // 100 and float(x) // 100 <= max_level // 100)]
    
    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# RETURN: Filtered Dataframe of courses whose class size is within the range of sizes given
# INPUT min_size: Default 0. Minimum bound of class size of the courses returned.
# INPUT max_size: Default 2500. Maximum bound of class size of the courses returned.
# INPUT data: Default is the global course_data DataFrame. DataFrame to be filtered.
def parse_courses_by_class_sizes(min_size: int = 0, max_size: int = 2500, data: pd.DataFrame = course_data):
    output_data = data[data['size'].apply(lambda x: False if x == '' else float(x) >= min_size and float(x) <= max_size)]
    
    # Reset the indexing of the dataframe before returning
    output_data = output_data.reset_index(drop=True)

    return output_data


# HELPER FUNCTION OF parse_courses_by_criteria_dictionary
# RETURN: Criteria data defined by the keys passed in.
# INPUT criteria_dictionary: Required field. Dictionary to search.
# INPUT keys: Required field. Tuple of keys to search.
# INPUT type: Required field. The type of the data it must be. Incompatible data is skipped.
def extract_criteria(criteria_dictionary: dict, keys: tuple, check_type):
    for key in keys:
        if key in criteria_dictionary:
            if (type(criteria_dictionary[key]) is check_type):
                return criteria_dictionary[key]

    return None

# RETURN: A tuple of -->
#   Filtered Dataframe of courses that match the criteria set by the given dictionary in its specified page of up to 100 courses
#   Number of Courses in that Dataframe
#   Highest Page index for that Dataframe
#   Current Page
# INPUT criteria_dictionary: Required Field. Dictionary of criteria. 
#   * Keys and values need to match supported keys and value type defined near beginning of function
#   * NOT ALL KEYS NEED TO BE USED, ONLY INCLUDE THE KEYS FOR THE DESIRED FILTERING RULES IN criteria_dictionary
# INPUT page_number: Default 0. Each page is 100 courses. Pages outside the range will return empty dataframe.
def parse_courses_by_criteria_dictionary(criteria_dictionary: dict, page_number: int = 0):
    # IDK how frontend wants to do with keys so here's what the currently supported keys are for each filter
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
    

    # Extract Json Data to Variables
    geneds = extract_criteria(criteria_dictionary, gened_keys, list)
    match_all_geneds = extract_criteria(criteria_dictionary, gened_match_all_keys, bool)
    departments = extract_criteria(criteria_dictionary, department_keys, list)
    instructor_name = extract_criteria(criteria_dictionary, primary_instructor_keys, str)
    max_gpa = extract_criteria(criteria_dictionary, max_gpa_keys, float)
    min_gpa = extract_criteria(criteria_dictionary, min_gpa_keys, float)
    course_number = extract_criteria(criteria_dictionary, course_number_keys, int)
    course_name = extract_criteria(criteria_dictionary, course_name_keys, str)
    max_course_level = extract_criteria(criteria_dictionary, max_course_level_keys, int)
    min_course_level = extract_criteria(criteria_dictionary, min_course_level_keys, int)
    exact_course_level = extract_criteria(criteria_dictionary, course_level_keys, int)
    min_class_size = extract_criteria(criteria_dictionary, min_class_size_keys, int)
    max_class_size = extract_criteria(criteria_dictionary, max_class_size_keys, int)
    sort_by = extract_criteria(criteria_dictionary, sort_by_keys, str)
    sort_ascending = extract_criteria(criteria_dictionary, sort_ascending_keys, bool)
    
    # If exact level is given, it overrides the min and max
    if exact_course_level:
        min_course_level = exact_course_level
        max_course_level = exact_course_level

    # If match_all_geneds is not given, it is automatically false by default
    if match_all_geneds is None:
        match_all_geneds = False

    # If sort_ascending is not given, it is automatically false by default
    if sort_ascending is None:
        sort_ascending = False


    # DEBUG
    #print([geneds, match_all_geneds, departments, instructor_name, max_gpa, min_gpa, course_number, 
    #    course_name, max_course_level, min_course_level, exact_course_level, min_class_size, sort_by, sort_ascending
    #])

    # Filter based on extraced data
    course_list = course_data

    if geneds and match_all_geneds:
        course_list = parse_courses_by_all_geneds(geneds, course_list)
    
    if geneds and not match_all_geneds:
        course_list = parse_courses_by_geneds(geneds, course_list)
    
    if departments:
        course_list = parse_courses_by_departments(departments, course_list)
    
    if instructor_name:
        course_list = parse_courses_by_primary_instructor(instructor_name, course_list)
    
    if max_gpa and min_gpa:
        course_list = parse_courses_by_gpa(min = min_gpa, max = max_gpa, data = course_list)
    elif max_gpa and not min_gpa:
        course_list = parse_courses_by_gpa(max = max_gpa, data = course_list)
    elif not max_gpa and min_gpa:
        course_list = parse_courses_by_gpa(min = min_gpa, data = course_list)

    if course_number:
        course_list = parse_courses_by_course_number(course_number, course_list)
    
    if course_name:
        course_list = parse_courses_by_course_name(course_name, course_list)
    
    if max_course_level and min_course_level:
        course_list = parse_courses_by_course_levels(min_level = min_course_level, max_level = max_course_level, data = course_list)
    elif max_course_level and not min_course_level:
        course_list = parse_courses_by_course_levels(max_level = max_course_level, data = course_list)
    elif not max_course_level and min_course_level:
        course_list = parse_courses_by_course_levels(min_level = min_course_level, data = course_list)
    
    if max_class_size and min_class_size:
        course_list = parse_courses_by_class_sizes(min_size = min_class_size, max_size = max_class_size, data = course_list)
    elif max_class_size and not min_class_size:
        course_list = parse_courses_by_class_sizes(max_size = max_class_size, data = course_list)
    elif not max_class_size and min_class_size:
        course_list = parse_courses_by_class_sizes(min_size = min_class_size, data = course_list)


    # Sort based on extracted sort_by and sort_ascending
    try:
        match sort_by:
            case None:
                course_list = course_list.sort_values(by = ['GPA'], ascending = sort_ascending)

            case 'Course Name':
                course_list = course_list.sort_values(by = ['Course Name'], ascending = sort_ascending)
                
            case 'dept':
                course_list = course_list.sort_values(by = ['dept'], ascending = sort_ascending)

            case 'Number':
                course_list = course_list.sort_values(by = ['Number'], ascending = sort_ascending)

            case 'size':
                course_list = course_list.sort_values(by = ['size'], ascending = sort_ascending)

            case _:
                course_list = course_list.sort_values(by = ['GPA'], ascending = sort_ascending)
    except KeyError:
        # Catch sorting errors sometimes when dataframe is empty
        return (pd.DataFrame(columns = ['dept', 'Number', 'Course Name', 'Number of Credits', 'Primary Instructor', 'GPA', 'geneds','size']), 0, 0, 0, page_number)

    # Reset the indexing of the dataframe
    course_list = course_list.reset_index(drop=True)

    # Return the correct page and its rows
    final_length = len(course_list)
    highest_page_index = final_length // 100
    first_index_of_page = page_number * 100
    last_index_of_page = page_number * 100 + 100

    if page_number < 0:
        # If negative page number is asked for, still give the other info
        return (pd.DataFrame(columns = ['dept', 'Number', 'Course Name', 'Number of Credits', 'Primary Instructor', 'GPA', 'geneds','size']), 0, final_length, highest_page_index, page_number)

    if first_index_of_page > final_length:
        # If the first index requested is out of bounds, the page number was too high
        return (pd.DataFrame(columns = ['dept', 'Number', 'Course Name', 'Number of Credits', 'Primary Instructor', 'GPA', 'geneds','size']), 0, final_length, highest_page_index, page_number)

    if last_index_of_page > final_length:
        # If the last index requested is out of bounds, adjust it down to the bounds
        last_index_of_page = final_length

    course_list = course_list.iloc[first_index_of_page:last_index_of_page]

    return (course_list, len(course_list), final_length, highest_page_index, page_number)

'''
##### TESTING/EXAMPLE CODE #####
test_dict_1 = {
    'geneds' : ['WCC', 'HA'],
    'match all' : True,
    'sort by' : 'size'
}

print("-----")
print("Test Dictionary 1:")
print(parse_courses_by_criteria_dictionary(test_dict_1, 0))

test_dict_2 = {
    'depts' : ['MUSC', 'CLCV', 'ENGL', 'GER'],
    'sort by' : 'dept',
    'min gpa' : 2.000,
    'max gpa' : 3.7
}

print("-----")
print("Test Dictionary 2:")
print(parse_courses_by_criteria_dictionary(test_dict_2, 0))

test_dict_3 = {
    'course name' : 'nTro',
    'sort by' : 'Number',
    'ascending' : True,
    'min cl' : 200
}

print("-----")
print("Test Dictionary 3:")
print(parse_courses_by_criteria_dictionary(test_dict_3, 0))


test_dict_4 = {
    'instructor' : 'Ma C', # Contains both 'ma' and 'c' in name somewhere
    'course level' : 200
}

print("-----")
print("Test Dictionary 4:")
print(parse_courses_by_criteria_dictionary(test_dict_4, 0))


test_dict_5 = {
    'min gpa' : 3.00
}

print("Test Dictionary 5: Pg 0 / 11")
print(parse_courses_by_criteria_dictionary(test_dict_5, 0))
print("-----")
print("Test Dictionary 5: Pg 8 / 11")
print(parse_courses_by_criteria_dictionary(test_dict_5, 8))
print("-----")
print("Test Dictionary 5: Pg 11 / 11")
print(parse_courses_by_criteria_dictionary(test_dict_5, 11))
print("-----")
print("Test Dictionary 5: Pg 12 / 11")
print(parse_courses_by_criteria_dictionary(test_dict_5, 12)) # Out of bounds
print("-----")
print("Test Dictionary 5: Pg -1 / 11")
print(parse_courses_by_criteria_dictionary(test_dict_5, -1)) # Out of bounds


'''
