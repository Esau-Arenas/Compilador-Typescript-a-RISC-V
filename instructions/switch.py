from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue

class Switch(Instruction):
    def __init__(self, line, col, exp, block_case):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block_case

    def ejecutar(self, ast, env, gen):
        validate = self.exp.ejecutar(ast, env, gen)
        final = gen.new_fin()

        for block in self.block:
            if block.exp != "default":
                gen.add_lw("t1", validate.value)
                gen.add_li("t2", block.exp.value)
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation("beq","t1", "t2", case)
                gen.add_jump(case2)
                gen.add_code(f"{case}: \n")
                switch_env = Environment(env, "SWITCH")
                returnValue = StatementExecuter(block.block, ast, switch_env, gen)
                gen.add_jump(final)
                gen.add_code(f"{case2}: \n")

            if block.exp == "default":
                gen.add_jump("default\n")
                gen.add_code(f"default: \n")
                switch_env = Environment(env, "SWITCH")
                returnValue = StatementExecuter(block.block, ast, switch_env, gen)
                gen.add_code(f"{final}: \n")
                    
            #for case in cases:
             #   gen.add_code(f"{case}: \n")