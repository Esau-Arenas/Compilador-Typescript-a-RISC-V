from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.errores import agregar_error
from environment.table import getNombreVar, getId, getValueVar
from environment.value import Value

class Lower(Expression):
    def __init__(self, line, col, id):
        self.line = line
        self.col = col
        self.id = id

    def ejecutar(self, ast, env, gen):
        # Realizar busqueda en entorno
        id_tabla= getNombreVar(self.id)
        tipo_val= getId(self.id)
        #sym = env.getVariable(ast, self.id)
        if tipo_val != 2:
            agregar_error("Sintactico","El tipo de dato no es correcto para Lower",self.line, self.col)
            return
        if tipo_val == 2:
            #gen.add_lw("a0",self.id)
            valor_obtenido=getValueVar(self.id)
            valor = valor_obtenido.lower()
            return  Value(self.id, valor, ExpressionType.STRING, [], [], [])
