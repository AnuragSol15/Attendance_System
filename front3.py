from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from backend import fetch_sheet_data, summarize_attendance
import pandas as pd


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(name=kwargs["name"])
        
        # Gradient background
        with self.canvas.before:
            self.bg_color = Color(0.05, 0.1, 0.15, 1)  # Dark blue gradient
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Scrollable Layout
        root_layout = ScrollView(size_hint=(1, 1))
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))  # Adjust height dynamically
        
        # Logos and Heading
        logo_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)
        
        # Left Logo
        logo_left = Image(source="Davv_LOGO_removed_bg.png", size_hint=(None, None), size=(80, 80), allow_stretch=True)
        logo_layout.add_widget(logo_left)
        
        # Heading
        heading_label = Label(
            text="International Institute of Professional Studies, DAVV, Indore (M.P.)",
            font_size=24,
            bold=True,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        heading_label.bind(size=heading_label.setter('text_size'))  # Ensure text wraps properly
        logo_layout.add_widget(heading_label)
        
        # Right Logo
        logo_right = Image(source="iipslogo.jpg", size_hint=(None, None), size=(80, 80), allow_stretch=True)
        logo_layout.add_widget(logo_right)
        
        self.layout.add_widget(logo_layout)

        # Adding uploaded image as a banner
        banner_image = Image(source="https://cdn2.iconfinder.com/data/icons/education-59/128/check_up-512.png", size_hint=(1, None), height=150, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(banner_image)

        # Course Selection in a Card
        course_card = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.9, None), height=150, pos_hint={'center_x': 0.5})
        with course_card.canvas.before:
            self.card_color = Color(0.15, 0.15, 0.2, 1)  # Card background color
            self.card_rect = RoundedRectangle(size=course_card.size, pos=course_card.pos, radius=[10])
        course_card.bind(size=self._update_card, pos=self._update_card)

        course_selection_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.course_label = Label(text="Select Course:", color=(1, 1, 1, 1))
        self.course_dropdown = DropDown()
        for course in ["B.Com.(Hons.)(3Y)", "MCA(5Y)", "MTech(IT)(5Y)", "MBA(MS)(5Y)", "MBA(TA)(5Y)", "MBA(MS)(2Y)", "MBA(TA)(2Y)", "MBA(APR)(2Y)", "MBA(Eship)(2Y)"]:
            btn = Button(text=course, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.course_dropdown.select(btn.text))
            self.course_dropdown.add_widget(btn)
        self.course_input = Button(text="Select a Course", size_hint=(1, None), height=40, background_color=(0.2, 0.6, 0.8, 1))
        self.course_input.bind(on_release=self.course_dropdown.open)
        self.course_dropdown.bind(on_select=lambda instance, x: setattr(self.course_input, 'text', x))
        course_selection_layout.add_widget(self.course_label)
        course_selection_layout.add_widget(self.course_input)
        course_card.add_widget(course_selection_layout)
        self.layout.add_widget(course_card)

        # Link Input in a Card
        link_card = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.9, None), height=100, pos_hint={'center_x': 0.5})
        with link_card.canvas.before:
            self.link_card_color = Color(0.15, 0.15, 0.2, 1)  # Card background color
            self.link_card_rect = RoundedRectangle(size=link_card.size, pos=link_card.pos, radius=[10])
        link_card.bind(size=self._update_card, pos=self._update_card)

        link_input_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.link_label = Label(text="Enter Google Sheet Link:", color=(1, 1, 1, 1))
        self.link_input = TextInput(hint_text="Paste sheet link here", multiline=False)
        link_input_layout.add_widget(self.link_label)
        link_input_layout.add_widget(self.link_input)
        link_card.add_widget(link_input_layout)
        self.layout.add_widget(link_card)

        # Fetch Button
        self.fetch_button = Button(
            text="Fetch Attendance",
            size_hint=(None, None),
            size=(150, 50),
            background_color=(0.2, 0.6, 0.8, 1),
            border=(20, 20, 20, 20),
            pos_hint={'center_x': 0.5}
        )
        self.fetch_button.bind(on_press=kwargs["attend"].fetch_data)
        self.layout.add_widget(self.fetch_button)

        # Add the layout to the ScrollView
        root_layout.add_widget(self.layout)
        self.add_widget(root_layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _update_card(self, instance, value):
        self.card_rect.size = instance.size
        self.card_rect.pos = instance.pos


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.main_layout = GridLayout(cols=1)
        self.add_widget(self.main_layout)

    def update_result(self, df):
        table_layout = GridLayout(cols=len(df.columns), size_hint_y=None)
        table_layout.bind(minimum_height=table_layout.setter('height'))

        for col in df.columns:
            table_layout.add_widget(Label(text=str(col), bold=True, size_hint_y=None, height=40))
            

        for _, row in df.iterrows():
            for value in row:
                table_layout.add_widget(Label(text=str(value), size_hint_y=None, height=30))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(table_layout)

        self.main_layout.clear_widgets()
        self.main_layout.add_widget(scroll_view)


class AttendanceApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.1, 0.15, 1)  # Dark modern background

        self.screen_manager = ScreenManager()
        self.welcome_screen = WelcomeScreen(name='welcome', attend=self)
        self.result_screen = ResultScreen(name='result')
        self.screen_manager.add_widget(self.welcome_screen)
        self.screen_manager.add_widget(self.result_screen)

        return self.screen_manager

    def fetch_data(self, instance):
        sheet_url = self.welcome_screen.link_input.text
        course = self.welcome_screen.course_input.text

        try:
            data = fetch_sheet_data(sheet_url, course)
            summary = summarize_attendance(data, "IM-2K24-70 NAYRA VIJAYVARGIYA")
            self.result_screen.update_result(summary)
            self.screen_manager.current = 'result'

        except Exception as e:
            self.result_screen.update_result(f"Error: {str(e)}")
            self.screen_manager.current = 'result'


if __name__ == "__main__":
    AttendanceApp().run()
