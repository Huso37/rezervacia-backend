# import datetime
# from db import get_db_connection

# def create_default_appointments():
#     """
#     Generate default appointments for all barbers.
#     """
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     # Define working days and hours
#     working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#     start_time = datetime.time(9, 0)  # 9:00 AM
#     end_time = datetime.time(17, 0)  # 5:00 PM

#     # Fetch all barbers
#     cursor.execute("SELECT barber_id FROM barbers")
#     barbers = cursor.fetchall()

#     # Define a date range (e.g., next 30 days)
#     today = datetime.date.today()
#     date_range = [today + datetime.timedelta(days=i) for i in range(30)]

#     # Generate appointments for each barber
#     for barber in barbers:
#         barber_id = barber[0]
#         for date in date_range:
#             if date.strftime('%A') in working_days:
#                 current_time = start_time
#                 while current_time < end_time:
#                     # Insert appointment
#                     query = """
#                         INSERT IGNORE INTO appointments (barber_id, date, start_time, status, created_by)
#                         VALUES (%s, %s, %s, 'available', 'admin')
#                     """
#                     cursor.execute(query, (barber_id, date, current_time))

#                     # Increment time by 1 hour
#                     current_time = (datetime.datetime.combine(datetime.date.today(), current_time) +
#                                     datetime.timedelta(hours=1)).time()

#     connection.commit()
#     cursor.close()
#     connection.close()

#     print("Default appointments created successfully!")
