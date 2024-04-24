from functools import wraps
from flask import flash, redirect, session, url_for
from flask_login import current_user

def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'role' in session and session['role'] == 'admin':
            print(session['role'])
            return view_func(*args, **kwargs)
        else:
            flash('You do not have permission to access this page.', 'danger')
            
            return redirect(url_for('routes.home'))
    return wrapped_view

def member_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args,**kwargs):
        if 'role' in session and session['role'] =='member':
            return view_func(*args,**kwargs)
        else:
            flash('You do not have permission to access this page ')
            return redirect(url_for('routes.home'))
    return wrapped_view



def users_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args,**kwargs):
        if 'role' in session and session['role'] =='user':
            return view_func(*args,**kwargs)
        else:
            flash('you Dont have permission to login tthis page')
            return redirect(url_for('routes.home'))
    return wrapped_view