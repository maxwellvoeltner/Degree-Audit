from cws import get_corequisite, get_credits, get_crosslist, get_prerequisites, get_genEd, get_course_content

class Course:
    '''Creates a University of Maryland course.
    Attributes:
        name(str): name of the course as it appears on the Schedule of Classes.
        credits(int): number of credit hours the class is worth.
        prerequisites(list): list of prerequisite courses associated with course.
        corequisites(list): list of prerequisite courses associated with course.
        crosslist(list): list of courses that associated course grants credit for in addition to itself.
        genEd(list): list of general education requirements the course satisfies.
    '''

    def __init__(self, name):
        self.name = format_course_name(name)
        course_content = get_course_content(self.name)
        self.credits = get_credits(course_content)
        self.prerequisites = get_prerequisites(course_content)
        self.corequisites = get_corequisite(course_content)
        self.crosslist = get_crosslist(course_content)
        self.genEd = get_genEd(course_content)


def format_course_name(course_in):
    '''Formats a course name by the style standard that appears in the Schedule of Classes.
    Args:
        Course_in(str): name of a course
    Returns:
        Formatted_course_name(str): course name adhered to style standard of courses in the Schedule of Classes
    '''
    #the goal here is to give the users flexibility when entering course names by allowing them to enter lowercase letters 
    #when uppercase letters are required for the webscrapers to work

    #retreiving and formatting the department portion of the course name (the first 4 characters, ex: INST)
    #making it uppercase
    department = (course_in[:4]).upper()

    #formatting course name to be congruent with formatting of course names on website
    formatted_course_name = department + course_in[4:]

    #in the odd case there is a letter at the end of the course name 
    #make that letter uppercase
    if formatted_course_name[-1].isalpha():
        end_letter = formatted_course_name[-1].upper()
        formatted_course_name = formatted_course_name[:-1] + end_letter

    return formatted_course_name
