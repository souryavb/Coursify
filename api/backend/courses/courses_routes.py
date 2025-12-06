from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


# Create a Blueprint for NGO routes
courses = Blueprint("courses", __name__)


# GET /courses
# Return list of all courses with codes, titles,
# credits, and descriptions. [Jordan 1]
@courses.route("/courses", methods=["GET"])
def get_courses():
    try:
        current_app.logger.info("GET /courses called")
        cursor = db.get_db().cursor()

        query = """
            SELECT
                courseID    AS courseCode,
                course_name AS title,
                credits,
                description
            FROM Course
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_courses: {str(e)}")
        return jsonify({"error": str(e)}), 500