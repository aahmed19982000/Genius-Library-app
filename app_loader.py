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
    from screens.services_design import ServicesScreen
    
    sm = ScreenManager()
    
    # يجب أن تتطابق الأسماء هنا مع ما تستخدمه في الكود (root.manager.current)
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(RegisterScreen(name='register'))
    
    # غيرنا الاسم هنا إلى services_design ليطابق الكود الذي يسبب الانهيار
    sm.add_widget(MainDesign(name='main'))
    sm.add_widget(ServicesScreen(name='services_design'))
    
    sm.current = 'login'
    
    print("✅ تم تحميل التطبيق بنجاح")
    return sm

def load_kv_files():
    from kivy.lang import Builder
    import os
    
    # قائمة الملفات
    kv_files = [
        'screens/login.kv',
        'screens/register.kv',
        'screens/main-design.kv',
       # 'screens/services-design.kv'
    ]
    
    for kv_file in kv_files:
        if os.path.exists(kv_file):
            # استخدم unload_file أولاً لتنظيف أي محاولات تحميل خاطئة سابقة
            Builder.unload_file(kv_file)
            Builder.load_file(kv_file)
            print(f"✅ Loaded: {kv_file}")