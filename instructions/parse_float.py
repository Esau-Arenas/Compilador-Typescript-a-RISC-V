from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.errores import agregar_error
from environment.value import Value
import struct

class ParseFloat(Expression):
    def __init__(self, line, col, id):
        self.line = line
        self.col = col
        self.id = id

    def ejecutar(self, ast, env, gen):
        # Realizar busqueda en entorno 
        try:
            valor = float(self.id.value)
            valorhexa = float_to_hex(valor)
            return  Value("parseFloat", valorhexa, ExpressionType.FLOAT, [], [], [])
        except:
            print("Error en la conversion de cadena a entero")
            agregar_error("Sintactico","Error en la conversion de "+self.id+" a entero",self.line, self.col)
            return Value("parseFloat", valorhexa, ExpressionType.NULL, [], [], [])
    
def float_to_hex(f):
     #convertir float a hexadecimal
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])