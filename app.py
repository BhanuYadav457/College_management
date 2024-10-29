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
            CREATE TABLE IF NOT EXISTS Departments (
                department_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE, 
                building VARCHAR(255),
                head VARCHAR(255),
                budget DECIMAL(10, 2)
            );
            CREATE TABLE IF NOT EXISTS Courses (
                course_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                credits INT NOT NULL,
                department_id INT REFERENCES Departments(department_id),
                syllabus TEXT,
                semester_offered VARCHAR(50),
                UNIQUE(name, department_id)  
            );
            CREATE TABLE IF NOT EXISTS Students (
                student_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                department_id INT REFERENCES Departments(department_id),
                enrollment_date DATE,
                email VARCHAR(255) UNIQUE  
            );
            CREATE TABLE IF NOT EXISTS Instructors (
                instructor_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                department_id INT REFERENCES Departments(department_id),
                salary DECIMAL(10, 2),
                hire_date DATE,
                email VARCHAR(255) UNIQUE  
            );

            CREATE TABLE IF NOT EXISTS StudentAdvisors (
                advisor_id SERIAL PRIMARY KEY,
                student_id INT REFERENCES Students(student_id),
                instructor_id INT REFERENCES Instructors(instructor_id),
                UNIQUE(student_id, instructor_id)  
            );

            CREATE TABLE IF NOT EXISTS Enrollments (
                enrollment_id SERIAL PRIMARY KEY,
                student_id INT REFERENCES Students(student_id),
                course_id INT REFERENCES Courses(course_id),
                enrollment_date DATE,
                UNIQUE(student_id, course_id)  
            );

            CREATE TABLE IF NOT EXISTS CourseSections (
                section_id SERIAL PRIMARY KEY,
                course_id INT REFERENCES Courses(course_id),
                instructor_id INT REFERENCES Instructors(instructor_id),
                room_capacity INT,
                schedule VARCHAR(255)
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
            -- Seed Departments
            INSERT INTO Departments (name, building, head, budget) VALUES 
                ('Mathematics', 'Building A', 'Dr. Alice Johnson', 500000),
                ('Computer Science', 'Building B', 'Dr. Bob Smith', 600000),
                ('Physics', 'Building C', 'Dr. Rachel Green', 450000),
                ('Chemistry', 'Building D', 'Dr. David Lee', 550000),
                ('Biology', 'Building E', 'Dr. Emily Brown', 520000),
                ('Statistics', 'Building F', 'Dr. Frank Turner', 480000),
                ('Environmental Science', 'Building G', 'Dr. Clara White', 530000)
            ON CONFLICT DO NOTHING;

            -- Seed Courses
            INSERT INTO Courses (name, credits, department_id, syllabus, semester_offered) VALUES
                ('Calculus', 3, 1, 'Introductory calculus', 'Fall, Spring'),
                ('Algorithms', 4, 2, 'Introduction to algorithms', 'Fall'),
                ('Quantum Mechanics', 3, 3, 'Fundamentals of quantum mechanics', 'Fall'),
                ('Organic Chemistry', 4, 4, 'Study of organic compounds', 'Winter'),
                ('Genetics', 3, 5, 'Introduction to genetics', 'Spring'),
                ('Data Structures', 4, 2, 'In-depth study of data structures', 'Winter'),
                ('Linear Algebra', 3, 1, 'Matrix theory and linear algebra', 'Fall, Spring'),
                ('Machine Learning', 4, 2, 'Supervised and unsupervised learning techniques', 'Spring'),
                ('Environmental Policy', 3, 7, 'Policies affecting environmental management', 'Fall'),
                ('Statistical Inference', 4, 6, 'Principles of statistical inference', 'Fall')
            ON CONFLICT DO NOTHING;

            -- Seed Students
            INSERT INTO Students (name, department_id, enrollment_date, email) VALUES
                ('Liam White', 1, '2023-08-20', 'liam.white@example.com'),
                ('Olivia Green', 2, '2023-08-21', 'olivia.green@example.com'),
                ('Noah Brown', 3, '2023-08-22', 'noah.brown@example.com'),
                ('Emma Black', 4, '2023-08-23', 'emma.black@example.com'),
                ('Oliver Stone', 5, '2023-08-24', 'oliver.stone@example.com'),
                ('Charlotte Lee', 1, '2023-08-25', 'charlotte.lee@example.com'),
                ('James Williams', 2, '2023-08-26', 'james.williams@example.com'),
                ('Sophia Harris', 3, '2023-08-27', 'sophia.harris@example.com'),
                ('Mason Hall', 4, '2023-08-28', 'mason.hall@example.com'),
                ('Ava Walker', 5, '2023-08-29', 'ava.walker@example.com'),
                ('Ethan King', 6, '2023-08-30', 'ethan.king@example.com'),
                ('Isabella White', 7, '2023-09-01', 'isabella.white@example.com'),
                ('Mia Patel', 1, '2023-09-02', 'mia.patel@example.com'),
                ('Alexander Chan', 2, '2023-09-03', 'alexander.chan@example.com'),
                ('Harper Singh', 3, '2023-09-04', 'harper.singh@example.com')
            ON CONFLICT DO NOTHING;

            -- Seed Instructors
            INSERT INTO Instructors (name, department_id, salary, hire_date, email) VALUES
                ('Dr. Anna Martin', 1, 72000, '2018-01-15', 'anna.martin@example.com'),
                ('Dr. Robert Moore', 2, 80000, '2019-08-10', 'robert.moore@example.com'),
                ('Dr. William Scott', 3, 78000, '2020-05-12', 'william.scott@example.com'),
                ('Dr. Jessica Wright', 4, 75000, '2017-11-19', 'jessica.wright@example.com'),
                ('Dr. Michael Hill', 5, 74000, '2016-06-21', 'michael.hill@example.com'),
                ('Dr. Olivia Brooks', 6, 68000, '2021-03-15', 'olivia.brooks@example.com'),
                ('Dr. Henry Adams', 7, 79000, '2022-07-12', 'henry.adams@example.com')
            ON CONFLICT DO NOTHING;

            -- Seed Student Advisors
            INSERT INTO StudentAdvisors (student_id, instructor_id) VALUES
                (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                (6, 1), (7, 2), (8, 3), (9, 4), (10, 5),
                (11, 6), (12, 7), (13, 1), (14, 2), (15, 3)
            ON CONFLICT DO NOTHING;

            -- Seed Course Sections
            INSERT INTO CourseSections (course_id, instructor_id, room_capacity, schedule) VALUES
                (1, 1, 30, 'Mon-Wed-Fri 10:00-11:00 AM'),  
                (2, 2, 25, 'Tue-Thu 01:00-02:30 PM'),
                (3, 3, 20, 'Mon-Wed-Fri 02:00-03:00 PM'),  
                (4, 4, 35, 'Tue-Thu 10:00-11:30 AM'),  
                (5, 5, 40, 'Mon-Wed 09:00-10:30 AM'),  
                (6, 2, 25, 'Tue-Thu 03:00-04:30 PM'),
                (7, 1, 30, 'Mon-Wed-Fri 01:00-02:00 PM'),
                (8, 2, 20, 'Mon 01:00-03:00 PM, Fri 01:00-02:00 PM')
            ON CONFLICT DO NOTHING;

            -- Seed Enrollments - Enroll students in courses
            INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES
                (1, 1, '2023-08-21'), (2, 2, '2023-08-22'), (3, 3, '2023-08-23'),
                (4, 4, '2023-08-24'), (5, 5, '2023-08-25'), (6, 6, '2023-08-26'),
                (7, 1, '2023-08-27'), (8, 2, '2023-08-28'), (9, 3, '2023-08-29'),
                (10, 4, '2023-08-30'), (11, 5, '2023-09-01'), (12, 6, '2023-09-02'),
                (13, 7, '2023-09-03'), (14, 8, '2023-09-04'), (15, 1, '2023-09-05')
            ON CONFLICT DO NOTHING;
            """)
            conn.commit()
            st.success("Seed data inserted successfully.")
    except Exception as e:
        st.error(f"Error seeding data: {e}")


# View data functions
def view_courses(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Courses")
        return cursor.fetchall()

def view_students(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Students")
        return cursor.fetchall()

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

def assign_instructor_to_course(conn, course_id, instructor_id):
    try:
        with conn.cursor() as cursor:
            # Update CourseSections table with the selected course and instructor
            cursor.execute(
                """
                UPDATE CourseSections 
                SET instructor_id = %s 
                WHERE course_id = %s;
                """,
                (instructor_id, course_id)
            )
            conn.commit()
            st.success("Instructor assigned to the course successfully.")
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error assigning instructor: {e}")

# Insert new data functions
def add_student(conn, name, department_id, enrollment_date, email):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Students (name, department_id, enrollment_date, email) VALUES (%s, %s, %s, %s)", (name, department_id, enrollment_date, email))
            conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error adding student: {e}")

def add_instructor(conn, name, department_id, salary, hire_date, email):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Instructors (name, department_id, salary, hire_date, email) VALUES (%s, %s, %s, %s, %s)", (name, department_id, salary, hire_date, email))
            conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error adding instructor: {e}")

def add_course(conn, name, credits, department_id, syllabus, semester_offered):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Courses (name, credits, department_id, syllabus, semester_offered) VALUES (%s, %s, %s, %s, %s)", (name, credits, department_id, syllabus, semester_offered))
            conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        st.error(f"Error adding course: {e}")

# Assign student to a course
def enroll_student(conn, student_id, course_id, enrollment_date):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s)", (student_id, course_id, enrollment_date))
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
def search_courses_with_departments(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                Courses.course_id, 
                Courses.name AS course_name, 
                Courses.credits, 
                Courses.syllabus, 
                Courses.semester_offered,
                Departments.name AS department_name, 
                Departments.building,
                Departments.head, 
                Departments.budget
            FROM 
                Courses 
            JOIN 
                Departments ON Courses.department_id = Departments.department_id
        """)
        return cursor.fetchall()

def search_students_with_advisors(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT Students.name AS student, Instructors.name AS advisor
            FROM StudentAdvisors
            JOIN Students ON StudentAdvisors.student_id = Students.student_id
            JOIN Instructors ON StudentAdvisors.instructor_id = Instructors.instructor_id
        """)
        return cursor.fetchall()

def average_salary_by_department(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT Departments.name, AVG(Instructors.salary) AS avg_salary
            FROM Instructors 
            JOIN Departments ON Instructors.department_id = Departments.department_id
            GROUP BY Departments.name
        """)
        return cursor.fetchall()
    
def find_instructors_by_course(conn, course_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT i.instructor_id, i.name
            FROM Instructors i
            JOIN CourseSections cs ON i.instructor_id = cs.instructor_id
            JOIN Courses c ON cs.course_id = c.course_id
            WHERE c.course_id = %s; 
            """, (course_id,))
            instructors = cursor.fetchall()
            return instructors
    except Exception as e:
        st.error(f"Error fetching instructors: {e}")
        return []

def view_course_sections(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT cs.section_id, c.name AS course_name, i.name AS instructor_name, cs.room_capacity, cs.schedule
            FROM CourseSections cs
            JOIN Courses c ON cs.course_id = c.course_id
            JOIN Instructors i ON cs.instructor_id = i.instructor_id;
            """)
            sections = cursor.fetchall()
            return sections
    except Exception as e:
        st.error(f"Error fetching course sections: {e}")
        return []

# Fetch Departments for Dropdown
def get_departments(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT department_id, name FROM Departments")
            departments = cursor.fetchall()
        return departments
    except Exception as e:
        st.error(f"Error fetching departments: {e}")
        return []

# Find Students by Course
def find_students_by_course(conn, course_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(""" 
                SELECT Students.student_id, Students.name 
                FROM Enrollments 
                JOIN Students ON Enrollments.student_id = Students.student_id 
                WHERE Enrollments.course_id = %s
            """, (course_id,))
            results = cursor.fetchall()
            # Return list of tuples (student_id, student_name)
            return results
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []
def find_students_by_minimum_credits(conn, min_credits):
    try:
        with conn.cursor() as cursor:
            cursor.execute(""" 
            SELECT s.student_id, s.name, SUM(c.credits) AS total_credits
            FROM Students s
            JOIN Enrollments e ON s.student_id = e.student_id
            JOIN Courses c ON e.course_id = c.course_id
            GROUP BY s.student_id, s.name
            HAVING SUM(c.credits) >= %s;
            """, (min_credits,))
            students = cursor.fetchall()
            return students
    except Exception as e:
        st.error(f"Error fetching students: {e}")
        return []


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
            options=["View Courses", "Add Student", "View Students", "Search", "Enroll a Student", "Assign Instructor","Add Instructor", "Add Course", "Exit"],
            icons=["book", "person-plus", "people", "search", "plus-circle", "person-video3","person", "book-half","door-closed"], 
            menu_icon="app-indicator",
            default_index=0,
            )

    if selected == "View Courses":
        st.subheader("Courses")
        courses = view_courses(conn)
        if courses:
            # Create a DataFrame to display results in a table format
            columns = ["Course ID", "Course Name", "Credits", "Syllabus", "Semester Offered", "Department Name"]
            courses_df = pd.DataFrame(courses, columns=columns)
            st.table(courses_df)
        else:
            st.write("No courses found.")

    elif selected == "Add Student":
        name = st.text_input("Student Name")
        department_id = st.number_input("Department ID", min_value=1, step=1)
        enrollment_date = st.date_input("Enrollment Date")
        email = st.text_input("Email")

        if st.button("Add Student"):
            add_student(conn, name, department_id, enrollment_date, email)
            st.success("Student added successfully.")

    elif selected == "View Students":
        st.subheader("Students")
        students = view_students(conn)
        if students:
            # Create a DataFrame to display results in a table format
            columns = ["Student ID", "Name", "Enrollment Date", "Email", "Department Name"]
            students_df = pd.DataFrame(students, columns=columns)
            st.table(students_df)
        else:
            st.write("No students found.")

    # Adding New Instructor Form
    elif selected == "Add Instructor":
        st.title("Add New Instructor")
        name = st.text_input("Name")
        departments = get_departments(conn)

        # Display department names as a dropdown
        department_options = {dept[0]: dept[1] for dept in departments}
        selected_department_id = st.selectbox("Department", options=department_options.keys(), format_func=lambda x: department_options[x])

        salary = st.number_input("Salary", min_value=0.0, step=0.01)
        hire_date = st.date_input("Hire Date")
        email = st.text_input("Email")

        if st.button("Add Instructor"):
            add_instructor(conn, name, selected_department_id, salary, hire_date, email)

    # Adding New Course Form
    elif selected == "Add Course":
        st.title("Add New Course")
        name = st.text_input("Course Name")
        credits = st.number_input("Credits", min_value=1, step=1)
        
        # Display department names as a dropdown
        departments = get_departments(conn)
        department_options = {dept[0]: dept[1] for dept in departments}
        selected_department_id = st.selectbox("Department", options=department_options.keys(), format_func=lambda x: department_options[x])
    
        syllabus = st.text_area("Syllabus")
        semester_offered = st.text_input("Semester Offered")
        
        if st.button("Add Course"):
            add_course(conn, name, credits, selected_department_id, syllabus, semester_offered)
    elif selected == "Assign Instructor":
        st.title("Assign Instructor to Course")
    
        # Fetch available courses and instructors from the database
        courses = view_courses(conn)  # Assuming view_courses fetches all courses (id and name)
        instructors = view_instructors(conn)  # Assuming view_instructors fetches all instructors (id and name)
    
        # Prepare dropdown options for courses and instructors
        course_options = {course[0]: course[1] for course in courses}  # {course_id: course_name}
        instructor_options = {instructor[0]: instructor[1] for instructor in instructors}  # {instructor_id: instructor_name}
    
        # Dropdown selection for course and instructor
        selected_course_id = st.selectbox("Select Course", options=list(course_options.keys()), format_func=lambda x: course_options[x])
        selected_instructor_id = st.selectbox("Select Instructor", options=list(instructor_options.keys()), format_func=lambda x: instructor_options[x])
    
        # Button to assign instructor to the course
        if st.button("Assign Instructor"):
            assign_instructor_to_course(conn, selected_course_id, selected_instructor_id)

    

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
            results = search_courses_with_departments(conn)
            # Create a DataFrame to display results in a table format
            columns = ["Course ID", "Course Name", "Credits", "Syllabus", "Semester Offered", 
                       "Department Name", "Building", "Head", "Budget"]
            results_df = pd.DataFrame(results, columns=columns)
            st.table(results_df)

        elif search_choice == "Students with Advisors":
            results = search_students_with_advisors(conn)
            # Create a DataFrame to display results in a table format
            columns = ["Student", "Advisor"]
            results_df = pd.DataFrame(results, columns=columns)
            st.table(results_df)

        elif search_choice == "Average Salary by Department":
            results = average_salary_by_department(conn)
            # Create a DataFrame to display results in a table format
            columns = ["Department", "Average Salary"]
            results_df = pd.DataFrame(results, columns=columns)
            st.table(results_df)


        elif search_choice == "View Instructors":
            results = view_instructors(conn)
            # Create a DataFrame to display results in a table format
            columns = ["Instructor ID", "Name", "Email", "Department ID", "Salary", "Hire Date"]
            results_df = pd.DataFrame(results, columns=columns)
            st.table(results_df)

        elif search_choice == "Find Students by Course":
            # Fetch the list of available courses
            courses = view_courses(conn)  
            course_options = {course[0]: course[1] for course in courses} 

            selected_course_id = st.selectbox("Select a Course", options=list(course_options.keys()), format_func=lambda x: course_options[x])

            if st.button("Find Students"):
                students = find_students_by_course(conn, selected_course_id)  
                if students:
                    st.subheader(f"Students enrolled in Course ID {selected_course_id} ({course_options[selected_course_id]}):")
                    # Create a DataFrame to display results in a table format
                    columns = ["Student ID", "Name"]
                    students_df = pd.DataFrame(students, columns=columns)  # Create DataFrame with both ID and Name
                    st.table(students_df)  # Display the DataFrame as a table
                else:
                    st.write("No students found for this course.")
        
        elif search_choice == "Find Instructors by Course":
            st.title("Find Instructors by Course")

            # Fetch the list of available courses
            courses = view_courses(conn)
            course_options = {course[0]: course[1] for course in courses}

            selected_course_id = st.selectbox("Select a Course", options=list(course_options.keys()), format_func=lambda x: course_options[x])

            if st.button("Find Instructors"):
                instructors = find_instructors_by_course(conn, selected_course_id)
                if instructors:
                    st.subheader(f"Instructors for Course ID {selected_course_id} ({course_options[selected_course_id]}):")
                    # Create a DataFrame to display results in a table format
                    columns = ["Instructor ID", "Name"]
                    instructors_df = pd.DataFrame(instructors, columns=columns)
                    st.table(instructors_df)
                else:
                    st.write("No instructors found for this course.")

        elif search_choice == "View Course Sections with Room Capacity":
            st.title("Course Sections with Room Capacity")

            results = view_course_sections(conn)
            if results:
                # Create a DataFrame to display results in a table format
                columns = ["Section ID", "Course", "Instructor", "Room Capacity", "Schedule"]
                sections_df = pd.DataFrame(results, columns=columns)
                st.table(sections_df)
            else:
                st.write("No course sections found.")

        elif search_choice == "Find Students by Minimum Credits":
            st.title("Find Students by Minimum Credits")

            min_credits = st.number_input("Enter Minimum Credits:", min_value=0)

            if st.button("Find Students"):
                students = find_students_by_minimum_credits(conn, min_credits)
                if students:
                    st.subheader(f"Students with at least {min_credits} credits:")
                    # Create a DataFrame to display results in a table format
                    columns = ["Student ID", "Name", "Credits"]
                    students_df = pd.DataFrame(students, columns=columns)
                    st.table(students_df)
                else:
                    st.write("No students found with the specified minimum credits.")

    elif selected == "Enroll a Student":
                student_id = st.number_input("Student ID", min_value=1, step=1)

                # Fetch available courses
                courses = view_courses(conn) 
                course_options = {course[0]: course[1] for course in courses} 

                # Display courses in dropdown
                selected_course_id = st.selectbox("Select Course", options=list(course_options.keys()), format_func=lambda x: course_options[x])

                enrollment_date = st.date_input("Enrollment Date")

                if st.button("Enroll Student"):
                    enroll_student(conn, student_id, selected_course_id, enrollment_date)
                    st.success("Student enrolled successfully.")


    elif selected == "Exit":
        st.write("Thank you for using the College Management System!")
        conn.close()
        st.stop()

if __name__ == "__main__":
    main()
