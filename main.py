# ========== تفعيل الدعم التلقائي للعربية ==========
import arabic_patch

from kivy.app import App
from kivy.core.window import Window
import os
import sys


# ========== إعداد النافذة ==========
Window.size = (400, 700)
Window.minimum_width = 350
Window.minimum_height = 500

# ========== إضافة المسار الحالي للنظام ==========
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

class MyApp(App):
    current_user = None  # تعريف متغير المستخدم الحالي
    
    def build(self):
        Window.clearcolor = (0.98, 0.98, 0.98, 1)
        
        # تسجيل الخطوط
        self.register_fonts()
        
        # إنشاء جدول المستخدمين في قاعدة البيانات
        self.create_users_table()
        
        # استيراد وتحميل واجهات التطبيق
        from app_loader import load_application
        return load_application()
    
    def register_fonts(self):
        """تسجيل الخطوط العربية والرموز"""
        from kivy.core.text import LabelBase
        
        # تسجيل الخط العربي AwanZaman
        try:
            LabelBase.register(
                name='AwanZaman',
                fn_regular='fonts/ArbFONTS-AwanZaman-Regular.ttf'
            )
            print("✅ تم تسجيل الخط العربي (AwanZaman)")
        except Exception as e:
            print(f"⚠️ خطأ في تسجيل الخط العربي AwanZaman: {e}")
        
        # تسجيل خط Material Symbols Outlined
        try:
            LabelBase.register(
                name='MaterialSymbolsOutlined',
                fn_regular='fonts/MaterialSymbolsOutlined-VariableFont_FILL,GRAD,opsz,wght.ttf'
            )
            print("✅ تم تسجيل خط Material Symbols Outlined")
        except Exception as e:
            print(f"⚠️ خطأ في تسجيل Material Symbols Outlined: {e}")
            try:
                LabelBase.register(
                    name='MaterialSymbolsOutlined',
                    fn_regular='fonts/MaterialSymbolsOutlined.ttf'
                )
                print("✅ تم تسجيل خط Material Symbols Outlined (الاسم المختصر)")
            except:
                print("⚠️ لم يتم العثور على خط Material Symbols Outlined")
    
    def create_users_table(self):
        """إنشاء جدول المستخدمين في قاعدة البيانات"""
        try:
            import psycopg2
            conn = psycopg2.connect(
                host="localhost",
                database="kivy_app",
                user="ahmed",
                password="123456",
                port="5432"
            )
            cur = conn.cursor()
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    password VARCHAR(50)
                )
            """)
            
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
            
            if count == 0:
                cur.execute(
                    "INSERT INTO users (name, password) VALUES (%s, %s)",
                    ("admin", "admin123")
                )
                print("✅ تم إضافة مستخدم تجريبي")
            
            conn.commit()
            conn.close()
            print("✅ تم الاتصال بقاعدة البيانات بنجاح")
            
        except Exception as e:
            print("❌ خطأ في الاتصال بقاعدة البيانات:", e)
    
    def on_start(self):
        print("🚀 تم بدء تشغيل التطبيق")
    
    def on_stop(self):
        print("🛑 إغلاق التطبيق")

if __name__ == '__main__':
    MyApp().run()