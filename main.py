import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("Credentials.json", scopes= scopes)
client = gspread.authorize(creds)

sheet_id = "1KFjU2WfAwAVTH3C9ZNWd3aZYGkm_nuWc-hePuB1lduY"
sheet = client.open_by_key(sheet_id)

values_list = sheet.sheet1.row_values(1)
print(values_list)