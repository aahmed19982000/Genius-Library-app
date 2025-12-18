import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout

# 1. تحديد مسار ملف الـ KV (تأكد أن الاسم مطابق لملف الـ KV لديك)
cur_dir = os.path.dirname(__file__)
kv_path = os.path.join(cur_dir, "services-design.kv")

# 2. تعريف الكلاس الفرعي للبطاقة (يجب أن يكون قبل كلاس الشاشة)
class ServiceCard(BoxLayout):
    title = StringProperty("")
    description = StringProperty("")
    icon_source = StringProperty("")
    icon_bg_color = ColorProperty([1, 1, 1, 1])

# 3. تعريف كلاس الشاشة الرئيسي
class ServicesScreen(Screen):
    def __init__(self, **kw):
        super(ServicesScreen, self).__init__(**kw)

# 4. الربط الإجباري للملف (يمنع الشاشة البيضاء)
if os.path.exists(kv_path):
    Builder.load_file(kv_path)
    print(f"✅ تم ربط واجهة الخدمات بنجاح من المسار: {kv_path}")
else:
    print(f"❌ خطأ: لم يتم العثور على ملف الـ KV في: {kv_path}")