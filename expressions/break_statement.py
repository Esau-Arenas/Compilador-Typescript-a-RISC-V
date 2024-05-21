from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType
from environment.errores import agregar_error

class Break(Expression):
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def ejecutar(self, ast, env, gen):
        if env.LoopValidation():
            return Symbol(line=self.line, col=self.col, value=None, type=ExpressionType.BREAK)
        agregar_error("Sintactico","La sentencia de transferencia 'Break' no se encuentra dentro de un ciclo",self.line, self.col)
        return Symbol(line=self.line, col=self.col, value=None, type=ExpressionType.NULL)
