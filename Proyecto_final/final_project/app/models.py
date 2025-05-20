from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relationships
    tickets_as_user = db.relationship('Ticket', foreign_keys='Ticket.usuario_id', backref='usuario', lazy=True)
    tickets_as_tecnico = db.relationship('Ticket', foreign_keys='Ticket.tecnico_id', backref='tecnico', lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    asunto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.String(10), nullable=False)  # Baja, Media, Alta
    estado = db.Column(db.String(10), nullable=False, default='Abierto')  # Valor por defecto
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # ✅ Se permite NULL
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
