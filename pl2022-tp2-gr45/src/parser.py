import ply.yacc as yacc
import sys
import os

from lexer import tokens


file = ""
fileConverted = ""
finalFile = ""


flagLiterals = False
flagTokens = False
flagIgnore = False
flagPrecedence = False


############## General Productions #############

def p_ply(p):
	'''
	ply : commentary
		| section
		| atribution
		| atribution commentary
		| lex
		| lex commentary
		| yacc
		| yacc commentary
		| python
		|
	'''
	global finalFile
	p.lexer.lineno += 1
	size = len(p)

	if size == 2 :
		p[0] = p[1] + "\n"
	elif size == 3:
		p[0] = p[1] + "\t" + p[2] + "\n"

	else:
		p[0] = "\n"
	finalFile.write(p[0])
	#print(p[0])
	

def p_error(p):
	print(f"Syntax error in line {p.lexer.lineno}\n")
	os.remove(fileConverted)
	sys.exit()


################################################

############## Productions for commentaries and sections #############


def p_commentary(p):
	'''
	commentary : Comment Info END
	'''
	p[0] = p[1] + p[2]


def p_section(p):
	'''
	section : Section END
	'''
	p[0] = p[1] + "\n"


############## Productions for atribution #############

def p_atribution(p):
	'''
	atribution : Id '=' exp
			   | Id '=' FuncElem
			   | Id '=' Chars
			   | Id '=' list
			   | Id '=' dic
			   | Index '=' exp
			   | Index '=' Chars
			   | Index '=' list
			   | Index '=' dic
			   | Index '=' Index
	'''
	p[0] = p[1] + " " + p[2] + " " + p[3] + "\n"


def p_exp(p):
	'''
	exp : Value
		| exp '+' Value
		| exp '-' Value
		| exp '/' Value
		| exp '*' Value
		| '-' Value
	'''
	size = len(p)
	if size == 2:
		p[0] = p[1]
	elif size == 3:
		p[0] = p[1] + " " + p[2]
	else:
		p[0] = p[1] + " " + p[2] + " " + p[3]



################################################

############## Productions for lex #############

def p_lex(p):
	'''
	lex : regex
		| reservedWordsLex
		| erro
	'''
	p[0] = p[1]


def p_regex(p):
	'''
	regex : Regex Return regexTuple
	'''
	info = p[3]
	token = info[0]
	returnValue = info[1]
	p[0] = "def t_" + token + "(t):\n\t" + p[1] + "\n\tt.value = " + returnValue + "\n\t" + p[2] + " t\n"


def p_reservedWords(p):
	'''
	reservedWordsLex : Tokens '=' list 
				     | Literals '=' list
				     | Literals '=' Chars 
				     | Ignore '=' Chars
	'''
	global flagTokens, flagIgnore, flagLiterals
	if p[1] == "tokens":
		if flagTokens == True:
			print(f"<Error Message>: Redefinition of \'tokens\' (line: " + str(p.lexer.lineno ) + ")\n")
			print("----------------Please fix your file!----------------")
			os.remove(fileConverted)
			sys.exit()
		else:
			flagTokens = True
			p[0] = "tokens " + p[2] + p[3]

	if p[1] == "literals":
		if flagLiterals == True:
			print(f"<Error Message>: Redefinition of \'literals\' (line: " + str(p.lexer.lineno ) + ")\n")
			print("----------------Please fix your file!----------------")
			os.remove(fileConverted)
			sys.exit()
		else:
			flagLiterals = True
			p[0] = "literals " + p[2] + " " + p[3]

	if p[1] == "ignore":
		if flagIgnore == True:
			print(f"<Error Message>: Redefinition of \'ignore\' (line: " + str(p.lexer.lineno ) + ")\n")
			print("----------------Please fix your file!----------------")
			os.remove(fileConverted)
			sys.exit()
		else:
			flagIgnore = True
			p[0] = "t_ignore " + p[2] + " " + p[3]



def p_erro(p):
	'''
	erro : '.' reservedFunctions
	'''
	p[0] = "def t_error(t):\n\t" + p[2]


def p_reservedFunctions(p):
	'''
	reservedFunctions : Error Info END

	'''
	p[0] = "print" + p[2] + p[3] 

################################################

############## Productions for yacc #############


def p_yacc(p):
	'''
	yacc : reservedWordsYacc
		 | productions
	'''
	p[0] = p[1]


def p_reservedWordsYacc(p):
	'''
	reservedWordsYacc : Precedence '=' listOfTuples
	'''
	p[0] = p[1] + " " + p[2] + " " + p[3]


def p_productions(p):
	'''
	productions : Id ':' production Info
				| Id ':' production
	'''
	size = len(p)
	if size == 5:
		info = p[4]
		info = info.replace("{ ", "")
		info = info.replace("}", "")

		p[0] = "def p_production" + str(p.parser.production) + "(t):\n\t\'\'\'\n\t" + p[1] + " " + p[2] + " " + p[3] + "\n\t\'\'\'\n\t" + info + "\n"
	else:
		p[0] = "def p_production" + str(p.parser.production) + "(t):\n\t\'\'\'\n\t" + p[1] + " " + p[2] + "\n\t\'\'\'\n"

	p.parser.production+= 1


############## Productions for python #############


def p_Pyhton(p):
	'''
	python : Python
		   | Info
	'''
	if p[1] == "%%\n":
		p[0] = ""
	else:
		p[0] = p[1]


############## Productions for list, tuples, dictionaries and productions #############


def p_list(p):
	'''
	list : '[' Empty ']'
		 | '[' elems ']'
	'''
	p[0] = " [ " + p[2] + " ]"

#-------------------------------------------------------------------#


def p_listOfTuples(p):
	'''
	listOfTuples : '[' precs ']'
	'''
	p[0] = " [ " + p[2] + " ]"


def p_precs(p):
	'''
	precs : '(' tupleforPrec ')'
		  | precs ',' '(' tupleforPrec ')'
	'''
	size = len(p)
	if size == 4:
		p[0] = " ( " + p[2] + " )"
	else:
		p[0] = p[1] + p[2] + " " + " ( " + p[4] + " )"
	

def p_tupleforPrec(p):
	'''
	tupleforPrec : "'" Left "'" ',' elems
		  	     | "'" Right "'"  ',' elems
	'''
	p[0] = "\"" + p[2] + "\"" + p[4] + " " + p[5]

#-------------------------------------------------------------------#


def p_regexTuple(p):
	'''
	regexTuple : "(" "'" Id "'" "," Tvalue ")"
	'''
	lista = []
	lista.append(p[3])
	lista.append(p[6])
	
	p[0] = lista

#-------------------------------------------------------------------#


def p_dic(p):
	'''
	dic : Info
	'''
	p[0] = p[1]

#-------------------------------------------------------------------#


def p_production(p):
	'''
	production : '<' items '>' 
	'''
	p[0] = p[2]


def p_items_id(p):
	'''
	items : Id
		  | items Id
	'''
	size = len(p)
	if size == 2:
		p[0] = p[1]
	else: 
		p[0] = p[1] + " " + p[2]


def p_items_chars(p):
	'''
	items : Chars
		  | items Chars
	'''
	size = len(p)
	if size == 2:
		p[0] = p[1]
	else: 
		p[0] = p[1] + " " + p[2]


#-------------------------------------------------------------------#


def p_elems_id(p):
	'''
	elems : "'" Id "'"
		  | elems ',' "'" Id "'"
	'''
	size = len(p)
	if size == 4:
		p[0] = "\"" + p[2] + "\""
	else:
		p[0] = p[1] + p[2] + " " + "\"" + p[4] + "\""



def p_elems_chars(p):
	'''
	elems : Chars
		  | elems ',' Chars
	'''
	size = len(p)
	if size == 2:
		p[0] = p[1]
	else:
		p[0] = p[1] + p[2] + " " + p[3]


def p_Empty(p):
	'''
	Empty :
	'''
	p[0] = ""



def secure():
	if len(sys.argv) != 2:
		sys.exit("No file name found when running the application! It's 2 arguments (<application name> <file name>).")

	global file
	file = str(sys.argv[1])
	
	filename = file.split('.', 1)
	
	global fileConverted
	fileConverted = filename[0] + "(Converted to PLY)" + ".py"


def convertFile():
	global y
	global file
	global fileConverted
	global finalFile
	

	inputFile = open(file, "r")
	finalFile = open(fileConverted, "a")

	for line in inputFile:
		parser.parse(line)
	finalFile.close()
	print("File " + fileConverted + " created with sucess!")



parser = yacc.yacc()
parser.production = 0

secure()
convertFile()








#####################################################################