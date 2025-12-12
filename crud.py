from db import SessionLocal
from models import User

def get_user_by_username(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user
