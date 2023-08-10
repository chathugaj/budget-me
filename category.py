class Category:
	"""
	Creates an instance of Category
	"""
	def __init__(self, name, option):
		self.name = name
		self.option = option

	def description(self):
		return f'{self.option} {self.name}'

def get_categories(data):
	categories = {}
	print(data)
	for select_category in data:
		categories[select_category[1]] = Category(select_category[0], select_category[1])
		# print(select_category)

	return categories
