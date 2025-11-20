from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db initialization to avoid circular imports
from models.user import User
from models.medicine import Medicine
from models.sale import Sale
from models.alternative_medicine import AlternativeMedicine
