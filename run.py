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
    "https://www.googleapis.com/auth/drive",
]
CREDS = Credentials.from_service_account_file("budget_me_creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("budget_me")


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
        update_worksheet(category_data, "Category")
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
        update_worksheet(data, "Expences")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


def read_worksheet(worksheet):
    """
    Read data from the given worksheet
    """
    return SHEET.worksheet(worksheet).get_all_values()


def read_category_data():
    """
    Read category data from the worksheet
    """
    print("reading category data\n")
    read_data = read_worksheet("Category")
    category_names = []
    for data in read_data:
        category_names.append(data[0])

    return category_names


def read_expence_data():
    """
    Read expence data from the worksheet
    """
    print("reading expence data\n")
    read_data_expence = read_worksheet("Expences")
    return read_data_expence


def get_monthy_summery(expence_list):
    expence_summery = {}
    today = datetime.today()
    for line_expence in expence_list:
        try:
            if not line_expence[3] == "date":
                expense_date = datetime.strptime(line_expence[3], "%d/%m/%Y")
                if (
                    expense_date.year == today.year
                    and expense_date.month == today.month
                ):
                    dict_value = expence_summery.get(line_expence[0])
                    if dict_value is not None:
                        amount = int(line_expence[1])
                        expence_summery[line_expence[0]] = dict_value + amount
                    else:
                        expence_summery[line_expence[0]] = int(line_expence[1])

        except ValueError as e:
            print(f"Could not parse data, {e}")

    total_this_month = sum(expence_summery.values())
    expence_summery["Total"] = total_this_month

    days_this_month = calendar.monthrange(today.year, today.month)[1]
    expence_summery["Avg. Per Day"] = total_this_month / days_this_month

    return expence_summery


def main():
    print("======================================")
    print("Welcome to BUDGET ME!!")
    print("What would you like to do?")
    print("1. List category")
    print("2. List expences")
    print("3. Add category")
    print("4. Add expence")
    print("5. Get summary")
    input_option = input("Enter your option here: ")
    print("======================================")
    if input_option == "1":
        print("======================================")
        pprint(read_category_data())
        print("======================================")
    elif input_option == "2":
        print("======================================")
        pprint(read_expence_data())
        print("======================================")
    elif input_option == "3":
        print("======================================")
        name = input("Enter your category here:")
        category_list = read_category_data()
        option = len(category_list) + 1
        add_category(name, option, category_list)
        print("======================================")
    elif input_option == "4":
        print("======================================")
        expence_category = input("Enter your expence category:")
        date_object = datetime.now().strftime("%d/%m/%Y")
        expence_amount = input("Enter your amount:")
        expence_currency = input("Enter your currency:")
        category_list = read_category_data()

        add_expence(
            expence_category,
            expence_amount,
            expence_currency,
            date_object,
            category_list,
        )
        print("======================================")
    elif input_option == "5":
        print("======================================")
        print("Retrieving summary of expences\n")
        summary = get_monthy_summery(read_expence_data())
        for k, v in summary.items():
            print("{:<15} {:<15}".format(k, v))

        print("======================================")
    else:
      print("Please try again")

main()
