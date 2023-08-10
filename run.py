#   Your code goes here.
import category
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('budget_me_creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('budget_me')

category_data = SHEET.worksheet('Category').get_all_values()
categories = category.get_categories(category_data)
	
print(categories)

expences = SHEET.worksheet('Expences')

expense_data = expences.get_all_values()

def expences(expense_data):
  expences = []
  for select_expence in expense_data:
    print(select_expence)

expences(expense_data)


	











# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
