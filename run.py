#   Your code goes here.
import category
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('budget_me_creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('budget_me')


def update_worksheet(data, worksheet):
  """
  Receives a list of integers to be inserted into a worksheet
  Update the relevant worksheet with the data provided
  """
  print(f"Updating {worksheet} worksheet...\n")
  worksheet_to_update = SHEET.worksheet(worksheet)
  worksheet_to_update.append_row(data)
  print(f"{worksheet} worksheet updated successfully.\n")


def read_worksheet(worksheet):
  """
  Read data from the given worksheet
  """
  return SHEET.worksheet(worksheet).get_all_values()


def validate_data(values):

  """
  Inside the try,converts all string values into integers.
  Raises valueError if strings cannot be converted into int,
  or if there aren't exactly 6 vlaues.
  """
  
  try: 
    [int(value) for value in values]
    if len(values) != 6:
      raise ValueError(f"Exactly 6 vlaues required, you provided{len(values)}")
  except ValueError as e :
      print(f"Invalid data: {e}, please try again.\n") 
      return False
  return True


def read_category_data():
  """
  Read category data from the worksheet
  """
  print('reading category data')
  read_data = read_worksheet('Category')
  pprint(read_data)


def read_expence_data():
  """
  Read expence data from the worksheet
  """
  print('reading expence data')
  read_data_expence = read_worksheet('Expences')
  pprint( read_data_expence)

	









def get_sales_data():
  """
  Get sales figures input from the user
  """
  while True:
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60")

    data_str = input("Enter your data here: ")

    sales_data = data_str.split(",")

    if validate_data(sales_data):
      print("Data is valid!")
      break
    
  return sales_data
read_category_data()
read_expence_data()








# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
