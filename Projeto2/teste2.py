import ply.lex as lex
import sys
import ply.yacc as yacc


################## Global Variables ####################


file = ""
fileConverted = ""
finalFile = ""


flagLiterals = False
flagTokens = False
flagIgnore = False
flagPrecedence = False


listLiterals = []
listTokens = []


literals = "=\'[]\",(){}.:+-*/<>?"


tokens = ["Comment", 
			"Info", 
			"END", 
			"Section", 
			"Literals", 
			"Ignore", 
			"Tokens", 
			"Regex", 
			"Return", 
			"Id", 
			"Error", 
			"Value", 
			"Chars", 
			"Tvalue", 
			"Precedence", 
			"Right", 
			"Left",
			"Index",
			"Python"
		]

states = [("Comment", "exclusive"), ("Section", "exclusive"), ("Python", "exclusive"), ("Function", "exclusive")]

###############################################

#################### LEX  #####################

####### Syntax Rules for Comments #######

def t_Comment(t):
	r'\#'
	t.lexer.begin("Comment")
	return t


#------------------------------------------------#


def t_Comment_Info(t):
	r'.+'
	return t


def t_Comment_END(t):
	r'\n'
	t.lexer.begin("INITIAL")
	return t

###############################################

####### Syntax Rules for Python Section ########

def t_Python(t):
	r'%%\n'
	t.lexer.begin("Python")
	return t 


def t_Python_Info(t):
	r'[A-Za-z0-9\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\>\=\?\@\[\]\{\}\\\\^\_\`\~\n\t ]+'
	return t


###############################################

####### Syntax Rules for Code Sections ########

def t_Section(t):
	r'%%.+'
	t.lexer.begin("Section")
	return t


#------------------------------------------------#

def t_Section_END(t):
	r'\n'
	t.lexer.begin("INITIAL")
	return t 

###############################################

####### Syntax Rules for Reserved words #######


def t_Literals(t):
	r'literals'
	return t


def t_Ignore(t):
	r'ignore'
	return t


def t_Tokens(t):
	r'tokens'
	return t


def t_Return(t):
	r'return'
	return t


def t_Error(t):
	r'error'
	t.lexer.begin("Function")
	return t


def t_Function_Info(t):
	r'[A-Za-z0-9\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\>\=\?\@\[\]\{\}\\\\^\_\`\~\t ]+'
	return t


def t_Function_END(t):
	r'\n'
	t.lexer.begin("INITIAL")
	return t


def t_Precedence(t):
	r'precedence'
	return t


def t_Right(t):
	r'right'
	return t


def t_Left(t):
	r'left'
	return t


#------------------------------------------------#


################################################

####### Syntax Rules for Return key word #######


#------------------------------------------------#


################################################

############ General Syntax Rules ##############

def t_Regex(t):
	r'r\'[^\n\t]+\''
	return t


def t_Index(t):
	r'[a-zA-Z][a-zA-Z0-9_]*\[\d+\]'
	return t


def t_Info(t):
	r'\{[^\n\t]+\}'
	return t


def t_Tvalue(t):
	r'((float\(|int\(|double\(|str\()t\.value\)|t\.value)'
	return t


def t_Chars(t):
	r'\"[^\t\n]+\"|f\"[^\t\n]+\"'
	return t


def t_Id(t):
	r'([a-zA-Z\%][a-zA-Z0-9_]+(\.[a-zA-Z][a-zA-Z0-9_])?)+'
	return t

#def t_Function(t):



def t_Value(t):
	r'[\-\+]?[0-9]+(\.[0-9]+)?'
	return t


################################################

####### Syntax Rules for Ignoring stuff and Errors ########

t_ignore = "\n\t "
t_Comment_ignore = ""
t_Section_ignore = ""
t_Python_ignore = ""
t_Function_ignore = ""



def t_error(t):
	print(f"<Error Message>: Illegal character '{t.value[0]}', in line {t.lexer.lineno}\n")
	print("----------------Please fix your file!----------------")
	sys.exit()



def t_Comment_error(t):
	print(f"<Error Message>: Illegal character '{t.value[0]}' in comment (line: " + str(t.lexer.lineno) + ")\n")
	print("----------------Please fix your file!----------------")
	sys.exit()


def t_Section_error(t):
	print(f"<Error Message>: Illegal character '{t.value[0]}' in code section (line: " + str(t.lexer.lineno) + ")\n")
	print("----------------Please fix your file!----------------")
	sys.exit() 

def t_Python_error(t):
	print(f"<Error Message>: Illegal character '{t.value[0]}' in Pyhton (line: " + str(t.lexer.lineno) + ")\n")
	print("----------------Please fix your file!----------------")
	sys.exit() 


def t_Function_error(t):
	print(f"<Error Message>: Illegal character '{t.value[0]}' in Error message (line: " + str(t.lexer.lineno) + ")\n")
	print("----------------Please fix your file!----------------")
	sys.exit()


################################################



#################### YACC  #####################

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
	lexer.lineno += 1
	size = len(p)

	if size == 2 :
		p[0] = p[1] + "\n"
	elif size == 3:
		p[0] = p[1] + "\t" + p[2] + "\n"

	else:
		p[0] = "\n"
	finalFile.write(p[0])
	

def p_error(p):
	print(f"Syntax error in line {t.lexer.lineno}\n")


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
	p[1] = p[1].replace("%", "")
	p[0] = "\'\'\'\n" + p[1] + "\n\'\'\'\n"


############## Productions for atribution #############

def p_atribution(p):
	'''
	atribution : Id '=' exp
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
	p[0] = "def t_" + token + "(t):\n\t" + p[1] + "\n\t" + p[2] + " " + returnValue


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
			print(f"<Error Message>: Redefinition of \'tokens\' (line: " + str(lexer.lineno) + ")\n")
			print("----------------Please fix your file!----------------")
			sys.exit()
		else:
			flagTokens = True
			p[0] = "tokens " + p[2] + p[3]

	if p[1] == "literals":
		if flagLiterals == True:
			print(f"<Error Message>: Redefinition of \'literals\' (line: " + str(lexer.lineno) + ")\n")
			print("----------------Please fix your file!----------------")
			sys.exit()
		else:
			flagLiterals = True
			p[0] = "t_literals " + p[2] + " " + p[3]

	if p[1] == "ignore":
		if flagIgnore == True:
			print(f"<Error Message>: Redefinition of \'ignore\' (line: " + str(lexer.lineno) + ")\n")
			print("----------------Please fix your file!----------------")
			sys.exit()
		else:
			flagIgnore = True
			p[0] = "t_ignore " + p[2] + " " + p[3]






def p_erro(p):
	'''
	erro : '.' reservedFunctions
	'''
	p[0] = "def p_error(t):\n\t" + p[2]


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
		info = info.replace("{", "")
		info = info.replace("}", "")

		p[0] = "def p_" + p[1] + "(t):\n\t\'\'\'\n\t" + p[1] + " " + p[2] + " " + p[3] + "\n\t\'\'\'\n\t" + info + "\n"
	else:
		p[0] = "def p_" + p[1] + "(t):\n\t\'\'\'\n\t" + p[1] + " " + p[2] + "\n\t\'\'\'\n"


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
	dic : '{' Empty '}'
		| '{' conj '}'
	'''
	p[0] = "{ " + p[2] + " }"


def p_conj(p):
	'''
	conj : Value ':' Value
		 | Chars ':' Chars
		 | Value ':' Chars
		 | Chars ':' Value
		 | conj ',' Value ':' Value
		 | conj ',' Chars ':' Chars
		 | conj ',' Value ':' Chars
		 | conj ',' Chars ':' Value
	'''

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
	if len(sys.argv) == 1:
		sys.exit("No file name found when running the application! It's 2 arguments (<application name> <file name>).")
	elif len(sys.argv) > 2:
		sys.exit("Wrong number of arguments for the application! It's 2 arguments (<application name> <file name>).")

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
	#	lexer.input(line)
	#	for tok in lexer:
	#		print(tok)
		y.parse(line)
	finalFile.close()



lexer = lex.lex()
y = yacc.yacc()

secure()
convertFile()








#####################################################################