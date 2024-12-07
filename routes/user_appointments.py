from flask import Blueprint, jsonify, request
from db import get_db_connection

user_appointments_bp = Blueprint('user_appointments', __name__)

@user_appointments_bp.route('/user/appointments', methods=['GET'])
def get_user_appointments():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT a.id, a.barber_id, b.name AS barber_name, a.date, a.start_time, a.status
        FROM appointments a
        JOIN barbers b ON a.barber_id = b.barber_id
        WHERE a.user_id = %s
        ORDER BY a.date ASC, a.start_time ASC
    """
    cursor.execute(query, (user_id,))
    appointments = cursor.fetchall()
    cursor.close()
    connection.close()

    response = [
        {
            "appointment_id": appt[0],
            "barber_id": appt[1],
            "barber_name": appt[2],
            "date": str(appt[3]),
            "start_time": str(appt[4]),
            "status": appt[5]
        }
        for appt in appointments
    ]
    return jsonify(response)
