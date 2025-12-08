from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for requirements routes
requirements = Blueprint('requirements', __name__)


# GET /courses
# Return list of all reuirements needed
@requirements.route("/requirements", methods=["GET"])
def get_requirements():

    cursor = db.get_db().cursor()
    the_query = '''
        SELECT
            requirementID,
            creditsNeeded,
            requirementType,
            corequisites,
            prerequisites
        FROM Requirements;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    cursor.close()
    
    return jsonify(theData)

# POST /courses
# Changes requirements
@requirements.route("/requirements", methods=["UPDATE"])
def change_requirements(req_id):

    data = request.get_json()

    creditsNeeded = data.get("creditsNeeded")
    requirementType = data.get("requirementType")
    corequisites = data.get("corequisites")
    prerequisites = data.get("prerequisites")

    cursor = db.get_db().cursor()

    update_query = """
        UPDATE Requirements
        SET creditsNeeded = %s,
            requirementType = %s,
            corequisites = %s,
            prerequisites = %s
        WHERE requirementID = %s;
    """

    cursor.execute(update_query, (
        creditsNeeded,
        requirementType,
        corequisites,
        prerequisites,
        req_id
    ))

    db.get_db().commit()
    cursor.close()

    return jsonify({"message": "Requirement updated successfully"}), 200