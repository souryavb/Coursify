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
DROP TABLE IF EXISTS Enrollment;



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




CREATE TABLE Professor (
   profID      INT PRIMARY KEY,
   first_name  VARCHAR(100) NOT NULL,
   last_name   VARCHAR(100) NOT NULL,
   department  VARCHAR(100),
   hire_date    DATE,
   deptID      INT,
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
   profID      INT,
   courseID    INT,
   FOREIGN KEY (courseID) REFERENCES Course(courseID),
   FOREIGN KEY (profID) REFERENCES Professor(profID)
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
   planID        INT PRIMARY KEY,
   studentID     INT NOT NULL,
   date_created  DATE,
   plan_name     VARCHAR(150),
   is_active     TINYINT(1),
   expected_grad DATE,
   programID     INT,
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
   CRN     INT,
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
INSERT INTO Term (termID, name, startDate, endDate) VALUES
(3, 'Summer 2025', '2025-05-15', '2025-08-10'),
(4, 'Fall 2026',   '2026-09-01', '2026-12-15'),
(5, 'Spring 2027', '2027-01-10', '2027-05-05'),
(6, 'Summer 2026', '2026-05-15', '2026-08-10'),
(7, 'Fall 2027',   '2027-09-01', '2027-12-15'),
(8, 'Spring 2028', '2028-01-10', '2028-05-05');


INSERT INTO Department (deptID, deptName) VALUES
(10, 'Computer Science'),
(20, 'Mathematics');



INSERT INTO DegreePrograms (programID, program, type) VALUES
(1, 'BS Computer Science', 'Undergraduate'),
(2, 'BS Data Science',     'Undergraduate');


INSERT INTO DegreePrograms (programID, program, type) VALUES
(3, 'BS Computer Science and Mathematics', 'Undergraduate'),
(4, 'BS Data Science and Business',        'Undergraduate'),
(5, 'BS Cybersecurity',                    'Undergraduate'),
(6, 'MS Computer Science',                 'Graduate'),
(7, 'MS Data Science',                     'Graduate'),
(8, 'MS Artificial Intelligence',          'Graduate');


INSERT INTO Requirements (requirementID, creditsNeeded, requirementType, corequisites, prerequisites) VALUES
(1, 120, 'Major Core', 'None',  'Intro Programming'),
(2,  60, 'Minor',      'None',  'Calculus I');

INSERT INTO Requirements (requirementID, creditsNeeded, requirementType, corequisites, prerequisites) VALUES
(3,  40, 'Math Core',          'None',               'Calculus II'),
(4,  16, 'CS Electives',       'None',               'Data Structures'),
(5,  16, 'Math Electives',     'None',               'Linear Algebra'),
(6,   4, 'Capstone',           'Senior standing',    'Core major courses'),
(7,  12, 'General Education',  'None',               'First-year writing'),
(8,   8, 'Lab Science',        'Lab co-enrollment',  'Intro Physics'),
(9,  20, 'Open Electives',     'None',               'At least sophomore standing'),
(10, 15, 'Data Science Core',  'None',               'Intro to DS');





INSERT INTO Student (studentID, mobile, email, credits_completed, year, f_name, l_name, mid_names) VALUES
(1001, '555-1234', 'andrea.silva@example.edu', 30, 2, 'Andrea', 'Silva', NULL),
(1002, '555-5678', 'bob@example.edu',   90, 4, 'Bob',   'Jones',  NULL);



INSERT INTO Student (studentID, mobile, email, credits_completed, year, f_name, l_name, mid_names) VALUES

(1003, '555-8395', 'carol.taylor3@example.edu', 53, 2, 'Carol', 'Taylor', 'A.'),
(1004, '555-7555', 'david.brown4@example.edu', 119, 4, 'David', 'Brown', 'A.'),
(1005, '555-5945', 'emma.wilson5@example.edu', 52, 2, 'Emma', 'Wilson', 'A.'),
(1006, '555-2458', 'frank.martin6@example.edu', 87, 3, 'Frank', 'Martin', NULL),
(1007, '555-9578', 'grace.lee7@example.edu', 86, 3, 'Grace', 'Lee', 'A.'),
(1008, '555-3703', 'hannah.clark8@example.edu', 89, 3, 'Hannah', 'Clark', 'A.'),
(1009, '555-6391', 'ian.hall9@example.edu', 21, 1, 'Ian', 'Hall', 'A.'),
(1010, '555-4966', 'julia.young10@example.edu', 60, 2, 'Julia', 'Young', NULL),
(1011, '555-8448', 'kevin.king11@example.edu', 120, 4, 'Kevin', 'King', NULL),
(1012, '555-5593', 'liam.wright12@example.edu', 25, 1, 'Liam', 'Wright', NULL),
(1013, '555-9787', 'mia.lopez13@example.edu', 22, 1, 'Mia', 'Lopez', 'A.'),
(1014, '555-4107', 'noah.hill14@example.edu', 24, 1, 'Noah', 'Hill', 'A.'),
(1015, '555-8469', 'olivia.scott15@example.edu', 80, 3, 'Olivia', 'Scott', NULL),
(1016, '555-3264', 'peter.green16@example.edu', 52, 2, 'Peter', 'Green', 'A.'),
(1017, '555-4716', 'quinn.adams17@example.edu', 22, 1, 'Quinn', 'Adams', 'A.'),
(1018, '555-9069', 'ryan.baker18@example.edu', 87, 3, 'Ryan', 'Baker', NULL),
(1019, '555-5264', 'sara.gonzalez19@example.edu', 87, 3, 'Sara', 'Gonzalez', 'A.'),
(1020, '555-7334', 'tom.nelson20@example.edu', 83, 3, 'Tom', 'Nelson', 'A.'),
(1021, '555-7017', 'uma.carter21@example.edu', 84, 3, 'Uma', 'Carter', NULL),
(1022, '555-8985', 'victor.mitchell22@example.edu', 120, 4, 'Victor', 'Mitchell', 'A.'),
(1023, '555-4654', 'wendy.perez23@example.edu', 85, 3, 'Wendy', 'Perez', NULL),
(1024, '555-2521', 'xavier.roberts24@example.edu', 25, 1, 'Xavier', 'Roberts', NULL),
(1025, '555-7248', 'yara.turner25@example.edu', 83, 3, 'Yara', 'Turner', 'A.'),
(1026, '555-8774', 'zoe.phillips26@example.edu', 58, 2, 'Zoe', 'Phillips', 'A.'),
(1027, '555-3899', 'nate.campbell27@example.edu', 29, 1, 'Nate', 'Campbell', 'A.'),
(1028, '555-8786', 'isha.parker28@example.edu', 89, 3, 'Isha', 'Parker', 'A.'),
(1029, '555-4384', 'priya.evans29@example.edu', 110, 4, 'Priya', 'Evans', 'A.'),
(1030, '555-8306', 'omar.taylor30@example.edu', 112, 4, 'Omar', 'Taylor', NULL);




INSERT INTO Course (courseID, course_name, semesters_offered, Status, credits, description, deptID) VALUES
(101, 'CS2500 - Fundamentals of CS', 'Fall,Spring', 'Active', 4, 'Intro programming in Java', 10),
(102, 'CS2510 - Data Structures',    'Fall',        'Active', 4, 'Algorithms and data structures', 10);



INSERT INTO Course (courseID, course_name, semesters_offered, Status, credits, description, deptID) VALUES
(103, 'CS2800 - Logic and Computation',           'Fall',        'Active', 3, 'Logic and Computation course.', 10),
(104, 'CS3000 - Algorithms & Data',               'Spring',      'Active', 4, 'Algorithms & Data course.',     10),
(105, 'CS3200 - Database Design',                 'Fall,Spring', 'Active', 4, 'Database Design course.',       10),
(106, 'CS3500 - Object-Oriented Design',          'Fall',        'Active', 4, 'Object-Oriented Design course.',10),
(107, 'CS3650 - Computer Systems',                'Fall,Spring', 'Active', 4, 'Computer Systems course.',      10),
(108, 'CS3700 - Networks & Distributed Sys',      'Spring',      'Active', 4, 'Networks & Distributed Sys course.', 10),
(109, 'CS4100 - AI',                              'Fall',        'Active', 4, 'AI course.',                    10),
(110, 'CS4300 - Machine Learning',                'Fall,Spring', 'Active', 4, 'Machine Learning course.',      10),
(111, 'CS4520 - Mobile App Dev',                  'Spring',      'Active', 4, 'Mobile App Dev course.',        10),
(112, 'CS4550 - Web Development',                 'Fall,Summer', 'Active', 4, 'Web Development course.',       10),
(113, 'MATH1341 - Calculus 1',                    'Fall,Spring', 'Active', 4, 'Calculus 1 course.',            20),
(114, 'MATH1342 - Calculus 2',                    'Fall',        'Active', 4, 'Calculus 2 course.',            20),
(115, 'MATH2331 - Linear Algebra',                'Spring',      'Active', 4, 'Linear Algebra course.',        20),
(116, 'MATH3081 - Probability & Stats',           'Fall,Spring', 'Active', 4, 'Probability & Stats course.',   20),
(117, 'MATH2341 - Diff Eq',                       'Fall',        'Active', 4, 'Diff Eq course.',               20),
(118, 'CS1210 - CS & Society',                    'Fall',        'Active', 3, 'CS & Society course.',          10),
(119, 'CS3001 - Special Topics in CS',            'Spring',      'Active', 3, 'Special Topics in CS course.',  10),
(120, 'DS2000 - Intro to DS',                     'Fall',        'Active', 4, 'Intro to DS course.',           10),
(121, 'DS3000 - Foundations of DS',               'Spring',      'Active', 4, 'Foundations of DS course.',     10),
(122, 'DS3500 - Adv DS',                          'Fall,Spring', 'Active', 4, 'Adv DS course.',                10),
(123, 'CS4410 - Compilers',                       'Fall',        'Active', 4, 'Compilers course.',             10),
(124, 'CS4700 - Network Security',                'Spring',      'Active', 4, 'Network Security course.',      10),
(125, 'CS4500 - Software Dev',                    'Fall',        'Active', 4, 'Software Dev course.',          10),
(126, 'CS4800 - Algorithms',                      'Fall,Spring', 'Active', 4, 'Algorithms course.',            10),
(127, 'MATH1250 - Discrete Math',                 'Fall',        'Active', 4, 'Discrete Math course.',         20),
(128, 'MATH2001 - Intro Math Reasoning',          'Spring',      'Active', 4, 'Intro Math Reasoning course.',  20),
(129, 'MATH4573 - Numerical Analysis',            'Fall',        'Active', 3, 'Numerical Analysis course.',    20),
(130, 'MATH2342 - Stats for Eng',                 'Fall,Spring', 'Active', 3, 'Stats for Eng course.',         20);




INSERT INTO Professor (profID, first_name, last_name, department, hire_date, deptID) VALUES
(501, 'Grace', 'Hopper', 'Computer Science', '2010-08-15', 10),
(502, 'Alan',  'Turing', 'Computer Science', '2012-01-01', 10);




INSERT INTO Professor (profID, first_name, last_name, department, hire_date, deptID) VALUES
(503, 'Ada',      'Lovelace',    'Computer Science', '2019-01-15', 10),
(504, 'Edsger',   'Dijkstra',    'Mathematics',      '2019-08-28', 20),
(505, 'Barbara',  'Liskov',      'Computer Science', '2017-12-13', 10),
(506, 'Donald',   'Knuth',       'Mathematics',      '2014-03-21', 20),
(507, 'Tim',      'Berners-Lee', 'Computer Science', '2016-11-09', 10),
(508, 'Linus',    'Torvalds',    'Mathematics',      '2020-07-04', 20),
(509, 'Margaret', 'Hamilton',    'Computer Science', '2015-04-18', 10),
(510, 'Ken',      'Thompson',    'Mathematics',      '2012-10-12', 20),
(511, 'Dennis',   'Ritchie',     'Computer Science', '2011-06-23', 10),
(512, 'James',    'Gosling',     'Mathematics',      '2021-09-15', 20),
(513, 'John',     'McCarthy',    'Computer Science', '2013-05-19', 10),
(514, 'Leslie',   'Lamport',     'Mathematics',      '2018-02-22', 20),
(515, 'Niklaus',  'Wirth',       'Computer Science', '2010-01-10', 10),
(516, 'Bjarne',   'Stroustrup',  'Mathematics',      '2016-04-05', 20),
(517, 'Evelyn',   'Boyd',        'Computer Science', '2017-09-30', 10),
(518, 'Katherine','Johnson',     'Mathematics',      '2012-03-08', 20),
(519, 'George',   'Boole',       'Computer Science', '2013-12-01', 10),
(520, 'Mary',     'Klein',       'Mathematics',      '2015-08-14', 20),
(521, 'Andrew',   'Ng',          'Computer Science', '2018-07-19', 10),
(522, 'Ravi',     'Kumar',       'Mathematics',      '2019-05-25', 20),
(523, 'Sunita',   'Patel',       'Computer Science', '2016-02-11', 10),
(524, 'Anita',    'Borg',        'Mathematics',      '2011-11-03', 20),
(525, 'Raj',      'Gupta',       'Computer Science', '2020-09-07', 10),
(526, 'Sanjay',   'Mehta',       'Mathematics',      '2014-06-29', 20),
(527, 'Helen',    'Chen',        'Computer Science', '2013-10-17', 10),
(528, 'Victor',   'Garcia',      'Mathematics',      '2017-01-27', 20),
(529, 'Carlos',   'Silva',       'Computer Science', '2018-03-02', 10),
(530, 'Andrew',   'Parker',      'Mathematics',      '2021-04-09', 20);

INSERT INTO Section (CRN, location, day_of_week, section_num, start_time, end_time, semester, capacity, profID, courseID) VALUES
(101, 'SN101', 'Mon/Wed', '01', '09:00:00', '10:15:00', 'Fall 2025',10, 501, 128),
(102, 'SN102', 'Tue/Thu', '01', '11:00:00', '12:15:00', 'Fall 2025',20, 502, 129);


INSERT INTO Section (CRN, location, day_of_week, section_num, start_time, end_time, semester, capacity, profID, courseID) VALUES
(103, 'RY140', 'Tue/Thu', '04', '09:00:00', '10:15:00', 'Spring 2027', 40, 529, 120),
(104, 'SN102', 'Wed',     '01', '14:00:00', '15:15:00', 'Spring 2026', 40, 501, 103),
(105, 'WVH210','Mon/Wed', '02', '08:00:00', '09:15:00', 'Fall 2025',   35, 512, 104),
(106, 'WVH220','Tue/Thu', '01', '10:00:00', '11:15:00', 'Fall 2025',   30, 503, 105),
(107, 'SN101', 'Mon/Wed', '03', '11:00:00', '12:15:00', 'Spring 2026', 40, 504, 106),
(108, 'RY140', 'Mon',     '01', '13:00:00', '14:15:00', 'Fall 2026',   30, 505, 107),
(109, 'SH305', 'Tue/Thu', '02', '09:00:00', '10:15:00', 'Fall 2026',   35, 506, 108),
(110, 'CN100', 'Fri',     '01', '10:00:00', '11:15:00', 'Spring 2026', 30, 507, 109),
(111, 'CN110', 'Mon/Wed', '01', '15:00:00', '16:15:00', 'Spring 2026', 40, 508, 110),
(112, 'WVH210','Tue/Thu', '03', '08:00:00', '09:15:00', 'Fall 2025',   35, 509, 111),
(113, 'WVH220','Mon',     '01', '09:00:00', '10:15:00', 'Fall 2025',   30, 510, 112),
(114, 'SN101', 'Wed',     '02', '11:00:00', '12:15:00', 'Spring 2027', 35, 511, 113),
(115, 'SN102', 'Tue/Thu', '01', '13:00:00', '14:15:00', 'Spring 2027', 40, 512, 114),
(116, 'RY140', 'Mon/Wed', '02', '10:00:00', '11:15:00', 'Fall 2026',   35, 513, 115),
(117, 'SH305', 'Tue/Thu', '03', '14:00:00', '15:15:00', 'Fall 2026',   40, 514, 116),
(118, 'CN100', 'Mon',     '01', '08:00:00', '09:15:00', 'Spring 2026', 30, 515, 117),
(119, 'CN110', 'Wed',     '02', '09:00:00', '10:15:00', 'Spring 2026', 35, 516, 118),
(120, 'WVH210','Tue/Thu', '01', '11:00:00', '12:15:00', 'Fall 2025',   40, 517, 119),
(121, 'WVH220','Mon/Wed', '02', '13:00:00', '14:15:00', 'Fall 2025',   35, 518, 120),
(122, 'SN101', 'Tue/Thu', '03', '15:00:00', '16:15:00', 'Spring 2026', 40, 519, 121),
(123, 'SN102', 'Mon',     '01', '08:00:00', '09:15:00', 'Spring 2026', 30, 520, 122),
(124, 'RY140', 'Wed',     '02', '09:00:00', '10:15:00', 'Fall 2026',   35, 521, 123),
(125, 'SH305', 'Tue/Thu', '01', '10:00:00', '11:15:00', 'Fall 2026',   40, 522, 124),
(126, 'CN100', 'Mon/Wed', '03', '11:00:00', '12:15:00', 'Spring 2027', 35, 523, 125),
(127, 'CN110', 'Tue/Thu', '02', '13:00:00', '14:15:00', 'Spring 2027', 40, 524, 126),
(128, 'WVH210','Mon',     '01', '15:00:00', '16:15:00', 'Fall 2025',   30, 525, 127),
(129, 'WVH220','Wed',     '03', '08:00:00', '09:15:00', 'Fall 2025',   35, 526, 128),
(130, 'SN101', 'Tue/Thu', '02', '09:00:00', '10:15:00', 'Spring 2026', 40, 527, 129),
(131, 'SN102', 'Mon/Wed', '01', '10:00:00', '11:15:00', 'Spring 2026', 35, 528, 130),
(132, 'RY140', 'Tue/Thu', '04', '11:00:00', '12:15:00', 'Fall 2026',   40, 529, 101),
(133, 'SH305', 'Mon',     '01', '13:00:00', '14:15:00', 'Fall 2026',   30, 530, 102),
(134, 'CN100', 'Wed',     '02', '14:00:00', '15:15:00', 'Spring 2027', 35, 503, 103),
(135, 'CN110', 'Tue/Thu', '03', '15:00:00', '16:15:00', 'Spring 2027', 40, 504, 104),
(136, 'WVH210','Mon/Wed', '01', '08:00:00', '09:15:00', 'Fall 2025',   35, 505, 105),
(137, 'WVH220','Tue/Thu', '02', '09:00:00', '10:15:00', 'Fall 2025',   40, 506, 106),
(138, 'SN101', 'Mon',     '03', '10:00:00', '11:15:00', 'Spring 2026', 35, 507, 107),
(139, 'SN102', 'Wed',     '01', '11:00:00', '12:15:00', 'Spring 2026', 30, 508, 108),
(140, 'RY140', 'Tue/Thu', '02', '13:00:00', '14:15:00', 'Fall 2026',   40, 509, 109);

INSERT INTO Rating (profID, rated_num, created_aT, rating, comment) VALUES
(501, 1, '2025-10-01 12:00:00', 4.80, 'Great lecturer; very clear explanations'),
(502, 1, '2025-10-02 13:15:00', 3.50, 'Challenging but fair');

INSERT INTO Rating (profID, rated_num, created_aT, rating, comment) VALUES
(501, 2, '2025-10-05 12:34:00', 4.25, 'Engaging lectures and fair grading'),
(501, 3, '2025-10-12 09:21:00', 4.90, 'Very approachable during office hours'),
(502, 2, '2025-10-08 15:44:00', 3.90, 'Heavy workload but learned a lot'),
(502, 3, '2025-10-16 11:03:00', 4.10, 'Organized and responsive'),
(503, 1, '2025-10-01 10:10:00', 4.70, 'Engaging lectures and fair grading'),
(503, 2, '2025-10-09 13:15:00', 4.30, 'Tough exams but curves generously'),
(504, 1, '2025-10-03 09:05:00', 3.80, 'Great slides, assignments unclear at times'),
(504, 2, '2025-10-14 16:20:00', 4.00, 'Very approachable during office hours');



INSERT INTO DataQualityIssue (issueID, issueType, createdAt, status, severity, resolvedAt) VALUES
(1, 'Missing room',     '2025-08-20 10:00:00', 'Open',     'High',   NULL),
(2, 'Credits mismatch', '2025-08-22 09:30:00', 'Resolved', 'Medium', '2025-08-25 14:00:00');

INSERT INTO DataQualityIssue (issueID, issueType, createdAt, status, severity, resolvedAt) VALUES
(3, 'Invalid term',              '2025-08-22 10:00:00', 'In Progress', 'High',    NULL),
(4, 'Missing prereq',            '2025-08-10 12:00:00', 'Open',        'Medium',  NULL),
(5, 'Missing room',              '2025-08-03 02:00:00', 'Resolved',    'Low',     '2025-08-05 00:00:00'),
(6, 'Credits mismatch',          '2025-08-23 07:00:00', 'Resolved',    'Medium',  '2025-08-26 00:00:00'),
(7, 'Over capacity',             '2025-08-16 05:00:00', 'In Progress', 'High',    NULL),
(8, 'Time conflict',             '2025-08-29 08:00:00', 'Open',        'High',    NULL),
(9, 'Missing description',       '2025-08-02 09:00:00', 'Open',        'Low',     NULL),
(10,'Inactive course scheduled', '2025-08-26 06:00:00', 'Resolved',    'Medium',  '2025-08-29 00:00:00'),
(11,'Duplicate section',         '2025-08-09 09:00:00', 'Open',        'Low',     NULL),
(12,'Missing professor',         '2025-08-05 10:00:00', 'In Progress', 'High',    NULL),
(13,'Over capacity',             '2025-08-31 05:00:00', 'Resolved',    'Medium',  '2025-09-02 00:00:00'),
(14,'Missing room',              '2025-08-06 00:00:00', 'Open',        'Medium',  NULL),
(15,'Credits mismatch',          '2025-08-12 00:00:00', 'Open',        'High',    NULL),
(16,'Missing prereq',            '2025-08-18 00:00:00', 'Resolved',    'Medium',  '2025-08-21 00:00:00'),
(17,'Invalid term',              '2025-08-01 00:00:00', 'Open',        'Low',     NULL),
(18,'Duplicate section',         '2025-08-30 00:00:00', 'In Progress', 'Medium',  NULL),
(19,'Over capacity',             '2025-08-07 00:00:00', 'Open',        'High',    NULL),
(20,'Time conflict',             '2025-08-25 00:00:00', 'Resolved',    'High',    '2025-08-27 00:00:00'),
(21,'Missing professor',         '2025-08-11 00:00:00', 'Open',        'Medium',  NULL),
(22,'Missing description',       '2025-08-04 00:00:00', 'Resolved',    'Low',     '2025-08-06 00:00:00'),
(23,'Inactive course scheduled', '2025-08-14 00:00:00', 'Open',        'Medium',  NULL),
(24,'Credits mismatch',          '2025-08-20 00:00:00', 'In Progress', 'High',    NULL),
(25,'Missing room',              '2025-08-08 00:00:00', 'Resolved',    'Low',     '2025-08-10 00:00:00'),
(26,'Time conflict',             '2025-08-13 00:00:00', 'Open',        'Medium',  NULL),
(27,'Over capacity',             '2025-08-27 00:00:00', 'Resolved',    'High',    '2025-08-30 00:00:00'),
(28,'Missing prereq',            '2025-08-19 00:00:00', 'Open',        'Medium',  NULL),
(29,'Invalid term',              '2025-08-21 00:00:00', 'In Progress', 'Low',     NULL),
(30,'Duplicate section',         '2025-08-24 00:00:00', 'Open',        'Medium',  NULL),
(31,'Missing professor',         '2025-08-15 00:00:00', 'Resolved',    'High',    '2025-08-18 00:00:00'),
(32,'Missing description',       '2025-08-17 00:00:00', 'Open',        'Low',     NULL),
(33,'Inactive course scheduled', '2025-08-28 00:00:00', 'In Progress', 'Medium',  NULL),
(34,'Overlap Issue', '2025-08-28 00:00:00', 'In Progress', 'Medium',  NULL),
(35,'Missing room',              '2025-08-18 00:00:00', 'Resolved',    'Low',     '2025-08-20 00:00:00'),
(36,'Time conflict',             '2025-08-22 00:00:00', 'Open',        'Medium',  NULL),
(37,'Over capacity',             '2025-08-26 00:00:00', 'In Progress', 'High',    NULL),
(38,'Missing prereq',            '2025-08-20 00:00:00', 'Resolved',    'Medium',  '2025-09-02 00:00:00'),
(39,'Invalid term',              '2025-08-03 00:00:00', 'Open',        'Low',     NULL),
(40,'Duplicate section',         '2025-08-06 00:00:00', 'In Progress', 'Medium',  NULL),
(41,'Missing professor',         '2025-08-09 00:00:00', 'Open',        'High',    NULL),
(42,'Missing description',       '2025-08-11 00:00:00', 'Resolved',    'Low',     '2025-08-13 00:00:00'),
(43,'Inactive course scheduled', '2025-08-16 00:00:00', 'Open',        'Medium',  NULL),
(44,'Credits mismatch',          '2025-08-19 00:00:00', 'Resolved',    'High',    '2025-08-22 00:00:00'),
(45,'Missing room',              '2025-08-21 00:00:00', 'Open',        'Low',     NULL),
(46,'Time conflict',             '2025-08-23 00:00:00', 'In Progress', 'Medium',  NULL),
(47,'Over capacity',             '2025-08-25 00:00:00', 'Open',        'High',    NULL),
(48,'Missing prereq',            '2025-08-27 00:00:00', 'Resolved',    'Medium',  '2025-08-29 00:00:00'),
(49,'Invalid term',              '2025-08-29 00:00:00', 'Open',        'Low',     NULL),
(50,'Duplicate section',         '2025-08-31 00:00:00', 'In Progress', 'Medium',  NULL);


INSERT INTO Stu_degr (studentID, programID) VALUES
(1001, 1),  -- Andrea Silva in BS CS
(1002, 1),  -- Bob in BS CS
(1002, 2);  -- Bob also in BS DS (double major)

INSERT INTO Stu_degr (studentID, programID) VALUES
(1001, 2),
(1001, 3),
(1001, 4),
(1001, 5),
(1001, 6),
(1002, 3),
(1002, 4),
(1002, 5),
(1002, 6),
(1002, 7),
(1003, 1),
(1003, 2),
(1003, 3),
(1003, 4),
(1003, 5),
(1004, 1),
(1004, 2),
(1004, 3),
(1004, 4),
(1004, 5),
(1005, 1),
(1005, 2),
(1005, 3),
(1005, 4),
(1005, 6),
(1006, 1),
(1006, 2),
(1006, 3),
(1006, 4),
(1006, 7),
(1007, 1),
(1007, 2),
(1007, 3),
(1007, 5),
(1007, 8),
(1008, 1),
(1008, 2),
(1008, 4),
(1008, 5),
(1008, 6),
(1009, 1),
(1009, 3),
(1009, 4),
(1009, 5),
(1009, 6),
(1010, 1),
(1010, 2),
(1010, 3),
(1010, 4),
(1010, 7),
(1011, 1),
(1011, 2),
(1011, 4),
(1011, 5),
(1011, 6),
(1012, 1),
(1012, 2),
(1012, 3),
(1012, 5),
(1012, 7),
(1013, 1),
(1013, 2),
(1013, 3),
(1013, 4),
(1013, 6),
(1014, 1),
(1014, 2),
(1014, 4),
(1014, 5),
(1014, 8),
(1015, 1),
(1015, 2),
(1015, 3),
(1015, 4),
(1015, 5),
(1016, 1),
(1016, 2),
(1016, 3),
(1016, 6),
(1016, 7),
(1017, 1),
(1017, 2),
(1017, 3),
(1017, 4),
(1017, 5),
(1018, 1),
(1018, 2),
(1018, 4),
(1018, 5),
(1018, 6),
(1019, 1),
(1019, 2),
(1019, 3),
(1019, 4),
(1019, 7),
(1020, 1),
(1020, 2),
(1020, 3),
(1020, 5),
(1020, 6),
(1021, 1),
(1021, 2),
(1021, 3),
(1021, 4),
(1021, 8),
(1022, 1),
(1022, 2),
(1022, 3),
(1022, 4),
(1022, 6),
(1023, 1),
(1023, 2),
(1023, 3),
(1023, 5),
(1023, 7),
(1024, 1),
(1024, 2),
(1024, 3),
(1024, 4),
(1024, 5),
(1025, 1),
(1025, 2),
(1025, 3),
(1025, 4),
(1025, 6),
(1026, 1),
(1026, 2),
(1026, 3),
(1026, 5),
(1026, 7),
(1027, 1),
(1027, 2),
(1027, 3),
(1027, 4),
(1027, 6),
(1028, 1),
(1028, 2),
(1028, 3),
(1028, 5),
(1028, 8),
(1029, 1),
(1029, 2),
(1029, 3),
(1029, 4),
(1029, 5),
(1030, 1),
(1030, 2),
(1030, 3),
(1030, 4),
(1030, 6);




INSERT INTO StudentPlan (planID, studentID,date_created, plan_name, is_active, expected_grad, programID) VALUES
(1, 1028, '2025-08-01', 'Andrea Silva CS Standard Plan', 1, '2027-05-01', 1),
(2, 1029,'2025-08-01', 'Bob DS Accelerated Plan', 1, '2026-12-15', 2);




INSERT INTO StudentPlan (planID, studentID, date_created, plan_name, is_active, expected_grad, programID) VALUES
(3, 1001, '2025-08-20', 'Andrea Silva CS + Extra Electives',    0, '2027-12-15', 1),
(4, 1002, '2025-08-01', 'Bob DS Accelerated Plan',       1, '2026-12-15', 2),
(5,  1001, '2025-06-20', 'Plan 5 for Student 1001', 1, '2027-05-01', 2),
(6,  1002, '2025-08-04', 'Plan 6 for Student 1002', 1, '2028-06-01', 2),
(7,  1003, '2025-08-11', 'Plan 7 for Student 1003', 1, '2026-06-01', 2),
(8,  1004, '2025-06-17', 'Plan 8 for Student 1004', 1, '2027-06-01', 2),
(9,  1005, '2025-07-28', 'Plan 9 for Student 1005', 1, '2028-05-01', 1),
(10, 1006, '2025-06-26', 'Plan 10 for Student 1006', 1, '2027-06-01', 2),
(11, 1007, '2025-09-03', 'Plan 11 for Student 1007', 1, '2029-05-01', 1),
(12, 1008, '2025-08-24', 'Plan 12 for Student 1008', 1, '2027-06-01', 2),
(13, 1009, '2025-08-22', 'Plan 13 for Student 1009', 1, '2028-05-01', 1),
(14, 1010, '2025-06-27', 'Plan 14 for Student 1010', 1, '2027-06-01', 1),
(15, 1011, '2025-08-14', 'Plan 15 for Student 1011', 1, '2026-05-01', 2),
(16, 1012, '2025-06-25', 'Plan 16 for Student 1012', 1, '2028-05-01', 2),
(17, 1013, '2025-09-01', 'Plan 17 for Student 1013', 1, '2029-06-01', 1),
(18, 1014, '2025-08-20', 'Plan 18 for Student 1014', 1, '2027-06-01', 2),
(19, 1015, '2025-06-21', 'Plan 19 for Student 1015', 1, '2028-05-01', 1),
(20, 1016, '2025-08-17', 'Plan 20 for Student 1016', 1, '2027-06-01', 2),
(21, 1017, '2025-08-04', 'Plan 21 for Student 1017', 1, '2028-05-01', 2),
(22, 1018, '2025-07-26', 'Plan 22 for Student 1018', 1, '2027-05-01', 1),
(23, 1019, '2025-08-02', 'Plan 23 for Student 1019', 1, '2028-06-01', 2),
(24, 1020, '2025-06-22', 'Plan 24 for Student 1020', 1, '2027-06-01', 1),
(25, 1021, '2025-08-06', 'Plan 25 for Student 1021', 1, '2028-05-01', 2),
(26, 1022, '2025-06-28', 'Plan 26 for Student 1022', 1, '2027-05-01', 1),
(27, 1023, '2025-08-01', 'Plan 27 for Student 1023', 1, '2028-06-01', 2),
(28, 1024, '2025-06-23', 'Plan 28 for Student 1024', 1, '2027-05-01', 1),
(29, 1025, '2025-08-10', 'Plan 29 for Student 1025', 1, '2028-06-01', 2),
(30, 1026, '2025-06-30', 'Plan 30 for Student 1026', 1, '2027-06-01', 1),
(31, 1027, '2025-08-09', 'Plan 31 for Student 1027', 1, '2028-05-01', 2),
(32, 1028, '2025-07-02', 'Plan 32 for Student 1028', 1, '2027-06-01', 1),
(33, 1029, '2025-07-15', 'Plan 33 for Student 1029', 1, '2028-05-01', 2),
(34, 1030, '2025-07-18', 'Plan 34 for Student 1030', 1, '2027-06-01', 1);


INSERT INTO Course_req (courseID, requirementID) VALUES
(101, 1),
(102, 1);

INSERT INTO Course_req (courseID, requirementID) VALUES
(101, 2),
(101, 3),
(101, 4),
(101, 6),
(102, 2),
(102, 4),
(102, 5),
(102, 7),
(103, 1),
(103, 3),
(103, 4),
(103, 8),
(104, 1),
(104, 2),
(104, 4),
(104, 9),
(105, 1),
(105, 3),
(105, 6),
(105, 8),
(106, 1),
(106, 4),
(106, 5),
(106, 9),
(107, 1),
(107, 3),
(107, 5),
(107, 7),
(108, 1),
(108, 4),
(108, 6),
(108, 10),
(109, 1),
(109, 3),
(109, 5),
(109, 8),
(110, 1),
(110, 2),
(110, 4),
(110, 9),
(111, 2),
(111, 3),
(111, 5),
(111, 7),
(112, 2),
(112, 4),
(112, 6),
(112, 8),
(113, 3),
(113, 5),
(113, 7),
(113, 9),
(114, 3),
(114, 4),
(114, 6),
(114, 10),
(115, 3),
(115, 5),
(115, 8),
(115, 9),
(116, 3),
(116, 4),
(116, 5),
(116, 7),
(117, 3),
(117, 6),
(117, 8),
(117, 9),
(118, 1),
(118, 2),
(118, 7),
(118, 9),
(119, 1),
(119, 4),
(119, 5),
(119, 8),
(120, 1),
(120, 3),
(120, 6),
(120, 10),
(121, 1),
(121, 2),
(121, 5),
(121, 7),
(122, 1),
(122, 4),
(122, 6),
(122, 8),
(123, 1),
(123, 3),
(123, 5),
(123, 9),
(124, 1),
(124, 4),
(124, 7),
(124, 10),
(125, 1),
(125, 3),
(125, 6),
(125, 8),
(126, 1),
(126, 2),
(126, 5),
(126, 9),
(127, 2),
(127, 3),
(127, 6),
(127, 7),
(128, 2),
(128, 4),
(128, 5),
(128, 8),
(129, 3),
(129, 5),
(129, 6),
(129, 9),
(130, 3),
(130, 4),
(130, 7),
(130, 10);

INSERT INTO Course_plan (planID, courseID, planned_semester, course_status) VALUES
(1, 101, 'Fall 2025',   'Planned'),
(1, 102, 'Spring 2026', 'Planned'),
(2, 101, 'Fall 2025',   'Planned');

INSERT INTO Course_plan (planID, courseID, planned_semester, course_status) VALUES
(1, 103, 'Fall 2025',   'Planned'),
(1, 104, 'Spring 2026', 'Planned'),
(1, 105, 'Fall 2026',   'Planned'),
(1, 106, 'Spring 2027', 'Planned'),
(2, 102, 'Spring 2026', 'Planned'),
(2, 103, 'Summer 2025', 'Planned'),
(2, 107, 'Fall 2026',   'Planned'),
(2, 108, 'Spring 2027', 'Planned'),
(3, 101, 'Fall 2025',   'Planned'),
(3, 103, 'Spring 2026', 'Planned'),
(3, 109, 'Fall 2026',   'Planned'),
(3, 110, 'Spring 2027', 'Planned'),
(3, 111, 'Summer 2025', 'Planned'),
(4, 101, 'Fall 2025',   'Planned'),
(4, 102, 'Spring 2026', 'Planned'),
(4, 112, 'Fall 2026',   'Planned'),
(4, 113, 'Spring 2027', 'Planned'),
(4, 114, 'Summer 2025', 'Planned'),
(5, 101, 'Fall 2025',   'Planned'),
(5, 102, 'Spring 2026', 'Planned'),
(5, 115, 'Fall 2026',   'Planned'),
(5, 116, 'Spring 2027', 'Planned'),
(5, 117, 'Summer 2025', 'Planned'),
(6, 101, 'Fall 2025',   'Planned'),
(6, 103, 'Spring 2026', 'Planned'),
(6, 104, 'Fall 2026',   'Planned'),
(6, 118, 'Spring 2027', 'Planned'),
(7, 101, 'Fall 2025',   'Planned'),
(7, 105, 'Spring 2026', 'Planned'),
(7, 106, 'Fall 2026',   'Planned'),
(7, 119, 'Spring 2027', 'Planned'),
(8, 101, 'Fall 2025',   'Planned'),
(8, 102, 'Spring 2026', 'Planned'),
(8, 107, 'Fall 2026',   'Planned'),
(8, 120, 'Spring 2027', 'Planned'),
(8, 121, 'Summer 2025', 'Planned'),
(9, 101, 'Fall 2025',   'Planned'),
(9, 102, 'Spring 2026', 'Planned'),
(9, 122, 'Fall 2026',   'Planned'),
(9, 123, 'Spring 2027', 'Planned'),
(9, 113, 'Summer 2025', 'Planned'),
(10,101, 'Fall 2025',   'Planned'),
(10,102,'Spring 2026',  'Planned'),
(10,103,'Fall 2026',    'Planned'),
(10,124,'Spring 2027',  'Planned'),
(11,101, 'Fall 2025',   'Planned'),
(11,104,'Spring 2026',  'Planned'),
(11,114,'Fall 2026',    'Planned'),
(11,115,'Spring 2027',  'Planned'),
(12,101, 'Fall 2025',   'Planned'),
(12,102,'Spring 2026',  'Planned'),
(12,103,'Fall 2026',    'Planned'),
(12,104,'Spring 2027',  'Planned'),
(12,105,'Summer 2025',  'Planned'),
(13,101, 'Fall 2025',   'Planned'),
(13,106,'Spring 2026',  'Planned'),
(13,107,'Fall 2026',    'Planned'),
(13,108,'Spring 2027',  'Planned'),
(14,101, 'Fall 2025',   'Planned'),
(14,102,'Spring 2026',  'Planned'),
(14,109,'Fall 2026',    'Planned'),
(14,110,'Spring 2027',  'Planned'),
(15,101, 'Fall 2025',   'Planned'),
(15,103,'Spring 2026',  'Planned'),
(15,111,'Fall 2026',    'Planned'),
(15,112,'Spring 2027',  'Planned'),
(15,113,'Summer 2025',  'Planned'),
(16,101, 'Fall 2025',   'Planned'),
(16,102,'Spring 2026',  'Planned'),
(16,114,'Fall 2026',    'Planned'),
(16,115,'Spring 2027',  'Planned'),
(17,101, 'Fall 2025',   'Planned'),
(17,116,'Spring 2026',  'Planned'),
(17,117,'Fall 2026',    'Planned'),
(17,118,'Spring 2027',  'Planned'),
(18,101, 'Fall 2025',   'Planned'),
(18,102,'Spring 2026',  'Planned'),
(18,119,'Fall 2026',    'Planned'),
(18,120,'Spring 2027',  'Planned'),
(19,101, 'Fall 2025',   'Planned'),
(19,103,'Spring 2026',  'Planned'),
(19,121,'Fall 2026',    'Planned'),
(19,122,'Spring 2027',  'Planned'),
(20,101, 'Fall 2025',   'Planned'),
(20,102,'Spring 2026',  'Planned'),
(20,123,'Fall 2026',    'Planned'),
(20,124,'Spring 2027',  'Planned'),
(21,101, 'Fall 2025',   'Planned'),
(21,104,'Spring 2026',  'Planned'),
(21,105,'Fall 2026',    'Planned'),
(21,106,'Spring 2027',  'Planned'),
(21,107,'Summer 2025',  'Planned'),
(22,101, 'Fall 2025',   'Planned'),
(22,102,'Spring 2026',  'Planned'),
(22,108,'Fall 2026',    'Planned'),
(22,109,'Spring 2027',  'Planned'),
(23,101, 'Fall 2025',   'Planned'),
(23,103,'Spring 2026',  'Planned'),
(23,110,'Fall 2026',    'Planned'),
(23,111,'Spring 2027',  'Planned'),
(24,101, 'Fall 2025',   'Planned'),
(24,102,'Spring 2026',  'Planned'),
(24,112,'Fall 2026',    'Planned'),
(24,113,'Spring 2027',  'Planned'),
(24,114,'Summer 2025',  'Planned'),
(25,101, 'Fall 2025',   'Completed'),
(25,102,'Spring 2026',  'In Progress'),
(25,103,'Fall 2026',    'Planned'),
(25,104,'Spring 2027',  'Planned'),
(26,101, 'Fall 2025',   'Completed'),
(26,102,'Spring 2026',  'Completed'),
(26,105,'Fall 2026',    'In Progress'),
(26,106,'Spring 2027',  'Planned'),
(27,101, 'Fall 2025',   'Completed'),
(27,103,'Spring 2026',  'Completed'),
(27,107,'Fall 2026',    'In Progress'),
(27,108,'Spring 2027',  'Planned'),
(28,101, 'Fall 2025',   'Completed'),
(28,102,'Spring 2026',  'Completed'),
(28,109,'Fall 2026',    'In Progress'),
(28,110,'Spring 2027',  'Planned'),
(29,101, 'Fall 2025',   'Completed'),
(29,103,'Spring 2026',  'Completed'),
(29,111,'Fall 2026',    'In Progress'),
(29,112,'Spring 2027',  'Planned'),
(30,101, 'Fall 2025',   'Completed'),
(30,102,'Spring 2026',  'Completed'),
(30,113,'Fall 2026',    'In Progress'),
(30,114,'Spring 2027',  'Planned'),
(31,101, 'Fall 2025',   'Completed'),
(31,104,'Spring 2026',  'Completed'),
(31,115,'Fall 2026',    'In Progress'),
(31,116,'Spring 2027',  'Planned'),
(32,101, 'Fall 2025',   'Completed'),
(32,102,'Spring 2026',  'Completed'),
(32,117,'Fall 2026',    'In Progress'),
(32,118,'Spring 2027',  'Planned'),
(33,101, 'Fall 2025',   'Completed'),
(33,103,'Spring 2026',  'Completed'),
(33,119,'Fall 2026',    'In Progress'),
(33,120,'Spring 2027',  'Planned'),
(34,101, 'Fall 2025',   'Completed'),
(34,102,'Spring 2026',  'Completed'),
(34,121,'Fall 2026',    'In Progress'),
(34,122,'Spring 2027',  'Planned');



INSERT INTO Scheduled_in (termID, CRN) VALUES
(1, 101),
(1, 102);

INSERT INTO Scheduled_in (termID, CRN) VALUES
(2, 101),
(2, 102),
(3, 101),
(3, 103),
(4, 101),
(4, 103),
(5, 101),
(5, 104),
(6, 102),
(6, 103),
(7, 102),
(7, 104),
(8, 102),
(8, 103),
(1, 103),
(1, 104),
(2, 103),
(2, 104),
(3, 104),
(3, 105),
(4, 104),
(4, 105),
(5, 105),
(5, 106),
(6, 105),
(6, 106),
(7, 106),
(7, 107),
(8, 106),
(8, 107),
(1, 105),
(1, 106),
(2, 105),
(2, 106),
(3, 107),
(3, 108),
(4, 107),
(4, 108),
(5, 107),
(5, 108),
(6, 107),
(6, 108),
(7, 108),
(7, 109),
(8, 108),
(8, 109),
(1, 107),
(1, 108),
(2, 107),
(2, 108),
(3, 109),
(3, 110),
(4, 109),
(4, 110),
(5, 109),
(5, 110),
(6, 109),
(6, 110),
(7, 110),
(7, 111),
(8, 110),
(8, 111),
(1, 109),
(1, 110),
(2, 109),
(2, 110),
(3, 111),
(3, 112),
(4, 111),
(4, 112),
(5, 111),
(5, 112),
(6, 111),
(6, 112),
(7, 112),
(7, 113),
(8, 112),
(8, 113),
(1, 111),
(1, 112),
(2, 111),
(2, 112),
(3, 113),
(3, 114),
(4, 113),
(4, 114),
(5, 113),
(5, 114),
(6, 113),
(6, 114),
(7, 114),
(7, 115),
(8, 114),
(8, 115),
(1, 113),
(1, 114),
(2, 113),
(2, 114),
(3, 115),
(3, 116),
(4, 115),
(4, 116),
(5, 115),
(5, 116),
(6, 115),
(6, 116),
(7, 116),
(7, 117),
(8, 116),
(8, 117),
(1, 115),
(1, 116),
(2, 115),
(2, 116),
(3, 117),
(3, 118),
(4, 117),
(4, 118),
(5, 117),
(5, 118),
(6, 117),
(6, 118),
(7, 118),
(7, 119),
(8, 118),
(8, 119),
(1, 117),
(1, 118);

INSERT INTO OverrideRequest (request_id, request_date, status, student_message, decision_date, studentID, CRN) VALUES
(1, '2025-09-05', 'Pending',  'Please add me; I meet the prereqs.',  NULL,          1001, 101),
(2, '2025-09-06', 'Approved', 'Need this course to graduate on time', '2025-09-07', 1002, 102);

INSERT INTO OverrideRequest (request_id, request_date, status, student_message, decision_date, studentID, CRN) VALUES
(3,  '2025-09-08', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1003, 103),
(4,  '2025-09-09', 'Approved', 'Time conflict with work; requesting a specific section.',    '2025-09-12',  1004, 104),
(5,  '2025-09-10', 'Denied',   'Prerequisite in transfer evaluation; please allow enrollment.', '2025-09-13', 1005, 105),
(6,  '2025-09-11', 'Pending',  'Advisor recommended I request an override.',                NULL,          1006, 106),
(7,  '2025-09-12', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-09-15', 1007, 107),
(8,  '2025-09-13', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1008, 108),
(9,  '2025-09-14', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-09-18',  1009, 109),
(10, '2025-09-15', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-09-19', 1010, 110),
(11, '2025-09-16', 'Pending',  'Advisor recommended I request an override.',                NULL,          1011, 111),
(12, '2025-09-17', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-09-20', 1012, 112),
(13, '2025-09-18', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1013, 113),
(14, '2025-09-19', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-09-22',  1014, 114),
(15, '2025-09-20', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-09-23', 1015, 115),
(16, '2025-09-21', 'Pending',  'Advisor recommended I request an override.',                NULL,          1016, 116),
(17, '2025-09-22', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-09-24', 1017, 117),
(18, '2025-09-23', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1018, 118),
(19, '2025-09-24', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-09-27',  1019, 119),
(20, '2025-09-25', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-09-29', 1020, 120),
(21, '2025-09-26', 'Pending',  'Advisor recommended I request an override.',                NULL,          1021, 121),
(22, '2025-09-27', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-09-30', 1022, 122),
(23, '2025-09-28', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1023, 123),
(24, '2025-09-29', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-10-02',  1024, 124),
(25, '2025-09-30', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-10-03', 1025, 125),
(26, '2025-10-01', 'Pending',  'Advisor recommended I request an override.',                NULL,          1026, 126),
(27, '2025-10-02', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-10-05', 1027, 127),
(28, '2025-10-03', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1028, 128),
(29, '2025-10-04', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-10-07',  1029, 129),
(30, '2025-10-05', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-10-08', 1030, 130),
(31, '2025-10-06', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1001, 131),
(32, '2025-10-07', 'Approved', 'Time conflict with work; requesting a specific section.',   '2025-10-10',  1002, 132),
(33, '2025-10-08', 'Denied',   'Prerequisite in transfer evaluation; please allow enrollment.', '2025-10-12', 1003, 133),
(34, '2025-10-09', 'Pending',  'Advisor recommended I request an override.',                NULL,          1004, 134),
(35, '2025-10-10', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-10-13', 1005, 135),
(36, '2025-10-11', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1006, 136),
(37, '2025-10-12', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-10-15',  1007, 137),
(38, '2025-10-13', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-10-16', 1008, 138),
(39, '2025-10-14', 'Pending',  'Advisor recommended I request an override.',                NULL,          1009, 139),
(40, '2025-10-15', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-10-18', 1010, 140),
(41, '2025-10-16', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1011, 101),
(42, '2025-10-17', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-10-20',  1012, 102),
(43, '2025-10-18', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-10-21', 1013, 103),
(44, '2025-10-19', 'Pending',  'Advisor recommended I request an override.',                NULL,          1014, 104),
(45, '2025-10-20', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-10-23', 1015, 105),
(46, '2025-10-21', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1016, 106),
(47, '2025-10-22', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-10-25',  1017, 107),
(48, '2025-10-23', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-10-26', 1018, 108),
(49, '2025-10-24', 'Pending',  'Advisor recommended I request an override.',                NULL,          1019, 109),
(50, '2025-10-25', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-10-28', 1020, 110),
(51, '2025-10-26', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1021, 111),
(52, '2025-10-27', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-10-30',  1022, 112),
(53, '2025-10-28', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-10-31', 1023, 113),
(54, '2025-10-29', 'Pending',  'Advisor recommended I request an override.',                NULL,          1024, 114),
(55, '2025-10-30', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-11-02', 1025, 115),
(56, '2025-10-31', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1026, 116),
(57, '2025-11-01', 'Denied',   'Time conflict with work; requesting a specific section.',   '2025-11-04',  1027, 117),
(58, '2025-11-02', 'Approved', 'Prerequisite in transfer evaluation; please allow enrollment.', '2025-11-05', 1028, 118),
(59, '2025-11-03', 'Pending',  'Advisor recommended I request an override.',                NULL,          1029, 119),
(60, '2025-11-04', 'Approved', 'I am on the waitlist and would appreciate an enrollment override.', '2025-11-07', 1030, 120),
(61, '2025-11-05', 'Pending',  'Need this course to stay on track for graduation.',         NULL,          1001, 121),
(62, '2025-11-06', 'Approved', 'Time conflict with work; requesting a specific section.',   '2025-11-09',  1002, 122);

INSERT INTO Flag_course (issueID, courseID) VALUES
(2, 101);  -- credits mismatch on CS2500

INSERT INTO Flag_course (issueID, courseID) VALUES
(1, 102),
(1, 103),
(2, 102),
(2, 103),
(3, 101),
(3, 104),
(4, 101),
(4, 105),
(5, 102),
(5, 106),
(6, 103),
(6, 107),
(7, 104),
(7, 108),
(8, 105),
(8, 109),
(9, 106),
(9, 110),
(10, 107),
(10, 111),
(11, 108),
(11, 112),
(12, 109),
(12, 113),
(13, 110),
(13, 114),
(14, 111),
(14, 115),
(15, 112),
(15, 116),
(16, 113),
(16, 117),
(17, 114),
(17, 118),
(18, 115),
(18, 119),
(19, 116),
(19, 120),
(20, 117),
(20, 121),
(21, 118),
(21, 122),
(22, 119),
(22, 123),
(23, 120),
(23, 124),
(24, 101),
(24, 102),
(25, 103),
(25, 104),
(26, 105),
(26, 106),
(27, 107),
(27, 108),
(28, 109),
(28, 110),
(29, 111),
(29, 112),
(30, 113),
(30, 114);


INSERT INTO Flag_section (issueID, CRN) VALUES
(1, 101);  -- missing room info for section 101

INSERT INTO Flag_section (issueID, CRN) VALUES
(1, 102),
(1, 103),
(2, 101),
(2, 104),
(3, 103),
(3, 105),
(4, 104),
(4, 106),
(5, 105),
(5, 107),
(6, 106),
(6, 108),
(7, 107),
(7, 109),
(8, 108),
(8, 110),
(9, 109),
(9, 111),
(10,110),
(10,112),
(11,111),
(11,113),
(12,112),
(12,114),
(13,113),
(13,115),
(14,114),
(14,116),
(15,115),
(15,117),
(16,116);

INSERT INTO Enrollment (studentID, CRN, grade, enrollment_status) VALUES
(1001, 101, 92.5, 'Completed'),
(1002, 101, 88.0, 'Completed'),
(1001, 102, 85.5, 'Enrolled'),
(1002, 102, 91.0, 'Dropped');

INSERT INTO Enrollment (studentID, CRN, grade, enrollment_status) VALUES
(1010, 101, NULL,  'Dropped'),
(1024, 101, 67.9,  'Enrolled'),
(1016, 101, 73.3,  'Completed'),
(1028, 101, 77.4,  'Enrolled'),
(1026, 101, 84.3,  'Enrolled'),
(1027, 102, 87.7,  'Completed'),
(1010, 102, 84.6,  'Completed'),
(1013, 102, 96.9,  'Completed'),
(1030, 102, NULL,  'Dropped'),
(1018, 103, 80.3,  'Enrolled'),
(1001, 103, 85.1,  'Completed'),
(1009, 103, NULL,  'Dropped'),
(1017, 103, NULL,  'Dropped'),
(1020, 103, 84.4,  'Completed'),
(1007, 103, 90.3,  'Enrolled'),
(1013, 103, NULL,  'Dropped'),
(1014, 104, NULL,  'Dropped'),
(1005, 104, 85.2,  'Enrolled'),
(1025, 104, NULL,  'Dropped'),
(1011, 104, NULL,  'Dropped'),
(1016, 104, NULL,  'Dropped'),
(1019, 104, 96.9,  'Enrolled'),
(1013, 104, NULL,  'Dropped'),
(1029, 104, NULL,  'Dropped'),
(1019, 140, 83.5,  'Enrolled'),
(1020, 140, 91.7,  'Completed'),
(1021, 140, 76.2,  'Enrolled'),
(1022, 140, NULL,  'Dropped'),
(1023, 140, 88.8,  'Completed'),
(1024, 140, 79.9,  'Enrolled'),
(1025, 140, 82.1,  'Enrolled'),
(1026, 140, NULL,  'Dropped');