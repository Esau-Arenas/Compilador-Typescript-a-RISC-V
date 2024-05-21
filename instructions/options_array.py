from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.errores import agregar_error
from environment.value import Value
from environment.types import ExpressionType
from environment.table import getValueVar, getPushValue, getPopValue


class OptionArray(Expression):
    def __init__(self, line, col, array, option, exp):
        self.line = line
        self.col = col
        self.array = array
        self.option = option
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        #PUSH
        if self.option =="push":
            # Traer el arreglo
            for exp in self.exp:
                indexExp = exp.ejecutar(ast, env, gen)
                getPushValue(self.array, indexExp.intValue)

        #POP
        if self.option =="pop":
            # Traer el arreglo
            val = self.array.ejecutar(ast, env, gen)
            valor_pop = getPopValue(val.value)
            gen.add_li("a0",valor_pop)
            return Value(str("pop_"+val.value), 0, "ARRAY", [], [], [])

        #LENGTH
        if self.option =="length":
            # Traer el arreglo
            val = self.array.ejecutar(ast, env, gen)
            id = getValueVar(val.value)
            tamaño = len(id)
            gen.add_li("a0",tamaño)
            return Value(str("len_"+val.value), 0, "ARRAY", [], [], [])
        
        #INDEX
        if self.option =="index":
            print("INDEX")
            encontrado = False
            x=0

            # Traer el arreglo
            val = self.array.ejecutar(ast, env, gen)
            valores = getValueVar(val.value)
            #recorrer el arreglo
            for valor in valores:
                if int(valor)==int(self.exp.value):
                    encontrado=True
                    gen.add_li("a0",x)
                    return Value(str("index_"+str(self.exp.value)), 0, "ARRAY", [], [], [])
                x+=1
                
            if not encontrado:
                gen.add_li("a0",'-1')
                return Value(str("index_"+str(self.exp.value)), 0, "ARRAY", [], [], [])
        
        #JOIN
        if self.option == "join":
            # Traer el arreglo
            sym = env.getVariable(ast, self.array.id) 
            # Validar tipo principal
            if sym.type != ExpressionType.ARRAY:
                agregar_error("Sintactico",'La variable '+self.array.id+' no es un arreglo',self.line, self.col)
                return
            # Validar indice
            cadena=""
            for valor in sym.value:
                if sym.value.index(valor)==len(sym.value)-1:
                    cadena+=str(valor.value)
                else:
                    cadena+=str(valor.value)+","
            return Symbol(line=self.line, col=self.col, value=cadena, type=ExpressionType.STRING)
