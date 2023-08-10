class Expence:
  def __init__(self,category,amount,currency,date):
    self.category = category
    self.amount = amount
    self.currency = currency
    self.date = date

  def description(self):
    return f'{self.category} {self.amount} {self.currency} {self.date}'

def expense_data(data):
  categories = {}
  for select_category in data: