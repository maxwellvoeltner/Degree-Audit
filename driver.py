from misc import Course

plan_complete = False
graduation_plan = {}
current_semester = 0

while plan_complete == False:

    current_semester += 1
    print("Semester " + str(current_semester) + ":")

    semester_complete = False
    semester_courses = []
    
    while semester_complete == False:
        course = input("Enter Course: \n")

        if course == "plan done":
            plan_complete = True
            semester_complete = True
        elif course == "semester done":
            semester_complete = True
        else:
            semester_courses.append(course)

    graduation_plan[current_semester] = semester_courses

updated_plan = {}

for semester, courses in graduation_plan.items():

    course_list = []
    for course in courses:

        course = Course(course)
        course_list.append(course)

    updated_plan[semester] = course_list

for semester, courses in updated_plan.items():
    for course in courses:
        print("name:", course.name)
        print("credits:", course.credits)
        print("prerequisites:", course.prerequisites)
        print("corequisite:", course.corequisites)
        print("crosslist:", course.crosslist)
        print("genEd:", course.genEd)
    