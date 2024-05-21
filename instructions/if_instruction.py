from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue

class If(Instruction):
    def __init__(self, line, col, exp, block, else_block):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block
        self.else_block = else_block

    def ejecutar(self, ast, env, gen):
        # Obtener simbolo
        validate = self.exp.ejecutar(ast, env, gen)
        print(validate.intValue)

        exit = gen.new_fin()
        true = gen.new_label()
        false = gen.new_label()
        gen.add_li('t1', '1')
        gen.add_li('t2', validate.intValue)
        print("valor del inmediato: ",validate.intValue)
        gen.add_operation('beq', 't1', 't2', true)
        gen.add_jump(false)

        # Entorno True
        gen.add_code(f"{true}: \n")
        if_env = Environment(env, "IF")
        returnValue = StatementExecuter(self.block, ast, if_env, gen)
        gen.add_jump(exit)

        # Entorno False
        gen.add_code(f"{false}: \n")
        if_env = Environment(env, "IF")
        returnValue = StatementExecuter(self.else_block, ast, if_env, gen)
        gen.add_jump(exit)

        # Etiqueta de salida
        gen.add_code(f"{exit}: \n")


        # Evaluar
        '''if validate.value:
            # Crear entorno del If
            if_env = Environment(env, "IF")
            returnValue = StatementExecuter(self.block, ast, if_env, gen)
            if returnValue != None:
                return returnValue
        else:
            if_env = Environment(env, "IF")
            returnValue = StatementExecuter(self.else_block, ast, if_env, gen)
            if returnValue != None:
                return returnValue
        return None'''
