import streamlit as st
import psycopg2
import pandas as pd
from streamlit_option_menu import option_menu

# Database connection
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="assignment",
            user="postgres",
            password="1513",
            host="localhost"
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        st.error("Error connecting to the database.")
        return None


# Migration - Create tables if they don't exist
def create_tables(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS classroom (
                building VARCHAR(50),
                room_number VARCHAR(10),
                capacity INT,
                PRIMARY KEY (building, room_number)
            );

            CREATE TABLE IF NOT EXISTS department (
                dept_name VARCHAR(50),
                building VARCHAR(50),
                budget INT,
                PRIMARY KEY (dept_name)
            );

            CREATE TABLE IF NOT EXISTS course (
                course_id VARCHAR(10),
                title VARCHAR(100),
                dept_name VARCHAR(50),
                credits INT,
                PRIMARY KEY (course_id),
                FOREIGN KEY (dept_name) REFERENCES department(dept_name)
            );

            CREATE TABLE instructor (
                ID INT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                dept_name VARCHAR(50) NOT NULL,
                salary INT CHECK (salary >= 0),
                FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE CASCADE
            );


            CREATE TABLE IF NOT EXISTS section (
                course_id VARCHAR(10),
                sec_id VARCHAR(10),
                semester VARCHAR(10),
                year INT,
                building VARCHAR(50),
                room_number VARCHAR(10),
                time_slot_id VARCHAR(5),
                PRIMARY KEY (course_id, sec_id, semester, year),
                FOREIGN KEY (course_id) REFERENCES course(course_id),
                FOREIGN KEY (building, room_number) REFERENCES classroom(building, room_number)
            );

            CREATE TABLE IF NOT EXISTS teaches (
                ID INT,
                course_id VARCHAR(10),
                sec_id VARCHAR(10),
                semester VARCHAR(10),
                year INT,
                PRIMARY KEY (ID, course_id, sec_id, semester, year),
                FOREIGN KEY (ID) REFERENCES instructor(ID),
                FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year)
            );

            CREATE TABLE IF NOT EXISTS student (
                ID VARCHAR(10),
                name VARCHAR(50),
                dept_name VARCHAR(50),
                tot_cred INT,
                PRIMARY KEY (ID),
                FOREIGN KEY (dept_name) REFERENCES department(dept_name)
            );

            CREATE TABLE IF NOT EXISTS takes (
                ID VARCHAR(10),
                course_id VARCHAR(10),
                sec_id VARCHAR(10),
                semester VARCHAR(10),
                year INT,
                grade CHAR(2),
                PRIMARY KEY (ID, course_id, sec_id, semester, year),
                FOREIGN KEY (ID) REFERENCES student(ID),
                FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year)
            );

            CREATE TABLE IF NOT EXISTS advisor (
                s_ID VARCHAR(10),
                i_ID INT,
                PRIMARY KEY (s_ID),
                FOREIGN KEY (s_ID) REFERENCES student(ID),
                FOREIGN KEY (i_ID) REFERENCES instructor(ID)
            );

            CREATE TABLE time_slot (
    time_slot_id VARCHAR(5),
    day VARCHAR(1),
    start_hour INT,
    start_minute INT,
    end_hour INT,
    end_minute INT,
    PRIMARY KEY (time_slot_id, day, start_hour, start_minute)
);

            CREATE TABLE IF NOT EXISTS prereq (
                course_id VARCHAR(10),
                prereq_id VARCHAR(10),
                PRIMARY KEY (course_id, prereq_id),
                FOREIGN KEY (course_id) REFERENCES course(course_id),
                FOREIGN KEY (prereq_id) REFERENCES course(course_id)
            );
            """)
            conn.commit()
            st.success("Tables created successfully.")
    except Exception as e:
        st.error(f"Error creating tables: {e}")

# Seed data
def seed_data(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                -- Delete existing data
                DELETE FROM prereq;
                DELETE FROM time_slot;
                DELETE FROM advisor;
                DELETE FROM takes;
                DELETE FROM student;
                DELETE FROM teaches;
                DELETE FROM section;
                DELETE FROM instructor;
                DELETE FROM course;
                DELETE FROM department;
                DELETE FROM classroom;

                -- Insert Classroom data
                INSERT INTO classroom VALUES 
                    ('Packard', '101', '500'),
                    ('Painter', '514', '10'),
                    ('Taylor', '3128', '70'),
                    ('Watson', '100', '30'),
                    ('Watson', '120', '50');

                -- Insert Department data
                INSERT INTO department VALUES 
                    ('Biology', 'Watson', '90000'),
                    ('Comp. Sci.', 'Taylor', '100000'),
                    ('Elec. Eng.', 'Taylor', '85000'),
                    ('Finance', 'Painter', '120000'),
                    ('History', 'Painter', '50000'),
                    ('Music', 'Packard', '80000'),
                    ('Physics', 'Watson', '70000');

                -- Insert Course data
                INSERT INTO course VALUES 
                    ('BIO-101', 'Intro. to Biology', 'Biology', '4'),
                    ('BIO-301', 'Genetics', 'Biology', '4'),
                    ('BIO-399', 'Computational Biology', 'Biology', '3'),
                    ('CS-101', 'Intro. to Computer Science', 'Comp. Sci.', '4'),
                    ('CS-190', 'Game Design', 'Comp. Sci.', '4'),
                    ('CS-315', 'Robotics', 'Comp. Sci.', '3'),
                    ('CS-319', 'Image Processing', 'Comp. Sci.', '3'),
                    ('CS-347', 'Database System Concepts', 'Comp. Sci.', '3'),
                    ('EE-181', 'Intro. to Digital Systems', 'Elec. Eng.', '3'),
                    ('FIN-201', 'Investment Banking', 'Finance', '3'),
                    ('HIS-351', 'World History', 'History', '3'),
                    ('MU-199', 'Music Video Production', 'Music', '3'),
                    ('PHY-101', 'Physical Principles', 'Physics', '4');

                -- Insert Instructor data
                INSERT INTO instructor VALUES 
                    ('10101', 'Srinivasan', 'Comp. Sci.', '65000'),
                    ('12121', 'Wu', 'Finance', '90000'),
                    ('15151', 'Mozart', 'Music', '40000'),
                    ('22222', 'Einstein', 'Physics', '95000'),
                    ('32343', 'El Said', 'History', '60000'),
                    ('33456', 'Gold', 'Physics', '87000'),
                    ('45565', 'Katz', 'Comp. Sci.', '75000'),
                    ('58583', 'Califieri', 'History', '62000'),
                    ('76543', 'Singh', 'Finance', '80000'),
                    ('76766', 'Crick', 'Biology', '72000'),
                    ('83821', 'Brandt', 'Comp. Sci.', '92000'),
                    ('98345', 'Kim', 'Elec. Eng.', '80000');

                -- Insert Section data
                INSERT INTO section VALUES 
                    ('BIO-101', '1', 'Summer', '2017', 'Painter', '514', 'B'),
                    ('BIO-301', '1', 'Summer', '2018', 'Painter', '514', 'A'),
                    ('CS-101', '1', 'Fall', '2017', 'Packard', '101', 'H'),
                    ('CS-101', '1', 'Spring', '2018', 'Packard', '101', 'F'),
                    ('CS-190', '1', 'Spring', '2017', 'Taylor', '3128', 'E'),
                    ('CS-190', '2', 'Spring', '2017', 'Taylor', '3128', 'A'),
                    ('CS-315', '1', 'Spring', '2018', 'Watson', '120', 'D'),
                    ('CS-319', '1', 'Spring', '2018', 'Watson', '100', 'B'),
                    ('CS-319', '2', 'Spring', '2018', 'Taylor', '3128', 'C'),
                    ('CS-347', '1', 'Fall', '2017', 'Taylor', '3128', 'A'),
                    ('EE-181', '1', 'Spring', '2017', 'Taylor', '3128', 'C'),
                    ('FIN-201', '1', 'Spring', '2018', 'Packard', '101', 'B'),
                    ('HIS-351', '1', 'Spring', '2018', 'Painter', '514', 'C'),
                    ('MU-199', '1', 'Spring', '2018', 'Packard', '101', 'D'),
                    ('PHY-101', '1', 'Fall', '2017', 'Watson', '100', 'A');

                -- Insert Teaches data
                INSERT INTO teaches VALUES 
                    ('10101', 'CS-101', '1', 'Fall', '2017'),
                    ('10101', 'CS-315', '1', 'Spring', '2018'),
                    ('10101', 'CS-347', '1', 'Fall', '2017'),
                    ('12121', 'FIN-201', '1', 'Spring', '2018'),
                    ('15151', 'MU-199', '1', 'Spring', '2018'),
                    ('22222', 'PHY-101', '1', 'Fall', '2017'),
                    ('32343', 'HIS-351', '1', 'Spring', '2018'),
                    ('45565', 'CS-101', '1', 'Spring', '2018'),
                    ('45565', 'CS-319', '1', 'Spring', '2018'),
                    ('76766', 'BIO-101', '1', 'Summer', '2017'),
                    ('76766', 'BIO-301', '1', 'Summer', '2018'),
                    ('83821', 'CS-190', '1', 'Spring', '2017'),
                    ('83821', 'CS-190', '2', 'Spring', '2017'),
                    ('83821', 'CS-319', '2', 'Spring', '2018'),
                    ('98345', 'EE-181', '1', 'Spring', '2017');

                -- Insert Student data
                INSERT INTO student VALUES 
                    ('00128', 'Zhang', 'Comp. Sci.', '102'),
                    ('12345', 'Shankar', 'Comp. Sci.', '32'),
                    ('19991', 'Brandt', 'History', '80'),
                    ('23121', 'Chavez', 'Finance', '110'),
                    ('44553', 'Peltier', 'Physics', '56'),
                    ('45678', 'Levy', 'Physics', '46'),
                    ('54321', 'Williams', 'Comp. Sci.', '54'),
                    ('55739', 'Sanchez', 'Music', '38'),
                    ('70557', 'Snow', 'Physics', '0'),
                    ('76543', 'Brown', 'Comp. Sci.', '58'),
                    ('76653', 'Aoi', 'Elec. Eng.', '60'),
                    ('98765', 'Bourikas', 'Elec. Eng.', '98'),
                    ('98988', 'Tanaka', 'Biology', '120');

                -- Insert Takes data
                INSERT INTO takes VALUES 
                    ('00128', 'CS-101', '1', 'Fall', '2017', 'A'),
                    ('00128', 'CS-347', '1', 'Fall', '2017', 'A-'),
                    ('12345', 'CS-101', '1', 'Fall', '2017', 'C'),
                    ('12345', 'CS-190', '2', 'Spring', '2017', 'A'),
                    ('12345', 'CS-315', '1', 'Spring', '2018', 'A'),
                    ('12345', 'CS-347', '1', 'Fall', '2017', 'A'),
                    ('19991', 'HIS-351', '1', 'Spring', '2018', 'B'),
                    ('23121', 'FIN-201', '1', 'Spring', '2018', 'C+'),
                    ('44553', 'PHY-101', '1', 'Fall', '2017', 'B-'),
                    ('45678', 'CS-101', '1', 'Fall', '2017', 'F'),
                    ('45678', 'CS-101', '1', 'Spring', '2018', 'B+'),
                    ('45678', 'CS-319', '1', 'Spring', '2018', 'B'),
                    ('54321', 'CS-101', '1', 'Fall', '2017', 'A-'),
                    ('54321', 'CS-190', '2', 'Spring', '2017', 'B+'),
                    ('55739', 'MU-199', '1', 'Spring', '2018', 'A-'),
                    ('76543', 'CS-101', '1', 'Fall', '2017', 'A'),
                    ('76653', 'EE-181', '1', 'Spring', '2017', 'C'),
                    ('98765', 'EE-181', '1', 'Spring', '2017', 'A'),
                    ('98988', 'BIO-101', '1', 'Summer', '2017', 'A');

                -- Insert Advisor data
                INSERT INTO advisor VALUES 
                    ('00128', '45565'),
                    ('12345', '10101'),
                    ('23121', '76543'),
                    ('44553', '22222'),
                    ('45678', '22222'),
                    ('76543', '10101'),
                    ('76653', '98345'),
                    ('98765', '98345'),
                    ('98988', '76766');

                -- Insert Time_Slot data
                insert into time_slot values ('A', 'M', '8', '0', '8', '50');
insert into time_slot values ('A', 'W', '8', '0', '8', '50');
insert into time_slot values ('A', 'F', '8', '0', '8', '50');
insert into time_slot values ('B', 'M', '9', '0', '9', '50');
insert into time_slot values ('B', 'W', '9', '0', '9', '50');
insert into time_slot values ('B', 'F', '9', '0', '9', '50');
insert into time_slot values ('C', 'M', '11', '0', '11', '50');
insert into time_slot values ('C', 'W', '11', '0', '11', '50');
insert into time_slot values ('C', 'F', '11', '0', '11', '50');
insert into time_slot values ('D', 'M', '13', '0', '13', '50');
insert into time_slot values ('D', 'W', '13', '0', '13', '50');
insert into time_slot values ('D', 'F', '13', '0', '13', '50');
insert into time_slot values ('E', 'T', '10', '30', '11', '45 ');
insert into time_slot values ('E', 'R', '10', '30', '11', '45 ');
insert into time_slot values ('F', 'T', '14', '30', '15', '45 ');
insert into time_slot values ('F', 'R', '14', '30', '15', '45 ');
insert into time_slot values ('G', 'M', '16', '0', '16', '50');
insert into time_slot values ('G', 'W', '16', '0', '16', '50');
insert into time_slot values ('G', 'F', '16', '0', '16', '50');
insert into time_slot values ('H', 'W', '10', '0', '12', '30');

                -- Insert Prereq data
                INSERT INTO prereq VALUES 
                    ('BIO-301', 'BIO-101'),
                    ('BIO-399', 'BIO-101'),
                    ('CS-190', 'CS-101'),
                    ('CS-315', 'CS-101'),
                    ('CS-319', 'CS-101'),
                    ('CS-347', 'CS-101');
            """)
            conn.commit()
            print("Data seeding complete!")
    except Exception as e:
        conn.rollback()
        print(f"Error seeding data: {e}")
# View data functions
def view_courses(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM course")
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error retrieving courses: {e}")
        return []


def view_students(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ID, name, tot_cred, dept_name FROM student")
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error retrieving students: {e}")
        return []
#function to check whether a student has completed the required prerequisites for a course
def check_prerequisites(conn, student_id, course_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT prereq_id
                FROM prereq
                WHERE course_id = %s
            """, (course_id,))
            prereqs = cursor.fetchall()

            # Check if the student has completed all prerequisites
            for prereq in prereqs:
                cursor.execute("""
                    SELECT grade
                    FROM takes
                    WHERE ID = %s AND course_id = %s
                """, (student_id, prereq[0]))
                grade = cursor.fetchone()
                if grade is None or grade[0] == 'F':  # Assuming 'F' means not passed
                    return False
            return True
    except Exception as e:
        st.error(f"Error checking prerequisites: {e}")
        return False



def view_instructors(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Instructors")
        return cursor.fetchall()

def view_student_advisors(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT Students.name AS student, Instructors.name AS advisor
            FROM StudentAdvisors
            JOIN Students ON StudentAdvisors.student_id = Students.student_id
            JOIN Instructors ON StudentAdvisors.instructor_id = Instructors.instructor_id
        """)
        return cursor.fetchall()

# Detailed view of a course
def course_details(conn, course_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT Courses.name, Courses.credits, Departments.name AS department, Instructors.name AS instructor
            FROM Courses 
            JOIN Departments ON Courses.department_id = Departments.department_id
            LEFT JOIN CourseSections ON Courses.course_id = CourseSections.course_id
            LEFT JOIN Instructors ON CourseSections.instructor_id = Instructors.instructor_id
            WHERE Courses.course_id = %s
        """, (course_id,))
        course = cursor.fetchone()

        cursor.execute("""
            SELECT Students.name 
            FROM Enrollments 
            JOIN Students ON Enrollments.student_id = Students.student_id 
            WHERE Enrollments.course_id = %s
        """, (course_id,))
        students = cursor.fetchall()

        return course, students

def section_exists(conn, course_id, sec_id, semester, year):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM section 
            WHERE course_id = %s AND sec_id = %s AND semester = %s AND year = %s
        """, (course_id, sec_id, semester, year))
        count = cursor.fetchone()[0]
    return count > 0

def assign_instructor_to_course(conn, instructor_id, course_id, sec_id, semester, year):
    try:
        # Check if the section exists
        if not section_exists(conn, course_id, sec_id, semester, year):
            st.error("The specified section does not exist. Please check the course ID, section ID, semester, and year.")
            return
        
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO teaches (ID, course_id, sec_id, semester, year) 
                VALUES (%s, %s, %s, %s, %s)
            """, (instructor_id, course_id, sec_id, semester, year))
            conn.commit()
            st.success("Instructor assigned to course successfully.")
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error assigning instructor to course: {e}")


def add_student(conn, student_id, name, dept_name, tot_cred):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO student (ID, name, dept_name, tot_cred) VALUES (%s, %s, %s, %s)",
                (student_id, name, dept_name, tot_cred)
            )
            conn.commit()
            st.success("Student added successfully!")
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error adding student: {e}")


def add_instructor(conn, name, dept_name, salary):
    try:
        with conn.cursor() as cursor:
            # Ensure the instructor ID is unique by finding the maximum existing ID and adding 1
            cursor.execute("SELECT MAX(ID) FROM instructor")
            max_id = cursor.fetchone()[0]
            new_id = max_id + 1 if max_id is not None else 1
            
            cursor.execute(
                "INSERT INTO instructor (ID, name, dept_name, salary) VALUES (%s, %s, %s, %s)",
                (new_id, name, dept_name, salary)
            )
            conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error adding instructor: {e}")


def add_course(conn, course_id, title, dept_name, credits):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO course (course_id, title, dept_name, credits) VALUES (%s, %s, %s, %s)",
                (course_id, title, dept_name, credits)
            )
            conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error adding course: {e}")


# Assign student to a course
def enroll_student(conn, student_id, course_id, sec_id, semester, year):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO takes (ID, course_id, sec_id, semester, year)
                VALUES (%s, %s, %s, %s, %s)
            """, (student_id, course_id, sec_id, semester, year))
            conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error enrolling student: {e}")



# Assign instructor to a course section
def assign_instructor(conn, course_id, instructor_id, room_capacity, schedule):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO CourseSections (course_id, instructor_id, room_capacity, schedule) VALUES (%s, %s, %s, %s)", (course_id, instructor_id, room_capacity, schedule))
            conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error assigning instructor to course section: {e}")

# Search functionality
def view_courses_with_department(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_id, c.title, c.credits, d.dept_name 
                FROM course c
                JOIN department d ON c.dept_name = d.dept_name
            """)
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error retrieving courses: {e}")
        return None

def view_students_with_advisors(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.ID, s.name, a.i_ID, i.name 
                FROM student s
                LEFT JOIN advisor a ON s.ID = a.s_ID
                LEFT JOIN instructor i ON a.i_ID = i.ID
            """)
            return [(student_id, student_name, int(advisor_id) if advisor_id is not None else None, advisor_name) 
                    for student_id, student_name, advisor_id, advisor_name in cursor.fetchall()]
    except Exception as e:
        st.error(f"Error fetching students with advisors: {e}")
        return None
    
def view_average_salary_by_department(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT dept_name, AVG(salary) AS average_salary
                FROM instructor
                GROUP BY dept_name
            """)
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching average salary by department: {e}")
        return None
    
def view_instructors(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT ID, name, dept_name, salary
                FROM instructor
            """)
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching instructors: {e}")
        return None
    
def find_students_by_course(conn, course_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.ID, s.name, s.dept_name, t.grade
                FROM student s
                JOIN takes t ON s.ID = t.ID
                WHERE t.course_id = %s
            """, (course_id,))
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching students for course {course_id}: {e}")
        return None

def find_instructors_by_course(conn, course_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT i.ID, i.name, i.salary
                FROM instructor i
                JOIN teaches t ON i.ID = t.ID
                WHERE t.course_id = %s
            """, (course_id,))
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching instructors for course {course_id}: {e}")
        return None

def view_course_sections_with_capacity(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.course_id, s.sec_id, s.semester, s.year, c.building, c.room_number, c.capacity
                FROM section s
                JOIN classroom c ON s.building = c.building AND s.room_number = c.room_number;
            """)
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching course sections with room capacity: {e}")
        return None
    
def find_students_by_minimum_credits(conn, min_credits):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT ID, name, dept_name, tot_cred
                FROM student
                WHERE tot_cred >= %s;
            """, (min_credits,))
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching students by minimum credits: {e}")
        return None




# Function to retrieve department names for the dropdown
def get_departments(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT dept_name FROM department")
            departments = cursor.fetchall()
            return [dept[0] for dept in departments]
    except Exception as e:
        st.error(f"Error fetching departments: {e}")
        return []
    
# Function to get the next student ID
def get_next_student_id(conn):
    try:
        with conn.cursor() as cursor:
            # Fetch the latest student ID
            cursor.execute("SELECT ID FROM student ORDER BY ID DESC LIMIT 1")
            last_id = cursor.fetchone()
            if last_id:
                # Increment the last ID by 1 (assuming the IDs are numerical)
                next_id = str(int(last_id[0]) + 1).zfill(10)  # Zero-pad to maintain ID format, if needed
            else:
                next_id = "0000000001"  # Starting ID if no records are found
            return next_id
    except Exception as e:
        st.error(f"Error generating student ID: {e}")
        return None
    
def get_sections_for_course(conn, course_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT sec_id, semester, year
                FROM section
                WHERE course_id = %s
            """, (course_id,))
            return cursor.fetchall()  # Returns a list of tuples (sec_id, semester, year)
    except Exception as e:
        st.error(f"Error fetching sections for course {course_id}: {e}")
        return []

def get_course_details(conn, course_id):
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT 
                c.course_id, 
                c.title AS course_title, 
                STRING_AGG(DISTINCT i.name, ', ') AS instructor_names, 
                s.semester, 
                s.year, 
                ts.day, 
                ts.start_hour, 
                ts.start_minute, 
                ts.end_hour, 
                ts.end_minute,
                STRING_AGG(DISTINCT st.name, ', ') AS enrolled_students
            FROM 
                course c
            JOIN 
                section s ON c.course_id = s.course_id
            JOIN 
                teaches t ON s.course_id = t.course_id AND s.sec_id = t.sec_id AND s.semester = t.semester AND s.year = t.year
            JOIN 
                instructor i ON t.ID = i.ID
            JOIN 
                time_slot ts ON s.time_slot_id = ts.time_slot_id
            LEFT JOIN 
                takes tk ON tk.course_id = c.course_id AND tk.sec_id = s.sec_id AND tk.semester = s.semester AND tk.year = s.year
            LEFT JOIN 
                student st ON tk.ID = st.ID
            WHERE 
                c.course_id = %s
            GROUP BY 
                c.course_id, c.title, s.semester, s.year, ts.day, ts.start_hour, ts.start_minute, ts.end_hour, ts.end_minute
            ORDER BY 
                ts.day, ts.start_hour, ts.start_minute;
            """
            cursor.execute(query, (course_id,))
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching course details: {e}")
        return None

# Streamlit UI
def main():
    st.title("College Management System")
    conn = connect_db()
    if not conn:
        st.stop()

    if st.sidebar.button("Create Database"):
        create_tables(conn)
        seed_data(conn)
        st.success("Database created and seeded successfully.")

    # Sidebar menu using option_menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["View Courses", "Add Student", "View Students", "Search", "Enroll a Student", "Assign Instructor","Add Instructor", "Add Course","View Course Details","Exit"],
            icons=["book", "person-plus", "people", "search", "plus-circle", "person-video3","person", "book-half","credit-card-2-front-fill","door-closed"], 
            menu_icon="app-indicator",
            default_index=0,
            )

    if selected == "View Courses":
        st.subheader("Courses")
        courses = view_courses(conn)
        if courses:
            # Define column names based on the course schema
            columns = ["Course ID", "Title", "Department Name", "Credits"]
            # Create a DataFrame with course data and display in a table format
            courses_df = pd.DataFrame(courses, columns=columns)
            st.table(courses_df)
        else:
            st.write("No courses found.")



    # Add Student section with auto-generated student ID
    elif selected == "Add Student":
        student_id = get_next_student_id(conn)  # Automatically generate student ID
        if student_id:
            st.write(f"Generated Student ID: {student_id}")
            name = st.text_input("Student Name")
            dept_name = st.selectbox("Department Name", get_departments(conn))  # Dropdown for department names
            tot_cred = st.number_input("Total Credits", min_value=0, step=1)
    
            if st.button("Add Student"):
                add_student(conn, student_id, name, dept_name, tot_cred)
                st.success("Student added successfully.")

    elif selected == "View Students":
        st.subheader("Students")
        students = view_students(conn)
        if students:
            # Create a DataFrame to display results in a table format
            columns = ["Student ID", "Name", "Total Credits", "Department Name"]
            students_df = pd.DataFrame(students, columns=columns)
            st.table(students_df)
        else:
            st.write("No students found.")
    elif selected == "Assign Instructor":
        instructor_id = st.number_input("Instructor ID", min_value=1, step=1)
        course_id = st.text_input("Course ID")
        sec_id = st.text_input("Section ID")
        semester = st.text_input("Semester (e.g., Fall, Spring)")
        year = st.number_input("Year", min_value=2000, max_value=2100, step=1)

        if st.button("Assign Instructor"):
            if instructor_id and course_id and sec_id and semester and year:
                assign_instructor_to_course(conn, instructor_id, course_id, sec_id, semester, year)
            else:
                st.error("Please fill in all fields.")

    # Adding New Instructor Form
    elif selected == "Add Instructor":
        st.subheader("Add Instructor")
        name = st.text_input("Instructor Name")
        dept_name = st.selectbox("Department Name", get_departments(conn))  # Function to fetch department names
        salary = st.number_input("Salary", min_value=0)
        if st.button("Add Instructor"):
            add_instructor(conn, name, dept_name, salary)
            st.success("Instructor added successfully.")
    # Adding New Course Form
    elif selected == "Add Course":
        st.subheader("Add Course")
        course_id = st.text_input("Course ID")
        title = st.text_input("Course Title")
        dept_name = st.selectbox("Department Name", get_departments(conn))  # Function to fetch department names
        credits = st.number_input("Credits", min_value=1)
    
        if st.button("Add Course"):
            add_course(conn, course_id, title, dept_name, credits)
            st.success("Course added successfully.")
    
    elif selected == "Search":
        search_menu = [
            "Courses with Department Details", 
            "Students with Advisors",
            "Average Salary by Department",
            "View Instructors",
            "Find Students by Course",
            "Find Instructors by Course",
            "View Course Sections with Room Capacity",
            "Find Students by Minimum Credits"
        ]
        search_choice = st.selectbox("Select Search Option", search_menu)

        if search_choice == "Courses with Department Details":
            st.subheader("Courses with Department Details")
            courses = view_courses_with_department(conn)
            if courses:
                # Create a DataFrame to display results in a table format
                columns = ["Course ID", "Course Title", "Credits", "Department Name"]
                courses_df = pd.DataFrame(courses, columns=columns)
                st.table(courses_df)
            else:
                st.write("No courses found.")

        elif search_choice == "Students with Advisors":
            st.subheader("Students and their Advisors")
            student_advisor_data = view_students_with_advisors(conn)
            if student_advisor_data:
                # Create a DataFrame to display results in a table format
                columns = ["Student ID", "Student Name", "Advisor ID", "Advisor Name"]
                students_advisors_df = pd.DataFrame(student_advisor_data, columns=columns)

                # Convert Advisor ID to integer (it should already be, but to ensure no formatting issues)
                students_advisors_df["Advisor ID"] = students_advisors_df["Advisor ID"].astype('Int64')  # Int64 handles NA gracefully

                # Display the DataFrame
                st.table(students_advisors_df)
            else:
                st.write("No students found or no advisors assigned.")


        elif search_choice == "Average Salary by Department":
            st.subheader("Average Salary by Department")
            average_salaries = view_average_salary_by_department(conn)

            if average_salaries:
                # Create a DataFrame to display results in a table format
                columns = ["Department Name", "Average Salary"]
                avg_salaries_df = pd.DataFrame(average_salaries, columns=columns)

                # Display the DataFrame
                st.table(avg_salaries_df)
            else:
                st.write("No salary data found.")

        elif search_choice == "View Instructors":
            st.subheader("Instructors List")
            instructors = view_instructors(conn)

            if instructors:
                # Create a DataFrame to display results in a table format
                columns = ["Instructor ID", "Instructor Name", "Department Name", "Salary"]
                instructors_df = pd.DataFrame(instructors, columns=columns)

                # Display the DataFrame
                st.table(instructors_df)
            else:
                st.write("No instructors found.")


        elif search_choice == "Find Students by Course":
            st.subheader("Find Students by Course")

            # Retrieve all courses to populate the dropdown
            courses = view_courses(conn)  # Assuming you have this function from previous implementation
            if courses:
                course_options = [course[0] for course in courses]  # Assuming course[0] is course_id
                selected_course = st.selectbox("Select a Course", course_options)

                if st.button("Find Students"):
                    students = find_students_by_course(conn, selected_course)
                    if students:
                        # Create a DataFrame to display results in a table format
                        columns = ["Student ID", "Student Name", "Department Name", "Grade"]
                        students_df = pd.DataFrame(students, columns=columns)
                        st.table(students_df)
                    else:
                        st.write("No students found for the selected course.")
            else:
                st.write("No courses available.")

        
        elif search_choice == "Find Instructors by Course":
            st.subheader("Find Instructors by Course")

            # Retrieve all courses to populate the dropdown
            courses = view_courses(conn)  # Assuming you have this function from previous implementation
            if courses:
                course_options = [course[0] for course in courses]  # Assuming course[0] is course_id
                selected_course = st.selectbox("Select a Course", course_options)

                if st.button("Find Instructors"):
                    instructors = find_instructors_by_course(conn, selected_course)
                    if instructors:
                        # Create a DataFrame to display results in a table format
                        columns = ["Instructor ID", "Instructor Name", "Salary"]
                        instructors_df = pd.DataFrame(instructors, columns=columns)
                        st.table(instructors_df)
                    else:
                        st.write("No instructors found for the selected course.")
            else:
                st.write("No courses available.")


        elif search_choice == "View Course Sections with Room Capacity":
            st.subheader("Course Sections with Room Capacity")

            sections = view_course_sections_with_capacity(conn)
            if sections:
                # Create a DataFrame to display results in a table format
                columns = ["Course ID", "Section ID", "Semester", "Year", "Building", "Room Number", "Capacity"]
                sections_df = pd.DataFrame(sections, columns=columns)
                st.table(sections_df)
            else:
                st.write("No course sections found.")


        elif search_choice == "Find Students by Minimum Credits":
            st.subheader("Find Students by Minimum Credits")

            # Input for minimum credits
            min_credits = st.number_input("Enter Minimum Credits", min_value=0, step=1)

            if st.button("Find Students"):
                students = find_students_by_minimum_credits(conn, min_credits)
                if students:
                    # Create a DataFrame to display results in a table format
                    columns = ["Student ID", "Name", "Department Name", "Total Credits"]
                    students_df = pd.DataFrame(students, columns=columns)
                    st.table(students_df)
                else:
                    st.write("No students found with the specified minimum credits.")

    elif selected == "Enroll a Student":
        student_id = st.text_input("Student ID")

        courses = view_courses(conn)
        course_options = {course[0]: course[1] for course in courses}
        # Display courses in dropdown
        selected_course_id = st.selectbox("Select Course", options=list(course_options.keys()), format_func=lambda x: course_options[x])
        # Fetch available sections for the selected course
        sections = get_sections_for_course(conn, selected_course_id)

        # Prepare section options to show in the dropdown
        section_options = {f"{section[0]} - {section[1]} {section[2]}": section for section in sections}  # (sec_id, semester, year)

        if section_options:  # Check if there are any sections available
            selected_section = st.selectbox("Select Section", options=list(section_options.keys()))
            selected_sec_id, selected_semester, selected_year = section_options[selected_section]

            if st.button("Enroll Student"):
                enroll_student(conn, student_id, selected_course_id, selected_sec_id, selected_semester, selected_year)
                st.success("Student enrolled successfully.")
        else:
            st.write("No sections available for the selected course.")

    elif selected == "View Course Details":
        course_id = st.text_input("Enter Course ID:")
        if st.button("Get Course Details"):
            course_details = get_course_details(conn, course_id)
            if course_details:
                columns = ["Course ID", "Course Title", "Instructor Names", "Semester", "Year", "Day", "Start Hour", "Start Minute", "End Hour", "End Minute", "Enrolled Students"]
                course_details_df = pd.DataFrame(course_details, columns=columns)
                st.table(course_details_df)
            else:
                st.write("No course details found.")

    elif selected == "Exit":
        st.write("Thank you for using the College Management System!")
        conn.close()
        st.stop()

if __name__ == "__main__":
    main()
