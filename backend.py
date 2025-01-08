import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

def fetch_sheet_data(sheet_url):
    # Authenticate using the Service Account JSON file
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("Credentials.json", scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet by URL
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)  # Assuming the first sheet
    data = worksheet.get_all_records()
    return data



def summarize_attendance(data):
    summary = defaultdict(int)  # Dictionary to store attendance counts
    for row in data:
        for key, value in row.items():
            if key.startswith("IM-"):  # Check for student columns
                summary[key] += 1 if value.strip().lower() == "present" else 0
    return summary
