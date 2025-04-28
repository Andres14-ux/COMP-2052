# app.py

from flask import Flask, redirect, url_for, request, render_template_string
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed, Identity, AnonymousIdentity, identity_changed

app = Flask(__name__)
app.secret_key = "super_secret_key"

#Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#Configurar Flask-Principal
principal = Principal(app)

#Definir roles
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

#Simulando base de datos de usuarios
users = {
    "admin": {
        "password": "adminpass",
        "role": "admin"
    },
    "user": {
        "password": "userpass",
        "role": "user"
    }
}

#Clase Usuario
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = users[username]["role"]

#Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

#Asignar identidad cuando un usuario inicia sesión
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if current_user.is_authenticated:
        identity.user = current_user
        identity.provides.add(UserNeed(current_user.id))
        identity.provides.add(RoleNeed(current_user.role))

#Ruta principal
@app.route('/')
def home():
    return "Bienvenido. <a href='/login'>Login</a>"

#Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = users.get(username)
        if user_data and user_data["password"] == password:
            user = User(username)
            login_user(user)
            identity_changed.send(app, identity=Identity(user.id))
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos."
    
    return '''
    <form method="POST">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    '''

#Ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('home'))

#Ruta protegida general
@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hola {current_user.id}, tu rol es {current_user.role}. <a href='/admin'>Admin Page</a> | <a href='/profile'>Profile Page</a> | <a href='/logout'>Logout</a>"

#Ruta para admins
@app.route('/admin')
@login_required
@admin_permission.require(http_exception=403)
def admin_page():
    return "Bienvenido a la página de administrador."

#Ruta para usuarios normales
@app.route('/profile')
@login_required
@user_permission.require(http_exception=403)
def user_page():
    return "Bienvenido a tu perfil de usuario."

#Error
@app.errorhandler(403)
def forbidden(e):
    return "403 - No tienes permiso para acceder aquí.", 403

if __name__ == '__main__':
    app.run(debug=True)
