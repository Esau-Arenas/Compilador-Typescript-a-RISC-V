from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.execute import StatementExecuter
from environment.types import ExpressionType
from expressions.continue_statement import Continue
from environment.errores import agregar_error

class While(Instruction):
    def __init__(self, line, col, exp, block):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block

    def ejecutar(self, ast, env, gen):
        #generar etiquetas
        true = gen.new_label()
        continuar = gen.new_label()
        exit = gen.new_fin()

        #validar condicion
        gen.add_br()
        gen.add_code(f"{true}: \n")
        validate = self.exp.ejecutar(ast, env, gen)

        #evaluar si cumple la condicion
        gen.add_li('t1', '1')
        gen.add_li('t3', validate.value)
        gen.add_lw('t2', '0(t3)')
        gen.add_operation('beq', 't1', 't2', continuar) 
        gen.add_jump(exit)

        #entorno while
        gen.add_code(f"{continuar}: \n")
        while_env = Environment(env, "WHILE")
        Flag = StatementExecuter(self.block, ast, while_env, gen)
        gen.add_jump(true)

        #etiqueta de salida
        gen.add_code(f"{exit}: \n")
