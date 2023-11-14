import sys
from misc import Course

graduation_plan = {
    0: [Course("STAT100")],
    1: [Course("MATH115"), Course("STAT100"), Course("ENGL101"), Course("JOUR200"), Course("AASP200")],
    2: [Course("INST126"), Course("PSYC100"), Course("RDEV250"), Course("COMM107"), Course("THET116")],
    3: [Course("INST201"), Course("INST326"), Course("INST311"), Course("BSCI135"), Course("ANSC101")],
    4: [Course("INST327"), Course("INST335"), Course("ENGL290"), Course("AMST202"), Course("KNES265")],
    5: [Course("INST314"), Course("INST364"), Course("ENGL394"), Course("AGST333"), Course("AGST426")],
    6: [Course("INST352"), Course("INST341"), Course("WGSS263"), Course("EDSP210"), Course("GEOG272")],
    7: [Course("INST346"), Course("INST362"), Course("INST366"), Course("AREC365"), Course("COMM230")],
    8: [Course("INST490"), Course("INST464"), Course("inst408i"), Course("COMM250"), Course("ECON185")],
}


def verify_credits(graduation_plan):
    '''assesses validity of graduation plan in terms of credit requirements for graduation at UMD
    Args:
        graduation_plan(dict): dictionary of semester numbers matched with associated list of course objects
    Returns:
        credits_satisfaction(boolean): true or false depending on whether the plan satisfies the credit requirements for graduation
    '''
    #default flag for credit satisfaction
    credits_satisfaction = True
    #initializing output message that describes credit amount violations
    output_message = ""
    #initializing total credits for the enitre plan
    total_credits = 0

    #cycling through semester numbers and associated list of courses
    for semester, courses in graduation_plan.items():

        #initializing credit number for semester
        semester_credits = 0

        #cycling through the courses and adding their credit amount to the running totals for the semester and total plan
        for course in courses:

            semester_credits += course.credits
            total_credits += course.credits

        #the total credits for the semester is greater than the 18 credit maximum
        if semester_credits > 18:

            #graduation plan is invalid
            credits_satisfaction = False
            #describes how many credits over the max amount the semester is
            output_message += f"Semester {semester} is {semester_credits - 18} credits over the 18 credit maximum\n"

    #the total number of credits is less than the 120 credit minimum
    if total_credits < 120:

        #graduation plan is invalid
        credits_satisfaction = False
        #describes how many credits under the minimum amount the plan is
        output_message += f"Your graduation plan is {120 - total_credits} credits under the 120 credit minimum"

    #if the plan failed, print message describing where the plan fails the credit requirements
    if credits_satisfaction == False:
        print(output_message)

    return credits_satisfaction


def verify_genEd(graduation_plan):
    '''
    '''
    #these are the numbers used to assess requirement satisfaction for each genEd requirement
    #accurate as of fall 2023
    '''
    FSAW_required_credits = 3
    FSPW_required_credits = 3
    FSOC_required_credits = 3
    FSMA_required_credits = 3
    FSAR_required_credits = 3
    DSNL_required_credits = 1
    DSNS_and_DSNL_credits = 7
    DSHS_required_credits = 6
    DSHU_required_credits = 6
    DSSP_required_credits = 6
    SCIS_required_credits = 6
    DVUP_required_credits = 4
    '''

    #initializing the genEd credit counters for the plan before taking into account the "or" situation possibilites
    pre_or_FSAW_credit_count = 0
    pre_or_FSPW_credit_count = 0
    pre_or_FSOC_credit_count = 0
    pre_or_FSMA_credit_count = 0
    pre_or_FSAR_credit_count = 0
    pre_or_DSNL_credit_count = 0
    pre_or_DSNS_and_DSNL_credit_count = 0
    pre_or_DSHS_credit_count = 0
    pre_or_DSHU_credit_count = 0
    pre_or_DSSP_credit_count = 0
    pre_or_SCIS_credit_count = 0
    pre_or_DVUP_credit_count = 0

    #list for all of the "or" situations to go into
    or_queue = []
    #list of credits associated with the "or" situations (matching indexes)
    or_situations_credits = []

    #cycling through list of courses each semester
    for courses in graduation_plan.values():

        #cycling through each course in the list of courses
        for course in courses:
            
            #getting the credits and genEd satisfactions for the course
            credits = course.credits
            genEds = course.genEd

            #cycling through each genEd satisfaction in the list of genEd satisfactions
            for genEd in genEds:
                
                #if the genEd is a list that means it is an "or" situation and will be handled later
                if isinstance(genEd, list):

                    #store the "or" situation in the or_queue and move onto the next genEd in the list
                    or_queue.append(genEd)
                    or_situations_credits.append(credits)
                    continue
                
                #counters that get updated if the genEd matches the requirement satisfaction associated with the counter
                if genEd == "FSAW":
                    pre_or_FSAW_credit_count += credits
                elif genEd == "FSPW":
                    pre_or_FSPW_credit_count += credits
                elif genEd == "FSOC":
                    pre_or_FSOC_credit_count += credits
                elif genEd == "FSMA":
                    pre_or_FSMA_credit_count += credits
                elif genEd == "FSAR":
                    pre_or_FSAR_credit_count += credits
                elif genEd == "DSNL":
                    pre_or_DSNL_credit_count += credits
                    pre_or_DSNS_and_DSNL_credit_count += credits
                elif genEd == "DSNS":
                    pre_or_DSNS_and_DSNL_credit_count += credits
                elif genEd == "DSHS":
                    pre_or_DSHS_credit_count += credits
                elif genEd == "DSHU":
                    pre_or_DSHU_credit_count += credits
                elif genEd == "DSSP":
                    pre_or_DSSP_credit_count += credits
                elif genEd == "SCIS":
                    pre_or_SCIS_credit_count += credits
                elif genEd == "DVUP":
                    pre_or_DVUP_credit_count += credits

    #if theres no or situations then the "pre or situation" counts are the same counts as the total counts
    #so the genEd satisfaction checking can immediately begin
    if len(or_queue) == 0:

        FSAW_credit_count = pre_or_FSAW_credit_count
        FSPW_credit_count = pre_or_FSPW_credit_count
        FSOC_credit_count = pre_or_FSOC_credit_count
        FSMA_credit_count = pre_or_FSMA_credit_count
        FSAR_credit_count = pre_or_FSAR_credit_count
        DSNL_credit_count = pre_or_DSNL_credit_count
        DSNS_and_DSNL_credit_count = pre_or_DSNS_and_DSNL_credit_count
        DSHS_credit_count = pre_or_DSHS_credit_count
        DSHU_credit_count = pre_or_DSHU_credit_count
        DSSP_credit_count = pre_or_DSSP_credit_count
        SCIS_credit_count = pre_or_SCIS_credit_count
        DVUP_credit_count = pre_or_DVUP_credit_count

        #checking if each of the credit counts are at least at the required amounts 
        if (FSAW_credit_count >= 3 and FSPW_credit_count >= 3 and FSOC_credit_count >= 3 and FSMA_credit_count >= 3 and 
            FSAR_credit_count >= 3 and DSNL_credit_count >= 1 and DSNS_and_DSNL_credit_count >= 7 and DSHS_credit_count >= 6 and 
            DSHU_credit_count >= 6 and DSSP_credit_count >= 6 and FSAW_credit_count >= 6 and DVUP_credit_count >= 4):

            return True

    '''
    Heres the idea of whats happening below:

    Assuming that some of the courses had genEd satisfactions with "or" situations...
    The or_queue is going to be populated with lists of those genEds (the "or" situations)
    An "or" situation occurs when a course can count towards only one of a few selected genEd satisfactions
    Example: the genEd satisfactions for HIST200 are: DSHS or DSHU
    The code from prp.py handles that by putting the genEds separated by an "or" in a list
    So the genEd attribute for HIST200 would be: ['DSHS', 'DSHU']
    This is an example of what the or_queue could look like:
        [['DSHU', 'DVUP'], ['DSHU', 'DVCC'], ['DSHS', 'DVUP', 'DSHU']]
    
    There is an initialized list, or_combinations, that will house all of the possible combinations
    Of the genEds from the or_queue
    The genEds in the or_queue will get cycled through in order to build the combinations

    At the start, the or_combinations list is empty, so the genEds in the first "or" situation will serve as the first combinations
    *combinations are represented as lists
    Example of starting with the genEds for HIST200: [['DSHS'], ['DSHU']]
    Now there are combinations to branch off of

    For each of the remaining "or" situations in the or_queue, every combination in or_combinations...
    will need to be copied enough times to attach a different genEd onto each one
    Walkthrough:
        or_combinations --> [['DSHS'], ['DSHU']]
        next "or" situation: ['DSHU', 'DVUP']
        make new combinations by adding each genEd in the "or" situation to each existing combination
        new combinations: ['DSHS', 'DSHU']
                          ['DSHS', 'DVUP']
                          ['DSHU', 'DSHU']
                          ['DSHU', 'DVUP']
        add the new combinations to or_combinations and get rid of the previous combinations
        or_combinations --> [['DSHS', 'DSHU'], ['DSHS', 'DVUP'], ['DSHU', 'DSHU'], ['DSHU', 'DVUP']]
        *repreat process with all "or" situations
    It works with any amount of genEds in the "or" situation
    Ex: If you have 4 combinations and the next "or" situation has 3 genEds, then you would end up with 12 new combinations
    *It may seem like the amount of combinations can get very large very fast,
     but there aren't too many "or" situations and students don't need a whole lot of genEd classes anyway,
     so the combination list will most likely be small
    '''

    #initializing combinations list
    or_combinations = []

    #cycling through every or situation
    for or_situation in or_queue:

        #creating the first combinations if none exist
        if len(or_combinations) == 0:

            for genEd in or_situation:
                or_combinations.append([genEd])

        #branching off existing combinations
        else:

            #temporary list to store the new combinations in
            temp = []

            #cycling through each combination
            for combination in or_combinations:
                
                #the amount of genEds in the "or" situation is how many times the combination will be copied
                #each copy of the combination will have a different genEd from the "or" situation attached onto it
                #the newly created combinations will be added to the combination list
                for i in range(len(or_situation)):

                    #making a copy of the combination
                    new_combination = combination.copy()
                    #adding genEd onto the end of new_combination to make a new combination
                    new_combination.append(or_situation[i])
                    #adding the combination to the temporary list
                    temp.append(new_combination)

            #assigning the newly created combinations to or_combinations...
            #effectively getting rid of the original combinations and replacing them with the new ones
            or_combinations = temp

    #cycling through each of the combinations created from the "or" situations
    for combination in or_combinations:

        #resetting the index for the credits list after every iteration
        index = 0
        #resetting the credit counts
        FSAW_credit_count = pre_or_FSAW_credit_count
        FSPW_credit_count = pre_or_FSPW_credit_count
        FSOC_credit_count = pre_or_FSOC_credit_count
        FSMA_credit_count = pre_or_FSMA_credit_count
        FSAR_credit_count = pre_or_FSAR_credit_count
        DSNL_credit_count = pre_or_DSNL_credit_count
        DSNS_and_DSNL_credit_count = pre_or_DSNS_and_DSNL_credit_count
        DSHS_credit_count = pre_or_DSHS_credit_count
        DSHU_credit_count = pre_or_DSHU_credit_count
        DSSP_credit_count = pre_or_DSSP_credit_count
        SCIS_credit_count = pre_or_SCIS_credit_count
        DVUP_credit_count = pre_or_DVUP_credit_count

        #cycling through the genEds in the combination
        #assessing if pre_or totals combined with additions from the combination satisfy all of the genEd requirements
        for genEd in combination:

            if genEd == "FSAW":
                FSAW_credit_count += or_situations_credits[index]
            elif genEd == "FSPW":
                FSPW_credit_count += or_situations_credits[index]
            elif genEd == "FSOC":
                FSOC_credit_count += or_situations_credits[index]
            elif genEd == "FSMA":
                FSMA_credit_count += or_situations_credits[index]
            elif genEd == "FSAR":
                pre_or_FSAR_credit_count += or_situations_credits[index]
            elif genEd == "DSNL":
                DSNL_credit_count += or_situations_credits[index]
                DSNS_and_DSNL_credit_count += or_situations_credits[index]
            elif genEd == "DSNS":
                DSNS_and_DSNL_credit_count += or_situations_credits[index]
            elif genEd == "DSHS":
                DSHS_credit_count += or_situations_credits[index]
            elif genEd == "DSHU":
                DSHU_credit_count += or_situations_credits[index]
            elif genEd == "DSSP":
                DSSP_credit_count += or_situations_credits[index]
            elif genEd == "SCIS":
                SCIS_credit_count += or_situations_credits[index]
            elif genEd == "DVUP":
                DVUP_credit_count += or_situations_credits[index]
            
            #updating the index by 1
            index += 1

        #checking if this combination satisfies all genEd requirements
        if (FSAW_credit_count >= 3 and FSPW_credit_count >= 3 and FSOC_credit_count >= 3 and FSMA_credit_count >= 3 and 
            FSAR_credit_count >= 3 and DSNL_credit_count >= 1 and DSNS_and_DSNL_credit_count >= 7 and DSHS_credit_count >= 6 and 
            DSHU_credit_count >= 6 and DSSP_credit_count >= 6 and SCIS_credit_count >= 6 and DVUP_credit_count >= 4):

            #a combination was found that satisfies the requirements
            genEd_satisfaction = True
            return genEd_satisfaction
        
        else:
            #combination does not satisfy the requirements so move onto next combination
            continue

    #if the code below executes then that means none of the combinations satisfied all of the genEd requirements
    #the combination chosen to be applied to the graduation plan will be the last combination attempted
    genEd_satisfaction = False
    #initializing the message that describes how many credits of each genEd satisfaction the plan is missing (using last or combination)
    satisfaction_message = ""

    #these conditionals check if the amount of credits for each genEd is enough to satisy the requirement
    #if not then a phrase explaining how many credits are missing from requirement is added to the message

    if FSAW_credit_count < 3:
        satisfaction_message += f"{3 - FSAW_credit_count} more credits are needed to satisfy FSAW\n"

    if FSPW_credit_count < 3:
        satisfaction_message += f"{3 - FSPW_credit_count} more credits are needed to satisfy FSPW\n"

    if FSOC_credit_count < 3:
        satisfaction_message += f"{3 - FSOC_credit_count} more credits are needed to satisfy FSOC\n"

    if FSMA_credit_count < 3:
        satisfaction_message += f"{3 - FSMA_credit_count} more credits are needed to satisfy FSMA\n"

    if FSAR_credit_count < 3:
        satisfaction_message += f"{3 - FSAR_credit_count} more credits are needed to satisfy FSAR\n"

    if DSNL_credit_count < 1:
        satisfaction_message += "1 more credit is needed to satisfy DSNL\n"

    if DSNS_and_DSNL_credit_count < 7:
        satisfaction_message += f"{7 - DSNS_and_DSNL_credit_count} more credits are needed to satisfy DSNS/DSNL\n"

    if DSHS_credit_count < 6:
        satisfaction_message += f"{6 - DSHS_credit_count} more credits are needed to satisfy DSHS\n"

    if DSHU_credit_count < 6:
        satisfaction_message += f"{6 - DSHU_credit_count} more credits are needed to satisfy DSHU\n"

    if DSSP_credit_count < 6:
        satisfaction_message += f"{6 - DSSP_credit_count} more credits are needed to satisfy DSSP\n"

    if SCIS_credit_count < 6:
        satisfaction_message += f"{6 - SCIS_credit_count} more credits are needed to satisfy SCIS\n"

    if DVUP_credit_count < 4:
        satisfaction_message += f"{4 - DVUP_credit_count} more credits are needed to satisfy DVUP\n"

    #the code only gets here if the genEd_satisfaction is false
    #print out what went wrong (satisfaction_message)
    print(satisfaction_message)
    return genEd_satisfaction



def verify_prerequisite(graduation_plan):
    '''checks if the prerequisites for each course in a graduation plan have been fulfilled prior to the courses beeing taken
    Args:
        graduation_plan(dict): dictionary of semester numbers matched with associated list of course objects
    Returns:
        completed_prerequisites(boolean): condition that all prerequisites for all courses are fulfilled
    '''

    #default flag representing the condition that all prerequisites for the graduation plan are fulfilled
    completed_prerequisites = True

    credited_courses = []

    #initializing the output message that describes unfulfilled prerequistes
    output_message = ""
    
    #cycling through each semester of courses in order
    for semester, courses in graduation_plan.items():
        
        #if the semester is 0 then the courses have already been awarded credit because it is pre-UMD
        #so they can be added directly to the credited_courses list
        if semester == 0:

            for course in courses:
                credited_courses.append(course.name)
        
        #move onto the first semester at UMD
        continue

        #cycling through each course in the semester
        for course in courses:
            
            #getting list of prerequisites
            prereqs = course.prerequisites

            #cycling through each prerequisite
            for prereq in prereqs:
                
                #a sublist of prerequisites within the list of prerequisites is an "or" situation
                #this means that the prerequisite can be satisfied by any of the courses in the sublist of prerequisites
                #checking if prereq is a list type (meaning an "or" situation)
                if isinstance(prereq, list):

                    #default "or" situation flag
                    or_situation_fulfilled = False
                    
                    #cycling through each individual course in the "or" situation sublist
                    for individual_course in prereq:

                        #if the individual course is found in the credited course list
                        if individual_course in credited_courses:
                            
                            #flag the "or" situation as true
                            or_situation_fulfilled = True

                    #a true flag will skip over the remaining conditionals and continue onto the next prerequisite

                    #a false flag indicates none of the courses in the prerequisite sublist were fulfilled
                    if or_situation_fulfilled == False:

                        #the graduation plan did not pass the prerequisite verification
                        completed_prerequisites = False

                        #adding phrase, to the output message, describing which specific prerequisite was not fulfilled
                        output_message += f"No credit for {prereq} for the course: {course.name}\n"

                #if code gets inside else statement that means the prerequisite is a singular course
                else:
                    
                    #checking if prerequisite has not been completed (not in the credited course list)
                    if prereq not in credited_courses:
                    
                        #the graduation plan did not pass the prerequisite verification
                        completed_prerequisites = False

                        #adding phrase, to the output message, describing which specific prerequisite was not fulfilled
                        output_message += f"No credit for {prereq} for the course: {course.name}\n"

        
        #the courses taken in the current semester will be added to the credited course list
        for course in courses:

            #checking if the course already exists in the completed course_list to avoid duplicates
            if course.name not in credited_courses:

                credited_courses.append(course.name)

            #all associated crosslist courses for a course will also be added to the credited course list
            for crosslisted_course in course.crosslist:
                
                #checking if the crosslisted course already exists in the completed course_list to avoid duplicates
                if crosslisted_course not in credited_courses:

                    credited_courses.append(crosslisted_course)

    #printing output message if any prerequisites were not fulfilled
    if completed_prerequisites == False:

        print(output_message)

    return completed_prerequisites


def verify_corequisite(graduation_plan):
    '''checks if the prerequisites for each course in a graduation plan have been fulfilled prior to the courses beeing taken
    Args:
        graduation_plan(dict): dictionary of semester numbers matched with associated list of course objects
    Returns:
        completed_prerequisites(boolean): condition that all prerequisites for all courses are fulfilled
    '''
    
    #default flag for corequisite satisfaction
    corequisite_satisfaction = True
    #initializing output message
    output_message = ""
    #initializing list to house completed courses
    completed_courses = []

    #cycling through each semester number and course list in the plan
    for semester, courses in graduation_plan.items():

        #semester number of 0 means pre-UMD
        #those classes do not need to be chekced because they already happened
        #they automatically get added to the completed course list 
        if semester == 0:

            for course in courses:

                completed_courses.append(course.name)

        #for every semester after 0

        #initialize list of course names for the semester
        semester_course_names = []

        #cycle through each course in the list of courses and add the course names to the list of courses for the semester
        for course in courses:
            
            semester_course_names.append(course.name)

        #cycling through each course in the list of courses
        for course in courses:
            
            #getting the corequisites(list) for the course
            corequisites = course.corequisites

            #cycling through the corequisites in corequisites
            for corequisite in corequisites:
                '''
                a corequisite can be satisfied by either...
                taking the corequisite course at the same time as the course
                or already have completed the corequisite course
                '''
                #determining whether the corequisite satisfaction for the course is false by...
                #checking that corequisite course is not in the current semester course names list and also not in the completed course list
                if (corequisite not in semester_course_names) and (corequisite not in completed_courses):

                    corequisite_satisfaction = False
                    output_message += f"Need to be taking or have already completed {corequisite} in order to take {course.name}\n"
            
            #after cycling through all the courses in the semester...
            #add the courses to the completed course list
            completed_courses.append(course.name)

    #after all the courses in the plan have been cycled through

    #if the corequisite satisfaction got reassigned to false
    #something went wrong so print out what went wrong
    if corequisite_satisfaction == False:
        print(output_message)
    
    return corequisite_satisfaction


def verify_major_requirements(major, graduation_plan):
    '''checks if the graduation plan satisfies the major requirements for the given major
    Args:
        major(str): one of the select majors at UMD this program handles
        graduation_plan(dict): dictionary of semester numbers matched with associated list of course objects
    Returns:
        requirements_satisfied(boolean): condition that all major requirements are fulfilled
    '''

    #default return value
    requirements_satisfied = True
    #initializing output message that will describe what requirements are unsatisfied if any
    output_message = ""
    #changing the major to lowercase to give the user case flexibility when inputting major
    major = major.lower()

    if major == "information science":

        #retrieving the information science major requirement data
        from majorrequirementdata import information_science_data
        data = information_science_data
        #initializing the elective count that will need to get to 5 in order to satisfy the upper level major elective requirement
        elective_count = 0

        #cycling throuhg the list of courses each semester
        for courses in graduation_plan.values():

            #cycling through each course in a semester
            for course in courses:
                name = course.name
                #checking if the course name is in the list of core courses
                if name in data["core_courses"]:
                    #removing the core course from the list to facilitate checking later on
                    #effectively checking them off
                    data["core_courses"].remove(name)

                if name in data["electives"]:
                    elective_count += 1

        '''
        if all of the requirements are satisified:
        
            there will be no more core couses left in the core courses list
            because they would have been all "checked off" (removed)

            the upper level major elective count will be atleast 5
            because 5 is the minimum required upper level major elective courses to satisfy the requirement

        if there are courses left in the core courses list and/or the elective count is less than 5
        then not all major requirements were satisfied
        '''
        if len(data["core_courses"]) > 0:
            requirements_satisfied = False
            output_message += "Missing the following:\n"
            for course in data["core_courses"]:
                output_message += f"{course.name}\n"

        if elective_count < 5:
            requirements_satisfied = False
            output_message += f"Need {5 - elective_count} more upper level major electives"
    else:
        
        requirements_satisfied = False

    #if the requirements were not all satisfied then print out what went wrong
    if requirements_satisfied == False:
        print(output_message)

    return requirements_satisfied

         
print(verify_credits(graduation_plan))
print(verify_prerequisite(graduation_plan))
print(verify_corequisite(graduation_plan))
print(verify_genEd(graduation_plan))
print(verify_major_requirements("information science", graduation_plan))
