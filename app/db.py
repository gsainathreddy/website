# db.py
from app import app, mysql


with app.app_context():
    cur = mysql.connection.cursor()
    with app.open_resource('schema.sql', mode='r') as f:
        cur.execute(f.read())
    
    cur.close()
