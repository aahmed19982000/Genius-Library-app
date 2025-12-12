from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
import psycopg2
from bidi.algorithm import get_display
import arabic_reshaper
import re


def go_to_login(self):
        """الانتقال لشاشة الدخول"""
        try:
            if hasattr(self, 'manager') and self.manager:
                self.manager.current = 'login'
        except Exception as e:
            print(f"Error going to login: {str(e)}")

class RegisterScreen(Screen):
    def reshape_arabic_text(self, textinput_instance):
        """إعادة تشكيل النص العربي في TextInput"""
        try:
            if not textinput_instance:
                return
                
            text = textinput_instance.text
            if not text:
                return
                
            # تحقق مما إذا كان هناك حروف عربية
            has_arabic = False
            for char in text:
                # نطاق الحروف العربية في Unicode
                if ('\u0600' <= char <= '\u06FF' or  # العربية
                    '\u0750' <= char <= '\u077F' or  # امتدادات العربية
                    '\u08A0' <= char <= '\u08FF' or  # امتدادات إضافية
                    '\uFB50' <= char <= '\uFDFF' or  # أشكال العرض العربية-أ
                    '\uFE70' <= char <= '\uFEFF'):   # أشكال العرض العربية-ب
                    has_arabic = True
                    break
            
            if has_arabic:
                # حفظ موضع المؤشر
                cursor_pos = textinput_instance.cursor[0]
                
                # إعادة تشكيل النص العربي
                reshaped = arabic_reshaper.reshape(text)
                bidi_text = get_display(reshaped)
                
                # تحديث النص فقط إذا كان مختلفاً
                if bidi_text != text:
                    textinput_instance.text = bidi_text
                    # استعادة موضع المؤشر مع التأكد من عدم تجاوز طول النص
                    new_cursor_pos = min(cursor_pos, len(bidi_text))
                    textinput_instance.cursor = (new_cursor_pos, 0)
                    
        except Exception as e:
            print(f"Error reshaping text: {str(e)}")
    
    def register_user(self):
        """تسجيل مستخدم جديد مع معالجة محسنة للأخطاء"""
        try:
            # استخراج البيانات مع التحقق من وجود العناصر في self.ids
            username = self.ids.get('username_input', '').text.strip() if hasattr(self, 'ids') and 'username_input' in self.ids else ''
            password = self.ids.get('password_input', '').text.strip() if hasattr(self, 'ids') and 'password_input' in self.ids else ''
            confirm_password = self.ids.get('confirm_password_input', '').text.strip() if hasattr(self, 'ids') and 'confirm_password_input' in self.ids else ''
            fullname = self.ids.get('fullname_input', '').text.strip() if hasattr(self, 'ids') and 'fullname_input' in self.ids else ''
            email = self.ids.get('email_input', '').text.strip() if hasattr(self, 'ids') and 'email_input' in self.ids else ''
            phone = self.ids.get('phone_input', '').text.strip() if hasattr(self, 'ids') and 'phone_input' in self.ids else ''
            address = self.ids.get('address_input', '').text.strip() if hasattr(self, 'ids') and 'address_input' in self.ids else ''
            
            # التحقق من البيانات الأساسية
            if not username or not password or not confirm_password:
                self.show_error(get_display(arabic_reshaper.reshape("اسم المستخدم وكلمة المرور مطلوبة!")))
                return
            
            if not fullname:
                self.show_error(get_display(arabic_reshaper.reshape("الاسم الكامل مطلوب!")))
                return
            
            if password != confirm_password:
                self.show_error(get_display(arabic_reshaper.reshape("كلمات المرور غير متطابقة!")))
                return
            
            if len(password) < 6:
                self.show_error(get_display(arabic_reshaper.reshape("كلمة المرور يجب أن تكون 6 أحرف على الأقل!")))
                return
            
            # التحقق من صحة البريد الإلكتروني (إذا تم إدخاله)
            if email and not self.is_valid_email(email):
                self.show_error(get_display(arabic_reshaper.reshape("البريد الإلكتروني غير صالح!")))
                return
            
            # الاتصال بقاعدة البيانات
            conn = psycopg2.connect(
                host="localhost",
                database="kivy_app",
                user="ahmed",
                password="123456",
                port="5432"
            )
            cur = conn.cursor()
            
            # التحقق من وجود اسم المستخدم
            cur.execute("SELECT id FROM users WHERE name = %s", (username,))
            if cur.fetchone():
                self.show_error(get_display(arabic_reshaper.reshape("اسم المستخدم موجود مسبقاً!")))
                conn.close()
                return
            
            # التحقق من وجود البريد الإلكتروني (إذا كان فريداً)
            if email:
                cur.execute("SELECT id FROM users WHERE email = %s AND email IS NOT NULL", (email,))
                if cur.fetchone():
                    self.show_error(get_display(arabic_reshaper.reshape("البريد الإلكتروني مستخدم مسبقاً!")))
                    conn.close()
                    return
            
            # إضافة المستخدم الجديد مع إرجاع الID المولد
            cur.execute(
                """INSERT INTO users (name, password, fullname, email, phone, address) 
                   VALUES (%s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (
                    username, 
                    password, 
                    fullname if fullname else None,
                    email if email else None,
                    phone if phone else None,
                    address if address else None
                )
            )
            
            # الحصول على الID المولد
            new_user_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            
            print(f"تم إنشاء مستخدم جديد برقم ID: {new_user_id}")
            self.show_success(get_display(arabic_reshaper.reshape("تم التسجيل بنجاح!")))
            go_to_login(self)
            # مسح الحقول بعد 1.5 ثانية
            Clock.schedule_once(lambda dt: self.clear_fields(), 1.5)
            

        
            
        except psycopg2.IntegrityError as e:
            # خطأ في تكامل البيانات (مثل ID مكرر أو بيانات فريدة مكررة)
            error_msg = str(e).lower()
            if "duplicate key" in error_msg or "already exists" in error_msg:
                self.show_error(get_display(arabic_reshaper.reshape("خطأ: بيانات مكررة في النظام!")))
            elif "unique constraint" in error_msg:
                self.show_error(get_display(arabic_reshaper.reshape("اسم المستخدم أو البريد الإلكتروني موجود مسبقاً!")))
            else:
                self.show_error(get_display(arabic_reshaper.reshape("خطأ في البيانات المدخلة!")))
            print(f"Database integrity error: {str(e)}")
            
        except psycopg2.Error as e:
            # خطأ عام في قاعدة البيانات
            self.show_error(get_display(arabic_reshaper.reshape("خطأ في الاتصال بقاعدة البيانات!")))
            print(f"Database error: {str(e)}")
            
        except Exception as e:
            # خطأ عام
            self.show_error(get_display(arabic_reshaper.reshape("حدث خطأ غير متوقع!")))
            print(f"Unexpected error: {str(e)}")
    
    def is_valid_email(self, email):
        """التحقق من صحة البريد الإلكتروني"""
        if not email:
            return True
            
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def show_error(self, message):
        """عرض رسالة خطأ"""
        try:
            # التأكد من وجود العناصر قبل استخدامها
            if hasattr(self, 'ids'):
                if 'error_label' in self.ids:
                    self.ids.error_label.text = message
                
                if 'error_container' in self.ids:
                    anim = Animation(height=dp(45), opacity=1, duration=0.3)
                    anim.start(self.ids.error_container)
                
                # إخفاء رسالة النجاح إذا كانت ظاهرة
                if 'success_label_container' in self.ids:
                    anim2 = Animation(height=0, opacity=0, duration=0.3)
                    anim2.start(self.ids.success_label_container)
            else:
                print("Warning: self.ids not available")
                
        except Exception as e:
            print(f"Error showing error message: {str(e)}")
    
    def show_success(self, message):
        """عرض رسالة نجاح"""
        try:
            # التأكد من وجود العناصر قبل استخدامها
            if hasattr(self, 'ids'):
                if 'success_label' in self.ids:
                    self.ids.success_label.text = message
                
                if 'success_label_container' in self.ids:
                    anim = Animation(height=dp(45), opacity=1, duration=0.3)
                    anim.start(self.ids.success_label_container)
                
                # إخفاء رسالة الخطأ إذا كانت ظاهرة
                if 'error_container' in self.ids:
                    anim2 = Animation(height=0, opacity=0, duration=0.3)
                    anim2.start(self.ids.error_container)
            else:
                print("Warning: self.ids not available")
                
        except Exception as e:
            print(f"Error showing success message: {str(e)}")
    
    def clear_fields(self):
        """مسح جميع الحقول"""
        try:
            if hasattr(self, 'ids'):
                fields = ['username_input', 'password_input', 'confirm_password_input', 
                         'fullname_input', 'email_input', 'phone_input', 'address_input']
                
                for field in fields:
                    if field in self.ids:
                        self.ids[field].text = ""
        except Exception as e:
            print(f"Error clearing fields: {str(e)}")
    
    def go_to_login(self):
        """الانتقال لشاشة الدخول"""
        try:
            if hasattr(self, 'manager') and self.manager:
                self.manager.current = 'login'
        except Exception as e:
            print(f"Error going to login: {str(e)}")
    
    def on_pre_enter(self):
        """تم التنفيذ قبل دخول الشاشة"""
        try:
            # مسح أي رسائل سابقة عند الدخول للشاشة
            if hasattr(self, 'ids'):
                if 'error_container' in self.ids:
                    self.ids.error_container.height = 0
                    self.ids.error_container.opacity = 0
                    if 'error_label' in self.ids:
                        self.ids.error_label.text = ""
                
                if 'success_label_container' in self.ids:
                    self.ids.success_label_container.height = 0
                    self.ids.success_label_container.opacity = 0
                    if 'success_label' in self.ids:
                        self.ids.success_label.text = ""
                        
                # مسح الحقول
                self.clear_fields()
        except Exception as e:
            print(f"Error in on_pre_enter: {str(e)}")