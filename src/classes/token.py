from pdfminer.high_level import extract_text
from abc import ABC

class Token(ABC):
	'''
	Abstract Class Token

	Args:
	  name: Token data
	  type: Type of the token
	'''
	def __init__(
		self,
		name: str,
		type: str
	) -> None:
		self.name = name
		self.type = type

	def display(self):
		print(f'[ Type: "{self.type}", Name: "{self.name}" ]')


class CategoryToken(Token):
	'''
	Token for item Categories

	Args:
	  name: Category name
	'''
	def __init__(
		self,
		name: str,
	) -> None:
		super().__init__(name, 'CATEGORY_TOKEN')

class ItemToken(Token):
	def __init__(
		self,
		name: str,
		type: str = 'ITEM_TOKEN',
		cost = 0,
		discount = 0
	) -> None:
		'''
		Token for Items

		Args:
		name: Item name
		cost: Cost of the item
		discount: discount of the itme as negative number
		'''
		super().__init__(name, type)
		self.cost = cost
		self.discount = discount

	def display(self):
		print(f'[ Type: "{self.type}", Name: "{self.name}", Cost: "{self.cost}", Discount: "{self.discount}" ]')