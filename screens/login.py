from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock

from bidi.algorithm import get_display
import arabic_reshaper
import psycopg2

# ----------------------------------------------------------
#   دالة الاتصال وإحضار المستخدم من قاعدة البيانات
# ----------------------------------------------------------
def get_user(username, password):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="kivy_app",
            user="ahmed",
            password="123456",
            port="5432"
        )
        cur = conn.cursor()

        # البحث عن المستخدم
        cur.execute(
            "SELECT * FROM users WHERE name=%s AND password=%s",
            (username, password)
        )
        result = cur.fetchone()

        conn.close()
        return result

    except Exception as e:
        print("Database Error:", e)
        return None

# ----------------------------------------------------------
#                     شاشة تسجيل الدخول
# ----------------------------------------------------------
class LoginScreen(Screen):
    error_message = StringProperty('')
    success_message = StringProperty('')
    login_success = BooleanProperty(False)

    def validate_input(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()

        # تحقق من الحقول
        if not username:
            self.show_error_ar("يرجى إدخال اسم المستخدم")
            return False

        if not password:
            self.show_error_ar("يرجى إدخال كلمة المرور")
            return False

        if len(username) < 3:
            self.show_error_ar("اسم المستخدم يجب أن يكون 3 أحرف على الأقل")
            return False

        if len(password) < 6:
            self.show_error_ar("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
            return False

        # تسجيل الدخول الحقيقي
        user = get_user(username, password)

        if user:
            self.login_success = True
            self.show_success_ar("تم تسجيل الدخول بنجاح")
            Clock.schedule_once(self.go_to_main, 1)
            return True
        else:
            self.show_error_ar("اسم المستخدم أو كلمة المرور غير صحيحة")
            return False

    def login(self):
        self.validate_input()

    def go_to_main(self, dt):
        app = App.get_running_app()
        app.root.current = "main"

    # ----------------------------------------------------------
    #          رسائل الواجهة بالعربية مع دعم Kivy
    # ----------------------------------------------------------
    def show_error_ar(self, text):
        reshaped = arabic_reshaper.reshape(text)
        self.error_message = get_display(reshaped)
        if hasattr(self.ids, 'error_container'):
            self.ids.error_container.height = dp(50)
            self.ids.error_container.opacity = 1

    def show_success_ar(self, text):
        reshaped = arabic_reshaper.reshape(text)
        self.success_message = get_display(reshaped)
        if hasattr(self.ids, 'success_label_container'):
            self.ids.success_label_container.height = dp(50)
            self.ids.success_label_container.opacity = 1

    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""
        if hasattr(self.ids, 'error_container'):
            self.ids.error_container.height = 0
            self.ids.error_container.opacity = 0
        if hasattr(self.ids, 'success_label_container'):
            self.ids.success_label_container.height = 0
            self.ids.success_label_container.opacity = 0

    def clear_error(self):
        """لإخفاء رسائل الخطأ عند البدء بالكتابة"""
        if hasattr(self.ids, 'error_container'):
            self.ids.error_container.height = 0
            self.ids.error_container.opacity = 0

    def show_register_screen(self):
        """دالة جديدة للانتقال إلى شاشة التسجيل"""
        self.manager.current = 'register'

    def show_forgot_password_screen(self):
        print("فتح شاشة نسيت كلمة المرور")

    def on_pre_enter(self):
        self.clear_messages()