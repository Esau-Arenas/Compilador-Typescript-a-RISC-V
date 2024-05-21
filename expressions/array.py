from interfaces.instruction import Instruction
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.value import Value

class Array(Instruction):
    def __init__(self, line, col, list_exp):
        self.line = line
        self.col = col
        self.list_exp = list_exp

    def ejecutar(self, ast, env, gen):
        # Array valor
        arrVal = []
        # Recorrer el arreglo
        for exp in self.list_exp:
            indexExp = exp.ejecutar(ast, env, gen)
            arrVal.append(indexExp)
        print("entre a array")
        return Value("", arrVal, ExpressionType.ARRAY, [], [], [])

        