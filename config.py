import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu_clave_secreta')

    # Configuración de la base de datos
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Otras configuraciones de la aplicación
    # ...

