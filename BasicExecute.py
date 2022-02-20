import parser
from tkinter import *

class BasicExecute:

    def __init__(self, tree, env, n_editor, code_output):
        self.env = env
        result = self.walkTree(tree, n_editor, code_output)
        if not str(code_output.get("1.0", END)).__contains__("Error"):
            if result is None:
                pass
            elif result is not None and type(result) in [int, float]:
                n_editor.insert("1.0", result)
            elif isinstance(result, str):
                n_editor.insert("1.0", result)
            elif isinstance(result, bool):
                if result is True:
                    n_editor.insert("1.0", "True")
                else:
                    n_editor.insert("1.0", "False")

    def walkTree(self, node, n_editor, code_output):

        if isinstance(node, int):
            return node
        if isinstance(node, float):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] is None:
                self.walkTree(node[2], n_editor, code_output)
            else:
                self.walkTree(node[1], n_editor, code_output)
                self.walkTree(node[2], n_editor, code_output)
        if node[0] == 'print':
            return self.walkTree(node[1], n_editor, code_output)
        if node[0] == 'comma':
            return str(self.walkTree(node[1], n_editor, code_output))\
                   + str(self.walkTree(node[2], n_editor, code_output))
        if node[0] == 'comma1':
            return str(self.walkTree(node[1], n_editor, code_output))\
                   + str(self.walkTree(node[2], n_editor, code_output))\
                   + str(self.walkTree(node[3], n_editor, code_output))
        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1], n_editor, code_output)
            if result:
                return self.walkTree(node[2][1], n_editor, code_output)
            else:
                return self.walkTree(node[2][2], n_editor, code_output)

        if node[0] == 'if_stmt1':
            result = self.walkTree(node[1], n_editor, code_output)
            if result:
                return self.walkTree(node[2], n_editor, code_output)
        if node[0] == 'while':
            while self.walkTree(node[1], n_editor, code_output):
                self.walkTree(node[2], n_editor, code_output)

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]], n_editor, code_output)
            except LookupError:
                code_output.insert("1.0", "Undefined function '%s'" % node[1] + "\n")
                return 0
        if node[0] == 'group-expression':
            return self.walkTree(node[1], n_editor, code_output)
        elif node[0] == 'add':
            try:
                return self.walkTree(node[1], n_editor, code_output) + self.walkTree(node[2], n_editor, code_output)
            except TypeError:
                code_output.insert("1.0", "TypeError: unsupported operand type(s) for '+' found!\n")
                return 0
            except AttributeError:
                code_output.insert("1.0", "AttributeError: object has no attribute '"+node[1] + "\n")
                return 0
        elif node[0] == 'sub':
            try:
                return self.walkTree(node[1], n_editor, code_output) - self.walkTree(node[2], n_editor, code_output)
            except TypeError:
                code_output.insert("1.0", "TypeError: unsupported operand type(s) for '-' found!\n")
                return 0
            except AttributeError:
                code_output.insert("1.0", "AttributeError: object has no attribute '"+node[1] + "\n")
                return 0
        elif node[0] == 'mul':
            try:
                return self.walkTree(node[1], n_editor, code_output) * self.walkTree(node[2], n_editor, code_output)
            except TypeError:
                code_output.insert("1.0", "TypeError: unsupported operand type(s) for '*' found!\n")
                return 0
            except AttributeError:
                code_output.insert("1.0", "AttributeError: " + "object has no attribute '" + node[1] + "\n")
                return 0
        elif node[0] == 'mod':
            try:
                return self.walkTree(node[1], n_editor, code_output) % self.walkTree(node[2], n_editor, code_output)
            except TypeError:
                code_output.insert("1.0", "TypeError: unsupported operand type(s) for '%' found!\n")
                return 0
            except AttributeError:
                code_output.insert("1.0", "AttributeError: " + "object has no attribute '" + node[1] + "\n")
                return 0
        elif node[0] == 'div':
            try:
                return self.walkTree(node[1], n_editor, code_output) / self.walkTree(node[2], n_editor, code_output)
            except TypeError:
                code_output.insert("1.0", "TypeError: unsupported operand type(s) for '/' found!\n")
                return 0
            except AttributeError:
                code_output.insert("1.0", "AttributeError: " + "object has no attribute '"+node[1] + "\n")
                return 0
        elif node[0] == 'le':
            return self.walkTree(node[1], n_editor, code_output) <= self.walkTree(node[2], n_editor, code_output)
        elif node[0] == 'lt':
            return self.walkTree(node[1], n_editor, code_output) < self.walkTree(node[2], n_editor, code_output)
        elif node[0] == 'exp':
            try:
                x = 0
                xsum = 1
                while x < self.walkTree(node[2], n_editor, code_output):
                    xsum *= self.walkTree(node[1], n_editor, code_output)
                    x += 1
                return xsum
            except TypeError:
                code_output.insert("1.0", "TypeError: unsupported operand type(s) for '^' found!\n")
                return 0
            except AttributeError:
                code_output.insert("1.0", "AttributeError: " + "object has no attribute '" + node[1] + "\n")
                return 0
        elif node[0] == 'gt':
            return self.walkTree(node[1], n_editor, code_output) > self.walkTree(node[2], n_editor, code_output)
        elif node[0] == 'ge':
            return self.walkTree(node[1], n_editor, code_output) >= self.walkTree(node[2], n_editor, code_output)
        elif node[0] == 'equals':
            return self.walkTree(node[1], n_editor, code_output) == self.walkTree(node[2], n_editor, code_output)
        elif node[0] == 'ne':
            return self.walkTree(node[1], n_editor, code_output) != self.walkTree(node[2], n_editor, code_output)
        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2], n_editor, code_output)
            return node[1]
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                code_output.insert("1.0", "LookupError: Undefined variable '" + node[1] + "' found!\n")
                return 0
            except SyntaxError:
                code_output.insert("1.0", "Illegal character found at " % node[1]+"\n")
        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1], n_editor, code_output)

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count + 1, loop_limit + 1):
                    res = self.walkTree(node[2], n_editor, code_output)
                    if res is not None:
                        n_editor.insert("1.0", res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return self.walkTree(node[1], n_editor, code_output), self.walkTree(node[2], n_editor, code_output)
