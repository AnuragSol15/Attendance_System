from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from backend import fetch_sheet_data, summarize_attendance

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20)

        # Logos
        logo_layout = BoxLayout(orientation='horizontal')  # Fixed
        logo_left = Image(source="C:/Users/yuvra/OneDrive/Desktop/KASHI/IIPS_attendance_app/Attendance_System/Davv_LOGO_removed_bg.png")
        logo_right = Image(source="C:/Users/yuvra/OneDrive/Desktop/KASHI/IIPS_attendance_app/Attendance_System/iipslogo.jpg")
        logo_layout.add_widget(logo_left)
        logo_layout.add_widget(Label(text="The Name of Institute", font_size=24, bold=True, color=(1, 1, 1, 1), halign='center'))
        logo_layout.add_widget(logo_right)
        self.layout.add_widget(logo_layout)

        # Course Selection
        course_selection_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.course_label = Label(text="Select Course:", color=(1, 1, 1, 1))
        self.course_dropdown = DropDown()
        for course in ["B.Com.(Hons.)(3Y)","MCA(5Y)", "MTech(IT)(5Y)", "MBA(MS)(5Y)", "MBA(TA)(5Y)", "MBA(MS)(2Y)", "MBA(TA)(2Y)", "MBA(APR)(2Y)", "MBA(Eship)(2Y)"]:
            btn = Button(text=course, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.course_dropdown.select(btn.text))
            self.course_dropdown.add_widget(btn)
        self.course_input = Button(text="Select a Course", size_hint_y=None, height=40)
        self.course_input.bind(on_release=self.course_dropdown.open)
        self.course_dropdown.bind(on_select=lambda instance, x: setattr(self.course_input, 'text', x))
        course_selection_layout.add_widget(self.course_label)
        course_selection_layout.add_widget(self.course_input)
        self.layout.add_widget(course_selection_layout)

        # Link Input
        link_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.link_label = Label(text="Enter Google Sheet Link:", color=(1, 1, 1, 1))
        self.link_input = TextInput(hint_text="Paste sheet link here", multiline=False, foreground_color=(1, 1, 1, 1))
        link_input_layout.add_widget(self.link_label)
        link_input_layout.add_widget(self.link_input)
        self.layout.add_widget(link_input_layout)

        # Fetch Button
        self.fetch_button = Button(text="Fetch Attendance", size_hint_y=None, height=60, background_color=(0.5, 0.8, 1, 1))
        self.fetch_button.bind(on_press=self.fetch_data)
        self.layout.add_widget(self.fetch_button)

        self.add_widget(self.layout)
    
    def fetch_data(self, instance):
        sheet_url = self.welcome_screen.link_input.text
        course = self.welcome_screen.course_input.text  # Corrected to use the Button's text

        try:
            data = fetch_sheet_data(sheet_url, course)  # Pass course to backend
            summary = summarize_attendance(data)

            result_text = "\n".join([f"{student}: {attendance['total_days_present']} days present" for student, attendance in summary.items()])

            self.result_screen.update_result(result_text)
            self.screen_manager.current = 'result'

        except Exception as e:
            self.result_screen.update_result(f"Error: {str(e)}")
            self.screen_manager.current = 'result'



class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # Result Label
        self.result_label = Label(text="", text_size=(Window.width, None), halign='center', color=(1, 1, 1, 1))
        self.layout.add_widget(self.result_label)

        self.add_widget(self.layout)

    def update_result(self, result_text):
        self.result_label.text = result_text


class AttendanceApp(App):
    def build(self):
        Window.clearcolor = (0.25, 0.3, 0.35, 1)  # Dark blue background

        # Create Screen Manager
        self.screen_manager = ScreenManager()
        self.welcome_screen = WelcomeScreen(name='welcome')
        self.result_screen = ResultScreen(name='result')
        self.screen_manager.add_widget(self.welcome_screen)
        self.screen_manager.add_widget(self.result_screen)

        return self.screen_manager

    

if __name__ == "__main__":
    AttendanceApp().run()
