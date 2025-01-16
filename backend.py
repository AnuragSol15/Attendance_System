import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict
import pandas as pd
import re

def fetch_sheet_data(sheet_url):
    # Authenticate using the Service Account JSON file
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/yuvra/OneDrive/Desktop/KASHI/IIPS_attendance_app/Attendance_System/Credentials.json", scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet by URL
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)  # Assuming the first sheet
    data = worksheet.get_all_records()
    data = pd.DataFrame(data)
    data=get_roll_name_and_clean(data,"MBA(MS)")
    return data

def summarize_attendance(data,student_name):
    summary = {}
    grouped_data=data[data[student_name]=="Present"].groupby("Select Subject")[student_name].count()
    grouped_data=grouped_data.reset_index()
    grouped_data["Total"]=grouped_data["Select Subject"].map(data.groupby("Select Subject")[student_name].count())
    grouped_data["Percentage"]=(grouped_data[student_name]/grouped_data["Total"])*100
    print(grouped_data)
    return grouped_data

def get_subjectwise(data,subject):
    grouped_data=data.groupby("Select Subject")[data.iloc[:,3:-2].columns].agg(lambda x: (x == "Present").sum())
    grouped_data=grouped_data.loc[subject,:].to_frame()
    grouped_data=grouped_data.rename(columns={subject:"Classes_Attended"})
    Total_classes=data[data["Select Subject"]==subject].shape[0]
    grouped_data["Percentage_Classes_Attended"]=grouped_data["Classes_Attended"]/Total_classes*100
    print(Total_classes)
    return grouped_data

def filter_students_by_criteria(data,subject,criteria):
    data=get_subjectwise(data,subject)
    data=data[data["Percentage_Classes_Attended"]>=criteria]
    return data

def get_present(data,student_name,subject,date):
    date=pd.to_datetime(date)
    return data[(data["Select Subject"]==subject) & (data["Date"]=="2024-10-08")][student_name]

def get_roll_name_and_clean(data,course):
    Course={"MBA(MS)":"IM", "MCA":"IC", "MTECH":"IT"}
    col_dict={}
    columns=data.columns
    for col in columns:
        pattern = r'\[({}-2K[A-Za-z0-9-]+)\s*(.*)\]'.format(Course[course])
        match = re.search(pattern, col)
        if match:
            roll_number = match.group(1)  # Extract roll number
            name = match.group(2)  # Extract name
            new_col=roll_number +" "+ name
            col_dict[col]=new_col
    data=data.rename(columns=col_dict)
    data["Timestamp"]=pd.to_datetime(data["Timestamp"])
    data["Date"]=pd.to_datetime(data["Timestamp"].dt.date)
    data["Time"]=data["Timestamp"].dt.time
    data=data.drop(columns=["Timestamp","Remark"])
    return data

if __name__ == "__main__":
    data=fetch_sheet_data("https://docs.google.com/spreadsheets/d/1KFjU2WfAwAVTH3C9ZNWd3aZYGkm_nuWc-hePuB1lduY/edit?gid=1499235755#gid=1499235755")
    summarize_attendance(data,"IM-2K24-70 NAYRA VIJAYVARGIYA")
    print(filter_students_by_criteria(data,"IM-101 Principles and Practices of Management",72))