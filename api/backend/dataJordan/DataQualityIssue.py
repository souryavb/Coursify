from flask import Blueprint, jsonify, request, make_response
from backend.db_connection import db


data_quality = Blueprint("data_quality", __name__)


@data_quality.route("/data_quality/checks", methods=["GET", "DELETE"])
def data_quality_checks():
   cursor = db.get_db().cursor()
  
   if request.method == "GET":
       the_query = '''
       SELECT issueID, issueType, severity, status, createdAt
       FROM DataQualityIssue
       '''
       cursor.execute(the_query)
       theData = cursor.fetchall()
      
       json_data = []
       for row in theData:
           json_data.append({
               "issueID": row['issueID'],
               "issue_type": row['issueType'],
               "severity": row['severity'],
               "status": row['status'],
               "detected_at": row['createdAt']
           })
      
       return make_response(jsonify(json_data), 200)


   elif request.method == "DELETE":
       issue_id = request.args.get('issueID')
       if not issue_id:
           return make_response(jsonify({"error": "Missing issueID"}), 400)


       try:
           cursor.execute("DELETE FROM Flag_course WHERE issueID = %s", (issue_id,))
           cursor.execute("DELETE FROM Flag_section WHERE issueID = %s", (issue_id,))
           cursor.execute("DELETE FROM DataQualityIssue WHERE issueID = %s", (issue_id,))
           db.get_db().commit()
           return make_response(jsonify({"message": "Deleted"}), 200)
       except Exception as e:
           return make_response(jsonify({"error": str(e)}), 500)