🎓 Student Performance Analytics System 📊

Overview:
The Student Performance Analytics System is a Python-based desktop application that helps educational institutions manage and analyze student academic performance using SQLite database. Users can store student information, manage courses, record marks, and generate performance analytics including top student rankings, course averages, and GPA calculations.

Features:
- Add/manage student profiles with enrollment details
- Create/manage courses with credit hours and codes
- Record student marks
- View top students with grade calculation
- Analyze course performance
- Generate individual student reports with GPA
- View class-wide statistics
- Filter analytics by semester

Technologies Used:
- Python 3.8+ (OOP)
- SQLite3 (built-in database)
- SQL queries (JOINs, aggregate functions, filtering)
- Command-line interface

Database Schema:
Tables:
students(id, name, email, enrollment_year, created_at)
courses(id, name, code, credits)
marks(id, student_id, course_id, marks_obtained, semester)
![schema design](image.png)
Installation Instructions:
1. Clone the repository
2. Python 3.8+ required (SQLite included)
3. Run student_performance_system.py
4. Optional: Run sample_data.py to load test data

Usage Guide:
Menu options:
1. Add new student
2. Add new course
3. Record student marks
4. View top students
5. View course statistics
6. Generate student report
7. View class statistics
8. List all students
9. List all courses
10. Exit

Sample Output:
Student Report: John Doe
Email: john.doe@example.com
Enrollment Year: 2023
Courses:
Mathematics - 92 - A
Physics - 85 - B
Chemistry - 78 - C
GPA: 3.67

Project Structure:
student-performance-analytics/
│-- student_performance_system.py
│-- README.md
│-- LICENSE

Future Enhancements:
- GUI with Tkinter
- Export reports to PDF/Excel
- Data visualization with charts
- Web version with Flask
- Mobile app support
- Attendance tracking module

Contributing Guidelines:
1. Fork repository
2. Create branch
3. Commit changes
4. Push branch
5. Create pull request

