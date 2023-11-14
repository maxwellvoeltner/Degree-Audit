from bs4 import BeautifulSoup
import requests
import sys
from prp import crosslist_parser, prerequisite_assembler


def get_content(course_in, url):
    '''retreives the html content for a specific course on one of the schedule of classes pages
       this is a subportion of the get_course_content function
    Args:
        course_in(str): name of the course
        url(str): url link to the webpage where the content is housed
    Returns:
        content(soup object): html content of a specific course
    '''

    #webscraping:

    #retreiving source code from webpage
    source = requests.get(url).text

    #parsing source code using lxml parser in BeautifulSoup
    soup = BeautifulSoup(source, "lxml")

    #finding div tag with an id equal to formatted course and retreiving its content
    content = soup.find("div", id = course_in)

    return content

#need try and except clause for course_content = soup.find("div", id = formatted_course) line to handle invalid course error
def get_course_content(course_in):
    '''Finds the html content associated with a course on the Schedule of Classes on Testudo.
    Args:
        course_in(str): name of the course as appears on Schedule of classes.
    Returns:
        course_content(html): html content associated with course_in.
    '''

    #urls of the Schedule of Classes where all classes can be found
    # *some classes are only offered in the fall and some only in the spring so it is necessary to check both

    #Spring 2024
    classes_url1 = "https://app.testudo.umd.edu/soc/202401/"

    #Fall 2023
    classes_url2 = "https://app.testudo.umd.edu/soc/202308/"

    #retreiving and formatting the department portion of the course_in (the first 4 characters, ex: INST)
    department = (course_in[:4])

    #adding department onto url to get webpage containing course_in
    source_url = classes_url1 + department

    #trying the spring 2024 schedule of classes
    course_content = get_content(course_in, source_url)

    if course_content != None:

        return course_content
    
    #trying the fall 2023 schedule of classes
    source_url = classes_url2 + department

    course_content = get_content(course_in, source_url)
    
    if course_content != None:

        return course_content
    
    #no course content found indicates the course is not available or does not exist
    print(f"Course: {course_in} could not be found")
    sys.exit()


def get_credits(course_content):
    '''Finds credits associated with course_in.
    Args:
        course_in(str): name of the course as appears on Schedule of Classes.
    Returns:
        credits(int): number of credits associated with course_in.
    '''

    #retreiving the credits from the course on webpage
    #for courses with a range of credits, the minimum credits is assumed
    credits = course_content.find("span", class_ = "course-min-credits").text
    credits = int(credits)
    return credits


def clean_list(old_list):
    '''filters and cleanly formats items in a list to make so the items can be effectively used in other funcions
    Args:
        old_list(list): list of items
    Returns:
        clean_list(list): list with filtered and cleanly formatted items
    '''
    #initializing new list for cleaned requirements
    clean_list = []

    for item in old_list:

    #filters out empty strings that may occur from split function outside this method
    #gets rid of preceding/trailing whitespace and adds requirments to cleaned
        if len(item) > 0:
            clean_list.append(item.strip())

    return clean_list


def get_requirements(course_content):
    '''gets the restrictions, prerequisites, corequisites, and crosslists associated with a course
    Args:
        course_in(str): name of a course
    Returns:
        requirements(list): list of restrictions, prerequisites, corequisites, and crosslists associated with a course
        empty list if no requirements are found
    '''

    #retreiving the prerequisites from the course on webpage
    try:
        course_approved_content = course_content.find("div", class_ = "approved-course-text")
        requirements = course_approved_content.div.div.text

        #creating list of requirements
        requirements = requirements.split(".")

        requirements = clean_list(requirements)
        return requirements
    except:
        #no requirements found in the first div tag of the first div tag which is where the requirements are always housed
        return []


def get_corequisite(course_content):
    '''gets the corequisites course(s) of a course
    Args:
        course_in(str): name of a course
    Returns:
        requirement(str): phrase describing corequisite of a course
        empty list if no corequisites are found
    '''
    requirements = get_requirements(course_content)
    for requirement in requirements:

        #checking if a prerequisite requirement exists
        #returning that requirement if it does exist
        if requirement.startswith("Corequisite:"):

            requirement = requirement.replace("Corequisite: ", "")
            return [requirement]
        
    #none were found
    return []


def get_prerequisites(course_content):
    '''gets the prerequisite courses for a course
    Args:
        course_in(str): name of a course
    Returns:
        prerequisites(list): list of prerequisite courses for a course
        empty list if no prerequisites are found
    ''' 
    requirements = get_requirements(course_content)
    for requirement in requirements:

        #checking if a prerequisite requirement exists
        #returning that requirement if it does exist
        if requirement.startswith("Prerequisite:"):
            requirement_list = requirement.split(";")
            requirement_list = clean_list(requirement_list)
            prerequisites = prerequisite_assembler(requirement_list)
            return prerequisites
        
    #none were found
    return []


def get_crosslist(course_content):
    '''gets crosslist courses for a course
    Args:
        course_in(str): name of a course
    Returns:
        requirement(str): crosslist courses for a course
        empty list if no crosslist is found
    '''
    requirements = get_requirements(course_content)
    for requirement in requirements:
        if requirement.startswith("Credit only granted for:"):
            requirement = crosslist_parser(requirement)
            return requirement
        
    #none were found
    return []


def get_genEd(course_content):
    '''gets the genEd satisfactions for a course
    Args:
        course_in(str): name of a course
    Returns:
        genEd(list): list of genEds
        empty list if no genEds are found
    '''
    #retreiving the genEds from the course on webpage
    try:
        genEd = course_content.find("div", class_ = "gen-ed-codes-group six columns")
        genEd = genEd.text.replace("\t", "").replace("\n", " ").replace("GenEd:", "").replace(" ", "")
        genEd = genEd.split(",")

        for item in genEd:

            if "or" in item:

                genEd.remove(item)
                satisfactions = item.split("or")
                genEd.append(satisfactions)

            if len(genEd) == 1 and genEd[0] == "":
                genEd = []

        return genEd
    
    #no genEds were found
    except:
        return []
