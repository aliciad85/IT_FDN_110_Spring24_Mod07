# ------------------------------------------------------------------------------------------ #
# Title: assignment07
# Desc: This assignment demonstrates using data classes with structured error handling
# Change Log:
#   aliciad, 05/27/2024, Created script
# ------------------------------------------------------------------------------------------ #

import json
from sys import exit

# Constants and global variables
MENU: str = """
    ---- Course Registration Program ----
    Select from the following menu:
    1. Register a student for the course
    2. Show current data
    3. Save data to file
    4. Exit the program
    -------------------------------------
"""
FILE_NAME: str = "enrollments.json"

menu_choice: str = ""
students: list = []


# Data layer / File processing block
class Person:
    """Defines parent class to house student's first and last names"""

    def __init__(self, student_first_name: str = "", student_last_name: str = ""):
        self.student_first_name = student_first_name
        self.student_last_name = student_last_name

    @property
    def student_first_name(self):
        return self.__student_first_name.title()
    
    @student_first_name.setter
    def student_first_name(self, value: str):
        if value.isalpha():
            self.__student_first_name = value
        else:
            raise ValueError("First name can't contain non-alphanumeric values.")
        
    @property
    def student_last_name(self):
        return self.__student_last_name.title()
    
    @student_last_name.setter
    def student_last_name(self, value: str):
        if value.isalpha():
            self.__student_last_name = value
        else:
            raise ValueError("Last name can't contain non-alphanumeric values.")

    def __str__(self):
        return f"{self.student_first_name},{self.student_last_name}"


class Student(Person):
    """Defines child class of Person and adds course name"""

    def __init__(self, student_first_name: str, student_last_name: str, course_name: str = ""):
        super().__init__(student_first_name=student_first_name, student_last_name=student_last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name
    
    @course_name.setter
    def course_name(self, value: str):
        if len(value) != 0:
            self.__course_name = value
        else:
            raise ValueError("Course name can't be empty.")
        
    def __str__(self):
        return f"{self.student_first_name},{self.student_last_name},{self.course_name}"


class FileProcessor:
    """Class to handle data storage and retrieval"""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """Read file and load to json and return list"""
        
        try:
            with open(file_name) as file:
                list_of_dict_data = json.load(file)
                for student in list_of_dict_data:
                    student_object: Student = Student(student_first_name=student["FirstName"],
                                                      student_last_name=student["LastName"],
                                                      course_name=student["CourseName"])
                    student_data.append(student_object)
        except FileNotFoundError as error_message:
            IO.output_error_messages("\nFile not found.", error_message)
        except Exception as error_message:
            IO.output_error_messages("\nUnknown Error. Please contact support. ", error_message)
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Write data to json file"""
        
        try:
            list_of_dict_data: list = []
            for student in student_data:
                student_json: dict = {"FirstName": student.student_first_name,
                                      "LastName": student.student_last_name,
                                      "CourseName": student.course_name
                                      }
                list_of_dict_data.append(student_json)
            with open(file_name, "w") as file:
                json.dump(list_of_dict_data, file)
        except FileNotFoundError as error_message:
            IO.output_error_messages("\nFile not found.", error_message)
        except Exception as error_message:
            IO.output_error_messages("\nUnknown Error. Please contact support.", error_message)


# Presentation Layer / IO block
class IO:
    """Class to handle user input and output"""
    
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Standardized error messages for program"""
        
        print(message, end="\n\n")
        if error is not None:
            print("--- Error Details ---")
            print(error, error.__doc__, type(error), sep="\n")
    
    @staticmethod
    def output_menu(menu: str):
        """Display menu options to user"""
        
        print(menu, end="\n\n")

    @staticmethod
    def input_menu_choice():
        """Process user's menu choice"""

        choice = "0"
        try:
            choice = input("Choose a menu option (1-4): ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Invalid option.  Please choose between 1-4.")
        except Exception as error_message:
            IO.output_error_messages("\n", error_message)
        return choice

    @staticmethod
    def input_student_data(student_data: list):
        """Process user's input and append to dictionary"""
        
        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Enter the course name: ")

            new_student = Student(student_first_name, student_last_name, course_name)

            student_data.append(new_student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as error_message:
            IO.output_error_messages("\nInvalid Entry.  See details below.", error_message)
        except Exception as error_message:
            IO.output_error_messages("\nUnknown Error. Please contact support.", error_message)
        return student_data

    @staticmethod
    def output_student_courses(student_data: list):
        """Output current data to user"""

        print("-"*50)
        print("The current data is: ")
        for student in student_data:
            print(student.student_first_name, student.student_last_name, student.course_name)
        print("-"*50, end="\n\n")


# Processing Layer / Execution block
if __name__ == "__main__":
    students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

    while True:
        IO.output_menu(MENU)
        menu_choice = IO.input_menu_choice()
        match menu_choice:
            case "1":
                IO.input_student_data(student_data=students)
            
            case "2":
                IO.output_student_courses(student_data=students)
            
            case "3":
                FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
                print("INFO: Registrations have been saved.")
            
            case "4":
                print("Program Ended.")
                exit()
