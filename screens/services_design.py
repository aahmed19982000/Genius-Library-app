from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

# الحصول على المسار المطلق للمجلد الحالي
cur_dir = os.path.dirname(__file__)
kv_path = os.path.join(cur_dir, "services-design.kv")

# تحميل الملف خارج الكلاس لضمان تحميله مرة واحدة فقط عند استيراد الملف
if os.path.exists(kv_path):
    Builder.load_file(kv_path)

class ServicesDesign(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_back(self):
        self.manager.current = "main_design"