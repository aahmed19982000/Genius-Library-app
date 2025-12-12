# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
import re
from datetime import datetime
from .database import Base

class User(Base):
    """نموذج المستخدم (يشبه Django User Model)"""
    __tablename__ = "users"
    
    # الحقول الأساسية
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    password = Column(String(255), nullable=False)  # سيتم تشفيرها لاحقاً
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # الحقول الإضافية
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # معلومات إضافية
    address = Column(Text, nullable=True)
    city = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    
    # Timestamps تلقائية
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Validators (مثل validators في Django)
    @validates('username')
    def validate_username(self, key, username):
        """التحقق من صحة اسم المستخدم"""
        if not username:
            raise ValueError("اسم المستخدم مطلوب")
        if len(username) < 3:
            raise ValueError("اسم المستخدم يجب أن يكون 3 أحرف على الأقل")
        if len(username) > 50:
            raise ValueError("اسم المستخدم يجب ألا يتجاوز 50 حرفاً")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError("اسم المستخدم يمكن أن يحتوي على حروف وأرقام وشرطة سفلية فقط")
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        """التحقق من صحة البريد الإلكتروني"""
        if email:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValueError("بريد إلكتروني غير صالح")
        return email
    
    @validates('phone')
    def validate_phone(self, key, phone):
        """التحقق من صحة رقم الهاتف"""
        if phone:
            # قبول الصيغ: 01012345678، +201012345678، 00201012345678
            if not re.match(r'^[\+]?[0-9\s\-\(\)]{8,20}$', phone):
                raise ValueError("رقم هاتف غير صالح")
        return phone
    
    # Methods (مثل methods في Django)
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """الحصول على الاسم الكامل"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username
    
    def set_password(self, password):
        """تعيين كلمة المرور (سيتم تشفيرها لاحقاً)"""
        if len(password) < 6:
            raise ValueError("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
        self.password = password  # في الإنتاج، استخدم hashing
    
    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return self.password == password  # في الإنتاج، استخدم hash verification
    
    def to_dict(self):
        """تحويل النموذج لـ dictionary (مثل Django serializers)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,
            'date_joined': self.date_joined.isoformat() if self.date_joined else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class UserManager:
    """مدير المستخدمين (مشابه لـ Django Model Manager)"""
    
    @staticmethod
    def create_user(username, password, email=None, **extra_fields):
        """إنشاء مستخدم عادي"""
        with get_db() as db:
            user = User(username=username, email=email, **extra_fields)
            user.set_password(password)
            db.add(user)
            db.flush()  # للحصول على ID
            return user
    
    @staticmethod
    def create_superuser(username, password, email=None, **extra_fields):
        """إنشاء مدير نظام"""
        with get_db() as db:
            user = User(
                username=username,
                email=email,
                is_staff=True,
                is_superuser=True,
                is_active=True,
                **extra_fields
            )
            user.set_password(password)
            db.add(user)
            db.flush()
            return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """الحصول على مستخدم بواسطة الـ ID"""
        with get_db() as db:
            return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(username):
        """الحصول على مستخدم بواسطة اسم المستخدم"""
        with get_db() as db:
            return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """الحصول على مستخدم بواسطة البريد الإلكتروني"""
        with get_db() as db:
            return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def authenticate(username, password):
        """المصادقة على المستخدم (مثل Django authenticate)"""
        with get_db() as db:
            user = db.query(User).filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if user and user.check_password(password) and user.is_active:
                return user
        return None
    
    @staticmethod
    def get_all_users():
        """الحصول على جميع المستخدمين"""
        with get_db() as db:
            return db.query(User).order_by(User.created_at.desc()).all()
    
    @staticmethod
    def filter_users(**filters):
        """تصفية المستخدمين"""
        with get_db() as db:
            query = db.query(User)
            for key, value in filters.items():
                if hasattr(User, key):
                    query = query.filter(getattr(User, key) == value)
            return query.all()
    
    @staticmethod
    def update_user(user_id, **updates):
        """تحديث بيانات مستخدم"""
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                for key, value in updates.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                db.flush()
                return user
        return None
    
    @staticmethod
    def delete_user(user_id):
        """حذف مستخدم"""
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                db.delete(user)
                db.flush()
                return True
        return False