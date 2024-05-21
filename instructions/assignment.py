from interfaces.instruction import Instruction
from environment.table import extraer_datos_tabla
from environment.errores import agregar_error

class Assignment(Instruction):
    def __init__(self, line, col, id, exp):
        self.line = line
        self.col = col
        self.id = id
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        # Obtener simbolo
        result = self.exp.ejecutar(ast, env, gen)
        # Validar si existe
        Tablasym = extraer_datos_tabla()
        for Tsym in Tablasym:
            if Tsym[0] == self.id:
                if Tsym[6] == "var":
                    # Editar simbolo
                    print("valor: ", result.intValue)
                    gen.add_lw("a0",self.id)
                    gen.add_li('t3', result.value)
                    gen.add_lw('a0', '0(t3)')
                    gen.add_la('t0',self.id)
                    gen.add_sw('a0', '0(t0)')   
                    gen.add_br()
                    #env.setVariable(ast, self.id, result)
                else:
                    agregar_error("Semantico",'No se puede modificar una constante',self.line, self.col)
        
        