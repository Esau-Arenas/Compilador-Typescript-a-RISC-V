from interfaces.instruction import Instruction
from environment.ast import Ast
from environment.errores import agregar_error
from environment.table import agregar_simbolo
from environment.types import ExpressionType
from environment.table import getValueVar, getId


class Declaration(Instruction):
    def __init__(self, line, col, id, type, exp, tipo_variable):
        self.line = line
        self.col = col
        self.id = id
        self.type = type
        self.exp = exp
        self.tipo_variable = tipo_variable

    def ejecutar(self, ast, env, gen):
        # Obtener value
        result = self.exp.ejecutar(ast, env, gen)
        print("resultado: ",result) 
        print("tipo: ",result.type)
        
        # Validar tipo
        if result.type != self.type:
            if result.type != "ACCESS":
                agregar_error("Semantico","El tipo de dato para "+self.id+" no es correcto",self.line, self.col)
                return
        
        if result.type == ExpressionType.INTEGER:
            gen.add_variable_word(self.id, result.intValue)
        elif result.type == ExpressionType.FLOAT:
            gen.add_variable_word(self.id, result.intValue)
        elif result.type == ExpressionType.BOOLEAN:
            gen.add_variable_word(self.id, result.intValue)
        elif result.type == ExpressionType.STRING:
            gen.add_variable_asciz(self.id, result.intValue)
        elif result.type == ExpressionType.CHAR:
            gen.add_variable_byte(self.id, result.intValue)
        elif result.type == "ACCESS":
            valor= getValueVar(result.value)
            tipo_val= getId(result.value)
            if tipo_val == 0 or tipo_val == 3:
                gen.add_variable_word(self.id, valor)
            elif tipo_val == 2:
                gen.add_variable_asciz(self.id, valor)
        else:
            agregar_error("Semantico","El tipo de dato para "+self.id+" no es correcto",self.line, self.col)
            return
        
        #Manejo de tabla
        if self.tipo_variable == "var":
            agregar_simbolo(self.id, "Variable", self.type.value, env.id, self.line, self.col,self.tipo_variable,result.intValue)
        else:
            agregar_simbolo(self.id, "Constante", self.type.value, env.id, self.line, self.col,self.tipo_variable,result.intValue)
       