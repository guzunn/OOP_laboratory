from datetime import datetime
import  pickle

DOB_FORMAT = "%d-%m-%Y"


class Student:
    def __init__(self, first_name, last_name, email, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.enrollment_date = datetime.now().date()
        self.date_of_birth = datetime.strptime(date_of_birth, DOB_FORMAT)
        self.faculty = None

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}, Enrolled: {self.enrollment_date}, Birthday: {self.date_of_birth}"


class Faculty:
    def __init__(self, name, abbreviation, study_field):
        self.name = name
        self.abbreviation = abbreviation
        self.study_field = study_field
        self.students = []
        self.graduates = []

    def create_student(self, student):
        self.students.append(student)
        student.faculty = self
        Logger.log_operation(f"Created student: {student.first_name} {student.last_name} in {self.abbreviation}")

    def graduate_student(self, student):
        if student in self.students:
            self.students.remove(student)
            self.graduates.append(student)
            Logger.log_operation(f"Graduated student: {student.first_name} {student.last_name} from {self.abbreviation}")
            return f"{student} has graduated"
        else:
            Logger.log_operation(f"Failed to graduate. {student} is not enrolled in {self.abbreviation}")
            return f"{student} is not enrolled in this faculty"

    def enrolled_students(self):
        print(f"Currently enrolled at {self.abbreviation}")
        for student in self.students:
            print(f"{student.first_name} {student.last_name}")

    def graduated(self):
        print(f"Graduated students from {self.abbreviation}")
        for student in self.graduates:
            print(f"{student.first_name} {student.last_name}")

    def is_enrolled(self, student):
        return student in self.students

    def student_by_email(self, email):
        for student in self.students:
            if student.email == email:
                return student
        return s



    def __repr__(self):
        return f"{self.abbreviation} {self.name}"


class University:
    def __init__(self):
        self.faculties = []

    def create_faculty(self, faculty):
        self.faculties.append(faculty)

    def faculty_by_student_email(self, email):
        for faculty in self.faculties:
            for student in faculty.students:
                if student.email == email:
                    return faculty
        return faculty


    def all_faculties(self):
        return self.faculties

    def faculty_by_abbreviation(self, abbreviation):
        for faculty in self.faculties:
            if faculty.abbreviation == abbreviation:
                return faculty
        return None

    def faculties_by_study_field(self, study_field):
        return [faculty for faculty in self.faculties if faculty.study_field == study_field]


class SaveManager:
    SAVE_FILE = 'student_management_state.pkl'

    @staticmethod
    def save_state(university):
        with open(SaveManager.SAVE_FILE, 'wb') as file:
            pickle.dump(university, file)

    @staticmethod
    def load_state():
        try:
            with open(SaveManager.SAVE_FILE, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return University()
class Logger:
    LOG_FILE = 'operation_logs.txt'

    @staticmethod
    def log_operation(operation_description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {operation_description}\n"
        with open(Logger.LOG_FILE, 'a') as log_file:
            log_file.write(log_entry)





if __name__ == '__main__':
    UTM = SaveManager.load_state()

    while True:
        print("Welcome to TUM's student management system!")
        print("\nWhat do you want to do?")
        print('g - General operations\nf - Faculty operations \ns - Student operations \nq - Quit program')

        choice = input("Your input: ")

        # General operations
        if choice.lower() == 'g':
            print("\nGeneral operations \nWhat do you want to do?")
            choice = input("nf/<faculty name>/<faculty abbreviation>/<field of study> - create faculty"
                           "\nss/<student email> - search student and show faculty"
                           "\ndf - display faculties"
                           "\ndf/<field> - display all faculties of a field"
                           "\n\n\nb - Back"
                           "\nq - Quit program"
                           "\n\n\nYour input: ")
            if choice[0:2] == 'nf':
                data = choice[3:].split("/")
                name, abbreviation, study_field = data
                faculty = Faculty(name, abbreviation, study_field)
                UTM.create_faculty(faculty)
                Logger.log_operation(f"Created faculty: {faculty.name} ({faculty.abbreviation})")
            elif choice[0:2] == 'ss':
                data = choice[3:]
                faculty = UTM.faculty_by_student_email(data)
                if faculty:
                    print(f"Student with email {data} is enrolled in {faculty}")
                else:
                    print(f"No such student with email {data}")
            elif choice[0:2] == 'df':
                print(UTM.all_faculties())
            elif choice[0:3] == 'df/':
                data = choice[3:]
                faculties = UTM.faculties_by_study_field(data)
                print(f"Faculties in the field {data}: {faculties}")

        # Faculty operations
        elif choice.lower() == 'f':
            print("\nFaculty operations \nWhat do you want to do?")
            choice = input(
                "\nns/<faculty abbreviation>/<first name>/<last name>/<email>/<day>/<month>/<year> - create student"
                "\ngs/<email> - graduate student"
                "\nds/<faculty abbreviation> - display enrolled students"
                "\ndg/<faculty abbreviation> - display graduated students"
                "\nbf/<faculty abbreviation>/<email> - check if student belongs to faculty"
                "\n\n\nb - Back"
                "\nq - Quit program"
                "\n\n\nYour input: ")
            if choice[0:2] == 'ns':
                data = choice[3:].split("/")
                abrev, fn, ln, email, d, m, y = data
                birthday = f'{d}-{m}-{y}'
                new_student = Student(fn, ln, email, birthday)
                faculty = UTM.faculty_by_abbreviation(abrev)
                if faculty:
                    faculty.create_student(new_student)
                else:
                    print(f"No such faculty with abbreviation {abrev}")
                Logger.log_operation(f"Created student: {new_student.first_name} {new_student.last_name} in {faculty.abbreviation}")
            elif choice[0:2] == 'gs':
                data = choice[3:].split("/")
                faculty = UTM.faculty_by_student_email(data)
                student = faculty.student_by_email(data)
                if student:
                    print(f"{faculty.graduate_student(student)}")
                else:
                    print(f"No such student with email {data}")
                Logger.log_operation(f"Failed to graduate student: {data}. Student not present or not enrolled.")
            elif choice[0:2] == 'ds':
                data = choice[3:]
                faculty = UTM.faculty_by_abbreviation(data)
                if faculty:
                    faculty.enrolled_students()
                else:
                    print(f"No such faculty with abbreviation {data}")
                Logger.log_operation(f"Displayed enrolled students for {faculty.abbreviation}")
            elif choice[0:2] == 'dg':
                data = choice[3:]
                faculty = UTM.faculty_by_abbreviation(data)
                if faculty:
                    faculty.graduated()
                else:
                    print(f"No such faculty with abbreviation {data}")
            elif choice[0:2] == 'bf':
                data = choice[3:].split("/")
                abrev, email = data
                faculty = UTM.faculty_by_abbreviation(abrev)
                if faculty:
                    student = faculty.student_by_email(email)
                    if student:
                        print(f"{student} is enrolled in {faculty}")
                    else:
                        print(f"No such student with email {email}")
                else:
                    print(f"No such faculty with abbreviation {abrev}")


        elif choice.lower() == "s":
            print("\nStudent operations \nWhat do you want to do?")
            choice = input("\nns/<first_name>/<last_name>/<email>/<date_of_birth> - create student"
                           "\n\n\nb - Back"
                           "\nq - Quit program"
                           "\n\n\nYour input: ")
            if choice[0:2] == 'ns':
                data = choice[3:].split("/")
                fn, ln, email, dob = data
                new_student = Student(fn, ln, email, dob)

        # Quit program
        elif choice.lower() == 'q':
            SaveManager.save_state(UTM)
            Logger.log_operation("Quit program")
            break
