from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.core.window import Window
from bidi.algorithm import get_display
import arabic_reshaper
from kivy.metrics import dp
from main import MainWindow

class LoginScreen(Screen):
    error_message = StringProperty('')
    success_message = StringProperty('')
    login_success = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = ''
        self.password = ''

    def validate_input(self):
        """التحقق من صحة بيانات الإدخال"""
        self.username = self.ids.username_input.text.strip()
        self.password = self.ids.password_input.text

        if self.username == 'admin' and self.password == '123456':
            self.login_success = True
            self.success_message = get_display(arabic_reshaper.reshape("تم تسجيل الدخول بنجاح"))
            self.show_success()
            from kivy.clock import Clock
            Clock.schedule_once(self.go_to_main, 1)
            return True

        if not self.username:
            self.error_message = get_display(arabic_reshaper.reshape("يرجى إدخال اسم المستخدم"))
            self.show_error()
            return False

        if not self.password:
            self.error_message = get_display(arabic_reshaper.reshape("يرجى إدخال كلمة المرور"))
            self.show_error()
            return False

        if len(self.username) < 3:
            self.error_message = get_display(arabic_reshaper.reshape("اسم المستخدم يجب أن يكون 3 أحرف على الأقل"))
            self.show_error()
            return False

        if len(self.password) < 6:
            self.error_message = get_display(arabic_reshaper.reshape("كلمة المرور يجب أن تكون 6 أحرف على الأقل"))
            self.show_error()
            return False

        return True

    def login(self):
        """دالة تسجيل الدخول"""
        if not self.validate_input():
            return
        else:
            # التأكيد على رسالة النجاح
            self.success_message = get_display(arabic_reshaper.reshape("تم تسجيل الدخول بنجاح"))
            self.show_success()

    def go_to_main(self, dt):
        app = App.get_running_app()
        app.root.current = "main"

    def clear_error(self):
        """مسح رسائل الخطأ"""
        self.error_message = ''
        self.ids.error_container.height = 0
        self.ids.error_container.opacity = 0

    def show_error(self):
        """عرض رسالة الخطأ"""
        if self.error_message:
            self.ids.error_container.height = dp(50)
            self.ids.error_container.opacity = 1
        else:
            self.ids.error_container.height = 0
            self.ids.error_container.opacity = 0

    # ----------------------------
    # دوال رسائل النجاح الجديدة
    # ----------------------------
    def clear_success(self):
        """مسح رسالة النجاح"""
        self.success_message = ''
        self.ids.success_container.height = 0
        self.ids.success_container.opacity = 0

    def show_success(self):
        """عرض رسالة النجاح"""
        if self.success_message:
            self.ids.success_container.height = dp(50)
            self.ids.success_container.opacity = 1
        else:
            self.ids.success_container.height = 0
            self.ids.success_container.opacity = 0
    # ----------------------------

    def show_register_screen(self):
        print("الانتقال إلى شاشة التسجيل...")

    def show_forgot_password_screen(self):
        print("الانتقال إلى شاشة استعادة كلمة المرور...")

    def on_enter(self):
        """عند دخول الشاشة"""
        self.clear_error()
        self.clear_success()
        self.login_success = False

Builder.load_file("Screen/login.kv")

if __name__ == "__main__":
    from kivy.uix.screenmanager import ScreenManager

    class LoginApp(App):
        def build(self):
            Window.clearcolor = (0.98, 0.98, 0.98, 1)
            sm = ScreenManager()
            sm.add_widget(LoginScreen(name='login'))
            return sm

    LoginApp().run()
