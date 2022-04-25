import ply.lex as lex

literals = "+-*,/=)("

tokens = ["VAR", "NUMBER"]

t_ignore = ' \t\n\r'


def t_VAR(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	t.value = float(t.value)
	return t

def t_error(t):
	print(f"Illegal character ’{t.value[0]}’, [{t.lexer.lineno}]", t.lexer.skip(1))


# symboltable : dictionary of variables

ts = {}

import ply.yacc as yacc

precedence = [ ('left','+','-'), ('left','*','/'), ('right', 'UMINUS')]


def p_stat_Ig(p):
    "stat : VAR '=' exp"
    ts[p[1]] = p[3]


def p_stat_Exp(p):
    "stat : exp"
    print(p[1])


def p_exp_Plus(p):
    "exp : exp '+' exp"
    p[0] = p[1] + p[3]


def p_exp_Minus(p):
    "exp : exp '-' exp"
    p[0] = p[1] - p[3]


def p_exp_Multiply(p):
    "exp : exp '*' exp"
    p[0] = p[1] * p[3]


def p_exp_Divide(p):
    "exp : exp '/' exp"
    p[0] = p[1] / p[3]


def p_exp_UMINUS(p):
	"exp : '-' exp %prec UMINUS"
	p[0] = -p[2]

def p_exp_Between(p):
    "exp : '(' exp ')'"
    p[0] = p[2]


def p_exp_NUMBER(p):
	"exp : NUMBER"
	p[0] = p[1]


def p_exp_VAR(p):
	"exp : VAR"
	p[0] = getval(p[1])


# exp : ’-’ exp %prec UMINUS { t[0] = -t[2] }

def p_error(t):
	print(f"Syntax error at ’{t.value}’, [{t.lexer.lineno}]")


def getval(n):
	if n not in ts: print(f"Undefined name ’{n}’")
	return ts.get(n,0)

lexer = lex.lex()

y = yacc.yacc()
y.parse("3+4*7")


#for line in sys.stdin:
	#lexer.input(line)
	#for tok in lexer:
	#	print(tok)
#	y.parse(line)