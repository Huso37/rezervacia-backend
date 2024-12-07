from flask import Blueprint, jsonify
from db import get_db_connection

barbers_bp = Blueprint('barbers', __name__)

@barbers_bp.route('/barbers', methods=['GET'])
def get_barbers():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = "SELECT barber_id, name FROM barbers"
    cursor.execute(query)
    barbers = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify([{"barber_id": barber[0], "name": barber[1]} for barber in barbers])
