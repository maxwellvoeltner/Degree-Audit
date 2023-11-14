from misc import Course
from ver import verify_genEd, verify_prerequisite, verify_corequisite, verify_major_requirements, verify_credits

plan_complete = False
graduation_plan = {}
current_semester = -1
while plan_complete == False:

    current_semester += 1
    print(f"Semester {current_semester}:")

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
            semester_courses.append(Course(course))

    graduation_plan[current_semester] = semester_courses

print("Satisfies credit requirements:", verify_credits(graduation_plan))
print("Satisifies prerequisite requirements:", verify_prerequisite(graduation_plan))
print("Satisfies general Education requirements:", verify_genEd(graduation_plan))
print("Satisfies corequisite requirements:", verify_corequisite(graduation_plan))
print("Satisfies major requirements:", verify_major_requirements(graduation_plan))
