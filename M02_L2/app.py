from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'
csrf = CSRFProtect(app)
#Formulario utilizando Flask-WTF
class RegistroForm(FlaskForm):
    nombre = StringField("Nombre", validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, message="El nombre debe de ser de 3 caracteres o mas.")
    ])
    correo = StringField("Correo", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Debe ingresar un correo válido.")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe ser de 6 caracteres o mas.")
    ])
    submit = SubmitField("Registrarse")
#Ruta para la página de inicio
@app.route("/")
def home():
    return render_template("home.html")
#Ruta para la página de registro
@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        flash(f"¡Usuario {form.nombre.data} fue registrado", "success")
        return redirect(url_for("registro"))
    return render_template("registro.html", form=form)
#Para correr la aplicación
if __name__ == "__main__":
    app.run(debug=True)
