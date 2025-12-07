from flask import Blueprint, jsonify, request
from backend.db_connection import db

professors = Blueprint("professors", __name__)


# ---------- small helper for date/time/decimal ----------

def _row_to_jsonable(row):
    """Convert non-JSON types in a dict row to strings."""
    if not row:
        return row
    for k, v in row.items():
        # DATE, DATETIME, TIME, DECIMAL, etc. -> string
        if v is not None and not isinstance(v, (int, float, str, bool)):
            row[k] = str(v)
    return row


def _rows_to_jsonable(rows):
    return [_row_to_jsonable(r) for r in rows]


# -------------------------------------------------------
# 1. GET /professors/<prof_id>/sections
#    Returns all sections taught by this professor
# -------------------------------------------------------
@professors.route("/professors/<int:prof_id>/sections", methods=["GET"])
def get_professor_sections(prof_id):
    cursor = db.get_db().cursor()

    query = """
        SELECT 
            s.CRN,
            s.courseID,
            c.course_name,
            s.section_num,
            s.semester,
            s.day_of_week,
            s.start_time,
            s.end_time,
            s.location,
            s.capacity
        FROM Section AS s
        JOIN Course AS c ON s.courseID = c.courseID
        WHERE s.profID = %s
    """

    cursor.execute(query, (prof_id,))
    rows = cursor.fetchall()
    cursor.close()

    rows = _rows_to_jsonable(rows)
    return jsonify(rows), 200


# -------------------------------------------------------
# 2. GET /professors/<prof_id>/ratings
#    All ratings + average for this professor
# -------------------------------------------------------
@professors.route("/professors/<int:prof_id>/ratings", methods=["GET"])
def get_professor_ratings(prof_id):
    cursor = db.get_db().cursor()

    query = """
        SELECT
            rated_num,
            created_aT AS created_at,
            rating,
            comment
        FROM Rating
        WHERE profID = %s
        ORDER BY created_aT DESC
    """
    cursor.execute(query, (prof_id,))
    rows = cursor.fetchall()
    cursor.close()

    rows = _rows_to_jsonable(rows)

    avg_rating = None
    if rows:
        total = sum(float(r["rating"]) for r in rows if r["rating"] is not None)
        count = sum(1 for r in rows if r["rating"] is not None)
        avg_rating = total / count if count > 0 else None

    data = {
        "profID": prof_id,
        "average_rating": avg_rating,
        "num_ratings": len(rows),
        "ratings": rows,
    }
    return jsonify(data), 200


# -------------------------------------------------------
# 3. GET /sections/<CRN>/overriderequests
#    All override requests for one section, with student info
# -------------------------------------------------------
@professors.route("/sections/<int:crn>/overriderequests", methods=["GET"])
def get_section_override_requests(crn):
    cursor = db.get_db().cursor()

    query = """
        SELECT
            o.request_id,
            o.request_date,
            o.status,
            o.student_message,
            o.decision_date,
            o.studentID,
            s.f_name,
            s.l_name,
            s.email
        FROM OverrideRequest AS o
        JOIN Student AS s ON o.studentID = s.studentID
        WHERE o.CRN = %s
        ORDER BY o.request_date DESC
    """

    cursor.execute(query, (crn,))
    rows = cursor.fetchall()
    cursor.close()

    rows = _rows_to_jsonable(rows)
    return jsonify(rows), 200


# -------------------------------------------------------
# 4. GET /overriderequests/<request_id>
#    Single override request (full details)
# -------------------------------------------------------
@professors.route("/overriderequests/<int:request_id>", methods=["GET"])
def get_single_override_request(request_id):
    cursor = db.get_db().cursor()

    query = """
        SELECT
            o.request_id,
            o.request_date,
            o.status,
            o.student_message,
            o.decision_date,
            o.studentID,
            o.CRN,
            s.f_name,
            s.l_name,
            s.email
        FROM OverrideRequest AS o
        JOIN Student AS s ON o.studentID = s.studentID
        WHERE o.request_id = %s
    """

    cursor.execute(query, (request_id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"error": "Override request not found"}), 404

    row = _row_to_jsonable(row)
    return jsonify(row), 200


# -------------------------------------------------------
# 5. PUT /overriderequests/<request_id>
#    Update status of one override request
# -------------------------------------------------------
@professors.route("/overriderequests/<int:request_id>", methods=["PUT"])
def update_override_request_status(request_id):
    data = request.get_json() or {}
    new_status = data.get("status")

    if not new_status:
        return jsonify({"error": "Missing 'status' in request body"}), 400

    conn = db.get_db()
    cursor = conn.cursor()

    query = """
        UPDATE OverrideRequest
        SET status = %s,
            decision_date = CURRENT_DATE
        WHERE request_id = %s
    """
    cursor.execute(query, (new_status, request_id))
    conn.commit()

    changed = cursor.rowcount
    cursor.close()

    if changed == 0:
        return jsonify({"error": "Override request not found"}), 404

    return jsonify({"message": "Override request updated"}), 200


# -------------------------------------------------------
# 6. DELETE /overriderequests/<request_id>
#    Delete / cancel an override request
# -------------------------------------------------------
@professors.route("/overriderequests/<int:request_id>", methods=["DELETE"])
def delete_override_request(request_id):
    conn = db.get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM OverrideRequest WHERE request_id = %s",
        (request_id,),
    )
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()

    if deleted == 0:
        return jsonify({"error": "Override request not found"}), 404

    return jsonify({"message": "Override request deleted"}), 200


# -------------------------------------------------------
# 7. GET /professors/<prof_id>/overriderequests
#    All override requests across sections taught by this prof
# -------------------------------------------------------
@professors.route("/professors/<int:prof_id>/overriderequests", methods=["GET"])
def get_professor_override_requests(prof_id):
    cursor = db.get_db().cursor()

    query = """
        SELECT
            o.request_id,
            o.request_date,
            o.status,
            o.student_message,
            o.decision_date,
            o.studentID,
            o.CRN
        FROM OverrideRequest AS o
        JOIN Section AS s ON o.CRN = s.CRN
        WHERE s.profID = %s
        ORDER BY o.request_date DESC
    """

    cursor.execute(query, (prof_id,))
    rows = cursor.fetchall()
    cursor.close()

    rows = _rows_to_jsonable(rows)
    return jsonify(rows), 200


# -------------------------------------------------------
# 8. PUT /professors/<prof_id>/overriderequests
#    Bulk update multiple override requests
# -------------------------------------------------------
@professors.route("/professors/<int:prof_id>/overriderequests", methods=["PUT"])
def bulk_update_professor_override_requests(prof_id):
    body = request.get_json() or {}
    updates = body.get("updates")

    if not isinstance(updates, list) or not updates:
        return jsonify({"error": "'updates' must be a non-empty list"}), 400

    conn = db.get_db()
    cursor = conn.cursor()

    query = """
        UPDATE OverrideRequest
        SET status = %s,
            decision_date = CURRENT_DATE
        WHERE request_id = %s
    """

    total = 0
    for u in updates:
        req_id = u.get("request_id")
        status = u.get("status")
        if req_id is None or status is None:
            continue
        cursor.execute(query, (status, req_id))
        total += cursor.rowcount

    conn.commit()
    cursor.close()

    return jsonify({"message": "Bulk override update complete",
                    "rows_affected": total}), 200


# -------------------------------------------------------
# 9. GET /students/<student_id>
#    Basic student info (helper endpoint)
# -------------------------------------------------------
@professors.route("/students/<int:student_id>", methods=["GET"])
def get_basic_student_info(student_id):
    cursor = db.get_db().cursor()

    query = """
        SELECT studentID,
               f_name,
               l_name,
               email,
               mobile,
               year,
               credits_completed
        FROM Student
        WHERE studentID = %s
    """
    cursor.execute(query, (student_id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"error": "Student not found"}), 404

    row = _row_to_jsonable(row)
    return jsonify(row), 200