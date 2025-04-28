# app.py

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"  # Cambiar en producción

# Configurar Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Simulando una base de datos de usuarios
users = {
    "admin": {
        "password": generate_password_hash("adminpass"),
        "role": "admin"
    },
    "user": {
        "password": generate_password_hash("userpass"),
        "role": "user"
    }
}

# Modelo de Usuario
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = users[username]["role"]

# Cargar el usuario
@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# Ruta de inicio
@app.route("/")
def home():
    return "Bienvenido a la aplicación. <a href='/login'>Login</a>"

# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = users.get(username)
        
        if user and check_password_hash(user["password"], password):
            login_user(User(username))
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    
    return '''
        <form method="POST">
            Usuario: <input type="text" name="username"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Ruta protegida
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hola, {current_user.id}. Tu rol es {current_user.role}. <a href='/logout'>Logout</a>"

# Ruta para salir
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
