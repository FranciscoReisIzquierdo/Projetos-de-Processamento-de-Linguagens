import ply.lex as lex
import sys
import ply.yacc as yacc
import re



literals = "=\'[]\",(){}:"


tokens = ["CHARS", "RESERVEDWORD", "COMMENT", "TEXT", "END", "DEF", "PROD", "EXP", "FINAL", "LEFT", "RIGHT","SECTION", "ID", "TYPE", "KEYWORDS", "LITERALS", "TOKENS", "IGNORE", "PRECEDENCE", "SET", "TOK", "REGEX", "SPACE", "RETURN", "TVALUE", "ERROR", "TOKPREC", "TAB"]

states = [("LIST", "exclusive"), ("SET", "exclusive"), ("COMMENT", "exclusive"), ("SECTION", "exclusive"), ("KEYWORDS", "exclusive"), ("RETURN", "exclusive"), ("ERROR", "exclusive"), ("PROD", "exclusive"), ("DEF", "exclusive")]

# ("LIST", "exclusive"), ("SET", "exclusive"), 

##################################### Syntax Rules


####### Syntax Rules for Comments #######

def t_COMMENT(t):
	r'\#'
	t.lexer.begin("COMMENT")
	return t


def t_COMMENT_TEXT(t):
	r'.+'
	return t


def t_COMMENT_END(t):
	r'\n'
	t.lexer.begin("INITIAL")
	return t

##############################################

####### Syntax Rules for Code Sections #######

def t_SECTION(t):
	r'%%'
	t.lexer.begin("SECTION")
	return t


def t_SECTION_TEXT(t):
	r'.+'
	return t


def t_SECTION_END(t):
	r'\n'
	t.lexer.begin("INITIAL")
	return t 

##############################################


def t_RESERVEDWORD(t):
	r'(literals)|(ignore)|(tokens)'
	regex = r'(literals)|(ignore)|(tokens)'
	regexExp = re.compile(regex)


	if regexExp.search(t.value).group(1) or regexExp.search(t.value).group(2):
		t.lexer.begin("SET")

	elif regexExp.search(t.value).group(3):
		t.lexer.begin("LIST")

	rule = t.lexer
	return t



def t_SET_CHARS(t):
	r'\"[A-Za-z0-9\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\>\=\?\@\[\]\{\}\\\\^\_\`\~ ]+\"'
	return t


def t_LIST_TOK(t):
	r'[a-zA-Z]+|[0-9]+'
	return t 

def t_LIST_START(t):
	r'\['



def t_LIST_END(t):
	r'\]'
	lexer.begin("INITIAL")
	return t



t_LIST_ignore = " "



def t_KEYWORDS(t):
	r'%'
	t.lexer.begin("KEYWORDS")
	return t


def t_KEYWORDS_LITERALS(t):
	r'literals'
	return t


def t_KEYWORDS_TOKENS(t):
	r'tokens'
	return t


def t_KEYWORDS_IGNORE(t):
	r'ignore'
	return t


def t_DEF(t):
	r'def'
	t.lexer.begin("DEF")
	return t


def t_DEF_SECTION(t):
	r'\n\t+'
	return t

def t_DEF_TEXT(t):
	r'.*\n\t'

	return t


def t_DEF_END(t):
	r'\n+'
	t.lexer.begin("INITIAL")
	return t


def t_KEYWORDS_LEFT(t):
	r'\'left\''
	return t


def t_KEYWORDS_RIGHT(t):
	r'\'right\''
	return t


def t_KEYWORDS_PRECEDENCE(t):
	r'precedence'
	return t



def t_KEYWORDS_TOK(t):
	r'[a-zA-Z]+|[0-9]+'
	return t


def t_KEYWORDS_END(t):
	r'[\n\t ]+'
	t.lexer.begin("INITIAL")
	return t



def t_SPACE(t):
	r'[\t ]+'
	return t


def t_KEYWORDS_TOKPREC(t):
	r'\'.+\''
	return t





def t_REGEX(t):
	r'r\'[^\n\t]+\''
	return t



def t_RETURN(t):
	r'return'
	t.lexer.begin("RETURN")
	return t



def t_RETURN_TVALUE(t):
	r'((float\(|int\(|double\(|str\()t\.value\)|t\.value)'
	return t


def t_RETURN_TOK(t):
	r'[a-zA-Z]+|[0-9]+'
	return t


def t_RETURN_END(t):
	r'\n'
	t.lexer.begin("INITIAL")
	return t



def t_ERROR(t):
	r'\.'
	t.lexer.begin("ERROR")
	return t


def t_ERROR_KEYWORDS(t):
	r'error'
	return t



def t_ERROR_TEXT(t):
	r'\w+\d*'
	return t


def t_ERROR_SPACE(t):
	r'[\t ]+'
	return t


def t_ERROR_END(t):
	r'[\n\t ]+'
	t.lexer.begin("INITIAL")



def t_PROD(t):
	r'\:'
	t.lexer.begin("PROD")
	return t



def t_ID(t):
	r'[a-zA-Z][a-zA-Z0-9_]*'
	return t

def t_DEF_ID(t):
	r'[a-zA-Z][a-zA-Z0-9_]*'
	return t



def t_TYPE(t):
	r'\"[a-zA-Z]+\"|[\-\+]?[0-9]+(\.[0-9]+)?'
	return t


def t_PROD_FINAL(t):
	r'\{.+\}'
	return t


def t_PROD_ID(t):
	r'[\w\d(\'\+\')(\'\-\')(\'\*\')(\'\\\')(\'\=\')(\'\)\')(\'\(\')]+'
	return t

def t_PROD_TAB(t):
	r'\t+'
	return t

def t_PROD_END(t):
	r'\n+'
	t.lexer.begin("INITIAL")
	return t


t_ignore = "\n "
t_KEYWORDS_ignore = " "
t_RETURN_ignore = " ."
t_PROD_ignore = " "
t_DEF_ignore = " "




def t_error(t):
	print(f"Illegal character ’{t.value[0]}’, [{t.lexer.lineno}]", t.lexer.skip(1))

lexer = lex.lex()



def p_ply(p):
	'''
	ply : atribution
		| section
		| commentary
		| function
		| erro
		| production
		| definition
		| keys
		|
	'''


def p_keys(p):
	'''
	keys : RESERVEDWORD '=' list END
	'''
	#lexer.begin("INITIAL")


def p_lista(p):
	'''
	lista : '[' "'" TOK "'" ']'
	'''



def p_definition(p):
	'''
	definition : DEF ID '(' simpleTuple ')' ':' SECTION TEXT END

	'''


def p_simpleTuple(p):
	'''
	simpleTuple : ID
				| simpleTuple ',' ID
	'''

	
def p_production(p):
	'''
	production : ID PROD ID TAB FINAL END
	'''




def p_text(p):
	'''
	section : SECTION TEXT END
	'''
	p[0] = p[1]


def p_commentary(p):
	'''
	commentary : COMMENT TEXT END
	'''
	p[0] = p[1]


def p_atribution(p):
	'''
	atribution : ID '=' TYPE
			   | ID '=' TYPE SPACE commentary
			   | specialKeys END
			   | specialKeys END commentary
	'''
	


def p_specialKeys(p):
	'''
	specialKeys : KEYWORDS TOKENS '=' list 
				| KEYWORDS LITERALS '=' SET 
				| KEYWORDS IGNORE '=' SET
				| KEYWORDS PRECEDENCE '=' listTuple
	'''



# Production for list
def p_list(p):
	'''
	list : '[' elems ']'
	'''


def p_listTuple(p):
	'''
	listTuple : '[' precs ']'
	'''



# Production for elems_one
def p_elems_one(p):
	'''
	elems : "'" TOK "'"
		  | TOKPREC
	'''




# Production for elems_various
def p_elems_various(p):
	'''
	elems : elems ',' "'" TOK "'"
		  | elems ',' TOKPREC
	'''



def p_function(p):
	'''
	function : regex
	'''


def p_regex(p):
	'''
	regex : REGEX SPACE RETURN tuple
	'''

def p_tuple(p):
	'''
	tuple : "(" "'" TOK "'" "," TVALUE ")" END
		  | 
	'''


def p_erro(p):
	'''
	erro : ERROR SPACE KEYWORDS "(" TEXT ")"

	'''


def p_precs_one(p):
	'''
	precs : '(' tupleforPrec ')'
	'''
	



def p_precs_various(p):
	'''
	precs : precs ',' '(' tupleforPrec ')'
	'''
	



def p_tupleforPrec(p):
	'''
	tupleforPrec : LEFT ',' elems
		  	     | RIGHT  ',' elems
	'''




def p_error(p):
	print("Syntax error")	


y = yacc.yacc()

for line in sys.stdin:
	lexer.input(line)
	for tok in lexer:
		print(tok)
	y.parse(line)
