from interfaces.expression import Expression
from environment.value import Value
from environment.table import getId,getValueVar

class Access(Expression):
    def __init__(self, line, col, id):
        self.line = line
        self.col = col
        self.id = id

    def ejecutar(self, ast, env, gen):
        #Obtener el tipo de la variable
        print("ID: ",self.id)
        tipo = getId(self.id)
        print("Tipo acceso: ",tipo)

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
            print("No se encontro la variable")
            return
        #text +='\t'+'la t0, '+p[1]+'\n'
        # Realizar busqueda en entorno
        #sym = env.getVariable(ast, self.id)
        #return sym
