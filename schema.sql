CREATE DATABASE academic_tool;
USE academic_tool;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Store hashed passwords
    role ENUM('teacher', 'parent', 'admin') NOT NULL
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(50) NOT NULL,
    teacher_id INT, -- Assigning a teacher
    parent_id INT, -- Linking parents
    FOREIGN KEY (teacher_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_id) REFERENCES users(user_id)
);

CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    attendance INT NOT NULL CHECK (attendance BETWEEN 0 AND 100),
    test_score INT NOT NULL CHECK (test_score BETWEEN 0 AND 100),
    extracurricular_participation INT DEFAULT 0 CHECK (extracurricular_participation BETWEEN 0 AND 100),
    behavior_score INT DEFAULT 50 CHECK (behavior_score BETWEEN 0 AND 100),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE TABLE alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    message VARCHAR(255) NOT NULL,
    status ENUM('pending', 'resolved') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE interventions (
    intervention_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    intervention TEXT NOT NULL,
    outcome TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    intervention_id INT NOT NULL,
    feedback TEXT NOT NULL,
    given_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);
