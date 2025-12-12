# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, Session
import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

# رابط قاعدة البيانات، عدل حسب إعداداتك
DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://ahmed:123456@localhost:5432/kivy_app")

# إنشاء الـ engine
engine = create_engine(DB_URL, pool_size=5, max_overflow=10, pool_pre_ping=True)

# Session factory
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

# قاعدة البيانات الأساسية للـ ORM
Base = declarative_base()

# إنشاء الجداول في قاعدة البيانات
def init_db():
    from models import User  # استدعاء الموديل قبل إنشاء الجداول
    Base.metadata.create_all(bind=engine)
    # إضافة مستخدم افتراضي لاختبار تسجيل الدخول
    session = SessionLocal()
    try:
        if not session.query(User).filter_by(username="ahmed").first():
            from models import User
            user = User(username="ahmed", password="123456")  # لاحقًا يمكن تشفير الباسورد
            session.add(user)
            session.commit()
    finally:
        session.close()

# دالة لجلب مستخدم حسب اسم المستخدم وكلمة المرور
def get_user(username: str, password: str):
    session: Session = SessionLocal()
    try:
        from models import User  # استدعاء الموديل هنا لتجنب ImportError
        # تحقق من اسم المستخدم وكلمة المرور
        user = session.query(User).filter(User.username == username, User.password == password).first()
        return user
    finally:
        session.close()
