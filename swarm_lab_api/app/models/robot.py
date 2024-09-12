from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Robot(Base):
    __tablename__ = "robots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
