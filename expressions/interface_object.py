from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.errores import agregar_error


class InterfaceObject(Expression):
    def __init__(self, line, col, id, option):
        self.line = line
        self.col = col
        self.id = id
        self.option = option

    def ejecutar(self, ast, env):
        retorno = []
        if self.option == "keys":
            # Obtener el simbolo/entorno de la interfaz
            envInterface = self.id.ejecutar(ast, env)
            for key in envInterface.tabla:
                retorno.append(Symbol(self.line, self.col, key, ExpressionType.STRING))
            return Symbol(self.line, self.col, retorno, ExpressionType.ARRAY)
        if self.option == "values":
            # Obtener el simbolo/entorno de la interfaz
            envInterface = self.id.ejecutar(ast, env)
            valores = envInterface.tabla.values()
            return Symbol(self.line, self.col, valores, ExpressionType.ARRAY)
        return Symbol(self.line, self.col, None, ExpressionType.NULL)