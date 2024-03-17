from flask import (
  render_template, Blueprint, flash, g, redirect, request, session, url_for
 )
import functools
#Encriptacion de contraseña
from werkzeug.security import check_password_hash, generate_password_hash
from myblog.models.user import User
from myblog import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

#Registrar usuario
@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #capturar datos de POST
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username, generate_password_hash(password))

        error = None
        if not username:
            error = 'Se requiere Nombre de Usuario'
        elif not password:
            error = 'Se requiere una Contraseña'

        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El Usuario {username} ya esta registrado'
        flash(error)

    return render_template('auth/register.html')


#Iniciar Sesióm
@auth.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        #capturar datos de POST
        username = request.form.get('username')
        password = request.form.get('password')

        error = None

        user = User.query.filter_by(username = username).first()

        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'La contraseña es incorrecta'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('blog.index'))
        flash(error)

    return render_template('auth/login.html')

#Verifica si el usuario esta logeado
@auth.before_app_request
def load_logged_in_user():
    user_id =session.get('user_id')

    if user_id == None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

#Sirve para cerrar sesióm
@auth.route('/logout')
def log_out():
    session.clear()
    return redirect(url_for('blog.index'))


#le pide al usuario que es necesario loggearse para ver diferentes vistas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
