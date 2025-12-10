from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

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
        Window.clearcolor = (0.9, 0.9, 0.9, 1)
        
        # استيراد شاشة تسجيل الدخول
        from Screen.login import LoginScreen
        
        # تحميل ملف KV الرئيسي أولاً
        try:
            kv = Builder.load_file('main-design.kv')
        except Exception as e:
            print(f"خطأ في تحميل main-design.kv: {e}")
            # إنشاء واجهة بديلة
            kv = WindowManager()
        
        # إضافة شاشة تسجيل الدخول
        kv.add_widget(LoginScreen(name='login_screen'))
        kv.current = 'login_screen'
        kv.add_widget(MainWindow(name='main'))

        
        return kv
    
    def on_start(self):
        print("تم بدء تشغيل التطبيق")

if __name__ == '__main__':
    MyApp().run()