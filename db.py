import pymysql

def get_db_connection():
    """Create a new database connection."""
    return pymysql.connect(
        host="Huso38.mysql.pythonanywhere-services.com",
        user="Huso38",
        password="sqlroot123",
        database="Huso38$RezervaciaDB"
    )

def init_db(app):
    """Any database setup can go here (e.g., SQLAlchemy init)."""
    pass
