# app/views/routes.py
import json
import os
import re
import secrets
import MySQLdb
from flask import Blueprint, jsonify, render_template, request, session, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from app import mysql, user
from flask_login import login_required
from app.db import mysql

from flask_mail import Mail
from email.mime.text import MIMEText
from flask_mail import Message
from app.auth import admin_required,member_required, users_required
from datetime import datetime
from flask_mail import Mail
import qrcode
from werkzeug.utils import secure_filename
bp = Blueprint('routes', __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'files')
ALLOWED_EXTENSIONS = {'pdf'} # this is used for the extensions of pdf files to save in the file
bcrypt = Bcrypt()
mail=Mail()

@bp.route('/') 
def home(): # THIS IS USED FOR HOME PAGE
    return render_template('layout.html')

@bp.route('/register', methods=['POST', 'GET'])

def register():   #THIS IS USED FOR REGISTRATION PAGE
    msg  =''

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        relationship = request.form['relationship']
        phone_number=request.form['mobile']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email, ))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'^[6-9]\d{9}$',phone_number):
            msg='Invalid Phone number'
        elif not re.match(r'^[A-Za-z\s]+$',relationship):
            msg='Invalid Relationship'
        elif not email or not password or not relationship or not phone_number:
            msg = 'Please fill out the form!'
        else:
            role='user'
            print(role)
            cursor.execute('INSERT INTO accounts (name, email, password, relationship,role,mobile) VALUES (%s, %s, %s, %s,%s,%s)', (name, email, hashed_password, relationship,role,phone_number))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    else:
        msg = 'Please fill out the form!'

    # Use the full endpoint name when rendering the template
    return render_template('register.html', msg=msg)

@bp.route('/admin/add_users',methods=['POST','Get'])
@admin_required
def add_users():
    msg  =''

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        relationship = request.form['relationship']
        phone_number=request.form['mobile']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email, ))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'^[6-9]\d{9}$',phone_number):
            msg='Invalid Phone number'
        elif not re.match(r'^[A-Za-z\s]+$',relationship):
            msg='Invalid Relationship'
        elif not email or not password or not relationship or not phone_number:
            msg = 'Please fill out the form!'
        else:
            role='user'
            print(role)
            cursor.execute('INSERT INTO accounts (name, email, password, relationship,role,mobile) VALUES (%s, %s, %s, %s,%s,%s)', (name, email, hashed_password, relationship,role,phone_number))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('routes.admin'))
    else:
        msg = 'Please fill out the form!'
        
    # Use the full endpoint name when rendering the template
    return render_template('add_user.html', msg=msg)
# THIS IS USED FOR ADMIN ADD USER SAME LIKE REGISTRATION






@bp.route('/login', methods=['POST', 'GET'])
def login(): # THIS IS LOGIN PAGE FOR USER
    msg = ''
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email=%s AND status=%s', (email, 'approve'))
        account = cursor.fetchone()


        if account and bcrypt.check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['role'] = account['role']
            msg = 'Logged in successfully !'
            
            
            
            if account['role'] == 'admin':
                  
                    return redirect(url_for('routes.admin'))
            
            elif account['role'] == 'member':
                print("here in member page")
                
                return redirect(url_for('routes.member'))
            else:
                return redirect(url_for('routes.users'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('layout.html', msg=msg)
    
    



@bp.route('/logout')
@login_required               # LOGOUT PAGE
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('routes.login'))
    
'''@bp.route('/forgot', methods=['POST',"GET"]) # THIS IS FORGOT  ROUTE WHICH IS USED FOR EMAIL PASSWORD FOR CHANGING PASSWORD
def forgot():
    if request.method =='POST':
        email=request.form['email']
        
        users=user(email)
        print(users)
        use=users.get('email')
        id=users.get('id')
        print(use,id)
        if use:
             token = secrets.token_urlsafe(32)
             cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             cursor.execute('Insert into reset (user_id,token,created_at) VALUES(%s,%s,%s)',(id,token,datetime.utcnow()))
             mysql.connection.commit()
             msg = Message('Password Reset', sender='sainath0121@gmail.com', recipients=[email])
             msg.body = f'Hello, you have requested a password reset. Your token is: {token}'
             mail.send(msg)

             flash('An email with instructions to reset your password has been sent.')
             return redirect(url_for('routes.login'))
        else:
            flash('Email not found in our database.')

            
        

    return render_template('forgot_password.html')''' # this function has to be completed for forgetting password 
        


@bp.route('/member')
@member_required
def member():
    
    return render_template('member.html')  # Update as 


@bp.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')


def get_user_role():
    if 'role' in session :
        
        return session['role']
    else:
        return None
    

def user(email):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select id,email from accounts where email=%s',(email,))
    user=cursor.fetchone()
    cursor.close()
    
    return user






def get_user_email():
    if 'email' in session:
        return session['email'] 
    else:
        return None

@bp.route('/users')
@users_required
def users():
    return render_template('user.html')



def get_events(date):
    selected_date = request.args.get('date')
    print(selected_date)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM events where event_date = %s"
    cursor.execute(query, (selected_date,))
    events = cursor.fetchall()
    cursor.execute('select id from events where event_date=%s',(selected_date,))
    ids=cursor.fetchall()
    ids=[d['id'] for d in ids]
    ids=list(ids)
    events_registration_count = {}

    for id in ids:
        cursor.execute('select count(event_id) from event_registration where event_id=%s',(id,))
        events_registred=cursor.fetchone()
        type(events_registred)
        events_registration_count[id]=events_registred
    events_registration_count = {k: v['count(event_id)'] for k, v in events_registration_count.items()}
    events_registred=list(events_registration_count.values())
    



    

    
    
    event_list = []
    for event,registered_count in zip(events,events_registred):
        
            event_dict = {
                'id':event['id'],
                'name': event['event_name'],
                'start_time': str(event['start_time']),
                'end_time': str(event['end_time']),
                'tutor':str(event['tutor']),
                'count':registered_count
            
            }

            event_list.append(event_dict)

    cursor.close()
    user_role=get_user_role()
    return event_list

def fetch_date():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select distinct event_date from events')

    dates=cursor.fetchall()

    cursor.close()
    dates = [date['event_date'].strftime('%Y-%m-%d') for date in dates]
    return dates


def tutor():
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT  distinct name  FROM accounts WHERE basic='yes' OR advanced='yes' OR expert='yes'")

        tutors=cursor.fetchall()
        tutors=[tuto['name'] for tuto in tutors]
        return tutors


@bp.route('/users/calendar',methods=['POST','GET'])
def calendar():
    date=request.args.get('date')
    event_list=get_events(date)
    
    dates=fetch_date()
    print('this is dates',dates)
    user_role=get_user_role()

    location=locations()
    tutors=tutor()
    check='yes'
    return render_template('cal.html',event_list=event_list,user_role=user_role,dates=dates,location=location,tutors=tutors,check=check)



def Qrcode(data1,user_id):
    data2={'user_id':user_id}
    data1='\n'.join([f"{key}:{value}" for key,value in data1.items()])
    data2='\n'.join([f'{key}:{value}' for key,value in data2.items()])
    data=data1+'\n'+data2
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

                   
    qr.add_data(data)
    qr.make(fit=True)
    qr_image=qr.make_image(fill_color='black', back_color='white')
    
    return qr_image
    





@bp.route('/user/register_event/<int:event_id>',methods=['POST','GET'])
def register_event(event_id):
    if request.method =='POST' :
        user_id=session['id']
    
        cursor=mysql.connection.cursor()
        cursor.execute('select name,email,mobile from accounts where id=%s',(user_id,))
        
        data_from_accounts=cursor.fetchone()
        name,email,phone_number=data_from_accounts['name'],data_from_accounts['email'],data_from_accounts['mobile']
    

        cursor.execute('select  id,event_name,start_time,end_time, tutor from events where id=%s',(event_id,))
        data_from_events=cursor.fetchone()
        data_dict = dict(data_from_events)
        data_dict['event_id'] = data_dict.pop('id')
        print(data_dict)
    
        event_id, event_name,start_time,end_time,tutor= data_from_events['id'],data_from_events['event_name'],data_from_events['start_time'],data_from_events['end_time'],data_from_events['tutor']
       
       

        
       



        static_folder = os.path.join(os.getcwd(), 'app', 'static','qr')
    
        
        qr_image=Qrcode(data_dict,user_id)
        qr_image_path = os.path.join(static_folder,f'qr_code_{event_id,user_id}.png')
        qr_image.save(qr_image_path)
        event_qr_images = [f'qr_code_{event_id,user_id}.png']
    
       
       
        events=cursor.execute('select user_id,event_id from event_registration where user_id=%s and event_id=%s',(user_id,event_id,))
        if not events:  # If no rows were returned, the user is not registered
    # Insert the registration details into the event_registration table
            cursor.execute('INSERT INTO event_registration (user_id, event_id, user_name, user_email, event_name, start_time, end_time,tutor) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)',
                   (user_id, event_id, name, email, event_name, start_time, end_time,tutor))
            mysql.connection.commit()
        else:
            print('You have already registered')
        cursor.close()


        



    return render_template('Qr.html', event_qr_images=event_qr_images)




# this is used for checking wheather the user has registered in event or not




    

def validate_date(date_str):
    # Validate date format (YYYY-MM-DD)
    date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(date_regex.match(date_str))



@bp.route('/admin/cal', methods=['POST', 'GET'])
def cal():
    if request.method == 'POST':
        # Get form data
        date = request.form.get('date')
        name = request.form.get('name')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        tutor=request.form.get('tutor')
        print(start_time,end_time)
        user_id=session['id']

        # Validate form data
        if not all([date, name, start_time, end_time,tutor]):
            return 'All fields are required.'
        
       

        # Insert data into database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO events (event_date, event_name, start_time, end_time,user_id,tutor) VALUES (%s, %s, %s, %s,%s,%s)', (date, name, start_time, end_time,user_id,tutor))
        mysql.connection.commit()
        cursor.close()
        dates=fetch_date()
        user_role=get_user_role()

    return render_template('cal.html',dates=dates,user_role=user_role)

@bp.route('/admin/add_location', methods=['POST', 'GET'])
def add_location():
    error_message = None  # Initialize error message to None
    if request.method == 'POST':
        location = request.form.get('location')
        address = request.form.get('address')
        
        # Check if location and address are provided
        if not location:
            error_message = "Please provide a location."
        elif not address:
            error_message = "Please provide an address."
        else:
            # Validate location and address format
         
                # Insert location into the database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO location(location_name, address) VALUES (%s, %s)', (location, address))
                mysql.connection.commit()
                cursor.close()

    # Fetch locations from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM location')
    locations = cursor.fetchall()
    print(locations)
    cursor.close()

    
    return render_template('location.html', locations=locations, error_message=error_message)


def is_valid_location(location):
    return bool(re.match(r'^[A-Za-z\s]+$', location))

def is_valid_address(address):
    return bool(re.match(r'^[A-Za-z0-9\s]+$', address))







@bp.route('/admin/scan', methods=['POST', 'GET'])
def scan():
    if request.method == 'POST':
        data = request.get_json()
        qr_data_lines = data['qr_data'].split('\n')
        event_name = None
        start_time = None
        end_time = None
        tutor = None
        event_id=None
        user_id = None
        for line in qr_data_lines:
            parts = line.split(':')
            if len(parts) > 1:  # Ensure there's a key-value pair
                key = parts[0].strip()
                value = ':'.join(parts[1:]).strip()  # Join the remaining parts as the value
                if key == 'event_name':
                    event_name = value
                elif key == 'start_time':
                    start_time = parse_time(value)
                elif key == 'end_time':
                    end_time = parse_time(value)
                elif key == 'tutor':
                    tutor = value
                elif key=='event_id':
                    event_id =value
                elif key == 'user_id':
                    user_id = value

        # Print or process the extracted data as needed
        print('Event Name:', event_name)
        print('Start Time:', start_time)
        print('End Time:', end_time)
        print('Tutor:', tutor)
        print('User ID:', user_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT event_name, tutor, event_id, user_id FROM event_registration WHERE event_name=%s AND   tutor=%s AND event_id=%s AND user_id=%s',
               (event_name, tutor, event_id, user_id))


        attendence=cursor.fetchone()
        cursor.close()
        print('this is attendance',attendence)
        name=attendence['event_name']
        print(name)
        if attendence is not None:
    # Extract data from the attendance record
            event_name, tutor, event_id, user_id = attendence['event_name'], attendence['tutor'], attendence['event_id'], attendence['user_id']
   
            print(event_name, tutor, event_id)
    # Insert into the attendance table
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO attendance (event_name, tutor, user_id, event_id, attendance_status) VALUES (%s, %s, %s, %s, %s)',
                   (event_name, tutor, user_id, event_id, 'present'))
            mysql.connection.commit()
            cursor.close()
        else:
    # If attendance is not found, mark as absent
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO attendance (event_name, tutor, user_id, event_id, attendance_status) VALUES (%s, %s, %s, %s, %s)',
                   (event_name, tutor, user_id, event_id, 'absent'))
            mysql.connection.commit()
            cursor.close()

            

        
    return render_template('scan.html')

def parse_time(time_str):
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return f"{hours}:{minutes:02d}:{seconds:02d}"  # Format the time string
    except ValueError:
        print(f"Error parsing time: {time_str}")
    return None


def locations():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select distinct location_name from location')
    locations=cursor.fetchall()
    locations = [location['location_name'] for location in locations]
    print(locations)
    return locations





@bp.route('/admin/events',methods=['POST','GET'])
def events():

    selected_date = request.args.get('date') 

    
    event_list=get_events(selected_date)
  
    dates=fetch_date()
    user_role=get_user_role()
    location=locations()

    return render_template('cal.html',event_list=event_list,user_role=user_role,dates=dates,location=location)

@bp.route('/admin/registeredlist/<int:event_id>',methods=['POST','GET'])
def registeredlist(event_id):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select  user_name,user_email,event_name,start_time,end_time,tutor from event_registration where event_id=%s',(event_id,))
    events=cursor.fetchall()
    
    cursor.close()
    return render_template('usersregistration.html',events=events)


@bp.route('/admin/upload', methods=['POST', 'GET']) 
def upload():
    if request.method == 'POST':
        name = request.form.get('name')
        pdf_file = request.files['pdf']
        softcopy_file = request.files['softcopy']

        # Save the files to the UPLOAD_FOLDER
        pdf_filename = secure_filename(pdf_file.name) # This is used for pdf_file.name is used 
        softcopy_filename = secure_filename(softcopy_file.name)
        pdf_file.save(os.path.join(UPLOAD_FOLDER, pdf_filename))
        softcopy_file.save(os.path.join(UPLOAD_FOLDER, softcopy_filename))

        # Now you have the filenames, you can insert them into the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO event (name, pdf, softcopy) VALUES (%s, %s, %s)', (name, pdf_filename, softcopy_filename))
        mysql.connection.commit()
        cursor.close()

    return render_template('upload.html')



@bp.route('/admin/add_user',methods=['POST','GET'])
def add_user():
    msg  =''

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        relationship = request.form['relationship']
        phone_number=request.form['mobile']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email, ))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'^[6-9]\d{9}$',phone_number):
            msg='Invalid Phone number'
        elif not re.match(r'^[A-Za-z\s]+$',relationship):
            msg='Invalid Relationship'
        elif not email or not password or not relationship or not phone_number:
            msg = 'Please fill out the form!'
        else:
            role='user'
        
            cursor.execute('INSERT INTO accounts (name, email, password, relationship,role,mobile) VALUES (%s, %s, %s, %s,%s,%s)', (name, email, hashed_password, relationship,role,phone_number))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    else:
        msg = 'Please fill out the form!'

    # Use the full endpoint name when rendering the template
    return render_template('add_user.html', msg=msg)



@bp.route('/admin/approve_all_users', methods=['POST','GET'])
@admin_required
def approve_all_users():
    try:

        cur = mysql.connection.cursor()
        cur.execute("UPDATE accounts SET status = 'approve'")
        mysql.connection.commit()
        cur.close()
        flash('All users have been approved successfully.', 'success')
    except Exception as e:
        flash('An error occurred while approving all users.', 'error')
        print("Error:", e)
    cur = mysql.connection.cursor()
        
        # Get the count of users whose status is not 'approve'
    cur.execute("SELECT COUNT(*) FROM accounts WHERE status != 'approve'")
    result = cur.fetchone()
    count = result['COUNT(*)']
    print(count)
    cur.close()
   

# Pass the count to the template
    return redirect(url_for('routes.users_view'))
    
   




   



@bp.route('/admin/users_view', methods=['POST','GET'])
def users_view():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, relationship, role,mobile,volunteer,basic,advanced,food,expert,transport,event,status FROM accounts order by id DESC")
    users = cur.fetchall()
    
    cur.close()
    cur = mysql.connection.cursor()
        
        # Get the count of users whose status is not 'approve'
    cur.execute("SELECT COUNT(*) FROM accounts WHERE status != 'approve'")
    result = cur.fetchone()
    count = result['COUNT(*)']
    print(count)
    cur.close()
   
    
  
    
    return render_template('user_table.html',users=users,count=count)

@bp.route('/admin/events_view',methods=['POST','GET'])
def events_view():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, event_date, event_start_time,event_end_time, event_class FROM event1")
    events = cur.fetchall()
    
    cur.close()
    return render_template('events_table.html',events=events)

@bp.route('/admin/editevents/<int:event_id>', methods=['GET', 'POST'])
def editevents(event_id):

    


    cur = mysql.connection.cursor()
    cur.execute("SELECT id, event_name, start_time, end_time FROM events WHERE id=%s", (event_id,))
    event = cur.fetchone()
    
    cur.close()

    return render_template('edit_event.html', event=event)



@bp.route('/admin/update_event/<int:event_id>', methods=['POST'])
def update_event(event_id):
    if request.method == 'POST':
        # Fetch event details from the form data
        name = request.form['name']
    
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        tutor=request.form['tutor']

        # Update event details in the database
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE events SET event_name = %s, start_time = %s, end_time = %s, tutor=%s WHERE id = %s",
                       (name, start_time, end_time, tutor,event_id))
        mysql.connection.commit()
        cursor.close()

        # Redirect to a success page or another appropriate route
        flash('Event details updated successfully.', 'success')
        return redirect(url_for('routes.admin'))






@bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    # Check if the current user has the 'admin' role
    if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
          
            relationship = request.form['relationship']
            
            role = request.form['role']
            phone_number=request.form['mobile']
            volunter = 'yes' if 'volunteer' in request.form else 'no'
            teaching = 'yes' if 'basic' in request.form else 'no'
            ateaching = 'yes' if 'advanced' in request.form else 'no'
            expert='yes' if'expert' in request.form else 'no'
            food = 'yes' if 'food' in request.form else 'no'
            transport='yes' if 'transport' in request.form else 'no'
            event='yes' if 'event' in request.form else 'no'
            cur = mysql.connection.cursor()
            cur.execute("UPDATE accounts SET name=%s, email=%s, relationship=%s, role=%s, Mobile=%s, volunteer=%s, basic=%s, advanced=%s, expert=%s,food=%s ,transport=%s,event=%s WHERE id=%s",
                        (name, email, relationship, role, phone_number, volunter, teaching, ateaching,expert,food,transport,event, user_id))
            mysql.connection.commit()
            cur.close()

            flash('User information updated successfully.', 'success')
            return redirect(url_for('routes.users_view'))

        # Fetch user details by ID
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, relationship, role ,Mobile FROM accounts WHERE id=%s", (user_id,))
    user = cur.fetchone()
    
    cur.close()

    return render_template('edit_user.html', user=user)

@bp.route('/admin/approve_user/<int:user_id>',methods=['POST'])
@admin_required
def approve_user(user_id):
    
      if 'role' in session and session['role'] == 'admin':
        cur = mysql.connection.cursor()
        cur.execute('UPDATE accounts SET status=%s WHERE id=%s', ('approve', user_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('routes.users_view'))


    



@bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    # Check if the current user has the 'admin' role
    if 'role' in session and session['role'] == 'admin':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM accounts WHERE id=%s", (user_id,))
        mysql.connection.commit()
        cur.close()


        flash('User deleted successfully.', 'success')
        return redirect(url_for('routes.admin'))
    else:
        flash('Unauthorized access. Please log in as an admin.', 'danger')
        return redirect(url_for('routes.login'))



@bp.route('/admin/addevent', methods=['POST', 'GET'])
def addevent():
    if request.method == 'POST':
        date = request.form['eventDate']
        time_start = request.form['event-start-time']
        end_time = request.form['event-end-time']
        course = request.form['event-class']
    

        # Assuming you have a MySQL database connection named mysql
        cur = mysql.connection.cursor()

        # Corrected the number of placeholders in the SQL query
        cur.execute('INSERT INTO event1 (event_date, event_start_time, event_end_time, event_class) VALUES (%s, %s, %s, %s)',
                    (date, time_start, end_time, course))

        mysql.connection.commit()
        cur.close()


        
        return redirect(url_for('routes.admin'))
    

    return render_template('add_event.html')




@bp.route('/admin/edit_event/<int:event_id>', methods=['POST','GET'])

def edit_event(event_id):
    # Check if the current user has the 'admin' role
  

    return render_template('edit_event.html')




@bp.route('/user/delete/<int:event_id>', methods=['POST', 'GET'])
def delete(event_id):
    user_id = session['id']
    
    # Delete record from the database
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM event_registration WHERE event_id = %s AND user_id = %s', (event_id, user_id))
    mysql.connection.commit()
    cursor.close()
    
    # Delete corresponding image file
    filename = f"qr_code_({event_id}, {user_id}).png"
    folder_path = 'app/static/qr'
    file_path = os.path.join(folder_path, filename)
    
    try:
        os.remove(file_path)
        print(f"File '{filename}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting file '{filename}': {e}")
    
    return redirect(url_for('routes.calendar'))


@bp.route('/admin/delete_event/<int:event_id>', methods=['POST'])
@admin_required
def delete_event(event_id):
    # Check if the current user has the 'admin' role
    if 'role' in session and session['role'] == 'admin':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM events WHERE id=%s", (event_id,))
        mysql.connection.commit()
        cur.close()

        flash('User deleted successfully.', 'success')

        return redirect(url_for('routes.admin'))
    else:
        flash('Unauthorized access. Please log in as an admin.', 'danger')
        return redirect(url_for('routes.login'))


