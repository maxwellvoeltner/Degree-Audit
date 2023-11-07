from misc import Course

graduation_plan = {
    1: [Course("INST101"), Course("ENES210"), Course("COMM107"), Course("BSCI135")],
    2: [Course("INST201"), Course("INST311"), Course("INST126"), Course("JOUR200"), Course("CCJS100")],
    3: [Course("INST326"), Course("INST314"), Course("MATH206"), Course("CMSC131"), Course("RDEV250")],
    4: [Course("INST335"), Course("INST327"), Course("MATH140"), Course("MATH141"), Course("INST362")],
    5: [Course("INST364"), Course("INST380"), Course("INST366"), Course("INST464"), Course("INST466")],
    6: [Course("MUSC140"), Course("INST346"), Course("ENES140"), Course("INST352"), Course("MUSC130")],
    7: [Course("INST490")]
}


def verify_genEd(graduation_plan):
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

    FSAW_credit_count = 0
    FSPW_credit_count = 0
    FSOC_credit_count = 0
    FSMA_credit_count = 0
    FSAR_credit_count = 0
    DSNL_credit_count = 0
    DSNS_and_DSNL_credit_count = 0
    DSHS_credit_count = 0
    DSHU_credit_count = 0
    DSSP_credit_count = 0
    SCIS_credit_count = 0
    DVUP_credit_count = 0

    for semester, courses in graduation_plan.items():

        for course in courses:
            
            credits = course.credits
            genEds = course.genEd

            for genEd in genEds:
                
                if genEd == "FSAW":
                    FSAW_credit_count += credits
                elif genEd == "FSPW":
                    FSPW_credit_count += credits
                elif genEd == "FSOC":
                    FSOC_credit_count += credits
                elif genEd == "FSMA":
                    FSMA_credit_count += credits
                elif genEd == "FSAR":
                    FSAR_credit_count += credits
                elif genEd == "DSNL":
                    DSNL_credit_count += credits
                    DSNS_and_DSNL_credit_count += credits
                elif genEd == "DSNS":
                    DSNS_and_DSNL_credit_count += credits
                elif genEd == "DSHS":
                    DSHS_credit_count += credits
                elif genEd == "DSHU":
                    DSHU_credit_count += credits
                elif genEd == "DSSP":
                    DSSP_credit_count += credits
                elif genEd == "SCIS":
                    SCIS_credit_count += credits
                elif genEd == "DVUP":
                    DVUP_credit_count += credits

    genEd_satisfaction = True
    satisfaction_message = ""

    if FSAW_credit_count < 3:
        genEd_satisfaction = False
        satisfaction_message += f"{3 - FSAW_credit_count} more credits are needed to satisfy FSAW\n"

    if FSPW_credit_count < 3:
        genEd_satisfaction = False
        satisfaction_message += f"{3 - FSPW_credit_count} more credits are needed to satisfy FSPW\n"

    if FSOC_credit_count < 3:
        genEd_satisfaction = False
        satisfaction_message += f"{3 - FSOC_credit_count} more credits are needed to satisfy FSOC\n"

    if FSMA_credit_count < 3:
        genEd_satisfaction = False
        satisfaction_message += f"{3 - FSMA_credit_count} more credits are needed to satisfy FSMA\n"

    if FSAR_credit_count < 3:
        genEd_satisfaction = False
        satisfaction_message += f"{3 - FSAR_credit_count} more credits are needed to satisfy FSAR\n"

    if DSNL_credit_count < 1:
        genEd_satisfaction = False
        satisfaction_message += "1 more credit is needed to satisfy DSNL\n"

    if DSNS_and_DSNL_credit_count < 3:
        genEd_satisfaction = False
        satisfaction_message += f"{7 - DSNS_and_DSNL_credit_count} more credits are needed to satisfy DSNS/DSNL\n"

    if DSHS_credit_count < 6:
        genEd_satisfaction = False
        satisfaction_message += f"{6 - DSHS_credit_count} more credits are needed to satisfy DSHS\n"

    if DSHU_credit_count < 6:
        genEd_satisfaction = False
        satisfaction_message += f"{6 - DSHU_credit_count} more credits are needed to satisfy FSMA\n"

    if DSSP_credit_count < 6:
        genEd_satisfaction = False
        satisfaction_message += f"{6 - DSSP_credit_count} more credits are needed to satisfy DSSP\n"

    if SCIS_credit_count < 6:
        genEd_satisfaction = False
        satisfaction_message += f"{6 - SCIS_credit_count} more credits are needed to satisfy SCIS\n"

    if DVUP_credit_count < 4:
        genEd_satisfaction = False
        satisfaction_message += f"{4 - DVUP_credit_count} more credits are needed to satisfy DVUP\n"

    
    if genEd_satisfaction == True:
        satisfaction_message = "All General Education Requirements Satisfied"

    print(satisfaction_message)

    return genEd_satisfaction


#verify_genEd(graduation_plan)


credited_courses = ["MATH115", "PSYC100", "MATH140", "STAT100"]

def verify_prerequisite(graduation_plan, credited_courses):
    '''checks if the prerequisites for each course in a graduation plan have been fulfilled prior to the courses beeing taken
    Args:
        graduation_plan(dict): dictionary of semester numbers matched with associated list of course objects
        credited_courses(list): list of course names that credit has been awarded for
    Returns:
        completed_prerequisites(boolean): condition that all prerequisites for all courses are fulfilled
    '''

    #default flag representing the condition that all prerequisites for the graduation plan are fulfilled
    completed_prerequisites = True

    #initializing the output message that describes unfulfilled prerequistes
    output_message = ""
    
    #cycling through each semester of courses in order
    for semester, courses in graduation_plan.items():

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


print(verify_prerequisite(graduation_plan, credited_courses))