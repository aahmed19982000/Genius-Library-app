from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import psycopg2

# تعيين حجم النافذة
Window.size = (400, 700)
Window.minimum_width = 350
Window.minimum_height = 500

class MainWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        # تعيين لون خلفية النافذة
        Window.clearcolor = (0.98, 0.98, 0.98, 1)
        
        # إنشاء جدول المستخدمين إذا لم يكن موجوداً
        self.create_users_table()
        
        # استيراد شاشة تسجيل الدخول
        from Screen.login import LoginScreen
        from Screen.register import RegisterScreen
        
        # تحميل ملف KV الخاص بشاشة الدخول أولاً
        try:
            Builder.load_file('Screen/login.kv')
            Builder.load_file('Screen/register.kv')
            Builder.load_file('main-design.kv')
        except Exception as e:
            print(f"خطأ في تحميل login.kv: {e}")
        
        # إنشاء مدير الشاشات
        sm = WindowManager()
        
        # إضافة الشاشات
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainWindow(name='main'))
        
        # جعل شاشة تسجيل الدخول هي الشاشة الأولى
        sm.current = 'login'
        
        return sm
    
    def create_users_table(self):
        """إنشاء جدول المستخدمين في قاعدة البيانات"""
        try:
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
            
            # إضافة مستخدم تجريبي للاختبار إذا كان الجدول فارغاً
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
            
            if count == 0:
                cur.execute(
                    "INSERT INTO users (name, password) VALUES (%s, %s)",
                    ("admin", "admin123")
                )
                print("تم إضافة مستخدم تجريبي")
            
            conn.commit()
            conn.close()
            print("تم الاتصال بقاعدة البيانات بنجاح")
            
        except Exception as e:
            print("خطأ في الاتصال بقاعدة البيانات:", e)
    
    def on_start(self):
        print("تم بدء تشغيل التطبيق")

if __name__ == '__main__':
    MyApp().run()