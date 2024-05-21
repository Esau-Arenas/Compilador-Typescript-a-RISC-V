from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType
from environment.errores import agregar_error

class Return(Expression):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        if env.FunctionValidation():
            if self.exp == None:
                return Symbol(line=self.line, col=self.col, value=None, type=ExpressionType.RETURN)
            sym = self.exp.ejecutar(ast, env, gen)
            return Symbol(line=self.line, col=self.col, value=sym, type=ExpressionType.RETURN)
        agregar_error("Semantico","La sentencia de transferencia Return no se encuentra dentro de una función",self.line, self.col)
        return Symbol(line=self.line, col=self.col, value=None, type=ExpressionType.NULL)