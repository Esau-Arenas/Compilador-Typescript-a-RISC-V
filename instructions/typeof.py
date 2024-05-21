from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.table import getId
from environment.value import Value

class Typeof(Expression):
    def __init__(self, line, col, id):
        self.line = line
        self.col = col
        self.id = id

    def ejecutar(self, ast, env, gen):
        # Realizar busqueda en entorno
        tipo_val= getId(self.id)
        gen.add_type_of()
        '''sym = env.getVariable(ast, self.id)'''
        if tipo_val == 2:
            gen.add_la("a0","typeof_string")
            return  Value(str(self.id), [] , "TYPEOF", [], [], [])
        if tipo_val == 0:
            gen.add_la("a0","typeof_number")
            return  Value(str(self.id), [] , "TYPEOF", [], [], [])
        if tipo_val == 1:
            gen.add_la("a0","typeof_float")
            return  Value(str(self.id), [] , "TYPEOF", [], [], [])
        if tipo_val == 3:
            gen.add_la("a0","typeof_boolean")
            return  Value(str(self.id), [] , "TYPEOF", [], [], [])
        if tipo_val == 4:
            gen.add_la("a0","typeof_array")
            return  Value(str(self.id), [] , "TYPEOF", [], [], [])
        if tipo_val == 6:
            gen.add_la("a0","typeof_null")
            return  Value(str(self.id), [] , "TYPEOF", [], [], [])
        if tipo_val == 7:
            gen.add_la("a0","typeof_char")
            return  Value(str(self.id), [] , "TYPEOF", [], [], [])
        return None