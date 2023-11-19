from tkinter import *
from misc import Course
from ver import verify_genEd, verify_prerequisite, verify_corequisite, verify_major_requirements, verify_credits

root = Tk()

# Setting background color for the root window
root.configure(bg="#8B6212")


graduation_plan = {}
current_semester = 0


#creating and positioning labels onto GUI
title_label = Label(root, text = "Welcome to the UMD College of Information Studies Degree Audit", bg="#43572E", fg="white")
title_label.grid(row = 0, column = 0)
majors_label = Label(root, text = "---Select Major---", bg="#43572E", fg="white")
majors_label.grid(row = 1, column = 0)

#assigning major to string variable
major = StringVar()
#setting default value to "Information Science"
major.set("Information Science")
major_label = Label(root, textvariable=major, bg="#43572E")
major_label.grid(row=2, column=0, sticky="nsew")



#creating dropdown menu and positioning onto GUI
#major will be assigned to whatever major is selected here
majors_menu = OptionMenu(root, major, "Information Science", "Technology and Information Design", 
                        "Social Data Science:- African American Studies", "Social Data Science:-Anthropology", "Social Data Science:-Economics", "Social Data Science:-Geographical Sciences & GIS", 
                        "Social Data Science:-Government & Politics & International Relations", "Social Data Science:-Psychology", 
                        "Social Data Science:-Sociology", "Social Data Science:-Public Health")
majors_menu.grid(row = 2, column = 0)
majors_menu.config(bg="#43572E", fg= "white")


semester_label = Label(root, text = "Courses Credited Before Starting UMD",bg="#43572E", fg="white")
semester_label.grid(row = 4, column = 0, sticky="nsew")
course_text_box = Text(root, height= 10, width = 50, bg="#0F2143", fg="white")
course_text_box.grid(row = 5, column = 0)

#command the occurs when the sumbit courses button is clicked
def submit_courses_click():
    '''creates course objects out of text from the course text box...
    and matches the courses to their associated semester number in the graduation plan
    *This function was designed as a void Tkinter command which takes no arguments and does not explicitly return anything
    Args:
        no arguments
    Returns:
        no explicit return (None)
    '''

    #initializing semester courses
    semester_courses = []

    #getting the list of course names from the textbox
    courses_text = course_text_box.get("1.0", END)

    #removing the whitespace characters after text course_text
    #creating a list of course names by splitting the text up by every line
    courses = courses_text.strip().split("\n")

    #getting rid of the text in the textbox to make room for the courses in the next semester
    course_text_box.delete(1.0, END)

    #creating a Course object out of every course name in the list (courses)
    for course in courses:

        semester_courses.append(Course(course))

    #since this function is just a regular button command, it doesn't take parameters or return anything...
    #and because current semester is an integer variable (primitive)...
    #we have to add global in front of the variable name to ensure it is refering to the global variable current_semester

    global current_semester

    #assigning the semester number to the list of course objects associated with the semester in the graduation plan
    graduation_plan[current_semester] = semester_courses

    #updating the semester number for next semester
    current_semester += 1
    semester_label.config(text = f"Semester {current_semester}")


def submit_graduation_plan_click():
    '''runs the graduation plan through a series of verification tests and displays the results using labels
    *This function was designed as a void Tkinter command which takes no arguments and does not explicitly return anything
    Args:
        no arguments
    Returns:
        no explicit return (None)
    '''
    #getting rid of the text in the textbox to make room for the courses in the next semester
    course_text_box.delete(1.0, END)
    submit_graduation_plan_button.destroy()
    submit_semester_button.destroy()
    course_text_box.destroy()
    semester_label.destroy()
    majors_menu.destroy()
    majors_label.destroy()
    title_label.destroy()

    #running the graduation plan through all of the verifications
    #storing the results and detials of the tests
    credits_evaluation, credit_details = verify_credits(graduation_plan)
    prereq_evaulation, prereq_details = verify_prerequisite(graduation_plan)
    genEd_Evaluation, genEd_details = verify_genEd(graduation_plan)
    corequisite_evaluation, coreq_details = verify_corequisite(graduation_plan)
    major_requirements_evaluation, major_requirement_details = verify_major_requirements(major.get(), graduation_plan)

    #checking if all evaluations are true
    if credits_evaluation and prereq_evaulation and genEd_Evaluation and corequisite_evaluation and major_requirements_evaluation:
        result = "Passed"

    #one or more of the evaluations were false
    else:
        result = "Failed"

    #create and positioning label displaying result
    overall_evaluation_label = Label(text = f"Result: {result}\n", bg="#43572E", fg="white")
    overall_evaluation_label.grid(row = 8, column = 0)

    #create and positioning label displaying details of fail
    if result == "Failed":

        #creating and positioning labels displaying the details of each verification test
        credits_evaluation_label = Label(text = f"Credit Requirements:\n{credit_details}", bg="#43572E", fg="white")
        credits_evaluation_label.grid(row = 9, column = 0)

        prereq_evaluation_label = Label(text = f"Prerequisite Satisfaction:\n{prereq_details}", bg="#43572E", fg="white")
        prereq_evaluation_label.grid(row = 10, column = 0)

        corequisite_evaluation_label = Label(text = f"Corequisite Satisfaction:\n{coreq_details}", bg="#43572E", fg="white")
        corequisite_evaluation_label.grid(row = 11, column = 0)

        genEd_Evaluation_label = Label(text = f"General Education Requirements:\n{genEd_details}",bg="#43572E", fg="white")
        genEd_Evaluation_label.grid(row = 12, column = 0)

        major_requirements_evaluation_label = Label(text = f"Major Requirements:\n{major_requirement_details}", bg="#43572E", fg="white")
        major_requirements_evaluation_label.grid(row = 13, column = 0)

#creating and positioning the submit courses button and the submit graduation plan button on the GUI
submit_semester_button = Button(text="Submit Courses", command=submit_courses_click)
submit_semester_button.grid(row=6, column=0)

submit_graduation_plan_button = Button(text="Submit Graduation Plan", command=submit_graduation_plan_click)
submit_graduation_plan_button.grid(row=7, column=0)




#runs the program
if __name__ == "__main__":
    root.mainloop()
