from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

plans = Blueprint("plans", __name__)

# -----------------------------------------------------------
# GET /p/plans
#    /p/plans                -> all plans
#    /p/plans?studentID=1001 -> plans for that student only
# -----------------------------------------------------------
@plans.route("/plans", methods=["GET"])
def get_plans():
    try:
        student_id = request.args.get("studentID", type=int)
        current_app.logger.info(f"Fetching plans (studentID={student_id})")

        cursor = db.get_db().cursor()

        base_query = """
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
            WHERE 1 = 1
        """
        params = []

        # If they pass ?studentID=1001, filter by that
        if student_id is not None:
            base_query += " AND sp.studentID = %s"
            params.append(student_id)

        base_query += " ORDER BY sp.planID"

        current_app.logger.debug(
            f"Executing get_plans query: {base_query} with params={params}"
        )

        cursor.execute(base_query, params)
        rows = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f"Retrieved {len(rows)} plans")
        return jsonify(rows), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_plans: {str(e)}")
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# GET /p/plans/<planID>/courses
# Return all courses in a plan, ordered by planned_semester
# Example: /p/plans/1/courses
# -----------------------------------------------------------
@plans.route("/plans/<int:planID>/courses", methods=["GET"])
def get_plan_courses(planID: int):
    try:
        current_app.logger.info(f"Fetching courses for plan {planID}")
        cursor = db.get_db().cursor()

        # Ensure the plan exists
        cursor.execute(
            "SELECT planID, studentID, plan_name FROM StudentPlan WHERE planID = %s",
            (planID,),
        )
        plan_row = cursor.fetchone()
        if plan_row is None:
            cursor.close()
            return jsonify({"error": "Plan not found"}), 404

        # Get all courses for that plan
        query = """
            SELECT
                cp.planID,
                cp.courseID,
                cp.planned_semester,
                cp.course_status,
                c.course_name,
                c.credits
            FROM Course_plan AS cp
            JOIN Course AS c
              ON cp.courseID = c.courseID
            WHERE cp.planID = %s
            ORDER BY cp.planned_semester, cp.courseID
        """
        current_app.logger.debug(
            f"Executing get_plan_courses for planID={planID} with query: {query}"
        )

        cursor.execute(query, (planID,))
        rows = cursor.fetchall()
        cursor.close()

        # plan metadata
        response = {
            "title": f"Courses planned by semester for Plan {planID}",
            "planID": plan_row["planID"],
            "studentID": plan_row["studentID"],
            "plan_name": plan_row["plan_name"],
            "courses": rows,
        }

        return jsonify(response), 200

    except Error as e:
        current_app.logger.error(
            f"Database error in get_plan_courses for planID {planID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------
# POST /p/plans/<planID>/courses
# Add a course to the plan for a specific semester
# -----------------------------------------------------------
@plans.route("/plans/<int:planID>/courses", methods=["POST"])
def add_course_to_plan(planID: int):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        current_app.logger.info(
            f"Adding course to plan {planID} with data: {data}"
        )

        # Required fields
        required_fields = ["courseID", "planned_semester"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        course_id = data["courseID"]
        planned_semester = data["planned_semester"]
        course_status = data.get("course_status", "Planned")

        cursor = db.get_db().cursor()

        # Check that the plan exists
        cursor.execute(
            "SELECT 1 FROM StudentPlan WHERE planID = %s",
            (planID,),
        )
        if cursor.fetchone() is None:
            cursor.close()
            return jsonify({"error": "Plan not found"}), 404

        # Check that the course exists
        cursor.execute(
            "SELECT 1 FROM Course WHERE courseID = %s",
            (course_id,),
        )
        if cursor.fetchone() is None:
            cursor.close()
            return jsonify({"error": "Course not found"}), 404

        # prevent duplicates (same plan + course)
        cursor.execute(
            """
            SELECT 1
            FROM Course_plan
            WHERE planID = %s AND courseID = %s
            """,
            (planID, course_id),
        )
        if cursor.fetchone() is not None:
            cursor.close()
            return jsonify(
                {
                    "error": "This course is already in the plan. "
                             "Use PUT to update its semester/status."
                }
            ), 400

        # Insert into Course_plan
        insert_query = """
            INSERT INTO Course_plan (planID, courseID, planned_semester, course_status)
            VALUES (%s, %s, %s, %s)
        """
        params = (planID, course_id, planned_semester, course_status)

        current_app.logger.debug(
            f"Executing add_course_to_plan insert for planID={planID}: {params}"
        )
        cursor.execute(insert_query, params)
        db.get_db().commit()

        # Return newly-added row (joined with Course info)
        select_query = """
            SELECT
                cp.planID,
                cp.courseID,
                cp.planned_semester,
                cp.course_status,
                c.course_name,
                c.credits
            FROM Course_plan AS cp
            JOIN Course AS c
              ON cp.courseID = c.courseID
            WHERE cp.planID = %s AND cp.courseID = %s
        """
        cursor.execute(select_query, (planID, course_id))
        new_row = cursor.fetchone()
        cursor.close()

        return jsonify(
            {
                "message": "Course added to plan successfully",
                "course": new_row,
            }
        ), 201

    except Error as e:
        current_app.logger.error(
            f"Database error in add_course_to_plan for planID {planID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------
# PUT /p/plans/<planID>/courses/<courseID>
# Update a course in a plan (semester and/or status)
# -----------------------------------------------------------
@plans.route("/plans/<int:planID>/courses/<int:courseID>", methods=["PUT"])
def update_course_in_plan(planID: int, courseID: int):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        planned_semester = data.get("planned_semester")
        course_status = data.get("course_status")

        action_details = []
        if planned_semester:
            action_details.append(f"moving course to semester '{planned_semester}'")
        if course_status:
            action_details.append(f"setting status to '{course_status}'")

        action_text = " and ".join(action_details)

        current_app.logger.info(
            f"Updating course {courseID} for Plan {planID}: {action_text}"
        )


        # Only allow these fields to be updated
        allowed_fields = ["planned_semester", "course_status"]
        update_fields = []
        params = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify(
                {"error": "No valid fields to update (planned_semester, course_status)"}
            ), 400

        cursor = db.get_db().cursor()

        #Confirm(planID, courseID) exists
        cursor.execute(
            """
            SELECT 1
            FROM Course_plan
            WHERE planID = %s AND courseID = %s
            """,
            (planID, courseID),
        )
        if cursor.fetchone() is None:
            cursor.close()
            return jsonify({"error": "Course not found in this plan"}), 404

        # Update plane
        params.extend([planID, courseID])
        update_query = f"""
            UPDATE Course_plan
            SET {', '.join(update_fields)}
            WHERE planID = %s AND courseID = %s
        """

        current_app.logger.debug(
            f"Executing update_course_in_plan for planID={planID}, "
            f"courseID={courseID} with params: {params}"
        )
        cursor.execute(update_query, params)
        db.get_db().commit()

        # Return the updated row joined with Course info
        select_query = """
            SELECT
                cp.planID,
                cp.courseID,
                cp.planned_semester,
                cp.course_status,
                c.course_name,
                c.credits
            FROM Course_plan AS cp
            JOIN Course AS c
              ON cp.courseID = c.courseID
            WHERE cp.planID = %s AND cp.courseID = %s
        """
        cursor.execute(select_query, (planID, courseID))
        updated_row = cursor.fetchone()
        cursor.close()

        return jsonify({
            "message": f"Updating course {courseID} for Plan {planID}: {action_text}",
            "message": "Course in plan updated successfully",
            "planID": planID,
            "courseID": updated_row["courseID"],
            "course_name": updated_row["course_name"],
            "planned_semester": updated_row["planned_semester"],
            "course_status": updated_row["course_status"],
            "credits": updated_row["credits"]
            }), 200

    except Error as e:
        current_app.logger.error(
            f"Database error in update_course_in_plan for planID {planID}, "
            f"courseID {courseID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# DELETE /p/plans/<planID>/courses/<courseID>
# Remove a course from a specific plan
# Example:
#   DELETE /p/plans/1/courses/101
# -----------------------------------------------------------
@plans.route("/plans/<int:planID>/courses/<int:courseID>", methods=["DELETE"])
def delete_course_from_plan(planID: int, courseID: int):
    try:
        cursor = db.get_db().cursor()

        # 1) Log what we’re trying to do
        current_app.logger.info(
            f"Attempting to remove course {courseID} from Plan {planID}"
        )

        # 2) Check if the course is actually in that plan
        check_query = """
            SELECT
                planID,
                courseID,
                planned_semester,
                course_status
            FROM Course_plan
            WHERE planID = %s AND courseID = %s
        """
        current_app.logger.debug(
            f"Checking existence of course in plan with query: {check_query} "
            f"params=({planID}, {courseID})"
        )
        cursor.execute(check_query, (planID, courseID))
        row = cursor.fetchone()

        if row is None:
            cursor.close()
            return (
                jsonify(
                    {
                        "message": f"Course {courseID} not found in Plan {planID}",
                        "details": (
                            f"Attempting to remove course {courseID} from Plan {planID}; "
                            f"no matching row in Course_plan"
                        ),
                    }
                ),
                404,
            )

        # 3) Delete the row
        delete_query = """
            DELETE FROM Course_plan
            WHERE planID = %s AND courseID = %s
        """
        current_app.logger.debug(
            f"Executing delete for planID={planID}, courseID={courseID}"
        )
        cursor.execute(delete_query, (planID, courseID))
        db.get_db().commit()
        cursor.close()

        # 4) Build a nice message with the before-delete info
        details = [
            f"Attempting to remove course {courseID} from Plan {planID}",
            f"Successfully removed course {courseID} from Plan {planID}",
        ]

        return (
            jsonify(
                {
                    "details": details,
                    "removed_course": {
                        "planID": row["planID"],
                        "courseID": row["courseID"],
                        "planned_semester": row["planned_semester"],
                        "course_status": row["course_status"],
                    },
                }),200,
)

    except Error as e:
        current_app.logger.error(
            f"Database error in delete_course_from_plan for planID {planID}, "
            f"courseID {courseID}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500