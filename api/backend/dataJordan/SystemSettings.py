from flask import Blueprint, jsonify, request, make_response
from backend.db_connection import db



system_settings_bp = Blueprint("system_settings_bp", __name__)


@system_settings_bp.route("/system-settings/<string:setting_key>", methods=["GET", "PUT"])
def system_settings_spec(setting_key):
   cursor = db.get_db().cursor()
  
   if request.method == "GET":
       query = "SELECT settingKey, settingValue, description FROM SystemSetting WHERE settingKey = %s"
       cursor.execute(query, (setting_key,))
       theData = cursor.fetchall()
      
       json_data = []
       for row in theData:
           json_data.append({
               "settingKey": row['settingKey'],
               "settingValue": row['settingValue'],
               "description": row['description']
           })
      
       return make_response(jsonify(json_data), 200)


   elif request.method == "PUT":
       req_data = request.get_json()
       new_val = req_data.get('value')
       new_desc = req_data.get('description')
      
       query = "UPDATE SystemSetting SET settingValue = %s, description = %s WHERE settingKey = %s"
       try:
           cursor.execute(query, (new_val, new_desc, setting_key))
           db.get_db().commit()
           return make_response(jsonify({"message": "Updated"}), 200)
       except Exception as e:
           return make_response(jsonify({"error": str(e)}), 500)