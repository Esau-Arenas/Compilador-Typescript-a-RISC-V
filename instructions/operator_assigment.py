from interfaces.instruction import Instruction

class OperatorAssignment(Instruction):
    def __init__(self, line, col, id, op, exp):
        self.line = line
        self.col = col
        self.id = id
        self.op = op
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        #OBTENER EL VALOR DE LA VARIABLE
        gen.add_lw("a0",self.id)

        #MAS IGUAL
        if self.op == "+":
            gen.add_operation("addi","a0","a0",self.exp.value)
            gen.add_la('t0',self.id)
            gen.add_sw('a0', '0(t0)')
            
        #MENOS IGUAL
        if self.op == "-":
            gen.add_li('t1',self.exp.value)
            gen.add_operation("sub","a0","a0","t1")
            gen.add_la('t0',self.id)
            gen.add_sw('a0', '0(t0)')
           