from flask import Blueprint, jsonify, request, make_response
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for data routes
data = Blueprint("data", __name__)

@data.route("/data", methods=["GET"])
def get_all_data():
    
    cursor = db.get_db().cursor()
    the_query= '''
SELECT
   p.profID,
   p.last_name as professor_name,
   AVG(r.rating) as average_rating,
   COUNT(r.rated_num) as total_ratings,
   MAX(r.created_aT) as most_recent_rating
FROM Professor AS p
JOIN Rating AS r ON p.profID = r.profID
GROUP BY p.profID, p.first_name, p.last_name, p.department;
'''

    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response



@data.route("/data/student", methods=["GET"])
def get_student():
    
    cursor = db.get_db().cursor()
    the_query= '''
SELECT
   c.courseID,
   c.course_name,
   s.CRN,
   s.section_num,
   AVG(e.grade) as average_grade
FROM Section s
INNER JOIN Course c ON s.CRN = c.courseID
LEFT JOIN Enrollment e ON s.CRN = e.CRN
GROUP BY c.courseID, c.course_name, s.CRN, s.section_num
ORDER BY c.course_name, s.section_num;
'''

    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response 


@data.route("/data/course", methods=["GET"])
def get_course():
    
    cursor = db.get_db().cursor()
    the_query= '''
SELECT c.courseID, c.course_name, c.credits, d.deptName
FROM Course AS c
JOIN Department AS d ON c.deptID = d.deptID
ORDER BY d.deptName, c.course_name;
'''

    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response 

@data.route("/data/course/<int:course_id>", methods=["GET"])
def get_course_id(course_id):
    
    cursor = db.get_db().cursor()
    the_query= '''
SELECT
   c.courseID,
   c.course_name,
   d.deptName,
   COUNT(e.studentID) AS total_enrolled,
   SUM(e.enrollment_status = 'Completed') AS completed,
   SUM(e.enrollment_status = 'Dropped') AS dropped,
   ROUND(SUM(e.enrollment_status = 'Completed') * 100.0 / COUNT(e.studentID), 2) AS completion_rate
FROM Course AS c
JOIN Department AS d ON c.deptID = d.deptID
JOIN Section AS s ON c.courseID = s.CRN
JOIN Enrollment AS e ON s.CRN = e.CRN
WHERE c.courseID = %s
GROUP BY c.courseID, c.course_name, d.deptName;
'''

    cursor.execute(the_query, (course_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response 

@data.route("/data/professor", methods=["GET"])
def get_professor():
    
    cursor = db.get_db().cursor()
    the_query= '''
SELECT
   p.profID,
   p.last_name as last_name,
   p.first_name as first_name,
   AVG(r.rating) as average_rating,
   COUNT(r.rated_num) as total_ratings,
   MAX(r.created_aT) as most_recent_rating
FROM Professor AS p
JOIN Rating AS r ON p.profID = r.profID
GROUP BY p.profID, p.first_name, p.last_name, p.department;
'''

    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response 

@data.route("/data/professor/<int:prof_id>", methods=["GET"])
def get_professor_spec(prof_id):
    
    cursor = db.get_db().cursor()
    the_query= '''
SELECT
   p.last_name as last_name,
   p.first_name as first_name,
   r.rating as ratings,
   r.created_aT as rating_time,
   r.comment as comment
FROM Professor AS p
JOIN Rating AS r ON p.profID = r.profID
WHERE p.profID = %s;
'''

    cursor.execute(the_query, (prof_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response 