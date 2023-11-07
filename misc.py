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
    #retreiving and formatting the department portion of the course_in (the first 4 characters, ex: INST)
    department = (course_in[:4]).upper()

    #formatting course_in to be congruent with formatting of course names on website
    formatted_course_name = department + course_in[4:]

    return formatted_course_name
