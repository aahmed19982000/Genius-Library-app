
# ========== تفعيل الدعم التلقائي للعربية ==========
import arabic_patch

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import psycopg2
import os
import sys

# ========== استيراد الـ Header بشكل صحيح ==========
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# جرب استيراد الـ Header الجديد
try:
    # جرب استيراد من ملف widgets.header_module لو موجود
    import widgets.header as header_module
    CustomHeader = header_module.CustomHeader
    print("✅ تم استيراد CustomHeader من widgets.header")
except ImportError as e:
    print(f"⚠️ خطأ في استيراد CustomHeader: {e}")
    # أنشئ CustomHeader بديل في الملف نفسه
    from kivy.uix.boxlayout import BoxLayout
    
    class CustomHeader(BoxLayout):
        search_hint = "ابحث عن خدمة طباعة..."
        
        def _trigger_menu_press(self):
            print("🔘 فتح القائمة الجانبية")
            # اربط هذه الوظيفة مع الشاشة الرئيسية
            app = App.get_running_app()
            screen = app.root.get_screen('main') if app.root and hasattr(app.root, 'get_screen') else None
            if screen:
                screen.menu_pressed()
        
        def _trigger_search_press(self, text):
            print(f"🔍 بحث عن: {text}")
            app = App.get_running_app()
            screen = app.root.get_screen('main') if app.root and hasattr(app.root, 'get_screen') else None
            if screen:
                screen.search_pressed(text)
        
        def _trigger_orders_press(self):
            print("📋 فتح قائمة الطلبات")
            # يمكنك ربط هذا بوظيفة في MainWindow
        
        def _trigger_profile_press(self):
            print("👤 فتح الملف الشخصي")
            app = App.get_running_app()
            screen = app.root.get_screen('main') if app.root and hasattr(app.root, 'get_screen') else None
            if screen:
                screen.profile_pressed()

# ========== إعداد النافذة ==========
Window.size = (400, 700)
Window.minimum_width = 350
Window.minimum_height = 500

class MainWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("🔄 MainWindow initialized")
    
    def menu_pressed(self):
        """عند الضغط على زر القائمة"""
        print("🔘 تم الضغط على زر القائمة")
    
    def logo_pressed(self):
        """عند الضغط على الشعار"""
        print("🏠 تم الضغط على الشعار")
    
    def search_pressed(self, text):
        """عند البحث"""
        if text and text.strip():
            print(f"🔍 بحث عن خدمة: {text}")
        else:
            print("⚠️ أدخل نص للبحث")
    
    def orders_pressed(self):
        """عند الضغط على زر الطلبات"""
        print("📋 فتح صفحة الطلبات")
    
    def profile_pressed(self):
        """عند الضغط على زر الملف الشخصي"""
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            print(f"👤 فتح صفحة الملف الشخصي للمستخدم: {app.current_user.get('name')}")
        else:
            print("⚠️ يجب تسجيل الدخول أولاً")
            if self.manager:
                self.manager.current = 'login'
    
    # ========== دوال جديدة لدعم تصميم main-design.kv ==========
    
    def notifications_pressed(self):
        """عند الضغط على زر الإشعارات"""
        print("🔔 فتح الإشعارات")
    
    def start_new_order(self):
        """بدء طلب طباعة جديد"""
        print("🖨️ بدء طلب طباعة جديد")
    
    def show_all_actions(self):
        """عرض كل الإجراءات السريعة"""
        print("📋 عرض كل الإجراءات السريعة")
    
    def print_images(self):
        """فتح قسم طباعة الصور"""
        print("🖼️ فتح قسم طباعة الصور")
    
    def print_documents(self):
        """فتح قسم طباعة المستندات"""
        print("📄 فتح قسم طباعة المستندات")
    
    def reorder(self):
        """إعادة طلب"""
        print("🔄 إعادة طلب سابق")
    
    def show_discount(self):
        """عرض تفاصيل الخصم"""
        print("🎟️ عرض تفاصيل الخصم")
    
    def track_order(self, order_id):
        """تتبع طلب معين"""
        print(f"📦 تتبع الطلب رقم {order_id}")
    
    def go_home(self):
        """الذهاب إلى الرئيسية"""
        print("🏠 الذهاب إلى الرئيسية")
    
    def wallet_pressed(self):
        """فتح المحفظة"""
        print("💰 فتح المحفظة")
        
class WindowManager(ScreenManager):
    pass

class MyApp(App):
    current_user = None  # تعريف المتغير
    
    def build(self):
        Window.clearcolor = (0.98, 0.98, 0.98, 1)
        
        # ========== تسجيل الخطوط ==========
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
        
        # تسجيل خط Material Symbols Outlined (باستخدام الاسم الأصلي)
        try:
            LabelBase.register(
                name='MaterialSymbolsOutlined',
                fn_regular='fonts/MaterialSymbolsOutlined-VariableFont_FILL,GRAD,opsz,wght.ttf'
            )
            print("✅ تم تسجيل خط Material Symbols Outlined")
        except Exception as e:
            print(f"⚠️ خطأ في تسجيل Material Symbols Outlined: {e}")
            # حاول مع الاسم المختصر
            try:
                LabelBase.register(
                    name='MaterialSymbolsOutlined',
                    fn_regular='fonts/MaterialSymbolsOutlined.ttf'
                )
                print("✅ تم تسجيل خط Material Symbols Outlined (الاسم المختصر)")
            except:
                print("⚠️ لم يتم العثور على خط Material Symbols Outlined")
        
        self.create_users_table()
        
        # تأكد من استيراد الشاشات بعد تحميل KV
        from Screen.login import LoginScreen
        from Screen.register import RegisterScreen
        
        # تحميل ملفات KV بالترتيب الصحيح
        try:
            # تحميل ملفات الـ widgets أولاً
            Builder.load_file('widgets/header.kv')
            print("✅ تم تحميل header.kv")
        except Exception as e:
            print(f"⚠️ خطأ في تحميل header.kv: {e}")
        
        try:
            Builder.load_file('Screen/login.kv')
            print("✅ تم تحميل login.kv")
        except Exception as e:
            print(f"⚠️ خطأ في تحميل login.kv: {e}")
        
        try:
            Builder.load_file('Screen/register.kv')
            print("✅ تم تحميل register.kv")
        except Exception as e:
            print(f"⚠️ خطأ في تحميل register.kv: {e}")
        
        try:
            Builder.load_file('main-design.kv')
            print("✅ تم تحميل main-design.kv")
        except Exception as e:
            print(f"⚠️ خطأ في تحميل main-design.kv: {e}")
        
        # إنشاء مدير الشاشات
        sm = WindowManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainWindow(name='main'))
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