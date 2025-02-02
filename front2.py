from kivy.app import App
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from backendkashi import fetch_sheet_data, get_for_particular_student, get_subjectwise, get_overall_attendance
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import pandas as pd
from kivy.uix.anchorlayout import AnchorLayout

# Set global background color
Window.clearcolor = (0.678, 0.847, 0.902, 1)  # Light blue

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(name=kwargs["name"])
        
        self.app = kwargs["attend"]  # Get app instance
        
        # Background Color (Ensuring it applies correctly)
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Light Blue
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Main Layout
        self.layout = FloatLayout()

        # Logos and Heading
        logo_layout = BoxLayout(orientation='horizontal', size_hint=(0.9, 0.15), pos_hint={'center_x': 0.5, 'top': 1})
        
        logo_left = Image(source="Davv_LOGO_removed_bg.png", size_hint=(None, None), size=(80, 80))
        logo_right = Image(source="iipslogo.jpg", size_hint=(None, None), size=(80, 80))
        
        heading_label = Label(
            text="International Institute of Professional Studies\nDAVV, Indore (M.P.)",
            font_size=30,
            bold=True,
            color=(0, 0, 0.545, 1),
            halign='center',
            valign='middle'
        )
        heading_label.bind(size=heading_label.setter('text_size'))

        logo_layout.add_widget(logo_left)
        logo_layout.add_widget(heading_label)
        logo_layout.add_widget(logo_right)
        
        self.layout.add_widget(logo_layout)

        # Course Selection
        course_selection_layout = BoxLayout(orientation='horizontal', size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.course_label = Label(text="Select Course:", color=self.get_text_color(), size_hint=(0.4, 1))
        
        self.course_dropdown = DropDown()
        for course in ["B.Com.(Hons.)(3Y)", "MCA(5Y)", "MTech(IT)(5Y)", "MBA(MS)(5Y)", "MBA(TA)(5Y)"]:
            btn = Button(text=course, size_hint_y=None, height=40, background_color=(0, 0, 0.545, 1))
            btn.bind(on_release=lambda btn: self.course_dropdown.select(btn.text))
            self.course_dropdown.add_widget(btn)

        self.course_input = Button(text="Select a Course", size_hint=(0.6, 1), background_color=self.get_button_color())
        self.course_input.bind(on_release=self.course_dropdown.open)
        self.course_dropdown.bind(on_select=lambda instance, x: setattr(self.course_input, 'text', x))
        
        course_selection_layout.add_widget(self.course_label)
        course_selection_layout.add_widget(self.course_input)
        
        self.layout.add_widget(course_selection_layout)

        # Link Input
        link_input_layout = BoxLayout(orientation='horizontal', size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.link_label = Label(text="Google Sheet Link:", color=self.get_text_color(), size_hint=(0.4, 1))
        self.link_input = TextInput(hint_text="Paste sheet link here", size_hint=(0.6, 1))
        
        link_input_layout.add_widget(self.link_label)
        link_input_layout.add_widget(self.link_input)
        
        self.layout.add_widget(link_input_layout)

        # Fetch Button
        self.fetch_button = Button(
            text="Fetch Attendance", 
            size_hint=(0.4, 0.1), 
            background_color=self.get_button_color(), 
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        self.fetch_button.bind(on_press=self.app.get_selection)
        self.layout.add_widget(self.fetch_button)

        # Error Message
        self.error_label = Label(text="", color=(1, 0, 0, 1), size_hint=(0.9, 0.05), pos_hint={'center_x': 0.5, 'center_y': 0.35})
        self.layout.add_widget(self.error_label)

        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def get_text_color(self):
        return (0, 0, 0, 1)

    def get_button_color(self):
        """Returns light blue for light theme, dark blue for dark theme"""
        return (0.5, 0.8, 1, 1) if self.app.theme_cls.theme_style == "Light" else (0.2, 0.5, 0.9, 1)

class SelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectionScreen, self).__init__(**kwargs)

        # Set background color
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Light Blue (Same as WelcomeScreen)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.data = None
        
        self.label = Label(text="Choose an option to view attendance", font_size=24, bold=True, color=(0, 0, 0.545, 1))
        self.layout.add_widget(self.label)

        # Buttons
        self.subject_button = Button(text="See Overall Attendance", size_hint_y=None, height=50, background_color=(0, 0, 0.545, 1))
        self.subject_button.bind(on_press=self.show_overall)
        self.layout.add_widget(self.subject_button)
        
        self.student_button = Button(text="Get Attendance by Student", size_hint_y=None, height=50, background_color=(0, 0, 0.545, 1))
        self.student_button.bind(on_press=self.show_student_list)
        self.layout.add_widget(self.student_button)

        self.subject_button = Button(text="Get Attendance by Subject", size_hint_y=None, height=50, background_color=(0, 0, 0.545, 1))
        self.subject_button.bind(on_press=self.show_subject_list)
        self.layout.add_widget(self.subject_button)
        
        self.list_view = ScrollView(size_hint=(1, None), size=(Window.width, 200))
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.list_view.add_widget(self.list_layout)
        self.layout.add_widget(self.list_view)

        # Submit Button
        self.submit_button = Button(text="Submit", size_hint_y=None, height=50, background_color=(0, 0, 0.545, 1))
        self.submit_button.bind(on_press=self.submit_selection)
        self.layout.add_widget(self.submit_button)

        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def show_student_list(self, instance):
        self.list_layout.clear_widgets()
        student_list = self.data.columns[3:-2] # Replace with actual data
        self.list_type="student"
        for student in student_list:
            btn = Button(text=student, size_hint_y=None, height=40)
            btn.bind(on_release=self.select_item)
            self.list_layout.add_widget(btn)
            
    def show_overall(self, instance):
        try:
            data=get_overall_attendance(self.data)
            result_screen = self.manager.get_screen('result')
            result_screen.update_result(data)
            self.manager.current = 'result'
        except AttributeError:
            data="No data available"

    def show_subject_list(self, instance):
        self.list_layout.clear_widgets()
        subject_list = self.data["Select Subject"].cat.categories  # Replace with actual data
        self.list_type="subject"
        for subject in subject_list:
            btn = Button(text=subject, size_hint_y=None, height=40)
            btn.bind(on_release=self.select_item)
            self.list_layout.add_widget(btn)

    def select_item(self, instance):
        self.selected_item = instance.text

    def submit_selection(self, instance):
        try:
            result_screen = self.manager.get_screen('result')
            self.data= get_for_particular_student(self.data,self.selected_item) if(self.list_type=="student") else get_subjectwise(self.data,self.selected_item)
            result_screen.update_result(self.data)
            self.manager.current = 'result'
        except AttributeError:
            self.manager.get_screen('result').update_result("No selection made!")
            self.manager.current = 'result'

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(name=kwargs["name"])

        # Set background color
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Light Blue (Same as WelcomeScreen)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.main_layout = FloatLayout()
        
        self.error_label = Label(text="", color=(0, 0, 0.545, 1))
        self.main_layout.add_widget(self.error_label)
        self.selection_screen = kwargs["attend"]
      
        self.add_widget(self.main_layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_result(self, df):
        if type(df)==str:
            self.error_label.text=df
        else:
            # Access the current Android activity
            table_layout = AnchorLayout(anchor_x="center", anchor_y="center")
            back_button_layout = AnchorLayout(anchor_x="left", anchor_y="top")
            back_button = MDIconButton(
                icon="arrow-left",  # Arrow icon
                size_hint=(None, None),
                size=(dp(30), dp(30)),  # Square button
                pos_hint={"center_y": 0.5},
                on_release=self.selection_screen.go_back,
            )
            back_button_layout.add_widget(back_button)

            # Add the back button layout to the main layout
            self.main_layout.add_widget(back_button_layout)
            rows=df.astype(str).values.tolist()
            column_data = []
            for col_name in df.columns:
                col_dtype = df[col_name].dtype
                width = dp(30)  # Default width
                if col_dtype == "object":  # Strings
                    width = dp(90)
                elif "int" in str(col_dtype) or "float" in str(col_dtype):  # Numbers
                    width = dp(20)
                elif col_dtype == "bool":  # Booleans
                    width = dp(15)
                column_data.append((col_name, width))
            table = CustomMDDataTable(
            size_hint=(0.9, 0.9),
            column_data=column_data,  # Dynamically generated columns
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color_header=(0.2, 0.4, 0.6, 1), 
            rows_num=20, 
            row_data=rows,        # Dynamically generated rows
            use_pagination=True,
            elevation=2,
            pagination_menu_pos="center",
            )
            table_layout.add_widget(table)
            self.main_layout.add_widget(table_layout)
            


class AttendanceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        
        self.screen_manager = ScreenManager()
        self.welcome_screen = WelcomeScreen(name='welcome', attend=self)
        self.result_screen = ResultScreen(name='result', attend=self)
        self.selection_screen = SelectionScreen(name="selection")
        
        self.screen_manager.add_widget(self.welcome_screen)
        self.screen_manager.add_widget(self.selection_screen)
        self.screen_manager.add_widget(self.result_screen)

        return self.screen_manager
    
    def get_selection(self,instance):
        sheet_url = self.welcome_screen.link_input.text
        course = self.welcome_screen.course_input.text 
        #check for empty url or empty course selection
        if not course or course == "...":
            self.welcome_screen.error_label.text = "Please select a course."
        elif not sheet_url:
            self.welcome_screen.error_label.text = "Please enter a Google Sheet URL."
        else:
            self.welcome_screen.error_label.text = ""  # Clear the error message
        try:
            data = fetch_sheet_data(sheet_url, course)
            print(data)
            self.selection_screen.data = data # Pass course to backend
            self.screen_manager.current = 'selection'

        except Exception as e:
            self.welcome_screen.error_label.text=f"Error: {str(e)}"

    def go_back(self,instance):
        self.screen_manager.current = 'selection'
        
class CustomMDDataTable(MDDataTable):
 def create_header(self, *args):
        super().create_header(*args)  # Call the original header creation method

        # Add custom black borders to header cells
        for column in self._columns:  # Access each column header
            with column.canvas.after:
                Color(0, 0, 0, 1)  # Set black color for the border
                Line(
                    rectangle=(*column.pos, *column.size),  # Rectangle dimensions
                    width=1.5,  # Border thickness
                )
    
if __name__ == "__main__":
    AttendanceApp().run()
