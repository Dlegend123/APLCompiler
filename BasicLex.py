from sly import Lexer


class BasicLex(Lexer):
    # Define tokens as regular expressions
    # (stored as raw strings)

    tokens = {f'NAME', f'STRING', f'FLOAT', f'INTEGER', f'EQ', f'GT', f'LT', f'LE', f'GE', f'NE', f'IF', f'WHILE',
              f'ELSE', f'PRINT', f'THEN', f'TO', f'FOR', f'ARROW', f'FUN', f'EXP', f'LPAREN', f'RPAREN'}

    ignore = '\t '
    literals = {'=', '+', '-', '/', '*', '(', ')', ',', ';'}

    # Define tokens as regular expressions
    # (stored as raw strings)

    # Define tokens
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    FUN = r'FUN'
    TO = r'TO'
    ARROW = r'->'
    WHILE = r'WHILE'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    LPAREN = r'\('
    RPAREN = r'\)'
    EQ = r'=='
    PRINT = r'PRINT'


    # Number token
    @_(r"\d+\.\d*")
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTEGER(self, t):
        t.value = int(t.value)
        return t

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NAME['IF'] = IF
    NAME['ELSE'] = ELSE
    NAME['WHILE'] = WHILE
    NAME['PRINT'] = PRINT

    # Comment token
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    # Newline token(used only for showing
    # errors in new line)
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

    def error(self, t):
        self.index += 1
        from main import code_output
        code_output.insert("1.0", "Illegal character '%s'" % t.value[0])

