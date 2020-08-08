from app import db, ma
from app.models import Base

class Category(Base):
    name = db.Column(db.String(30), nullable=False, unique=True)