# models.py
from sqlalchemy import Column, Integer, String, DateTime, func
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # احفظ الـ hash مش الباسورد نصي
    created_at = Column(DateTime(timezone=True), server_default=func.now())
