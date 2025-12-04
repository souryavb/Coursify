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
    cursor.close()
    
    return jsonify(theData) 