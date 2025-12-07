from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

# Blueprint for student-related routes
students = Blueprint("students", __name__)


def get_student_name(studentID: int) -> str:
    """
    Look up the student's first + last name for responses.
    Returns 'Unknown Student' if not found.
    """
    cursor = db.get_db().cursor()
    cursor.execute(
        "SELECT f_name, l_name FROM Student WHERE studentID = %s",
        (studentID,),
    )
    row = cursor.fetchone()
    cursor.close()

    if row:
        return f"{row['f_name']} {row['l_name']}"
    return "Unknown Student"


# -----------------------------------------------------------
# GET /s/student{studentID}/plans
# Return all plans created by a specific student
# Example: /s/student1001/plans
# -----------------------------------------------------------
@students.route("/student<int:studentID>/plans", methods=["GET"])
def get_student_plans(studentID: int):
    try:
        student_name = get_student_name(studentID)
        current_app.logger.info(
            f"Fetching plans for {student_name} (ID {studentID})"
        )
        cursor = db.get_db().cursor()

        query = """
            SELECT
                sp.planID,
                sp.plan_name,
                sp.is_active,
                sp.expected_grad,
                sp.date_created,
                sp.programID,
                dp.program AS program_name,
                dp.type    AS program_type
            FROM StudentPlan AS sp
            JOIN DegreePrograms AS dp
              ON sp.programID = dp.programID
            WHERE sp.studentID = %s
            ORDER BY sp.planID;
        """

        current_app.logger.debug(
            f"Executing get_student_plans query for {student_name} (ID {studentID})"
        )
        cursor.execute(query, (studentID,))
        rows = cursor.fetchall()
        cursor.close()

        current_app.logger.info(
            f"Successfully retrieved {len(rows)} plans for {student_name} (ID {studentID})"
        )
        return jsonify(rows), 200

    except Error as e:
        current_app.logger.error(
            f"Database error in get_student_plans for studentID {studentID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# POST /s/student{studentID}/plans
# Create a new what-if plan for a specific student
# Example: POST /s/student1001/plans
# -----------------------------------------------------------
@students.route("/student<int:studentID>/plans", methods=["POST"])
def create_student_plan(studentID: int):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        student_name = get_student_name(studentID)
        current_app.logger.info(
            f"Creating new plan for {student_name} (ID {studentID}): {data}"
        )

        # Validate required fields
        required_fields = ["plan_name", "expected_grad", "programID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Check student exists
        cursor.execute("SELECT 1 FROM Student WHERE studentID = %s", (studentID,))
        if cursor.fetchone() is None:
            cursor.close()
            return jsonify({"error": "Student not found"}), 404

        # Generate the next planID
        cursor.execute("SELECT COALESCE(MAX(planID), 0) + 1 AS next_id FROM StudentPlan")
        next_plan_id = cursor.fetchone()["next_id"]

        # What-if plans default to is_active = 0 unless user specifies
        is_active = data.get("is_active", 0)

        query = """
            INSERT INTO StudentPlan
                (planID, studentID, date_created, plan_name, is_active, expected_grad, programID)
            VALUES
                (%s, %s, CURDATE(), %s, %s, %s, %s)
        """

        params = (
            next_plan_id,
            studentID,
            data["plan_name"],
            is_active,
            data["expected_grad"],
            data["programID"],
        )

        current_app.logger.debug(
            f"Executing create_student_plan insert for {student_name} (ID {studentID}) "
            f"with params: {params}"
        )
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(
            f"Plan {next_plan_id} created for {student_name} (ID {studentID})"
        )

        return (
            jsonify(
                {
                    "message": "Plan created successfully",
                    "planID": next_plan_id,
                    "studentID": studentID,
                }
            ),
            201,
        )

    except Error as e:
        current_app.logger.error(
            f"Database error in create_student_plan for studentID {studentID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# GET /s/student{studentID}/plans/{planID}
# Return complete semester-by-semester view of a specific plan
# with all its courses
# -----------------------------------------------------------
@students.route("/student<int:studentID>/plans/<int:planID>", methods=["GET"])
def get_student_plan_detail(studentID: int, planID: int):
    try:
        student_name = get_student_name(studentID)
        current_app.logger.info(
            f"Fetching detailed plan {planID} for {student_name} (ID {studentID})"
        )

        cursor = db.get_db().cursor()

        # Plan header
        header_query = """
            SELECT
                sp.planID,
                sp.studentID,
                sp.plan_name,
                sp.is_active,
                sp.expected_grad,
                sp.date_created,
                sp.programID,
                dp.program AS program_name,
                dp.type    AS program_type
            FROM StudentPlan AS sp
            JOIN DegreePrograms AS dp
              ON sp.programID = dp.programID
            WHERE sp.studentID = %s
              AND sp.planID = %s
        """
        cursor.execute(header_query, (studentID, planID))
        plan = cursor.fetchone()

        if not plan:
            cursor.close()
            return jsonify({"error": "Plan not found for this student"}), 404

        # Courses in the plan
        courses_query = """
            SELECT
                cp.courseID,
                c.course_name,
                c.credits,
                cp.planned_semester,
                cp.course_status
            FROM Course_plan AS cp
            JOIN Course AS c
              ON cp.courseID = c.courseID
            WHERE cp.planID = %s
            ORDER BY cp.planned_semester, cp.courseID
        """
        cursor.execute(courses_query, (planID,))
        courses = cursor.fetchall()
        cursor.close()

        plan["courses"] = courses
        return jsonify(plan), 200

    except Error as e:
        current_app.logger.error(
            f"Database error in get_student_plan_detail "
            f"for studentID {studentID}, planID {planID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# PUT /s/student{studentID}/plans/{planID}
# Activate / Deactivate a plan (is_active flag)
# If setting is_active = 1, all other plans for that student
# are set to 0.
# -----------------------------------------------------------
@students.route("/student<int:studentID>/plans/<int:planID>", methods=["PUT"])
def update_student_plan_status(studentID: int, planID: int):
    try:
        data = request.get_json() or {}
        if "is_active" not in data:
            return jsonify({"error": "Missing required field: is_active"}), 400

        new_is_active = int(data["is_active"])
        if new_is_active not in (0, 1):
            return jsonify({"error": "is_active must be 0 or 1"}), 400

        student_name = get_student_name(studentID)
        cursor = db.get_db().cursor()

        # Make sure the plan exists and belongs to the student
        cursor.execute(
            """
            SELECT planID
            FROM StudentPlan
            WHERE planID = %s AND studentID = %s
            """,
            (planID, studentID),
        )
        if cursor.fetchone() is None:
            cursor.close()
            return jsonify({"error": "Plan not found for this student"}), 404

        # If activating, deactivate all other plans for this student
        if new_is_active == 1:
            cursor.execute(
                "UPDATE StudentPlan SET is_active = 0 WHERE studentID = %s",
                (studentID,),
            )

        # Update this plan
        cursor.execute(
            """
            UPDATE StudentPlan
            SET is_active = %s
            WHERE planID = %s AND studentID = %s
            """,
            (new_is_active, planID, studentID),
        )
        db.get_db().commit()

        # Return the updated plan header
        cursor.execute(
            """
            SELECT
                sp.planID,
                sp.studentID,
                sp.plan_name,
                sp.is_active,
                sp.expected_grad,
                sp.date_created,
                sp.programID,
                dp.program AS program_name,
                dp.type    AS program_type
            FROM StudentPlan AS sp
            JOIN DegreePrograms AS dp
              ON sp.programID = dp.programID
            WHERE sp.planID = %s
              AND sp.studentID = %s
            """,
            (planID, studentID),
        )
        updated_plan = cursor.fetchone()
        cursor.close()

        current_app.logger.info(
            f"Updated is_active for plan {planID} for {student_name} "
            f"(ID {studentID}) to {new_is_active}"
        )

        return jsonify(updated_plan), 200

    except Error as e:
        current_app.logger.error(
            f"Database error in update_student_plan_status "
            f"for studentID {studentID}, planID {planID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# DELETE /s/student{studentID}/plans/{planID}
# Delete a what-if plan (is_active = 0) for that student
# Example: /s/student1001/plans/3
# -----------------------------------------------------------
@students.route("/student<int:studentID>/plans/<int:planID>", methods=["DELETE"])
def delete_student_plan(studentID: int, planID: int):
    try:
        student_name = get_student_name(studentID)

        current_app.logger.info(
            f"Attempting to delete plan {planID} for {student_name} (ID {studentID})"
        )

        cursor = db.get_db().cursor()

        # Ensure the plan exists and belongs to this student
        cursor.execute(
            """
            SELECT is_active
            FROM StudentPlan
            WHERE planID = %s AND studentID = %s
            """,
            (planID, studentID),
        )
        row = cursor.fetchone()

        if row is None:
            cursor.close()
            return jsonify({"error": "Plan not found for this student"}), 404

        # Only allow deleting what-if plans (is_active = 0)
        if row["is_active"] == 1:
            cursor.close()
            return jsonify(
                {
                    "error": "Cannot delete an active plan; only what-if plans can be deleted"
                }
            ), 400

        # Delete dependent rows in Course_plan first (FK constraint)
        cursor.execute("DELETE FROM Course_plan WHERE planID = %s", (planID,))

        # Delete the plan itself
        cursor.execute(
            "DELETE FROM StudentPlan WHERE planID = %s AND studentID = %s",
            (planID, studentID),
        )

        db.get_db().commit()
        cursor.close()

        current_app.logger.info(
            f"Successfully deleted plan {planID} for {student_name} (ID {studentID})"
        )

        return jsonify({"message": "Plan deleted successfully", "planID": planID}), 200

    except Error as e:
        current_app.logger.error(
            f"Database error in delete_student_plan for studentID {studentID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500
