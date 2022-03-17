import sys
import ply.lex as lex
import re
import json
import statistics

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


###################### Defining the tokens ###################

# List of tokens for the syntax

tokens = [ 'ID', 'DEFINEDLIST', 'BETWEENLIST', 'FUNCTIONAGREGLIST', "COMMA"]


##############################################################


###################### Regular Expressions ###################

columnID = r'[a-zA-Z\u00C0-\u017F\/_]+'
size = r'\{(\d+)\}'
interval = r'\{(\d+)\,(\d+)\}'
function = r'\:\:(\w+)'

readCell = r'([^,\n\t]*)(,|\n|\t?)'

###################### Rules for Regex #######################


# Rule for token FUNCTIONAGREGLIST
def t_FUNCTIONAGREGLIST(t):

	r'[a-zA-Z\u00C0-\u017F\/_]+\{\d+\,\d+\}\:\:\w+'

	regex = fr'({columnID})({interval})({function})'
	regexExp = re.compile(regex)

	obj = FunctionAgregList(regexExp.search(t.value).group(1), int(regexExp.search(t.value).group(3)),
	 int(regexExp.search(t.value).group(4)), regexExp.search(t.value).group(6))

	global formatHeader
	formatHeader.append(obj)


# Rule for token BETWEENLIST
def t_BETWEENLIST(t):

	r'[a-zA-Z\u00C0-\u017F\/_]+\{\d+\,\d+\}'

	regex = fr'({columnID})({interval})'

	regexExp = re.compile(regex)

	obj = BetweenList(regexExp.search(t.value).group(1), int(regexExp.search(t.value).group(3)),
	 int(regexExp.search(t.value).group(4)))

	global formatHeader
	formatHeader.append(obj)


# Rule for token DEFINEDLIST
def t_DEFINEDLIST(t):

	r'[a-zA-Z\u00C0-\u017F\/_]+\{(\d+)\}'

	regex = fr'({columnID})({size})'

	regexExp = re.compile(regex)

	obj = BetweenList(regexExp.search(t.value).group(1), int(regexExp.search(t.value).group(3)))

	global formatHeader
	formatHeader.append(obj)


# Rule for token ID
def t_ID(t):

	r'[a-zA-Z\u00C0-\u017F\/_]+'
	global formatHeader

	obj = ColumnID(t.value)

	formatHeader.append(obj)

# Rule to ignore
t_ignore = r',| "'
	

# Throw error if unkown token
def t_error(t):
	print("Error: Unknown token: ", t)
	sys.exit("")


##############################################################

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


# Function to build the format header
def buildHeader():
	global header
	with open(fileCSV, "r") as f:
		cabecalho = f.readline().strip()
		lexer = lex.lex()

		lexer.input(cabecalho)
		while True:
			for token in lexer:
				print(token)
			break
	f.close()


# Function to create the name of the JSON file
def createJSONNameFile():
	filename = fileCSV.split('.', 1)
	global fileJSON
	fileJSON = filename[0] + ".json"


secure()
buildHeader()
createJSONNameFile()


# Function that returns the most frequent element of a list
def most_frequent(l):
    counter = 0
    num = l[0]

    for i in l:
        curr_frequency = l.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num


#Function that builds a list with all the lines from the CSV file, organizing by dictionary per global struture
def buildJSON(list2JSON, allLines):
	dictionary = {} 

	for structure in list2JSON:
		if type(structure) == ColumnID:
			dictionary.update({structure.name : structure.parameter})

		elif type(structure) == DefinedList: 
			dictionary.update({structure.name : str(structure.list)})

		elif type(structure) == BetweenList:
			dictionary.update({structure.name : str(structure.list)})

		else:
			name = structure.name + "_" + structure.function
			if structure.list:
				if structure.function == "sum":
					dictionary.update({name : sum(map(int, structure.list))})

				elif structure.function == "media":
					dictionary.update({name : statistics.median(map(int, structure.list))})

				elif structure.function == "maisrecorrente":
					 dictionary.update({name : most_frequent(structure.list)})
				else:
					dictionary.update({name : ""})

	allLines.append(dictionary)


def buildLine(listOfCells):
	index = 0
	list2JSON = []
	for struct in formatHeader:
		if type(struct) == ColumnID:
			obj = ColumnID(struct.name)
			obj.parameter = listOfCells[index]
			list2JSON.append(obj)
			index += 1

		elif type(struct) == DefinedList:

			obj = DefinedList(struct.name, struct.size)
			for value in range(0, struct.size):
				if listOfCells[index] != "":
					obj.list.append(listOfCells[index])
				index += 1
			list2JSON.append(obj)

		elif type(struct) == BetweenList:
			obj = BetweenList(struct.name, struct.min, struct.max)
			for value in range(0, struct.max):
				if listOfCells[index] != "":
					obj.list.append(listOfCells[index])
				index += 1
			list2JSON.append(obj)

		else:

			obj = FunctionAgregList(struct.name, struct.min, struct.max, struct.function)
			for value in range(0, struct.max):
				if listOfCells[index] != "":
					obj.list.append(listOfCells[index])
				index += 1
			list2JSON.append(obj)
	return list2JSON


# Function that converts the CSV file to the JSON file
def csv2json():
	with open(fileCSV, "r") as file:
		maxLine = 0
		allLines = []
		regexExp = re.compile(readCell)

		for line in file:
			list2JSON = []
			line = line.strip()
 
			if maxLine == 0:
				maxLine += 1

			else:
				listOfCells = []
				for element in regexExp.finditer(line):
					listOfCells.append(element.group(1))

				list2JSON = buildLine(listOfCells)
				buildJSON(list2JSON, allLines)

	with open(fileJSON, "w") as file:
		formatList = json.dumps(allLines, indent = 4, ensure_ascii = False)
		file.write(formatList)
	file.close()
				
csv2json()

sys.exit("File " + fileJSON + " sucessfully created!")
#################################################################