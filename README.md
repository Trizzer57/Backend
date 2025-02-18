# Backend
This Python backend code is a Flask-based academic performance management system that integrates database management, role-based access control, encryption, machine learning, email notifications, audit logging, and PDF report generation. Below is a high-level breakdown of its key functionalities:

1. Web Framework & Security
Uses Flask to create a web server.
Implements session-based authentication (session stores user login info).
Role-Based Access Control (RBAC) (@requires_roles) restricts access to certain routes.
2. Database & User Authentication
Connects to a MySQL database (pymysql).
Provides a user login endpoint (/login) that verifies credentials and stores user info in a session.
Logs audit actions to track user activities (log_audit).
3. Performance Management
Allows teachers/admins to insert/update student performance data (/performance, /add_performance).
Implements trend analysis to identify underperforming students (/analyze_trends).
4. Machine Learning Integration
Uses Linear Regression (/predict_risk) to predict student risk levels based on attendance, test scores, and behavior.
Uses a Decision Tree Classifier (/predict_intervention) to recommend interventions (e.g., tutoring).
5. Security (Encryption)
Implements AES encryption (encrypt, decrypt) to secure sensitive data.
6. Notifications & Alerts
Sends email alerts to parents/teachers using Flask-Mail (/send_alerts).
Uses Firebase Admin SDK for potential push notifications.
7. Reporting & Visualization
Generates performance reports (/generate_report) with Chart.js.
Exports PDF reports (/export_pdf) with FPDF and Matplotlib.

# Database
The academic performance analytic system database is designed to manage student performance, interventions, and user roles (teachers, parents, and administrators). Below is a breakdown of its structure and purpose:

1. Users Table (users)
This table stores login credentials and roles of users (teachers, parents, admins).

user_id – Unique identifier for each user.
username – Unique name used for login.
password – Stores hashed passwords for security.
role – Defines the user’s role (teacher, parent, admin).
💡 Purpose: Enables role-based access control (RBAC).

2. Students Table (students)
This table stores student details and their relationship with teachers and parents.

student_id – Unique identifier for each student.
name – Student's full name.
class – Class or grade level.
teacher_id – Links to the teacher responsible for the student (from users).
parent_id – Links to the parent of the student (from users).
💡 Purpose:

Helps associate students with specific teachers and parents.
Useful for tracking student progress and interventions.
3. Subjects Table (subjects)
This table stores different subjects offered in the academic system.

subject_id – Unique identifier for each subject.
subject_name – Name of the subject (e.g., Mathematics, Science).
💡 Purpose:

Allows flexibility in tracking test scores for multiple subjects.
4. Performance Table (performance)
Tracks students' academic and non-academic performance.

performance_id – Unique identifier.
student_id – Links to the student (from students).
subject_id – Links to the subject (from subjects).
attendance – Percentage of classes attended (0-100).
test_score – Score in the subject (0-100).
extracurricular_participation – Participation score in extracurricular activities (0-100).
behavior_score – Behavior rating (0-100).
💡 Purpose:

Stores student academic performance in multiple subjects.
Tracks non-academic factors like behavior and extracurricular participation.
5. Alerts Table (alerts)
Stores alerts triggered by low performance, attendance, or behavior issues.

alert_id – Unique identifier.
student_id – Links to the affected student (from students).
message – Description of the issue.
status – Indicates if the alert is pending or resolved.
created_at – Timestamp of when the alert was generated.
💡 Purpose:

Notifies parents and teachers of student issues.
Helps in taking timely actions for improvement.
6. Interventions Table (interventions)
Stores actions taken to help students improve performance.

intervention_id – Unique identifier.
student_id – Links to the student (from students).
intervention – Description of the action taken.
outcome – Results of the intervention (optional).
date – Timestamp of when the intervention was applied.
💡 Purpose:

Helps track and evaluate strategies used to improve student performance.
7. Feedback Table (feedback)
Stores feedback on the effectiveness of interventions.

feedback_id – Unique identifier.
intervention_id – Links to the intervention (from interventions).
feedback – Comments or evaluation of the intervention.
given_at – Timestamp of when feedback was provided.
💡 Purpose:

Collects insights to refine future interventions.
📌 Summary of Relationships
Users (teachers & parents) → Students (A teacher/parent is linked to students).
Students → Performance (Each student has performance records).
Students → Alerts (Alerts are generated for specific students).
Students → Interventions (Interventions are applied to students).
Interventions → Feedback (Feedback is collected on interventions).

# Frontend
📌 Full Explanation of the Academic Performance Dashboard Frontend
This fully implemented frontend provides a user-friendly interface for managing student performance, interventions, and alerts. It follows modern UI/UX principles and integrates smoothly with the backend API.  


🖥️ 1. User Login System
🔹 Users (Admin, Teacher, Parent) log in via a secure form.  
🔹 Backend authentication (`/login` API) checks credentials and assigns a role (`admin`, `teacher`, or `parent`).  
🔹 Session-based role handling ensures users see only what they’re allowed to access.  

💻 Login Code Flow:
1. The login form collects `username` and `password`.
2. A `fetch` request sends data to `/login`.
3. If successful, the dashboard is displayed; otherwise, an error message appears.


📊 2. Dashboard Overview
🔹 Displays student performance data in bar charts using Chart.js.  
🔹 Alerts section lists students with low attendance or test scores.  
🔹 Role-based visibility ensures only authorized users can modify data.  

💻 Performance Visualization Code Flow:
1. Calls `/generate_report` API to fetch student attendance & test scores.  
2. Uses Chart.js to render bar charts dynamically.  
3. Calls `/analyze_trends` API to display alerts for underperforming students.  


⚠️ 3. Student Alerts System
🔹 Detects at-risk students (low attendance or test scores).  
🔹 Displays alerts in a Bootstrap-styled list for quick visibility.  
🔹 Uses `/analyze_trends` API to check students needing intervention.  


🧠 4. AI-Powered Intervention Prediction
🔹 Predicts recommended interventions based on attendance, test scores, extracurricular activities, and behavior.  
🔹 Calls `/predict_intervention` API using the form inputs.  
🔹 Displays a suggested intervention (e.g., tutoring, mentorship) based on machine learning predictions.  

💻 Intervention Form Code Flow:
1. User enters student details (attendance, scores, etc.).  
2. A fetch request sends data to `/predict_intervention`.  
3. The response contains a recommended intervention, which is displayed dynamically.  


📝 5. Feedback Submission System
🔹 Teachers/Parents provide feedback on assigned interventions.  
🔹 Calls `/add_feedback` API and displays confirmation messages.  

💻 Feedback Form Code Flow:
1. User enters intervention ID & feedback.  
2. A fetch request submits feedback to `/add_feedback`.  
3. A success message confirms submission.  

🎯 6. Fully Responsive & User-Friendly Design
✔ Bootstrap styling for a clean, modern UI.  
✔ Mobile-friendly layout ensures usability on all devices.  
✔ Instant feedback messages guide users smoothly.  
✔ Charts & interactive elements improve visualization.  


📌 Summary of Features
✅ Secure login with role-based access
✅ Performance tracking with interactive charts 
✅ Real-time alerts for at-risk students
✅ AI-powered intervention suggestions 
✅ Feedback system for monitoring interventions 
✅ Responsive design for desktops & mobile devices
🚀 Benefits of This Database
✅ Scalability – Can handle multiple subjects and students.
✅ Data Integrity – Uses FOREIGN KEY constraints to maintain relationships.
✅ Flexibility – Supports both academic and behavioral tracking.
✅ Automation Potential – Can integrate machine learning (e.g., Decision Trees) for predicting student risks.
