from interfaces.expression import Expression

class Ternario(Expression):
    def __init__(self, line, col, exp1, exp2, exp3):
        self.line = line
        self.col = col
        self.exp1 = exp1
        self.exp2 = exp2
        self.exp3 = exp3

    def ejecutar(self, ast, env):
        # Obtencion de valores
        condition = self.exp1.ejecutar(ast, env)
        # Comprobación
        if condition.value:
            return self.exp2.ejecutar(ast, env)
        return self.exp3.ejecutar(ast, env)
        


