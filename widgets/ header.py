# widgets/header.py
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock

class CustomHeader(BoxLayout):
    """Header مخصص مشابه لموقع Genius-Library"""
    
    # ✅✅✅ أضف هذه الخاصية
    notification_count = NumericProperty(0)
    
    # خصائص أخرى موجودة
    user_name = StringProperty("ضيف")
    search_hint = StringProperty("ابحث عن خدمة طباعة...")
    
    # Callbacks
    menu_press = ObjectProperty(None)
    logo_press = ObjectProperty(None)
    search_press = ObjectProperty(None)
    profile_press = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        
    def on_search_enter(self, instance, value):
        """عند الضغط على Enter في حقل البحث"""
        if value and not instance.focus:
            if self.search_press:
                self.search_press(value)
    
    def show_notification(self):
        """عرض الإشعارات"""
        if self.notification_count > 0:
            print(f"🔔 لديك {self.notification_count} إشعارات جديدة")