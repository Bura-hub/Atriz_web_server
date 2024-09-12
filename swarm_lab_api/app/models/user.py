from sqlalchemy import Column, Integer, String
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Asegurar que el nombre de usuario sea único
    hashed_password = Column(String)
