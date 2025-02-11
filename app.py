from flask import Flask, request, jsonify, session
from flask_mail import Mail, Message
from fpdf import FPDF
from Crypto.Cipher import AES
import base64
import pymysql
import firebase_admin
from firebase_admin import messaging
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'francischeboo404@gmail.com'
app.config['MAIL_PASSWORD'] = 'Fr@38998653'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

# Firebase Admin Initialization
firebase_admin.initialize_app()

# Database connection
def connect_db():
    return pymysql.connect(host='localhost', user='root', password='', database='academic_tool')

# Encryption helper functions
def encrypt(data, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return base64.b64encode(cipher.nonce + ciphertext).decode('utf-8')

def decrypt(encrypted_data, key):
    data = base64.b64decode(encrypted_data)
    nonce, ciphertext = data[:16], data[16:]
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode('utf-8')

@app.route('/admin/dashboard', methods=['GET'])
@requires_roles('admin')
def admin_dashboard():
    return "Admin Dashboard"

# Role-Based Access Control (RBAC)
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                return jsonify({"message": "Access denied"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# Audit logging
def log_audit(action):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO audit_logs (user_id, action, timestamp) VALUES (%s, %s, NOW())", (session.get('user_id'), action))
    db.commit()
    db.close()

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (data['username'], data['password']))
    user = cursor.fetchone()
    db.close()
    if user:
        session['user_id'] = user['user_id']
        session['role'] = user['role']
        log_audit('User login')
        return jsonify({"message": "Login successful!", "role": user['role']})
    return jsonify({"message": "Invalid credentials!"}), 401

# Insert or update performance data
@app.route('/performance', methods=['POST', 'PUT'])
@requires_roles('admin', 'teacher')
def manage_performance():
    data = request.json
    db = connect_db()
    cursor = db.cursor()
    if request.method == 'POST':
        cursor.execute("INSERT INTO performance (student_id, attendance, test_scores, extracurricular_participation, behavior_score) VALUES (%s, %s, %s, %s, %s)",
                       (data['student_id'], data['attendance'], data['test_scores'], data['extracurricular_participation'], data['behavior_score']))
        action = 'Insert performance data'
    else:
        cursor.execute("UPDATE performance SET attendance=%s, test_scores=%s, extracurricular_participation=%s, behavior_score=%s WHERE student_id=%s",
                       (data['attendance'], data['test_scores'], data['extracurricular_participation'], data['behavior_score'], data['student_id']))
        action = 'Update performance data'
    db.commit()
    db.close()
    log_audit(action)
    return jsonify({"message": f"Performance data {request.method.lower()}ed successfully!"})


@app.route('/add_performance', methods=['POST'])
add_performance():
    data = request.json
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("""INSERT INTO performance (student_id, attendance, test_scores, extracurricular_participation, behavior_score)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['student_id'], data['attendance'], data['test_scores'],
          data['extracurricular_participation'], data['behavior_score']))
    db.commit()
    db.close()

        return jsonify({"message": "Performance data added successfully!"})
    
    
def calculate_weighted_score(attendance, test_scores, extracurricular, behavior):
    return (0.4 * attendance) + (0.4 * test_scores) + (0.1 * extracurricular) + (0.1 * behavior)



# Dynamic threshold and trend analysis
@app.route('/analyze_trends', methods=['GET'])
@requires_roles('admin', 'teacher')
def analyze_trends():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT student_id, AVG(attendance) as avg_attendance, AVG(test_scores) as avg_scores FROM performance GROUP BY student_id")
    performance_data = cursor.fetchall()

    alerts = []
    for data in performance_data:
        if data['avg_attendance'] < 75 or data['avg_scores'] < 50:  # Example dynamic thresholds
            alerts.append({
                "student_id": data['student_id'],
                "message": "Performance is below acceptable thresholds."
            })

    db.close()
    log_audit('Trend analysis performed')
    return jsonify(alerts)


#Machine Learning Integration
from sklearn.linear_model import LinearRegression
import numpy as np

@app.route('/predict_risk', methods=['GET'])
def predict_risk():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT attendance, test_scores, extracurricular_participation, behavior_score FROM performance")
    data = cursor.fetchall()

    X = np.array([[d['attendance'], d['test_scores'], d['extracurricular_participation'], d['behavior_score']] for d in data])
    y = np.array([calculate_weighted_score(d['attendance'], d['test_scores'], d['extracurricular_participation'], d['behavior_score']) for d in data])

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)
    risks = ["High Risk" if pred < 50 else "Low Risk" for pred in predictions]

    db.close()
    return jsonify({"predictions": risks})



# Personalize Inverventions
from sklearn.tree import DecisionTreeClassifier
import numpy as np

@app.route('/predict_intervention', methods=['POST'])
def predict_intervention():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # Fetch intervention history
    cursor.execute("SELECT attendance, test_scores, extracurricular_participation, behavior_score, intervention FROM performance INNER JOIN interventions ON performance.student_id = interventions.student_id")
    data = cursor.fetchall()

    if not data:
        return jsonify({"message": "Not enough data for prediction"}), 400

    # Prepare data for the model
    X = np.array([[d['attendance'], d['test_scores'], d['extracurricular_participation'], d['behavior_score']] for d in data])
    y = np.array([d['intervention'] for d in data])

    # Train the model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # Predict intervention for a new student
    student_data = request.json  # e.g., {"attendance": 60, "test_scores": 50, "extracurricular_participation": 10, "behavior_score": 8}
    X_new = np.array([[student_data['attendance'], student_data['test_scores'], student_data['extracurricular_participation'], student_data['behavior_score']]])
    predicted_intervention = model.predict(X_new)

    db.close()

    return jsonify({"intervention": predicted_intervention[0]})

#@app.route('/add_intervention', methods=['POST'])
#def add_intervention():
#    data = request.json  # {"student_id": 1, "intervention": "Tutoring", "outcome": "Improved"}
#    db = connect_db()
#    cursor = db.cursor()
#    cursor.execute("INSERT INTO interventions (student_id, intervention, outcome) VALUES (%s, %s, %s)", data['student_id'], data['intervention'], data.get('outcome', None)))
#    db.commit()
#    db.close()
#    return jsonify({"message": "Intervention added successfully!"})

# Error Handling Example

@app.route('/add_intervention', methods=['POST'])
def add_intervention():
    try:
        data = request.json
        if not data.get('student_id') or not data.get('intervention'):
            return jsonify({"message": "Missing required fields!"}), 400

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO interventions (student_id, intervention, outcome)
            VALUES (%s, %s, %s)
        """, (data['student_id'], data['intervention'], data.get('outcome', None)))
        db.commit()
        db.close()
        return jsonify({"message": "Intervention added successfully!"})
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500




@app.route('/analyze_interventions', methods=['GET'])
def analyze_interventions():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT intervention, COUNT(*) as count, AVG(outcome = 'Improved') as success_rate FROM interventions GROUP BY intervention")
    data = cursor.fetchall()
    db.close()
    return jsonify(data)


# Integrated email notifications using Flask-Mail:
@app.route('/send_alerts', methods=['POST'])
def send_alerts():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT student_id, message FROM alerts")
    alerts = cursor.fetchall()

    for alert in alerts:
        # Example email logic
        msg = Message(
            subject="Student Performance Alert",
            sender=app.config['MAIL_USERNAME'],
            recipients=["parent@example.com"],
            body=alert['message']
        )
        mail.send(msg)

    db.close()
    return jsonify({"message": "Email alerts sent successfully!"})


# Added graphical representations to make reports visually informative using Chart.js:

@app.route('/generate_report', methods=['GET'])
def generate_report():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT student_id, attendance, test_scores FROM performance")
    performance_data = cursor.fetchall()
    db.close()

    # Generate graphical data for a dashboard (example JSON output)
    chart_data = {
        "labels": [str(d["student_id"]) for d in performance_data],
        "attendance": [d["attendance"] for d in performance_data],
        "test_scores": [d["test_scores"] for d in performance_data]
    }

    return jsonify(chart_data)



# Add calculated KPIs to the PDF:
@app.route('/kpi_report', methods=['GET'])
def kpi_report():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT AVG(attendance) as avg_attendance, AVG(test_scores) as avg_scores FROM performance")
    kpis = cursor.fetchone()
    db.close()

    insights = {
        "Average Attendance": kpis["avg_attendance"],
        "Average Test Scores": kpis["avg_scores"]
    }
    return jsonify(insights)


# Generate a PDF report with embedded bar and pie charts using matplotlib and fpdf:
import matplotlib.pyplot as plt
from fpdf import FPDF

@app.route('/export_pdf', methods=['GET'])
def export_pdf():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT student_id, attendance, test_scores FROM performance")
    data = cursor.fetchall()
    db.close()

    # Generate bar chart
    student_ids = [d['student_id'] for d in data]
    attendance = [d['attendance'] for d in data]
    test_scores = [d['test_scores'] for d in data]

    plt.bar(student_ids, attendance, color='blue', label='Attendance')
    plt.bar(student_ids, test_scores, color='green', label='Test Scores', alpha=0.5)
    plt.legend()
    plt.savefig("chart.png")
    plt.close()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Student Performance Report", ln=True, align="C")
    pdf.image("chart.png", x=10, y=20, w=180)
    pdf.output("performance_report.pdf")

    return jsonify({"message": "PDF report generated successfully!"})


# Added pdf report generation    
from fpdf import FPDF

@app.route('/export_pdf', methods=['GET'])
def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Student Performance Report", ln=True, align='C')

    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM performance")
    data = cursor.fetchall()

    for row in data:
        pdf.cell(200, 10, txt=f"Student ID: {row['student_id']} - Attendance: {row['attendance']} - Test Scores: {row['test_scores']}", ln=True)

    db.close()
    pdf.output("performance_report.pdf")
    return jsonify({"message": "PDF report generated successfully!"})
    
    for data in performance_data:
        if data['avg_score'] < 50 or data['avg_attendance'] < 75:
            message = "Student is at risk due to low performance or attendance."
            cursor.execute("INSERT INTO alerts (student_id, message) VALUES (%s, %s)", (data['student_id'], message))

    db.commit()
    db.close()
    return jsonify({"message": "Alerts generated successfully!"})


# Comprehensive Reporting
from flask import Response
import csv

@app.route('/export_reports', methods=['GET'])
def export_reports():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM performance")
    performance_data = cursor.fetchall()

    output = []
    for row in performance_data:
        output.append(row)

    csv_output = "student_id,attendance,test_scores\n"
    for data in output:
        csv_output += f"{data['student_id']},{data['attendance']},{data['test_scores']}\n"

    return Response(
        csv_output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=performance_reports.csv"}
    )

# Add feedback
@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    data = request.json  # {"intervention_id": 1, "feedback": "Effective"}
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO feedback (intervention_id, feedback) VALUES (%s, %s)", (data['intervention_id'], data['feedback']))
    db.commit()
    db.close()
    return jsonify({"message": "Feedback added successfully!"})


# Feedback analysis

@app.route('/refine_model', methods=['GET'])
def refine_model():
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT intervention, AVG(feedback = 'Effective') as effectiveness
        FROM feedback
        JOIN interventions ON feedback.intervention_id = interventions.intervention_id
        GROUP BY intervention
    """)
    data = cursor.fetchall()

    # Adjust weights based on effectiveness
    effectiveness_weights = {row['intervention']: row['effectiveness'] for row in data}
    db.close()

    # Example: Adjust decision tree logic
    global model_weights
    model_weights.update(effectiveness_weights)

    return jsonify({"message": "Model refined based on feedback!"})


# SCORM content upload
@app.route('/upload_scorm', methods=['POST'])
@requires_roles('admin')
def upload_scorm():
    file = request.files['file']
    file.save(f"/path/to/scorm/{file.filename}")
    log_audit('SCORM content uploaded')
    return jsonify({"message": "SCORM package uploaded successfully!"})

if __name__ == '__main__':
    app.run(debug=True)