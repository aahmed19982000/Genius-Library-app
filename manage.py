# manage.py
import sys
from models.database import init_db, Session
from models.user import UserManager

def show_help():
    print("""
أدوات إدارة المستخدمين:
    
    python manage.py createsuperuser   - إنشاء مدير نظام
    python manage.py listusers         - عرض جميع المستخدمين
    python manage.py createuser        - إنشاء مستخدم جديد
    python manage.py deleteuser <id>   - حذف مستخدم
    python manage.py deactivate <id>   - تعطيل مستخدم
    python manage.py activate <id>     - تفعيل مستخدم
    python manage.py help              - عرض هذه المساعدة
    """)

def create_superuser():
    print("\nإنشاء مدير نظام جديد:")
    username = input("اسم المستخدم: ")
    password = input("كلمة المرور: ")
    email = input("البريد الإلكتروني (اختياري): ") or None
    first_name = input("الاسم الأول (اختياري): ") or None
    last_name = input("الاسم الأخير (اختياري): ") or None
    
    try:
        user = UserManager.create_superuser(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        print(f"✅ تم إنشاء مدير النظام: {user.username}")
    except Exception as e:
        print(f"❌ خطأ: {e}")

def list_users():
    users = UserManager.get_all_users()
    print(f"\nعدد المستخدمين: {len(users)}")
    print("-" * 80)
    for user in users:
        status = "🟢" if user.is_active else "🔴"
        admin = "👑" if user.is_superuser else "👤"
        print(f"{status} {admin} {user.id:3} | {user.username:20} | {user.email or 'لا يوجد':30} | {user.created_at}")

if __name__ == '__main__':
    init_db()
    
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == 'createsuperuser':
        create_superuser()
    elif sys.argv[1] == 'listusers':
        list_users()
    elif sys.argv[1] == 'help':
        show_help()
    else:
        print(f"❌ أمر غير معروف: {sys.argv[1]}")
        show_help()