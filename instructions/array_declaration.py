from interfaces.instruction import Instruction
from environment.types import ExpressionType
from environment.errores import agregar_error
from environment.table import agregar_simbolo

class ArrayDeclaration(Instruction):
    def __init__(self, line, col, id, type, exp, tipo_variable):
        self.line = line
        self.col = col
        self.id = id
        self.type = type
        self.exp = exp
        self.tipo_variable = tipo_variable

    def ejecutar(self, ast, env, gen):
        # Obtener simbolo
        result = self.exp.ejecutar(ast, env, gen)

        
        # Validar tipo principal
        if result.type != ExpressionType.ARRAY:
            agregar_error("Sintactico",'La expresión no es un arreglo',self.line, self.col)
            return
        # Validar tipos
        for res in result.value:
            if res.type != self.type:
                agregar_error("Semantico",'El arreglo contiene tipos incorrectos',self.line, self.col)
                return
        # Agregar al entorno
        #env.saveVariable(ast, self.id, result)
        # Agregar a la tabla de simbolos'''
        valores_array = []
        for res in result.intValue:
            valores_array.append(str(res.intValue))
        
        #agregando valores en el .data
        valor_array = ",".join(valores_array)
        gen.add_variable_word(self.id, valor_array)
        #agregando cols
        gen.add_variable_word(self.id+"_cols", len(valores_array))

        print("tipo declaracion: ",result.type.value)
        
        agregar_simbolo(self.id, "Variable", result.type.value, env.id, self.line, self.col, self.tipo_variable,valores_array)