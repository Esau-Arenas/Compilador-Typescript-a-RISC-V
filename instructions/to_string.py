from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.value import Value
from environment.table import getValueVar, getId
from environment.table import agregar_simbolo

class ToString(Expression):
    def __init__(self, line, col, id):
        self.line = line
        self.col = col
        self.id = id

    def ejecutar(self, ast, env, gen):
        # Realizar busqueda en entorno
        print("Buscando en entorno: ", self.id)
        try:
            valor = self.id.value
            return  Value("parseFloat", valor.intValue, ExpressionType.STRING, [], [], [])
            
        except:
            valor = self.id.ejecutar(ast, env, gen)
            valor_entrante = getValueVar(valor.value)
            print("valir: ", valor_entrante)
            if valor_entrante == 1:
                valor_entrante = "true"
            elif valor_entrante == 0:
                valor_entrante = "false"
            else:
                valor_entrante = str(valor_entrante)    

            gen.add_variable_asciz("toString", valor_entrante)
            retorno =  Value("toString", valor_entrante, "ACCESS", [], [], [])
            gen.add_la('a0', 'toString')
            agregar_simbolo("toString", "Variable", 2, env.id, self.line, self.col,2,valor_entrante)
       
            return retorno