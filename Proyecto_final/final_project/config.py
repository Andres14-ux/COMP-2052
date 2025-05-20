import os

class Config:
    """
    Configuración general de la aplicación Flask para entorno local con XAMPP.
    """

    # Clave secreta para sesiones y protección CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-flask')

    # URI de conexión a la base de datos MySQL (XAMPP)
    # Asegúrate de que la base de datos 'tickets_db' exista y haya sido importada desde 06_tickets.sql
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost/seguimiento_tickets'
    )

    # Desactiva el seguimiento de modificaciones de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
