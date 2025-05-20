from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Formulario para login de usuario
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Formulario para registrar un nuevo usuario
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    
    role = SelectField(
        'Role',
        choices=[('Usuario', 'Usuario'), ('Técnico', 'Técnico')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')

# Formulario para cambiar la contraseña del usuario
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# Formulario para crear o editar un Ticket
class TicketForm(FlaskForm):
    asunto = StringField('Asunto', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    
    prioridad = SelectField(
        'Prioridad',
        choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta')],
        validators=[DataRequired()]
    )

    # Campo 'estado' solo se usa en edición, pero colocamos default para evitar errores
    estado = SelectField(
        'Estado',
        choices=[('Abierto', 'Abierto'), ('En Progreso', 'En Progreso'), ('Cerrado', 'Cerrado')],
        default='Abierto'
    )

    # Este campo requiere que se le asignen choices dinámicamente en la vista con coerce=int
    tecnico_id = SelectField('Técnico Asignado', coerce=int, choices=[])

    submit = SubmitField('Guardar')
