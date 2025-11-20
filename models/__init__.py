from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Import models after db is initialized
from models.user import User
from models.medicine import Medicine, AlternativeMedicine
from models.sale import Sale

__all__ = ['db', 'login_manager', 'User', 'Medicine', 'AlternativeMedicine', 'Sale']
