import sys
import csv
import ply.lex as lex
import re
import ply.yacc as yacc
import json


###################### Global variables ######################

# Global variable for the name of the csv file 
fileCSV = ""
# Global variable for the name of the csv file 
fileJSON = ""

# The header formated with our syntax
formatHeader = []

# The header we must follow
header = []


###############################################################


###################### Global Structures ######################

# Global struture for COLUMNID 
class ColumnID:

	# Function to initialize an object of this class
	def __init__(self, id):
		self.name = id
		self.parameter = ""

	# Function to print the fields of the objet of this class
	def print(self):
		print("Id: ", self.name)
		print("Parameter: ", self.parameter)


# Global struture for DEFINEDLIST
class DefinedList:

	# Function to initialize an object of this class
	def __init__(self, id, value):
		self.name = id
		self.size = value
		self.list = []

	# Function to print the fields of the objet of this class
	def print(self):
		print("Id: ", self.name)
		print("Size: ", self.size)
		print("List: ", self.list)


# Global struture for BETWEENLIST
class BetweenList:

	# Function to initialize an object of this class
	def __init__(self, id, min, max):
		self.name = id
		self.min = min
		self.max = max
		self.list = []

	# Function to print the fields of the objet of this class
	def print(self):
		print("Id: ", self.name)
		print("Min: ", self.min)
		print("Max: ", self.max)
		print("List: ", self.list)



# Global struture for FUNCTIONAGREGLIST
class FunctionAgregList:

	# Function to initialize an object of this class
	def __init__(self, id, min, max, function):
		self.name = id
		self.min = min
		self.max = max
		self.function = function
		self.list = []

	# Function to print the fields of the objet of this class
	def print(self):
		print("Id: ", self.name)
		print("Min: ", self.min)
		print("Max: ", self.max)
		print("Function: ", self.function)
		print("List: ", self.list)


##############################################################


# Function to build the format header
def buildHeader():
	global header
	with open(fileCSV, "r") as f:
		maxLine = 0
		reader = csv.reader(f)
		for row in reader:
			if maxLine == 1:
				break
			header = row
			maxLine += 1
	f.close()



# Function that evaluates if input is correct
def secure():
	if len(sys.argv) == 1:
		sys.exit("No file name found when running the application!")

	fileName = str(sys.argv[1])
	extension = fileName.split(".")

	if extension[1] != "csv":
		sys.exit("The file is not a csv file!")

	global fileCSV
	fileCSV = fileName


secure()
buildHeader()


###################### Defining the tokens ######################

# List of tokens for the syntax
tokens = [ 'ID', 'LCBRACKET', 'RCBRACKET', 'RANGE', 'COMMA', 'OP' ]

# Regex for the tokens
t_OP = r'\:\:'
t_COMMA = r'\,'

def t_RANGE(t):
	r'\d+'
	t.value = int(t.value)

	return t

t_LCBRACKET = r'\{'
t_RCBRACKET = r'\}'
t_ID = r'[a-zA-Z\u00C0-\u017F\/_]+'
# t_ID = r'[a-zA-Z\/_]+'
t_ignore = r' +'

# Throw error if unkown token
def t_error(t):
	print("Error: Unknown token: ", t)
	sys.exit("")



#################################################################

##################### Example of the Syntax #####################

# ID
# ID LCBRACKET RANGE RCBRACKET
# ID LCBRACKET RANGE COMMA RANGE RCBRACKET
# ID LCBRACKET RANGE RCBRACKET OP ID
# ID LCBRACKET RANGE COMMA RANGE RCBRACKET OP ID

#################################################################


##################### Syntax Rules ##############################

# Function that defines what could be our languange
def p_language(p):
	'''
	language : expression
			 | interval
			 | size
			 | function
			 | empty
	'''
	run(p[1])


# Function that defines what word is a interval
def p_interval(p):
	'''
	interval : LCBRACKET RANGE COMMA RANGE RCBRACKET
	'''
	p[0] = (p[2], p[4])


# Function that defines what word is a size
def p_size(p):
	'''
	size : LCBRACKET RANGE RCBRACKET
	'''
	p[0] = (p[2])

# Function that defines what word is a function
def p_function(p):
	'''
	function : OP expression
	'''
	p[0] = (p[2])


# Function that defines what phrase is a defined list
def p_expression_definedList(p):
	'''
	expression : expression size
	'''
	p[0] = (p[1], p[2])


# Function that defines what phrase is a between list
def p_expression_betweenList(p):
	'''
	expression : expression interval
	'''
	p[0] = (p[1], p[2])


# Function that defines what phrase is a function agregation list
def p_expression_functionAgregList(p):
	'''
	expression : expression interval function
	'''
	p[0] = (p[1], p[2], p[3])


# Function that defines what phrase is an id
def p_expression_id(p):
	'''
	expression : ID
	'''
	p[0] = p[1]


# Function that defines what word is empty
def p_empty(p):
	'''
	empty : 
	'''
	p[0] = None

# Function that defines what phrase is a syntax error
def p_error(p):
	print("Syntax error found! Syntax: ", p)


#################################################################


################## Converting from CSV to JSON ##################

parser = yacc.yacc()



# Function that builds the format header by following the syntax rules made
def run(p):
	global formatHeader
	if type(p) == tuple:
		if len(p) == 2 and type(p[1]) == tuple:
			interval = p[1]
			betweenList = BetweenList(p[0], interval[0], interval[1])
			formatHeader.append(betweenList)


		elif len(p) == 2:
			definedList = DefinedList(p[0], p[1])
			formatHeader.append(definedList)

		else:
			interval = p[1]
			functionAgregList = FunctionAgregList(p[0], interval[0], interval[1], p[2])
			formatHeader.append(functionAgregList)


	elif type(p) == str:
		column = ColumnID(p)
		formatHeader.append(column)



lexer = lex.lex()
while True:

	for element in header:
		parser.parse(element)

	break


#Function that builds a list with all the lines from the CSV file, organizing by dictionary per global struture
def buildJSON(list, allLines):

	dictionary = {} 
	for structure in list:
		if type(structure) == ColumnID:
			dictionary.update({structure.name : structure.parameter})

		elif type(structure) == DefinedList:
			dictionary.update({structure.name : structure.list})

		elif type(structure) == BetweenList:
			dictionary.update({structure.name : structure.list})

		else:
			name = structure.name + "_" + structure.function
			# print("FUNCTION NAME: ", name)
			dictionary.update({name : structure.list})

	allLines.append(dictionary)



# TAREFAS: QUANDO COMPARAR CENAS USAR REGEX
# MELHORAR CONDIÇÕES DE ERRO




# Function that converts the CSV file to the JSON file
def csv2json():

	filename = fileCSV.split('.', 1)
	
	global fileJSON
	fileJSON = filename[0] + ".json"

	
	allLines = []

	with open(fileCSV, "r") as f:
		
		maxLine = 0
		reader = csv.reader(f)
		for row in reader:
			list2JSON = []
			if maxLine == 0:
				maxLine += 1

			else:
				# print("Linha: ", row)
				index = 0
				for struct in formatHeader:

					if type(struct) == ColumnID:
						obj = ColumnID(struct.name)
						obj.parameter = row[index]
						list2JSON.append(obj)
						# obj.print()
						index += 1

					elif type(struct) == DefinedList:

						obj = DefinedList(struct.name, struct.size)

						for value in range(0, struct.size):
							if row[index] != "":
								obj.list.append(row[index])
							index += 1
						list2JSON.append(obj)
						# obj.print()

					elif type(struct) == BetweenList:

						obj = BetweenList(struct.name, struct.min, struct.max)

						for value in range(0, struct.max):
							if row[index] != "":
								obj.list.append(row[index])
							index += 1
						list2JSON.append(obj)
						# obj.print()
					elif type(struct) == FunctionAgregList:

						obj = FunctionAgregList(struct.name, struct.min, struct.max, struct.function)

						for value in range(0, struct.max):
							if row[index] != "":
								obj.list.append(row[index])
							index += 1
						list2JSON.append(obj)
						# obj.print()
			
				buildJSON(list2JSON, allLines)

		with open(fileJSON, "w") as f:
			formatList = json.dumps(allLines, indent = 4)
			f.write(formatList)


csv2json()


#################################################################