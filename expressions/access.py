from interfaces.expression import Expression
from environment.value import Value
from environment.table import getId,getValueVar
from environment.errores import agregar_error

class Access(Expression):
    def __init__(self, line, col, id):
        self.line = line
        self.col = col
        self.id = id

    def ejecutar(self, ast, env, gen):
        #Obtener el tipo de la variable
        tipo = getId(self.id)

        #Retornar el valor de la variable dependiendo del tipo de dato
        if tipo == 0 or tipo == 1 or tipo == 3:
            gen.add_lw("a0",self.id)
            return  Value(str(self.id), [] , "ACCESS", [], [], [])
        if tipo == 2:
            gen.add_la("a0",self.id)
            return  Value(str(self.id), [] , "ACCESS", [], [], [])
        if tipo == 4:
            valores = getValueVar(self.id)
            return  Value(str(self.id), valores , "ACCESS_ARRAY", [], [], [])
        else:
            agregar_error("Semantico", "No se encontro la variable: "+self.id, self.line, self.col)
            return
