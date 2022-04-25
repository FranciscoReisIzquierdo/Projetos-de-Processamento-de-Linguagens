# LEX

# Especials tokens -> literals, ignore, tokens, return, error;

# Tokens -> Words, %, %%;


import ply.lex as lex
import sys
import ply.yacc as yacc


#reserved = {'%literals' : 'LITERALS', '%ignore' : 'IGNORE', '%tokens' : 'TOKENS', '%return' : 'RETURN'}

tokens = ["SET", 
		"TOK", 
		"LITERALS", 
		"IGNORE", 
		"TOKENS", 
		"RETURN", 
		"REGEX",
		"ERROR", 
		"TVALUE", 
		"INFO", 
		"COMMENT", 
		"LINE", 
		"SECTION",
		"RIGHT",
		"LEFT",
		"PREC",
		"ID"
		]



literals = "[](),={}:"



#################################### Syntax Rules ##################################






 




# Rule for token SECTION
def t_SECTION(t):
	r'%%[ \t]*'
	return t

def t_LEFT(t):
	r'\'left\''
	return t


def t_RIGHT(t):
	r'\'right\''
	return t

# Rule for toke PRECEDENCE
def t_PREC(t):
	r'%precedence'
	return t

# Rule for token LITERALS
def t_LITERALS(t):
	r'%literals'
	return t


# Rule for token IGNORE
def t_IGNORE(t):
	r'%ignore'
	return t


# Rule for token TOKENS
def t_TOKENS(t):
	r'%tokens'
	return t


# Rule for token RETURN
def t_RETURN(t):
	r'return'
	return t


# Rule for token REGEX
def t_REGEX(t):
	r'r\'[a-zA-Z0-9\[\]\(\)\?\\\+\*\_\-\. ]+\''
	return t


# Rule for token ERROR
def t_ERROR(t):
	r'\.[\t ]+[A-Za-z0-9\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\>\=\?\@\[\]\{\}\\\\^\_\`\~ ]+'
	return t


# Rule for token TOK
def t_TOK(t):
	r'\'[A-Za-z0-9\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\>\=\?\@\[\]\{\}\\\\^\_\`\~ ]+\''
	return t


# Rule for token SET
def t_SET(t):
	r'\"[A-Za-z0-9\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\>\=\?\@\[\]\{\}\\\\^\_\`\~ ]+\"'
	return t


# Rule for token ATRIB
def t_TVALUE(t):
	r'((float\(|int\(|double\(|str\()t\.value\)|t\.value)'
	return t


# Rule for token COMMENT
def t_COMMENT(t):
	r'\#[^\n]*'
	return t


# Rule for token LINE
def t_LINE(t):
	r'[ \n\t]+'
	return t


# Rule for token INFO
def t_INFO(t):
	r'[A-Za-z0-9\"\'\\*\+\-\.\/\\\_\' ]+'
	return t


t_ignore = ' \r'


def t_error(t):
	print(f"Illegal character ’{t.value[0]}’, [{t.lexer.lineno}]", t.lexer.skip(1))


################################## Semantics Rules ################################


elements = []
index = 0

# Production for PLY
def p_ply(p):
	'''
	ply : LINE 
		| lex_comment LINE
		| yacc_comment LINE
		| yacc LINE
		| lex LINE
		| comment LINE
		| section LINE
		| atribution LINE
	'''
	p[0] = p[1]
	var = p[1]
	if var != "\n":
		print(p[1] + "\n")



# Production for lex_comment
def p_lex_comment(p):
	'''
	lex_comment : lex LINE comment
	'''
	p[0] = p[1] + p[2] + p[3]


# Production for lex_comment
def p_yacc_comment(p):
	'''
	yacc_comment : yacc LINE comment
	'''
	p[0] = p[1] + p[2] + p[3]



# Production for comment
def p_comment(p):
	'''
	comment : COMMENT
	'''
	p[0] = p[1]


def p_yacc(p):
	'''
	yacc : precedence
	'''
	p[0] = p[1]



def p_precedence(p):
	'''
	precedence : PREC '=' list
	'''
	p[0] = "precedence = [ " + p[3] + " ]"





# Production for lex
def p_lex(p):
	'''
	lex : literals
		| tokens
		| ignore
		| return
		| err 
	'''
	p[0] = p[1]


# Production for literals
def p_literals(p):
	'''
	literals : LITERALS '=' SET
	'''
	info = "literals = " 
	p[0] = info + p[3]



# Production for tokens
def p_tokens(p):
	'''
	tokens : TOKENS '=' list
	'''
	p[0] = "tokens = [ " + p[3] + " ]"



# Production for list
def p_list(p):
	'''
	list : '[' elems ']'
		 | '[' precs ']'

	'''
	#ALTERAR ISTO PARA DICIONÁRIO
	p[0] = p[2]



# Production for elems_one
def p_elems_one(p):
	'''
	elems : TOK
	'''
	p[0] = p[1]
	var = p[1]
	
	global index, elements
	if var not in elements:
		elements.insert(index, var)
		index += 1



# Production for elems_various
def p_elems_various(p):
	'''
	elems : elems ',' TOK
	'''
	p[0] = p[1] + p[2] + p[3]
	var = p[3]
	global index, elements
	if var not in elements:
		elements.insert(index, var)

	index = 0
	elements = []



def p_precs_one(p):
	'''
	precs : '(' tuple ')'
	'''
	p[0] = p[2]



def p_precs_various(p):
	'''
	precs : precs ',' '(' tuple ')'
	'''
	p[0] = p[1] + p[2] + p[4]



def p_tuple(p):
	'''
	tuple : LEFT ',' elems
		  | RIGHT  ',' elems
	'''
	p[0] = "(" + p[1] + p[2] + " " + p[3] + ")"



# Production for return
def p_return(p):
	'''
	return : REGEX LINE RETURN '(' TOK ',' TVALUE ')'
	'''
	var = p[5]
	var = var.replace("'", "")
	function = "def t_" + var + "(t):"
	regex = p[1]
	atribution = "t.value = " + p[7]
	p[0] = function + "\n\t" + p[1] + "\n\t" + atribution + "\n\t" + "return t"



# Production for ignore
def p_ignore(p):
	'''
	ignore : IGNORE '=' SET
	'''
	info = "t_ignore = "
	p[0] = info + p[3]



# Production for err
def p_err(p):
	'''
	err : ERROR
	'''
	error_message = p[1]
	error_message = error_message.replace(".", "")
	error_message = error_message.replace("\t", "")
	error_message = error_message.replace("error", "", 1)
	p[0] = "def t_error(t):\n\tprint" + error_message


def p_atribution(p):
	'''
	atribution : ID '=' ID
			   | ID '=' list
			   | ID '=' emptyList
			   | ID '=' emptyDicionary
	'''
	p[0] = p[1] + " " + p[2] + " " + p[3]


def p_emptyList(p):
	'''
	emptyList : '[' ']'
	'''
	p[0] = p[1] + p[2]


def p_emptyDicionary(p):
	'''
	emptyDicionary : '{' '}'
	'''
	p[0] = p[1] + p[2]


# Production for section
def p_section(p):
	'''
	section : SECTION INFO
			| SECTION ID
	'''
	p[0] = "\"\"\"\n" + p[2] + "\n\"\"\""


# Production for an error 
def p_error(p):
	print("Syntax error")



lexer = lex.lex()
y = yacc.yacc()

for line in sys.stdin:
	#lexer.input(line)
	#for tok in lexer:
	#	print(tok)
	y.parse(line)

