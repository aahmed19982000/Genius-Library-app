# widgets/bottom_nav.py
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty

class BottomNavigationBar(BoxLayout):
    """شريط التنقل السفلي المخصص"""
    
    # خصائص اللون
    active_color = StringProperty("#1976d2")
    inactive_color = StringProperty("#9e9e9e")
    border_color = StringProperty("#e0e0e0")
    
    # خصائص الأزرار
    home_icon = StringProperty("home")
    orders_icon = StringProperty("receipt_long")
    wallet_icon = StringProperty("account_balance_wallet")
    profile_icon = StringProperty("person")
    
    home_label = StringProperty("الرئيسية")
    orders_label = StringProperty("الطلبات")
    wallet_label = StringProperty("المحفظة")
    profile_label = StringProperty("حسابي")
    
    # Callbacks
    home_press = ObjectProperty(None)
    orders_press = ObjectProperty(None)
    wallet_press = ObjectProperty(None)
    profile_press = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 85