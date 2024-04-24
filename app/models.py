# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta
import app

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.Time, nullable=False)
    organizer = db.Column(db.String(255), nullable=False)

class ResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('accounts.id'), nullable=False)
    token = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



    def __repr__(self):
        return f'<Event {self.name}>'

# Run this code to create the table
with app.app_context():
    db.create_all()
