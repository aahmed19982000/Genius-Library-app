from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# تعيين حجم النافذة
Window.size = (400, 600)

class MainWindow(Screen):
    pass

class ImagesWindow(Screen):
    pass

class AudiosWindow(Screen):
    pass

class VideosWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class ArabicFormatConvertor(App):
    def build(self):
        # تحميل ملف KV
        return Builder.load_file('main-design.kv')

if __name__ == '__main__':
    ArabicFormatConvertor().run()