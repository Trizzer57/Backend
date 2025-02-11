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
