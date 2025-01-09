import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict
import pandas as pd
import re

def fetch_sheet_data(sheet_url):
    # Authenticate using the Service Account JSON file
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("Credentials.json", scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet by URL
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)  # Assuming the first sheet
    data = worksheet.get_all_records()
    data = pd.DataFrame(data)
    data=get_roll_name(data)
    print(data.iloc[0:10,-2:])
    return data

def summarize_attendance(data):
    summary = {}
    for row in data:
        for key, value in row.items():
            # Clean the key to remove leading/trailing spaces and tabs
            cleaned_key = key.strip()
            
            # Check if the cleaned key starts with "IM-"
            if cleaned_key.startswith("IM-"):
                summary[cleaned_key] += 1 if value.strip().lower() == "present" else 0
    
    return summary


# def summarize_attendance(data):
#     summary = defaultdict(int)  # Dictionary to store attendance counts
    
#     for row in data:
#         for key, value in row.items():
#             # Clean the key to remove leading/trailing spaces and tabs
#             cleaned_key = key.strip()
            
#             # Check if the cleaned key starts with "IM-"
#             if cleaned_key.startswith("IM-"):
#                 summary[cleaned_key] += 1 if value.strip().lower() == "present" else 0
    
#     return summary


def get_roll_name(data):
    col_dict={}
    columns=data.columns
    for col in columns:
        pattern = r'\[(IM-2K[A-Za-z0-9-]+)\s*(.*)\]'
        match = re.search(pattern, col)
        if match:
            roll_number = match.group(1)  # Extract roll number
            name = match.group(2)  # Extract name
            new_col=roll_number + " "+ name
            col_dict[col]=new_col
    data=data.rename(columns=col_dict)
    data["Timestamp"]=pd.to_datetime(data["Timestamp"])
    data["Date"]=data["Timestamp"].dt.date
    data["Time"]=data["Timestamp"].dt.time
    return data
