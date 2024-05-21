from interfaces.instruction import Instruction
from environment.types import ExpressionType
from environment.table import getId

class Print(Instruction):
    def __init__(self, line, col, Exp):
        self.line = line
        self.col = col
        self.Exp = Exp

    def ejecutar(self, ast, env, gen):
        for exp in self.Exp:
            val = exp.ejecutar(ast, env, gen)

            #Validación del tipo de dato a imprimir

            if val.type == ExpressionType.INTEGER:
                gen.add_br()
                gen.add_li('t3', str(val.value))
                gen.add_lw('a0', '0(t3)')
                gen.add_li('a7', '1')
                gen.add_system_call()

            elif val.type == ExpressionType.FLOAT:
                gen.add_li('a7', '34')
                gen.add_system_call()
            
            if val.type == ExpressionType.BOOLEAN:
                # Imprimiendo expresion
                #print("entro a boolean")
                gen.add_br()
                gen.add_li('t3', str(val.value))
                gen.add_lw('a0', '0(t3)')
                gen.add_li('a7', '1')
                gen.add_system_call()

            elif val.type == ExpressionType.STRING:
                gen.add_br()
                gen.add_li('t3', str(val.value))
                for caracter in val.intValue:
                    gen.add_lw('a0', '0(t3)')
                    gen.add_li('a7', '11')
                    gen.add_system_call()
                    gen.add_operation('addi', 't3', 't3', '1')
                
            elif val.type == "ACCESS":
                tipo_val= getId(val.value)
                if tipo_val == 0 or tipo_val == 3:
                    gen.add_li('a7', '1')
                    gen.add_system_call()
                elif tipo_val == 1:
                    gen.add_li('a7', '34')
                    gen.add_system_call()
                elif tipo_val == 2:
                    gen.add_li('a7', '4')
                    gen.add_system_call()

            elif val.type == "TYPEOF":
                gen.add_li('a7', '4')
                gen.add_system_call()

            elif val.type == "ACCESS_ARRAY":
                valores = val.intValue
                for valor in valores:
                    gen.add_li('a0', str(valor))
                    gen.add_li('a7', '1')
                    gen.add_system_call()
                    gen.add_li('a0', '44')
                    gen.add_li('a7', '11')
                    gen.add_system_call()
            
            elif val.type == "ARRAY":
                print("entro a caso array")
                gen.add_li('a7', '1')
                gen.add_system_call()
                
            else:
                print("no entro a caso")
                

            # Imprimiendo salto de linea
            gen.add_br()
            gen.add_li('a0', '10')
            gen.add_li('a7', '11')
            gen.add_system_call()

            #print(val.type)
            

        return None