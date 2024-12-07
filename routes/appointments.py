from flask import Blueprint, jsonify, request
from db import get_db_connection

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    barber_id = request.args.get('barber_id')
    date = request.args.get('date')

    if not barber_id or not date:
        return jsonify({"error": "Both barber_id and date are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT start_time, status
        FROM appointments
        WHERE barber_id = %s AND date = %s
        ORDER BY start_time ASC
    """
    cursor.execute(query, (barber_id, date))
    appointments = cursor.fetchall()
    cursor.close()
    connection.close()

    response = [
        {"start_time": str(appt[0]), "status": appt[1]}
        for appt in appointments
    ]
    return jsonify(response)

@appointments_bp.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json

    # Validate required fields
    if not all(key in data for key in ('barber_id', 'user_id', 'date', 'start_time')):
        return jsonify({"error": "Chýbajú povinné údaje"}), 400

    user_id = data['user_id']
    appointment_date = data['date']

    # Extract the month and year from the appointment date
    year, month, _ = map(int, appointment_date.split('-'))

    connection = get_db_connection()
    cursor = connection.cursor()

    # Skip the 3-appointment limit check if the user is the admin (id=2)
    if user_id != 2:
        # Check how many appointments the user already has this month
        query = """
            SELECT COUNT(*) FROM appointments
            WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
        """
        cursor.execute(query, (user_id, year, month))
        appointment_count = cursor.fetchone()[0]

        if appointment_count >= 3:
            return jsonify({"error": "Už máte zarezervovaný maximálny počet 3 termínov na tento mesiac."}), 403

    # Insert the new appointment
    query = """
        INSERT INTO appointments (barber_id, user_id, date, start_time, status, created_by)
        VALUES (%s, %s, %s, %s, 'booked', 'user')
    """
    try:
        cursor.execute(query, (data['barber_id'], user_id, appointment_date, data['start_time']))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

    return jsonify({"message": "Appointment booked successfully!"})
