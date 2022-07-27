import ply.lex as lex
import re

literals = "=\'[]\",(){}.:+-*/<>?"

reserved = {
	"literals" : "Literals",
	"tokens" : "Tokens",
	"ignore" : "Ignore",
	"return" : "Return",
	"right" : "Right",
	"left" : "Left",
	"precedence" : "Precedence",
	"error" : "Error"
}


tokens = ["Comment", 
			"Info", 
			"END", 
			"Section", 
			"Regex", 
			"Id", 
			"Value", 
			"Chars", 
			"Tvalue", 
			"Index",
			"Python",
			"FuncElem"
		] + list(reserved.values())

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

	regex = r'%%(.+)'
	regexExp = re.compile(regex)
	imp = regexExp.search(t.value).group(1)
	imp = imp.replace(" ", "")	
	
	t.value = f"import ply.{imp.lower()} as {imp.lower()}"

	return t


#------------------------------------------------#

def t_Section_END(t):
	r'\n'
	t.lexer.begin("INITIAL")
	return t 

###############################################

####### Syntax Rules for Reserved words #######

def t_Function_Info(t):
	r'[A-Za-z0-9\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\>\=\?\@\[\]\{\}\\\\^\_\`\~\t ]+'
	return t


def t_Function_END(t):
	r'\n'
	t.lexer.begin("INITIAL")
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


def t_FuncElem(t):
	r'([a-zA-Z][a-zA-Z0-9_]*\.)*[a-zA-Z][a-zA-Z0-9_]*\(\)'
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
	t.type = reserved.get(t.value, 'Id')
	if t.type == "Error":
		t.lexer.begin("Function")

	return t


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


lexer = lex.lex()
lexer.lineno = 1
################################################
