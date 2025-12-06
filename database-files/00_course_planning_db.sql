DROP DATABASE IF EXISTS course_planning_db;
CREATE DATABASE course_planning_db;
USE course_planning_db;

DROP TABLE IF EXISTS Flag_course;
DROP TABLE IF EXISTS Flag_section;
DROP TABLE IF EXISTS Scheduled_in;
DROP TABLE IF EXISTS Course_req;
DROP TABLE IF EXISTS Course_plan;
DROP TABLE IF EXISTS Stu_degr;
DROP TABLE IF EXISTS StudentPlan;
DROP TABLE IF EXISTS OverrideRequest;
DROP TABLE IF EXISTS Rating;
DROP TABLE IF EXISTS Professor;
DROP TABLE IF EXISTS Section;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Requirements;
DROP TABLE IF EXISTS DegreePrograms;
DROP TABLE IF EXISTS Term;
DROP TABLE IF EXISTS DataQualityIssue;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS SystemSetting;



CREATE TABLE SystemSetting (
   settingKey      VARCHAR(100) PRIMARY KEY,
   settingValue    VARCHAR(255) NOT NULL,
   description     VARCHAR(255)
);


CREATE TABLE Term (
   termID      INT PRIMARY KEY,
   name        VARCHAR(100) NOT NULL,
   startDate   DATE NOT NULL,
   endDate     DATE NOT NULL
);


CREATE TABLE DataQualityIssue (
   issueID     INT PRIMARY KEY,
   issueType   VARCHAR(100) NOT NULL,
   createdAt   DATETIME NOT NULL,
   status      VARCHAR(50) NOT NULL,
   severity    VARCHAR(50) NOT NULL,
   resolvedAt  DATETIME
);


CREATE TABLE Department (
   deptID      INT PRIMARY KEY,
   deptName    VARCHAR(100) NOT NULL
);


CREATE TABLE DegreePrograms (
   programID   INT PRIMARY KEY,
   program     VARCHAR(100) NOT NULL,
   type        VARCHAR(50)  NOT NULL
);


CREATE TABLE Requirements (
   requirementID   INT PRIMARY KEY,
   creditsNeeded   INT NOT NULL,
   requirementType VARCHAR(100) NOT NULL,
   corequisites    VARCHAR(255),
   prerequisites   VARCHAR(255)
);


CREATE TABLE Student (
   studentID        INT PRIMARY KEY,
   mobile           VARCHAR(20),
   email            VARCHAR(150),
   credits_completed INT,
   year             INT,
   f_name            VARCHAR(100),
   l_name            VARCHAR(100),
   mid_names         VARCHAR(150)
);


CREATE TABLE Course (
   courseID         INT PRIMARY KEY,
   course_name       VARCHAR(150) NOT NULL,
   semesters_offered VARCHAR(100),
   Status           VARCHAR(50),
   credits          INT,
   description      VARCHAR(255),
   deptID           INT,
   FOREIGN KEY (deptID) REFERENCES Department(deptID)
);


CREATE TABLE Section (
   CRN         INT PRIMARY KEY,
   location    VARCHAR(50),
   day_of_week   VARCHAR(20),
   section_num  VARCHAR(10),
   start_time  TIME,
   end_time    TIME,
   semester    VARCHAR(50),
   capacity    INT,
   FOREIGN KEY (CRN) REFERENCES Course(courseID)
);




CREATE TABLE Professor (
   profID      INT PRIMARY KEY,
   first_name  VARCHAR(100) NOT NULL,
   last_name   VARCHAR(100) NOT NULL,
   department  VARCHAR(100),
   hire_date    DATE,
   deptID      INT,
   FOREIGN KEY (deptID) REFERENCES Department(deptID)
);


CREATE TABLE Rating (
   profID      INT,
   rated_num    INT,
   created_aT   DATETIME NOT NULL,
   rating      DECIMAL(3,2),
   comment     VARCHAR(255),
   PRIMARY KEY (profID, rated_num),
   FOREIGN KEY (profID) REFERENCES Professor(profID)
);


CREATE TABLE OverrideRequest (
   request_id      INT PRIMARY KEY,
   request_date    DATE NOT NULL,
   status          VARCHAR(50) NOT NULL,
   student_message TEXT,
   decision_date   DATE,
   studentID       INT NOT NULL,
   CRN             INT NOT NULL,
   FOREIGN KEY (studentID) REFERENCES Student(studentID),
   FOREIGN KEY (CRN) REFERENCES Section(CRN)
);


CREATE TABLE StudentPlan (
   planID       INT PRIMARY KEY,
   date_created  DATE,
   plan_name     VARCHAR(150),
   is_active     TINYINT(1),
   expected_grad DATE,
   programID    INT,
   FOREIGN KEY (programID) REFERENCES DegreePrograms(programID)
);




CREATE TABLE Stu_degr (
   studentID INT,
   programID INT,
   PRIMARY KEY (studentID, programID),
   FOREIGN KEY (studentID) REFERENCES Student(studentID),
   FOREIGN KEY (programID) REFERENCES DegreePrograms(programID)
);


CREATE TABLE Course_req (
   courseID      INT,
   requirementID INT,
   PRIMARY KEY (courseID, requirementID),
   FOREIGN KEY (courseID) REFERENCES Course(courseID),
   FOREIGN KEY (requirementID) REFERENCES Requirements(requirementID)
);


CREATE TABLE Course_plan (
   planID          INT,
   courseID        INT,
   planned_semester VARCHAR(50),
   course_status VARCHAR(50),
   PRIMARY KEY (planID, courseID),
   FOREIGN KEY (planID) REFERENCES StudentPlan(planID),
   FOREIGN KEY (courseID) REFERENCES Course(courseID)
);


CREATE TABLE Scheduled_in (
   termID INT,
   CRN    INT,
   PRIMARY KEY (termID, CRN),
   FOREIGN KEY (termID) REFERENCES Term(termID),
   FOREIGN KEY (CRN) REFERENCES Section(CRN)
);


CREATE TABLE Flag_course (
   issueID  INT,
   CourseID INT,
   PRIMARY KEY (issueID, courseID),
   FOREIGN KEY (issueID) REFERENCES DataQualityIssue(issueID),
   FOREIGN KEY (courseID) REFERENCES Course(courseID)
);


CREATE TABLE Flag_section (
   issueID INT,
   CRN INT,
   PRIMARY KEY (issueID, CRN),
   FOREIGN KEY (issueID) REFERENCES DataQualityIssue(issueID),
   FOREIGN KEY (CRN) REFERENCES Section(CRN)
);

CREATE TABLE Enrollment (
    studentID INT,
    CRN INT,
    grade DECIMAL(4,2),
    enrollment_status VARCHAR(50),
    PRIMARY KEY (studentID, CRN),
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (CRN) REFERENCES Section(CRN)
);








INSERT INTO SystemSetting (settingKey, settingValue, description) VALUES
('max_enroll', '35', 'Default maximum enrollment'),
('override_deadline_days', '7', 'Override cutoff after term start');


INSERT INTO Term (termID, name, startDate, endDate) VALUES
(1, 'Fall 2025',   '2025-09-01', '2025-12-15'),
(2, 'Spring 2026', '2026-01-10', '2026-05-05');


INSERT INTO Department (deptID, deptName) VALUES
(10, 'Computer Science'),
(20, 'Mathematics');


INSERT INTO DegreePrograms (programID, program, type) VALUES
(1, 'BS Computer Science', 'Undergraduate'),
(2, 'BS Data Science',     'Undergraduate');


INSERT INTO Requirements (requirementID, creditsNeeded, requirementType, corequisites, prerequisites) VALUES
(1, 120, 'Major Core', 'None',  'Intro Programming'),
(2,  60, 'Minor',      'None',  'Calculus I');




INSERT INTO Student (studentID, mobile, email, credits_completed, year, f_name, l_name, mid_names) VALUES
(1001, '555-1234', 'alice@example.edu', 30, 2, 'Alice', 'Smith', 'Marie'),
(1002, '555-5678', 'bob@example.edu',   90, 4, 'Bob',   'Jones',  NULL);




INSERT INTO Course (courseID, course_name, semesters_offered, Status, credits, description, deptID) VALUES
(101, 'CS2500 - Fundamentals of CS', 'Fall,Spring', 'Active', 4, 'Intro programming in Java', 10),
(102, 'CS2510 - Data Structures',    'Fall',        'Active', 4, 'Algorithms and data structures', 10);




INSERT INTO Section (CRN, location, day_of_week, section_num, start_time, end_time, semester, capacity) VALUES
(101, 'SN101', 'Mon/Wed', '01', '09:00:00', '10:15:00', 'Fall 2025', 35),
(102, 'SN102', 'Tue/Thu', '01', '11:00:00', '12:15:00', 'Fall 2025', 30);


INSERT INTO Professor (profID, first_name, last_name, department, hire_date, deptID) VALUES
(501, 'Grace', 'Hopper', 'Computer Science', '2010-08-15', 10),
(502, 'Alan',  'Turing', 'Computer Science', '2012-01-01', 10);


INSERT INTO Rating (profID, rated_num, created_aT, rating, comment) VALUES
(501, 1, '2025-10-01 12:00:00', 4.80, 'Great lecturer; very clear explanations'),
(502, 1, '2025-10-02 13:15:00', 3.50, 'Challenging but fair');




INSERT INTO DataQualityIssue (issueID, issueType, createdAt, status, severity, resolvedAt) VALUES
(1, 'Missing room',     '2025-08-20 10:00:00', 'Open',     'High',   NULL),
(2, 'Credits mismatch', '2025-08-22 09:30:00', 'Resolved', 'Medium', '2025-08-25 14:00:00');


INSERT INTO Stu_degr (studentID, programID) VALUES
(1001, 1),  -- Alice in BS CS
(1002, 1),  -- Bob in BS CS
(1002, 2);  -- Bob also in BS DS (double major)




INSERT INTO StudentPlan (planID, date_created, plan_name, is_active, expected_grad, programID) VALUES
(1, '2025-08-01', 'Alice CS Standard Plan', 1, '2027-05-01', 1),
(2, '2025-08-01', 'Bob DS Accelerated Plan', 1, '2026-12-15', 2);


INSERT INTO Course_req (courseID, requirementID) VALUES
(101, 1),
(102, 1);


INSERT INTO Course_plan (planID, courseID, planned_semester, course_status) VALUES
(1, 101, 'Fall 2025',   'Planned'),
(1, 102, 'Spring 2026', 'Planned'),
(2, 101, 'Fall 2025',   'Planned');




INSERT INTO Scheduled_in (termID, CRN) VALUES
(1, 101),
(1, 102);




INSERT INTO OverrideRequest (request_id, request_date, status, student_message, decision_date, studentID, CRN) VALUES
(1, '2025-09-05', 'Pending',  'Please add me; I meet the prereqs.',  NULL,          1001, 101),
(2, '2025-09-06', 'Approved', 'Need this course to graduate on time', '2025-09-07', 1002, 102);


INSERT INTO Flag_course (issueID, courseID) VALUES
(2, 101);  -- credits mismatch on CS2500


INSERT INTO Flag_section (issueID, CRN) VALUES
(1, 101);  -- missing room info for section 101

INSERT INTO Enrollment (studentID, CRN, grade, enrollment_status) VALUES
-- Section CRN 101 (CS2500 - Section 01, Mon/Wed 9:00-10:15)
(1001, 101, 92.5, 'Completed'),
(1002, 101, 88.0, 'Completed'),

-- Section CRN 102 (CS2510 - Section 01, Tue/Thu 11:00-12:15)
(1001, 102, 85.5, 'Enrolled'),
(1002, 102, 91.0, 'Dropped');
