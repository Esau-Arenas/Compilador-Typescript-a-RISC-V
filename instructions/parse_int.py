from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.errores import agregar_error
from environment.table import getNombreVar, getId, getValueVar
from environment.value import Value

class ParseInt(Expression):
    def __init__(self, line, col, id):
        self.line = line
        self.col = col
        self.id = id

    def ejecutar(self, ast, env,gen):
        # Realizar busqueda en entorno 
        '''try:    
            valor = int(self.id.value)
            retorno = Symbol(self.line, self.col, valor, ExpressionType.INTEGER)
            print("Valor de la cadena: ", valor)
            return retorno
        except:
            print("Error en la conversion de cadena a entero")
            agregar_error("Sintactico","Error en la conversion de "+self.id+" a entero",self.line, self.col)
            return Symbol(self.line, self.col, valor, ExpressionType.NULL)'''
        
        try:
            print("entre parse int")
            valor = int(self.id.value)
            return  Value("parseInt", valor, ExpressionType.INTEGER, [], [], [])
        except:
            print("Error en la conversion de cadena a entero")
            agregar_error("Sintactico","Error en la conversion de "+self.id+" a entero",self.line, self.col)
            return Value("parseInt", valor, ExpressionType.NULL, [], [], [])