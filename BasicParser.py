from sly import Parser

import BasicLex


class BasicParser(Parser):
	#tokens are passed from lexer to parser
	tokens = BasicLex.BasicLex.tokens

	precedence = (
		('left', 'IF', 'ELSE'),
		('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
		('left', '+', '-'),
		('left', '*', '/'),
		('right', 'UMINUS'),
	)

	def __init__(self):
		self.env = {}

	@_('')
	def statement(self, p):
		pass

	@_('FOR var_assign TO expr THEN statement')
	def statement(self, p):
		return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

	@_('IF expr THEN statement ELSE statement')
	def statement(self, p):
		return ('if_stmt', p.expr, ('branch', p.statement0, p.statement1))

	@_('IF expr THEN statement')
	def statement(self, p):
		return ('if_stmt1', p.expr, ('branch', p.statement0))

	@_('FUN NAME "(" ")" ARROW statement')
	def statement(self, p):
		return ('fun_def', p.NAME, p.statement)

	@_('NAME "(" ")"')
	def statement(self, p):
		return ('fun_call', p.NAME)

	@_('var_assign')
	def statement(self, p):
		return p.var_assign

	@_('NAME "=" expr')
	def var_assign(self, p):
		return ('var_assign', p.NAME, p.expr)

	@_('NAME "=" STRING')
	def var_assign(self, p):
		return ('var_assign', p.NAME, p.STRING)

	@_('expr')
	def statement(self, p):
		return (p.expr)

	@_('expr "+" expr')
	def expr(self, p):
		return ('add', p.expr0, p.expr1)

	@_('expr "-" expr')
	def expr(self, p):
		return ('sub', p.expr0, p.expr1)

	@_('expr "*" expr')
	def expr(self, p):
		return ('mul', p.expr0, p.expr1)

	@_('expr "/" expr')
	def expr(self, p):
		return ('div', p.expr0, p.expr1)

	@_('"-" expr %prec UMINUS')
	def expr(self, p):
		return p.expr

	@_('NAME')
	def expr(self, p):
		return ('var', p.NAME)

	@_('expr GT expr')
	def expr(self, p):
		return ('gt', p.expr0, p.expr1)

	@_('expr EXP expr')
	def expr(self, p):
		return ('exp', p.expr0, p.expr1)

	@_('expr LT expr')
	def expr(self, p):
		return ('lt', p.expr0, p.expr1)

	@_('expr EQ expr')
	def expr(self, p):
		return ('equals', p.expr0, p.expr1)

	@_('expr LE expr')
	def expr(self, p):
		return ('le', p.expr0, p.expr1)

	@_('expr GE expr')
	def expr(self, p):
		return ('ge', p.expr0, p.expr1)

	@_('expr NE expr')
	def expr(self, p):
		return ('ne', p.expr0, p.expr1)

	@_('expr "," expr')
	def expr(self, p):
		return ('comma', p.expr0, p.expr1)

	@_('FLOAT')
	def expr(self, p):
		return ('num', p.FLOAT)

	@_('INTEGER')
	def expr(self, p):
		return ('num', p.INTEGER)

	@_('LPAREN expr RPAREN')
	def expr(self, p):
		return p.expr

	@_('PRINT expr')
	def statement(self, p):
		return 'print', p.expr

	@_('STRING')
	def expr(self, p):
		return 'str', p.STRING
