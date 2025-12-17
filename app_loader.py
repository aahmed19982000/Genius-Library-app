"""
ملف تحميل التطبيق الرئيسي
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

def load_application():
    """تحميل التطبيق بالكامل مع إصلاح المسميات"""
    print("🔄 جاري تحميل التطبيق...")
    
    # تحميل ملفات KV أولاً
    load_kv_files()
    
    # استيراد الشاشات
    from screens.login import LoginScreen
    from screens.register import RegisterScreen
    from screens.main_design import MainDesign
    from screens.services_design import ServicesDesign
    
    sm = ScreenManager()
    
    # يجب أن تتطابق الأسماء هنا مع ما تستخدمه في الكود (root.manager.current)
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(RegisterScreen(name='register'))
    
    # غيرنا الاسم هنا إلى services_design ليطابق الكود الذي يسبب الانهيار
    sm.add_widget(MainDesign(name='main'))
    sm.add_widget(ServicesDesign(name='services_design'))
    
    sm.current = 'login'
    
    print("✅ تم تحميل التطبيق بنجاح")
    return sm

def load_kv_files():
    """تحميل جميع ملفات KV مع إصلاح الفواصل والمسارات"""
    import os
    from kivy.lang import Builder
    
    # أضفنا الفواصل الناقصة وتأكدنا من المسارات
    kv_files = [
        'screens/login.kv',
        'screens/register.kv',
        'screens/main-design.kv', # أضفنا فاصلة هنا
        'screens/services-design.kv',
        'screens/widgets/bottom_nav.kv'
    ]
    
    for kv_file in kv_files:
        if os.path.exists(kv_file):
            # التأكد من عدم تكرار تحميل الملف إذا كان الـ Screen يحمله داخله
            try:
                Builder.load_file(kv_file)
                print(f"✅ تم تحميل {kv_file}")
            except Exception as e:
                print(f"⚠️ {kv_file} محمل مسبقاً أو به خطأ: {e}")