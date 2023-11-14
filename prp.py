import re

# straightforward one or more courses format
# #Prerequisite: MATH240, MATH241

def prereq_format1_parser(prereq_description):
    '''parses prerequisite with format: Prerequisite: course-name, course-name, and/or course name.
    Args:
        prereq_description(str): prerequisite written in english words
    Returns:
        prereqs(list): list of prerequisite courses found in the english description
        orFlag(boolean): true or flase based on whether "or" was present or not in the english description
    '''
    if "or" in prereq_description:
        orFlag = True
    else:
        orFlag = False
    prereqs = prereq_description.replace("Prerequisite: ", "")
    prereqs = prereqs.replace("and ", "").replace("or", "").replace(",", "").split()
    return prereqs, orFlag


# 1 course with minumum grade of C- from... format

def prereq_format2a_parser(prereq_description):
    '''parses prerequisite with format: C- from; with an "and" in it.
    Args:
        prereq_description(str): prerequisite written in english words
    Returns:
        prereq(list): list of prerequisite courses found in the english description
    '''
    prereq = re.search(r'(?<=from \().*(?=\))', prereq_description).group().split(", ")
    return prereq

# 1 course with minumum grade of C- from... format

def prereq_format2b_parser(prereq_description):
    '''parses prerequisite with format: Prerequisite: C- from; with an "and" in it
    Args:
        prereq_description(str): prerequisite written in english words
    Returns:
        prereq(list): list of prerequisite courses found in the english description
        andFlag(boolean): true or flase based on whether "and" was present or not in the english description
    '''
    prereq = re.search(r'(?<=from ).*', prereq_description).group()
    andFlag = False
    if "and" in prereq:
        andFlag = True
    prereq = prereq.replace("or ", "").replace("and ", "").replace(",", "").split(" ")
    return prereq, andFlag

def prereq_format2c_parser(prereq_description):
    '''parses prerequisite with format: and (...)
    Args:
        prereq_description(str): prerequisite written in english words
    Returns:
        prereq(list): list of prerequisite courses found in the english description
        andFlag(boolean): true or flase based on whether "and" was present or not in the english description
    '''
    prereq = re.search(r'(?<=and \().*(?=\))', prereq_description).group()
    andFlag = False
    if "and" in prereq:
        andFlag = True
    prereq = prereq.replace("or ", "").replace("and ", "").replace(",", "").split(" ")
    return prereq, andFlag


# minimum grade of C- in... format

def prereq_format3_parser(prereq_description):
    '''parses prerequisite with format: C- in
    Args:
        prereq_description(str): prerequisite written in english words
    Returns:
        prereq(list): list of prerequisite courses found in the english description
        andFlag(boolean): true or flase based on whether "and" was present or not in the english description
    '''
    prereq = re.search(r'(?<=C- in ).*', prereq_description).group()
    andFlag = False
    if "and" in prereq:
        andFlag = True
    prereq = prereq.replace("or ", "").replace("and ", "").replace(",", "").split(" ")
    return prereq, andFlag

# one of the following (...)

def prereq_format4_parser(prereq_description):
    '''parses prerequisite with format: one of the following (...)
    Args:
        prereq_description(str): prerequisite written in english words
    Returns:
        prereqs(list): list of prerequisite courses found in the english description
    '''
    prereq = re.search(r'(?<=\().*(?=\))', prereq_description).group().replace("or", "").split(", ")
    return prereq


'''
prereq list assembler
'''

def prerequisite_assembler(prerequisites):
    '''assembles all of the prerequisites together in a list
    Args:
        prerequisites(list): list of prerequisite descriptions
    Returns:
        assembled_prereqs(list): list of parsed and formatted prerequisite courses
    '''
    assembled_prerequisites = []

    for prereq in prerequisites:

        '''
        these conditionals search for substrings within the unassembled prerequisites

        if a condition is met, there is an associated parser function that will handle
        the prerequisite that contains a specific substring
        '''

        #filters out the ambiguous prerquisites that people can get around with permission and/or placement tests
        if ("higher" in prereq) or ("must" in prereq) or ("Must" in prereq) or ("permission" in prereq) or ("eligibility" in prereq) or ("test" in prereq):
            return []
        
        #the prerequisites that made it past the filter have strict course prerequisites that cannot be avoided

        if "following" in prereq:
            parsed_prereq = prereq_format4_parser(prereq)
            assembled_prerequisites.append(parsed_prereq)
        
        elif "C- from (" in prereq:

            parsed_prereq = prereq_format2a_parser(prereq)
            assembled_prerequisites.append(parsed_prereq)

        elif "C- from " in prereq:

            parsed_prereq, andFlag = prereq_format2b_parser(prereq)

            # if the andFlag is true, that means the courses should be entered seperately because they are all required
            # if there is only 1 course then it can just be entered seperately
            if andFlag == True or len(parsed_prereq) == 1:
                for prereq in parsed_prereq:
                    assembled_prerequisites.append(prereq)
            # if the flag is false then that means any one of those classes suffice, so they should be entered together in a list
            else:
                assembled_prerequisites.append(parsed_prereq)

        elif "and (" in prereq:
            parsed_prereq, andFlag = prereq_format2c_parser(prereq)
            if andFlag == True or len(parsed_prereq) == 1:
                for prereq in parsed_prereq:
                    assembled_prerequisites.append(prereq)
            # if the flag is false then that means any one of those classes suffice, so they should be entered together in a list
            else:
                assembled_prerequisites.append(parsed_prereq)

        elif "C- in" in prereq:

            parsed_prereq, andFlag = prereq_format3_parser(prereq)

            # if the andFlag is true, that means the courses should be entered seperately because they are all required
            # if there is only 1 course then it can just be entered seperately
            if andFlag == True or len(parsed_prereq) == 1:
                for prereq in parsed_prereq:
                    assembled_prerequisites.append(prereq)
            # if the flag is false then that means any one of those classes suffice, so they should be entered together in a list
            else:
                assembled_prerequisites.append(parsed_prereq)

        elif prereq.startswith("Prerequisite: "):
            if not any(char.isdigit() for char in prereq):
                continue
            parsed_prereq, orFlag = prereq_format1_parser(prereq)
            if orFlag == True:
                assembled_prerequisites.append(parsed_prereq)
            else:
                for prereq in parsed_prereq:
                    assembled_prerequisites.append(prereq)

    #return the list of assembled prerequisites after all iterations of prerequisites
    return assembled_prerequisites

'''
Crosslist parser
'''

def crosslist_parser(script):
    '''formats the crosslist courses in a list
    Args:
        script(str): phrase containing crosslist courses
    Returns:
        crosslist(list): list of crosslisted courses
    '''
    #getting rid of the non-course words
    script = script.replace("Credit only granted for: ", "")
    script = script.replace(",", "").replace("and ", "").replace("or ", "")
    #creating a list of the courses
    crosslist = script.split()
    return crosslist

def genEd_parser(genEd):
    '''formats the general education satisfactions in a list
    Args:
        genEd(str): phrases containing general education satisfactions
    returns:
        genEd(list): list of formatted general education requirements
    '''
    if "or" in genEd:
        orFlag = True
    genEd = genEd.replace("\t", "").replace("\n", " ").replace("GenEd:", "").replace(" ", "")
    genEd = genEd.split(",")
    if orFlag == True:
        temp = []
        genEd.split("or")
        for gen in genEd:
            temp.append(gen)
        genEd = [temp]
    return genEd
