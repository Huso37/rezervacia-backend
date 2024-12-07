from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)
    role = db.Column(db.Enum('user', 'admin'), default='user')

    def __repr__(self):
        return f"<User {self.username}>"

class Barber(db.Model):
    __tablename__ = 'barbers'

    barber_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Barber {self.name}>"

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barbers.barber_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for admin-created appointments
    customer_name = db.Column(db.String(100), nullable=True)  # Nullable for user-created appointments
    customer_phone = db.Column(db.String(15), nullable=True)  # Nullable for user-created appointments
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum('available', 'booked'), default='available', nullable=False)
    created_by = db.Column(db.Enum('user', 'admin'), nullable=False)

    barber = db.relationship('Barber', backref='appointments')
    user = db.relationship('User', backref='appointments')

    def __repr__(self):
        return f"<Appointment {self.id} - Barber {self.barber_id}>"