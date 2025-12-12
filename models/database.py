# models/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os

# الحصول على بيانات الاتصال من متغيرات البيئة أو استخدام القيم الافتراضية
DATABASE_URL = os.getenv(
    'DATABASE_URL', 
    'postgresql://postgres:123456@localhost/kivy_app'
)

# إنشاء محرك قاعدة البيانات
engine = create_engine(
    DATABASE_URL,
    echo=True,  # عرض استعلامات SQL في الكونسول (للتطوير فقط)
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # التحقق من الاتصال قبل الاستخدام
)

# إنشاء جلسة محلية
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# جلسة عامة يمكن استخدامها في كل المكان
Session = scoped_session(SessionLocal)

# قاعدة Models
Base = declarative_base()

# Context Manager لإدارة الجلسات (مثل Django with)
@contextmanager
def get_db():
    """الحصول على جلسة قاعدة بيانات مع إدارة تلقائية للإغلاق"""
    db = Session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ تم إنشاء الجداول بنجاح")
        return True
    except Exception as e:
        print(f"❌ خطأ في إنشاء الجداول: {e}")
        return False

def drop_db():
    """حذف جميع الجداول (للتطوير فقط)"""
    Base.metadata.drop_all(bind=engine)
    print("🗑️ تم حذف جميع الجداول")