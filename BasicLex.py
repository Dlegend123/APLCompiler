from sly import Lexer
import collections
import math

class BasicLex(Lexer):
    # Define tokens as regular expressions
    # (stored as raw strings)

    tokens = {f'NAME', f'STRING', f'NUMBER', f'EQ', f'GT', f'LT', f'LE', f'TO', f'DO', f'GE', f'NE', f'IF', f'WHILE',
              f'ELSE', f'PRINT', f'THEN', f'SC', f'TO', f'BEGIN', f'END', f'FOR', f'ARROW', f'FUN', f'EXP', f'LPAREN', f'RPAREN'}

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
    SC = r';'
    ARROW = r'->'
    WHILE = r'WHILE'
    BEGIN = r'BEGIN'
    END = r'END'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    LPAREN = r'\('
    RPAREN = r'\)'
    EQ = r'=='
    PRINT = r'PRINT'
    DO = r'DO'

    # Number token
    @_(r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)')
    def NUMBER(self, token):
        if (
                self.index
                and self.text[:token.index] != token.index * ' '
        ):
            float_value = float(token.value)
            int_value = int(float_value)
            token.value = (
                int_value
                if math.isclose(int_value, float_value)
                else float_value
            )

        else:
            if '.' not in token.value:
                token.value = int(token.value)

            else:
                dot_index = token.value.index('.')
                self.index -= len(token.value) - dot_index
                token.value = int(token.value[:dot_index])

            token.type = 'LINENO'

            if self.text[self.index:].strip(' '):
                self.begin(LineLexer)

        return token

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
    NAME['THEN'] = IF
    NAME['ELSE'] = ELSE
    NAME['BEGIN'] = BEGIN
    NAME['END'] = END
    NAME['WHILE'] = WHILE
    NAME['PRINT'] = PRINT
    NAME['DO'] = DO
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
        from main import code_output
        code_output.insert("1.0", "Illegal character '%s'" % t.value[0])
        self.index += 1


class LineLexer(Lexer):

    @_(r'.+')
    def LINE(self, token):
        self.begin(BasicLex)
        return token
    tokens = {LINE}
    ignore = ' '

