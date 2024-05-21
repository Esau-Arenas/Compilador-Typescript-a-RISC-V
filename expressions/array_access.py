from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.errores import agregar_error
from environment.value import Value
from environment.table import getValueVar


class ArrayAccess(Expression):
    def __init__(self, line, col, array, index):
        self.line = line
        self.col = col
        self.array = array
        self.index = index

    def ejecutar(self, ast, env, gen):
        # Traer el arreglo
        sym = self.array.ejecutar(ast, env, gen)
        print("Tipo: ",sym.type)
        
        #Obtener los valores del arreglo
        valores = getValueVar(sym.value)
        
        # Traer el indice
        indexVal = self.index.ejecutar(ast, env, gen)
        try:
            valor_retorno= valores[indexVal.intValue]
            print(valor_retorno)
            
            #Accediendo al indice
            temp = gen.new_temp() # 4
            gen.add_br()
            gen.add_li('t0', str(valor_retorno))
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')

            
            return  Value(str(temp), int(valor_retorno) , ExpressionType.INTEGER, [], [], [])
    
        except:
            agregar_error("Semantico", "No se encontró indice del arreglo: "+sym.value, self.line, self.col)
            
