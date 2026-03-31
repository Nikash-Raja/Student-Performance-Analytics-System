# student_performance_system.py
# A simple system to track student grades and performance
# Created by: Nikash Raja
# Date: March 2026

import sqlite3
import sys
from datetime import datetime

class StudentPerformanceSystem:
    def __init__(self, db_name="student_performance.db"):
        """Set up the database connection when we start the program"""
        # Connect to SQLite database (creates file if it doesn't exist)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        # Create our tables right away
        self._setup_database()
    
    def _setup_database(self):
        """Create the tables we need for storing data"""
        
        # First, let's create the students table
        # We'll store basic info like name and email
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                enrollment_year INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Next, create courses table to store course information
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                credits INTEGER NOT NULL
            )
        ''')
        
        # Finally, the marks table links students and courses
        # We also track which semester the student took the course
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                marks_obtained INTEGER NOT NULL,
                semester INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE(student_id, course_id, semester)
            )
        ''')
        
        self.conn.commit()
        print("✓ Database is ready to go!")
    
    def add_student(self):
        """Add a new student to our system"""
        print("\n--- Add New Student ---")
        
        # Get student information from user
        name = input("Student's full name: ").strip()
        email = input("Email address: ").strip()
        
        # Validate year input
        while True:
            try:
                year = int(input("Enrollment year (e.g., 2024): "))
                if year < 2000 or year > 2030:
                    print("Please enter a valid year between 2000 and 2030")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        # Try to insert into database
        try:
            self.cursor.execute('''
                INSERT INTO students (name, email, enrollment_year)
                VALUES (?, ?, ?)
            ''', (name, email, year))
            self.conn.commit()
            print(f"✓ Successfully added {name} to the system!")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Oops! Email {email} is already registered.")
            return False
    
    def add_course(self):
        """Add a new course to the system"""
        print("\n--- Add New Course ---")
        
        name = input("Course name: ").strip()
        code = input("Course code (e.g., CS101): ").strip().upper()
        
        # Validate credits
        while True:
            try:
                credits = int(input("Number of credits: "))
                if credits < 1 or credits > 6:
                    print("Credits should be between 1 and 6")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        try:
            self.cursor.execute('''
                INSERT INTO courses (name, code, credits)
                VALUES (?, ?, ?)
            ''', (name, code, credits))
            self.conn.commit()
            print(f"✓ Added course: {name} ({code})")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Course code {code} already exists!")
            return False
    
    def add_marks(self):
        """Record marks for a student in a specific course"""
        print("\n--- Record Student Marks ---")
        
        # First, show existing students so user can choose
        self._show_students()
        
        # Get student ID
        while True:
            try:
                student_id = int(input("\nEnter student ID: "))
                # Verify student exists
                self.cursor.execute('SELECT id FROM students WHERE id = ?', (student_id,))
                if not self.cursor.fetchone():
                    print("Student not found. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid ID number")
        
        # Show available courses
        self._show_courses()
        
        # Get course ID
        while True:
            try:
                course_id = int(input("\nEnter course ID: "))
                self.cursor.execute('SELECT id FROM courses WHERE id = ?', (course_id,))
                if not self.cursor.fetchone():
                    print("Course not found. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid ID number")
        
        # Get marks (0-100)
        while True:
            try:
                marks = int(input("Marks obtained (0-100): "))
                if marks < 0 or marks > 100:
                    print("Marks must be between 0 and 100")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        # Get semester (1-8)
        while True:
            try:
                semester = int(input("Semester (1-8): "))
                if semester < 1 or semester > 8:
                    print("Semester must be between 1 and 8")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        # Save to database
        try:
            self.cursor.execute('''
                INSERT INTO marks (student_id, course_id, marks_obtained, semester)
                VALUES (?, ?, ?, ?)
            ''', (student_id, course_id, marks, semester))
            self.conn.commit()
            print("✓ Marks recorded successfully!")
            return True
        except sqlite3.IntegrityError:
            print("✗ Marks for this student, course, and semester already exist!")
            return False
    
    def view_top_students(self):
        """Show the top performing students"""
        print("\n--- Top Students ---")
        
        # Ask if user wants to filter by semester
        filter_by_semester = input("Filter by specific semester? (y/n): ").lower()
        
        if filter_by_semester == 'y':
            try:
                semester = int(input("Enter semester number: "))
                query = '''
                    SELECT s.name, s.email, AVG(m.marks_obtained) as avg_marks,
                           COUNT(m.course_id) as courses_taken
                    FROM students s
                    JOIN marks m ON s.id = m.student_id
                    WHERE m.semester = ?
                    GROUP BY s.id
                    ORDER BY avg_marks DESC
                    LIMIT 5
                '''
                self.cursor.execute(query, (semester,))
            except ValueError:
                print("Invalid semester number")
                return
        else:
            query = '''
                SELECT s.name, s.email, AVG(m.marks_obtained) as avg_marks,
                       COUNT(m.course_id) as courses_taken
                FROM students s
                JOIN marks m ON s.id = m.student_id
                GROUP BY s.id
                ORDER BY avg_marks DESC
                LIMIT 5
            '''
            self.cursor.execute(query)
        
        results = self.cursor.fetchall()
        
        if not results:
            print("No marks data available yet.")
            return
        
        print("\n" + "="*60)
        print("🏆 TOP 5 STUDENTS")
        if filter_by_semester == 'y':
            print(f"📚 Semester {semester}")
        print("="*60)
        
        for i, (name, email, avg, courses) in enumerate(results, 1):
            # Determine letter grade
            if avg >= 90:
                grade = "A+"
            elif avg >= 80:
                grade = "A"
            elif avg >= 70:
                grade = "B"
            elif avg >= 60:
                grade = "C"
            elif avg >= 50:
                grade = "D"
            else:
                grade = "F"
            
            print(f"\n{i}. {name}")
            print(f"   📧 {email}")
            print(f"   📊 Average: {avg:.1f}% (Grade: {grade})")
            print(f"   📚 Courses completed: {courses}")
    
    def view_course_stats(self):
        """Show performance statistics for each course"""
        print("\n--- Course Performance Analysis ---")
        
        # Ask for semester filter
        filter_by_semester = input("Filter by specific semester? (y/n): ").lower()
        
        if filter_by_semester == 'y':
            try:
                semester = int(input("Enter semester number: "))
                query = '''
                    SELECT c.name, c.code, AVG(m.marks_obtained) as avg_marks,
                           COUNT(m.student_id) as student_count,
                           MIN(m.marks_obtained) as min_score,
                           MAX(m.marks_obtained) as max_score
                    FROM courses c
                    JOIN marks m ON c.id = m.course_id
                    WHERE m.semester = ?
                    GROUP BY c.id
                    ORDER BY avg_marks DESC
                '''
                self.cursor.execute(query, (semester,))
            except ValueError:
                print("Invalid semester number")
                return
        else:
            query = '''
                SELECT c.name, c.code, AVG(m.marks_obtained) as avg_marks,
                       COUNT(m.student_id) as student_count,
                       MIN(m.marks_obtained) as min_score,
                       MAX(m.marks_obtained) as max_score
                FROM courses c
                JOIN marks m ON c.id = m.course_id
                GROUP BY c.id
                ORDER BY avg_marks DESC
            '''
            self.cursor.execute(query)
        
        results = self.cursor.fetchall()
        
        if not results:
            print("No course data available yet.")
            return
        
        print("\n" + "="*70)
        print("📊 COURSE PERFORMANCE SUMMARY")
        if filter_by_semester == 'y':
            print(f"📚 Semester {semester}")
        print("="*70)
        
        for name, code, avg, count, min_score, max_score in results:
            print(f"\n📖 {name} ({code})")
            print(f"   Average: {avg:.1f}%")
            print(f"   Students enrolled: {count}")
            print(f"   Score range: {min_score:.0f}% - {max_score:.0f}%")
    
    def student_report(self):
        """Generate a detailed report for a specific student"""
        print("\n--- Student Performance Report ---")
        
        # Show list of students
        self._show_students()
        
        # Get student ID
        try:
            student_id = int(input("\nEnter student ID: "))
        except ValueError:
            print("Invalid ID")
            return
        
        # Get student info
        self.cursor.execute('''
            SELECT name, email, enrollment_year FROM students WHERE id = ?
        ''', (student_id,))
        student = self.cursor.fetchone()
        
        if not student:
            print("Student not found!")
            return
        
        name, email, year = student
        
        # Get all marks for this student
        self.cursor.execute('''
            SELECT c.name, c.code, m.marks_obtained, m.semester, c.credits
            FROM marks m
            JOIN courses c ON m.course_id = c.id
            WHERE m.student_id = ?
            ORDER BY m.semester, c.name
        ''', (student_id,))
        
        marks = self.cursor.fetchall()
        
        if not marks:
            print(f"No marks recorded for {name} yet.")
            return
        
        # Calculate overall stats
        total_marks = 0
        total_credits = 0
        for mark in marks:
            total_marks += mark[2]
            total_credits += mark[4]
        
        avg_marks = total_marks / len(marks)
        
        # Calculate GPA
        if avg_marks >= 90:
            gpa = 4.0
        elif avg_marks >= 80:
            gpa = 3.0 + (avg_marks - 80) / 10
        elif avg_marks >= 70:
            gpa = 2.0 + (avg_marks - 70) / 10
        elif avg_marks >= 60:
            gpa = 1.0 + (avg_marks - 60) / 10
        elif avg_marks >= 50:
            gpa = 0.5 + (avg_marks - 50) / 20
        else:
            gpa = 0.0
        
        # Display report
        print("\n" + "="*60)
        print("📋 STUDENT PERFORMANCE REPORT")
        print("="*60)
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Enrolled: {year}")
        print("="*60)
        
        print("\n📚 COURSE HISTORY:")
        print("-"*60)
        
        current_semester = None
        for course_name, code, score, semester, credits in marks:
            if current_semester != semester:
                print(f"\nSemester {semester}:")
                current_semester = semester
            
            # Determine letter grade
            if score >= 90:
                grade = "A+"
            elif score >= 80:
                grade = "A"
            elif score >= 70:
                grade = "B"
            elif score >= 60:
                grade = "C"
            elif score >= 50:
                grade = "D"
            else:
                grade = "F"
            
            print(f"  • {course_name} ({code}): {score}% ({grade}) - {credits} credits")
        
        print("\n" + "="*60)
        print("📈 SUMMARY:")
        print(f"  Total Courses: {len(marks)}")
        print(f"  Total Credits: {total_credits}")
        print(f"  Overall Average: {avg_marks:.1f}%")
        print(f"  GPA: {gpa:.2f}")
        print("="*60)
    
    def class_statistics(self):
        """Show overall class performance statistics"""
        print("\n--- Class Performance Statistics ---")
        
        filter_by_semester = input("Filter by specific semester? (y/n): ").lower()
        
        if filter_by_semester == 'y':
            try:
                semester = int(input("Enter semester number: "))
                self.cursor.execute('''
                    SELECT AVG(marks_obtained), MIN(marks_obtained), 
                           MAX(marks_obtained), COUNT(DISTINCT student_id)
                    FROM marks
                    WHERE semester = ?
                ''', (semester,))
            except ValueError:
                print("Invalid semester number")
                return
        else:
            self.cursor.execute('''
                SELECT AVG(marks_obtained), MIN(marks_obtained), 
                       MAX(marks_obtained), COUNT(DISTINCT student_id)
                FROM marks
            ''')
        
        stats = self.cursor.fetchone()
        
        if not stats or stats[3] == 0:
            print("No marks data available yet.")
            return
        
        print("\n" + "="*60)
        print("📊 CLASS PERFORMANCE")
        if filter_by_semester == 'y':
            print(f"Semester {semester}")
        print("="*60)
        print(f"Class Average: {stats[0]:.1f}%")
        print(f"Highest Score: {stats[2]:.0f}%")
        print(f"Lowest Score: {stats[1]:.0f}%")
        print(f"Students Tracked: {stats[3]}")
    
    def _show_students(self):
        """Helper function to display all students"""
        self.cursor.execute('SELECT id, name, email FROM students ORDER BY name')
        students = self.cursor.fetchall()
        
        if not students:
            print("\nNo students in the system yet.")
            return
        
        print("\nCurrent Students:")
        print("-" * 50)
        for sid, name, email in students:
            print(f"ID: {sid} | {name} | {email}")
    
    def _show_courses(self):
        """Helper function to display all courses"""
        self.cursor.execute('SELECT id, name, code, credits FROM courses ORDER BY name')
        courses = self.cursor.fetchall()
        
        if not courses:
            print("\nNo courses in the system yet.")
            return
        
        print("\nAvailable Courses:")
        print("-" * 60)
        for cid, name, code, credits in courses:
            print(f"ID: {cid} | {name} ({code}) | {credits} credits")
    
    def show_menu(self):
        """Display the main menu and handle user choices"""
        while True:
            print("\n" + "="*50)
            print("🎓 STUDENT PERFORMANCE ANALYTICS SYSTEM")
            print("="*50)
            print("1. Add a new student")
            print("2. Add a new course")
            print("3. Record student marks")
            print("4. View top students")
            print("5. View course statistics")
            print("6. Generate student report")
            print("7. View class statistics")
            print("8. List all students")
            print("9. List all courses")
            print("10. Exit program")
            print("="*50)
            
            choice = input("What would you like to do? (1-10): ")
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.add_course()
            elif choice == '3':
                self.add_marks()
            elif choice == '4':
                self.view_top_students()
            elif choice == '5':
                self.view_course_stats()
            elif choice == '6':
                self.student_report()
            elif choice == '7':
                self.class_statistics()
            elif choice == '8':
                self._show_students()
            elif choice == '9':
                self._show_courses()
            elif choice == '10':
                print("\nThanks for using the system! Goodbye!")
                self.conn.close()
                sys.exit(0)
            else:
                print("Please enter a number between 1 and 10")
            
            # Pause before showing menu again
            input("\nPress Enter to continue...")

def main():
    """Main program entry point"""
    print("\n" + "="*50)
    print("Welcome to the Student Performance Analytics System!")
    print("="*50)
    
    try:
        # Create our system instance
        system = StudentPerformanceSystem()
        print("✓ System initialized successfully")
        
        # Start the menu
        system.show_menu()
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please make sure you have write permissions in this directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()