#   Your code goes here.
import category
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from datetime import datetime
import calendar

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


def add_category(name, option, category_list):
  """
  validate the data and add in the category worksheet
  """
  try:
    if name is None or category_list.count(name) > 0:
      raise ValueError("Duplicate category")
    category_data = [name, option]
    update_worksheet(category_data,'Category')  
  except ValueError as e:
    print(f"Invalid data: {e}, please try again.\n")     


def add_expence(category, amount, currency, date, category_list):
  """
  Validate the data and add in the expences worksheet
  """
  
  try:
    if category is None or category_list.count(category) == 0:
      raise ValueError("Please provide a valid category")
    elif not amount.isnumeric():
      raise ValueError(f"Please provide a valid amount")
    elif len(currency) > 3:
      raise ValueError(f"Please provide a valid three letter currency")
    
    data = [category, amount, currency, date]
    update_worksheet(data,'Expences')
  except ValueError as e:
    print(f"Invalid data: {e}, please try again.\n") 

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
  print('reading category data\n')
  read_data = read_worksheet('Category')
  category_names = []
  for data in read_data:
    category_names.append(data[0])
      
  return category_names


def read_expence_data():
  """
  Read expence data from the worksheet
  """
  print('reading expence data\n')
  read_data_expence = read_worksheet('Expences')
  return read_data_expence

def get_monthy_summery(expence_list):
  expence_summery = {}
  today = datetime.today()
  for line_expence in expence_list:
    try:
      if not line_expence[3] == "date":
        expense_date = datetime.strptime(line_expence[3], '%d/%m/%Y')
        if expense_date.year == today.year and expense_date.month == today.month:
          dictionary_value = expence_summery.get(line_expence[0])
          if (dictionary_value is not None):
            expence_summery[line_expence[0]] = dictionary_value + int(line_expence[1])
          else:
            expence_summery[line_expence[0]] = int(line_expence[1])

    except ValueError as e:
      print(f"Could not parse data, {e}")

  expence_summery['Total'] = sum(expence_summery.values())

  days_this_month = calendar.monthrange(today.year, today.month) [1]
  expence_summery['Avg. Per Day'] = sum(expence_summery.values()) / days_this_month

  return expence_summery


def main():
  print('What would you like to do?')
  print("1 List category")
  print("2 List expences")
  print("3 Add category")
  print("4 Add expence")
  print("5 Get summary")
  input_option = input("Enter your option here: ")
  if input_option == '1':
    read_category_data()
    pprint(read_category_data())
  if input_option == '2':
    read_expence_data()
    pprint(read_expence_data())
  if input_option == '3':
    add_category = input("Enter your category here:")
    category_list = read_category_data()
    category_option = len(category_list) + 1
    add_category(name,option,category_list)
  if input_option == '4':
    expence_category = input("Enter your expence category:")
    #expence_date = input("Enter your date:")
    date_object = datetime.now().strftime("%d/%m/%Y")
    expence_amount = input("Enter your amount:")
    expence_currency = input("Enter your currency:")
    category_list = read_category_data()

    add_expence(expence_category, expence_amount, expence_currency, date_object, category_list)
  if input_option == '5':
    print("Retrieving summary of expences\n")
    summary = get_monthy_summery(read_expence_data())
    for k, v in summary.items():
        print("{:<15} {:<15}".format(k, v))

  
main()

# add_expence('Health', '123', 'sekddd', datetime.now().strftime("%d/%m/%Y"), ['name', 'Groceries', 'Transport', 'Health', 'Housing', 'Health'])
# add_category('Education', 8, ['name', 'Groceries', 'Transport', 'Health', 'Housing', 'Health'])
#pprint(get_monthy_summery(read_expence_data()))










# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
