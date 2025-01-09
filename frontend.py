from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import sys
sys.path.append('C:/Users/HP/OneDrive/Desktop/Attendance/backend.py') 
from backend import fetch_sheet_data, summarize_attendance

class AttendanceApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.link_input = TextInput(hint_text="Enter Google Sheet Link", multiline=False)
        self.layout.add_widget(self.link_input)
        
        self.fetch_button = Button(text="Fetch Attendance")
        self.fetch_button.bind(on_press=self.fetch_data)
        self.layout.add_widget(self.fetch_button)
        
        self.result_label = Label(text="")
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
