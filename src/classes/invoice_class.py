from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader
import pandas as pd
from classes.token import Token, CategoryToken, ItemToken

class Invoice:
	'''
	Initializes Invoice object.

	Args:
	  invoice_path: Path to the invoice
	'''
	categories = [
		"mercearia + pet food", "talho", "frutas e vegetais",
		"padaria/pastelaria", "descontos extra",
		"congelados", "produtos lacteos", "queijos",
		"deterg. e prod. limpeza", "produtos pessoais",
		"charcutaria", "ovos", "bazar", "bebidas"
	]

	def __init__(
		self,
		invoice_path: str,
	) -> None:
		self.issue_date = PdfReader(invoice_path).metadata.creation_date
		self.text = extract_text(invoice_path)
		self.header = self.__get_header__()
		self.expenses = self.__get_expenses__()
		self.total = self.__get_total__()

	def parse(self) -> None:
		'''
		Parses the expenses attribute and returns a dataframe with four columns:
		Category, Item, Cost, and Discount
		'''
		tokens = self.__tokenize__()
		dataframe = self.__build_dataframe__(tokens)
		return dataframe

	def __parse_item__(self, line: str) -> (str, float):
		start = line.find('%') + 1

		# Try to convert last item to float to check if it's a cost
		try:
			cost = None
			for i in range(len(line) - 1, 0, -1):
				if line[i] == ' ':
					cost = float(line[i + 1:].replace(',', '.'))
					break
			end = line.find("  ", start)
			return (line[start:end].strip(), cost)
		except:
			return (line[start:].strip(), None)

	def __tokenize__(self) -> list[Token]:
		tokens = []

		# Split expenses into lines and 
		lines = self.expenses.split("\n")
		lines.append("")

		current_token = None
		for i in range(len(lines)):
			lines[i] = lines[i].strip()
			if i == len(lines) - 1 and current_token != None:
				tokens.append(current_token)
				break

			if lines[i].lower() in self.categories:

				if current_token != None:
					tokens.append(current_token)
				if lines[i].lower() == "descontos extra":
					current_token = ItemToken("DESCONTOS EXTRA")
					current_token.cost = 0
					i+=1
					for j in range(len(lines[i]) - 1, 0, -1):
						if lines[i][j] == '(':
							discount = float(lines[i][j + 1:-1].replace(',', '.'))
							break
						current_token.discount = -discount
					tokens.append(current_token)
					
				else:
					tokens.append(CategoryToken(lines[i]))
					current_token = None
				
			else:
				# End condition for a Token
				if lines[i][0].isalpha() and lines[i][len(lines[i]) - 1] != ')':
					if current_token != None:
						tokens.append(current_token)
					current_token = ItemToken(None)
					current_token.name, current_token.cost = self.__parse_item__(lines[i])
				else:
					if (lines[i][0].isdigit()):
						cost = 0
						for j in range(len(lines[i]) - 1, 0, -1):
							if lines[i][j] == ' ':
								cost = float(lines[i][j + 1:].replace(',', '.'))
								break
						current_token.cost = cost
					else:
						discount = 0
						for j in range(len(lines[i]) - 1, 0, -1):
							if lines[i][j] == '(':
								discount = float(lines[i][j + 1:-1].replace(',', '.'))
								break
						current_token.discount = -discount
		return tokens


	def __build_dataframe__(self, tokens: list) -> pd.DataFrame:
		data = {'Category': [], 'Item': [], 'Cost': [], 'Discount': []}
		current_category = ""
		for token in tokens:
			if token.type == 'CATEGORY_TOKEN':
				current_category = token.name
				continue
			data['Category'].append(current_category)
			data['Item'].append(token.name)
			data['Cost'].append(token.cost)
			data['Discount'].append(token.discount)
		
		return pd.DataFrame(data)


	def __get_header__(self) -> str:
		end = self.text.find('Artigos')
		return self.text[: end].strip()

	def __get_expenses__(self) -> str:
		start = self.text.find('Artigos') + len('Artigos')
		end = self.text.find('Resumo')
		return self.text[start : end].strip()
	
	def __get_total__(self) -> str:
		start = self.text.find('Resumo') + len('Resumo')
		end = self.text.find('Pagamentos')
		return self.text[start : end].strip()
