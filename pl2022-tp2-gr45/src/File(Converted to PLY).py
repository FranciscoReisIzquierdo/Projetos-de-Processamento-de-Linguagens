import ply.lex as lex

literals = "+-/*=()"	## a single char
t_ignore = " \t\n"
tokens = [ "VAR", "NUMBER" ]

#? = "t"

def t_VAR(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.value = t.value
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	t.value = float(t.value)
	return t

def t_error(t):
	print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]", t.lexer.skip(1) )


lexer = lex.lex()


import ply.yacc as yacc


precedence =  [  ( "left", "+", "-" ), ('left', "*" , "/"), ('right', "UMINUS" ) ]	# List of precedence

# symboltable : dictionary of variables
ts = { }


def p_production0(t):
	'''
	stat : VAR "=" exp
	'''
	ts[t[1]] = t[3] 

def p_production1(t):
	'''
	stat : exp
	'''
	print(t[1]) 

def p_production2(t):
	'''
	exp : exp "+" exp
	'''
	t[0] = t[1] + t[3] 

def p_production3(t):
	'''
	exp : exp "-" exp
	'''
	t[0] = t[1] - t[3] 

def p_production4(t):
	'''
	exp : exp "*" exp
	'''
	t[0] = t[1] * t[3] 

def p_production5(t):
	'''
	exp : exp "/" exp
	'''
	t[0] = t[1] / t[3] 

def p_production6(t):
	'''
	exp : "-" exp %prec UMINUS
	'''
	t[0] = -t[2] 

def p_production7(t):
	'''
	exp : NUMBER
	'''
	t[0] = t[1] 

def p_production8(t):
	'''
	exp : VAR
	'''
	t[0] = getval(t[1]) 





def p_error(t):

	print(f"Syntax error at '{t.value}', [{t.lexer.lineno}]")



def getval(n):

	if n not in ts: print(f"Undefined name '{n}'")

	return ts.get(n,0)



y=yacc.yacc()

y.parse("3+4*7")

