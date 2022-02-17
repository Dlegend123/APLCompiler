import re


class BasicExecute:

    def __init__(self, tree, env, code_output, x, t):
        self.env = env
        self.walkTree(tree, code_output)

    def walkTree(self, node, code_output):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] is None:
                self.walkTree(node[2], code_output)
            else:
                self.walkTree(node[1], code_output)
                self.walkTree(node[2], code_output)

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1], code_output)
            if result:
                return self.walkTree(node[2][1], code_output)
            else:
                return self.walkTree(node[2][2], code_output)
        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]], code_output)
            except LookupError:
                code_output.insert("1.0", "Undefined function '%s'" % node[1])

        if node[0] == 'add':
            return self.walkTree(node[1], code_output) + self.walkTree(node[2], code_output)
        elif node[0] == 'sub':
            return self.walkTree(node[1], code_output) - self.walkTree(node[2], code_output)
        elif node[0] == 'mul':
            return self.walkTree(node[1], code_output) * self.walkTree(node[2], code_output)
        elif node[0] == 'div':
            return self.walkTree(node[1], code_output) / self.walkTree(node[2], code_output)
        elif node[0] == 'comma':
            return self.walkTree(node[1], code_output), self.walkTree(node[2], code_output)
        elif node[0] == 'le':
            return self.walkTree(node[1], code_output) <= self.walkTree(node[2], code_output)
        elif node[0] == 'lt':
            return self.walkTree(node[1], code_output) < self.walkTree(node[2], code_output)
        elif node[0] == 'exp':
            x = 0
            xsum = 1
            while x < self.walkTree(node[2], code_output):
                xsum *= self.walkTree(node[1], code_output)
                x += 1
            return xsum
        elif node[0] == 'gt':
            return self.walkTree(node[1], code_output) > self.walkTree(node[2], code_output)
        elif node[0] == 'ge':
            return self.walkTree(node[1], code_output) >= self.walkTree(node[2], code_output)
        elif node[0] == 'equals':
            return self.walkTree(node[1], code_output) == self.walkTree(node[2], code_output)
        elif node[0] == 'ne':
            return self.walkTree(node[1], code_output) != self.walkTree(node[2], code_output)
        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2], code_output)
            return node[1]

        if node[0] == 'var':
            try:
                code_output.insert("1.0", self.env[node[1]])
                return self.env[node[1]]
            except LookupError:
                code_output.insert("1.0", "Undefined variable '" + node[1] + "' found!")
        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1], code_output)

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count + 1, loop_limit + 1):
                    res = self.walkTree(node[2], code_output)
                    if res is not None:
                        return res
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return self.walkTree(node[1], code_output), self.walkTree(node[2], code_output)
