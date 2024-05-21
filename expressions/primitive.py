from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.generator import Generator
from environment.value import Value
from environment.types import ExpressionType
import struct

class Primitive(Expression):
    def __init__(self, line, col, value, type):
        self.line = line
        self.col = col
        self.value = value
        self.type = type

    def ejecutar(self, ast, env, gen):
        if(self.type == ExpressionType.INTEGER):
            temp = gen.new_temp() # 4
            gen.add_br()
            gen.add_li('t0', str(self.value))
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), self.value, self.type, [], [], [])
        elif(self.type == ExpressionType.FLOAT):
            valor = float_to_hex(self.value)
            print("valor hexa"+valor)
            temp = gen.new_temp()
            gen.add_br()
            gen.add_li('t0', str(valor))
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), valor, self.type, [], [], [])
        
        elif(self.type == ExpressionType.BOOLEAN):
            temp = gen.new_temp()
            gen.add_br()
            if(self.value):
                gen.add_li('t0', '1')
                self.value = 1
            else:
                gen.add_li('t0', '0')
                self.value = 0
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), self.value, self.type, [], [], [])
        elif(self.type == ExpressionType.STRING):
            contador = 0
            temp = gen.new_temp()
            gen.add_br()
            gen.add_li('t3', str(temp))
            for caracter in self.value:
                gen.add_li('t0', str(ord(caracter)))
                gen.add_sb('t0', '0(t3)')
                gen.add_operation('addi', 't3', 't3', '1')
                contador = contador + 1
                if contador == 4 or contador == 8:
                    tempnew = gen.new_temp()
            gen.add_li('t0', '0')
            gen.add_sb('t0', '0(t3)')
            return Value(str(temp), self.value, self.type, [], [], [])
        elif(self.type == ExpressionType.CHAR):
            temp = gen.new_temp()
            gen.add_br()
            gen.add_li('t3', str(temp))
            gen.add_li('t0', str(ord(self.value)))
            gen.add_sb('t0', '0(t3)')
            return Value(str(temp), ord(self.value), self.type, [], [], [])
            
        else:
            return None
        
def float_to_hex(f):
    #convertir float a hexadecimal
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])