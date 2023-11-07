from bs4 import BeautifulSoup
import requests
import sys
from prp import crosslist_parser, prerequisite_assembler


def get_content(course_in, url):

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
    #initializing new list for cleaned requirements
    clean_list = []

    for item in old_list:

    #filters out empty strings that may occur from split function outside this method
    #gets rid of preceding/trailing whitespace and adds requirments to cleaned
        if len(item) > 0:
            clean_list.append(item.strip())

    return clean_list


def get_requirements(course_content):

    #retreiving the prerequisites from the course on webpage
    try:
        course_approved_content = course_content.find("div", class_ = "approved-course-text")
        requirements = course_approved_content.div.div.text

        #creating list of requirements
        requirements = requirements.split(".")

        requirements = clean_list(requirements)
        return requirements
    except:
        return []


def get_corequisite(course_content):
        
    requirements = get_requirements(course_content)
    for requirement in requirements:

        #checking if a prerequisite requirement exists
        #returning that requirement if it does exist
        if requirement.startswith("Corequisite:"):

            requirement = requirement.replace("Corequisite: ", "")
            return requirement
        
    #none were found
    return []


def get_prerequisites(course_content):
        
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
    
    requirements = get_requirements(course_content)
    for requirement in requirements:
        if requirement.startswith("Credit only granted for:"):
            requirement = crosslist_parser(requirement)
            return requirement
        
    #none were found
    return []


def get_genEd(course_content):

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
