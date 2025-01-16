from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from backend import fetch_sheet_data, summarize_attendance
# Assuming backend.py functions are defined as before

class AttendanceApp(App):
    def build(self):
        Window.clearcolor = (0.25, 0.3, 0.35, 1)  # Dark blue background

        # Create a base layout with a colored rectangle for the background
        self.layout = BoxLayout(orientation='vertical', padding=20)
        with self.layout.canvas.before:
            Color(*Window.clearcolor)  # Unpack clearcolor values
            self.background = Rectangle(size=(Window.width, Window.height), pos=(0, 0)) 

        # App Title with increased font size and centered alignment
        self.title_label = Label(text="Attendance Management System", font_size=24, bold=True, color=(1, 1, 1, 1), halign='center')
        self.layout.add_widget(self.title_label)

        # Course Selection with improved layout and spacing
        course_selection_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.course_label = Label(text="Select Course:", color=(1, 1, 1, 1))
        self.course_dropdown = DropDown()
        for course in ["B.Com.(Hons.)(3Y)","MCA(5Y)", "MTech(IT)(5Y)", "MBA(MS)(5Y)", "MBA(TA)(5Y)", "MBA(MS)(2Y)", "MBA(TA)(2Y)", "MBA(APR)(2Y)", "MBA(Eship)(2Y)"]:
            btn = Button(text=course, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.course_dropdown.select(btn.text))
            self.course_dropdown.add_widget(btn)
        self.course_input = Button(text="...", size_hint_y=None, height=40, on_release=self.course_dropdown.open)
        course_selection_layout.add_widget(self.course_label)
        course_selection_layout.add_widget(self.course_input)
        self.layout.add_widget(course_selection_layout)

        # Link Input with clear labels and white text color
        link_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.link_label = Label(text="Enter Google Sheet Link:", color=(1, 1, 1, 1))
        self.link_input = TextInput(hint_text="Paste sheet link here", multiline=False, foreground_color=(1, 1, 1, 1))
        link_input_layout.add_widget(self.link_label)
        link_input_layout.add_widget(self.link_input)
        self.layout.add_widget(link_input_layout)

        # Fetch Button with increased size and light blue color for better visibility
        self.fetch_button = Button(text="Fetch Attendance", size_hint_y=None, height=60, background_color=(0.5, 0.8, 1, 1))
        self.fetch_button.bind(on_press=self.fetch_data)
        self.layout.add_widget(self.fetch_button)

        # Result Label with white text color for readability
        self.result_label = Label(text="", text_size=(Window.width, None), halign='center', color=(1, 1, 1, 1))
        self.layout.add_widget(self.result_label)

        return self.layout

    def fetch_data(self, instance):
        sheet_url = self.link_input.text
        
        try:
            data = fetch_sheet_data(sheet_url)
            summary = summarize_attendance(data)
            summary_text = "\n".join([f"{key}: {value} days present" for key, value in summary.items()])
            print(summary_text)
            self.result_label.text = summary_text
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"


if __name__ == "__main__":
    AttendanceApp().run()