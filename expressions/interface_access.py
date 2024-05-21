from interfaces.expression import Expression
from environment.environment import Environment

class InterfaceAccess(Expression):
    def __init__(self, line, col, exp, id):
        self.line = line
        self.col = col
        self.exp = exp
        self.id = id

    def ejecutar(self, ast, env):
        # Obtener el simbolo/entorno de la interfaz
        envInterface = self.exp.ejecutar(ast, env)
        # Retornar busqueda de atributo
        sym = envInterface.getVariable(ast, self.id)
        return sym