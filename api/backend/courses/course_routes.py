from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

# Blueprint for course-related routes
courses = Blueprint("courses", __name__)


# -----------------------------------------------------------
# GET /courses
# Search and retrieve a list of courses using filters
# -----------------------------------------------------------
@courses.route("/courses", methods=["GET"])
def get_courses():
    try:
        cursor = db.get_db().cursor()

        subject  = request.args.get("subject")          # ex: CS
        level    = request.args.get("level")            # ex: 2000, 2500, 3000
        search   = request.args.get("search")           # free text
        credits  = request.args.get("credits", type=int)
        semester = request.args.get("semester")
        status   = request.args.get("status")

        current_app.logger.debug(
            f"Course filters - subject={subject}, level={level}, "
            f"search={search}, credits={credits}, semester={semester}, status={status}"
        )

        query = """
            SELECT
                courseID,
                course_name,
                semesters_offered,
                Status,
                credits,
                description,
                deptID
            FROM Course
            WHERE 1 = 1
        """
        params = []

        # Filter by subject prefix in course_name (e.g. "CS2500 - ...")
        if subject:
            query += " AND course_name LIKE %s"
            params.append(f"{subject}%")

        # Filter by *any* level (1000/2000/2500/3000/etc.)
        if level:
            first_digit = level[0]  # '2' from '2000'
            # Match things like "CS2500 - ..." / "MA2100 - ..." etc.
            query += " AND course_name REGEXP %s"
            params.append(f"^[A-Z]{{2}}{first_digit}[0-9]{{3}}")

        # Free-text search in name or description
        if search:
            query += " AND (course_name LIKE %s OR description LIKE %s)"
            like_term = f"%{search}%"
            params.extend([like_term, like_term])

        # Exact match on credits
        if credits is not None:
            query += " AND credits = %s"
            params.append(credits)

        # Match semester inside semesters_offered string
        if semester:
            query += " AND semesters_offered LIKE %s"
            params.append(f"%{semester}%")

        # Match on Status column
        if status:
            query += " AND Status = %s"
            params.append(status)

        query += " ORDER BY course_name"

        current_app.logger.debug(f"Executing get_courses query: {query} with params {params}")
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()

        return jsonify(rows), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_courses: {str(e)}")
        return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------
# GET /c/courses/<courseID>
# Retrieve detailed info for a specific course
# Example: /c/courses/101
# -----------------------------------------------------------
@courses.route("/courses/<int:courseID>", methods=["GET"])
def get_course(courseID: int):
    try:
        current_app.logger.info(f"Fetching details for course {courseID}")
        cursor = db.get_db().cursor()

        query = """
            SELECT
                c.courseID,
                c.course_name,
                c.semesters_offered,
                c.Status,
                c.credits,
                c.description,
                c.deptID,
                d.deptName
            FROM Course AS c
            LEFT JOIN Department AS d
              ON c.deptID = d.deptID
            WHERE c.courseID = %s
        """

        current_app.logger.debug(
            f"Executing get_course query for courseID={courseID}"
        )
        cursor.execute(query, (courseID,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return jsonify({"error": "Course not found"}), 404

        return jsonify(row), 200

    except Error as e:
        current_app.logger.error(
            f"Database error in get_course for courseID {courseID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# GET /c/courses/<courseID>/requirements
# Return course requisites/requirements
# Example: /c/courses/101/requirements
# -----------------------------------------------------------
@courses.route("/courses/<int:courseID>/requirements", methods=["GET"])
def get_course_requirements(courseID: int):
    try:
        current_app.logger.info(f"Fetching requirements for course {courseID}")
        cursor = db.get_db().cursor()

        # 1) Make sure the course exists (and get its name for context)
        cursor.execute(
            "SELECT courseID, course_name FROM Course WHERE courseID = %s",
            (courseID,),
        )
        course_row = cursor.fetchone()

        if course_row is None:
            cursor.close()
            return jsonify({"error": "Course not found"}), 404

        # 2) Get all linked requirements
        query = """
            SELECT
                r.requirementID,
                r.requirementType,
                r.creditsNeeded,
                r.corequisites,
                r.prerequisites
            FROM Course_req AS cr
            JOIN Requirements AS r
              ON cr.requirementID = r.requirementID
            WHERE cr.courseID = %s
            ORDER BY r.requirementID
        """

        current_app.logger.debug(
            f"Executing get_course_requirements for courseID={courseID}"
        )
        cursor.execute(query, (courseID,))
        req_rows = cursor.fetchall()
        cursor.close()

        response = {
            "courseID": course_row["courseID"],
            "course_name": course_row["course_name"],
            "requirements": req_rows,
        }

        return jsonify(response), 200

    except Error as e:
        current_app.logger.error(
            f"Database error in get_course_requirements for courseID {courseID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500
