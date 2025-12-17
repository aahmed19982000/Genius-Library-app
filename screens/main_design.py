from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.lang import Builder
import os

# تعريف الكلاسات المخصصة خارج MainDesign لضمان تعرف ملف KV عليها
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)

class ActionButton(Button):
    button_color = ListProperty([1, 1, 1, 1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)



class MainDesign(Screen):
    def __init__(self, **kwargs):
        # تأكد من تحميل الملف قبل super
        from kivy.lang import Builder
        kv_path = os.path.join(os.path.dirname(__file__), "main-design.kv")
        Builder.load_file(kv_path)
        super().__init__(**kwargs)

    def start_new_order(self):
        print("🖨️ بدء طلب جديد")

    def print_documents_action(self):
        # تأكد من إضافة صفحة الخدمات أولاً في ScreenManager
        if 'services_design' in self.manager.screen_names:
            self.manager.current = 'services_design'
        else:
            print("📄 طباعة مستندات (صفحة الخدمات غير مسجلة بعد)")

    # إضاافة الدالة التي تسببت في الخطأ
    def show_all_actions(self):
        print("🔍 تم الضغط على عرض الكل")
        # يمكنك توجيهه لصفحة الخدمات أيضاً هنا
        self.manager.current = 'services_design'