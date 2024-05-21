from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from environment.symbol import Symbol
from expressions.continue_statement import Continue
from environment.types import ExpressionType

class For(Instruction):
    def __init__(self, line, col, variable, exp, asignacion, block):
        self.line = line
        self.col = col
        self.exp = exp
        self.variable = variable
        self.asignacion = asignacion
        self.block = block
        
    def ejecutar(self, ast, env, gen):

        true = gen.new_label()
        false = gen.new_label()
        exit = gen.new_fin()

        print("Ejecutando FOR")
        print("variable: ", self.variable)
        print("exp: ", self.exp)
        print("asignacion: ", self.asignacion[0])
        print("block: ", self.block)
        for_env = Environment(env, "FOR")
        result = self.variable.ejecutar(ast, for_env, gen)
        #for_env.guardar_variable(self.variable, self.asignacion.ejecutar(ast, env))
        Flag = self.exp.ejecutar(ast, for_env)

        condicion = self.asignacion[0]

        while Flag.value:
            Flag2 = StatementExecuter(self.block, ast, for_env, gen)
            # Validar si es sentencia de transferencia
            if Flag2 != None:
                if Flag2.type == ExpressionType.BREAK:
                    break
                if Flag2.type == ExpressionType.CONTINUE:
                    continue
                if Flag2.type == ExpressionType.RETURN:
                    return Flag2
            if condicion[1] == "+":
                sym = for_env.getVariable(ast, condicion[0])
                for_env.setVariable(ast, condicion[0], Symbol(self.line, self.col, sym.value + 1, sym.type))
            elif condicion[1] == "-":
                sym = for_env.getVariable(ast, condicion[0])
                for_env.setVariable(ast, condicion[0], Symbol(self.line, self.col, sym.value - 1, sym.type))

            Flag = self.exp.ejecutar(ast, for_env)
            print("Flag: ", Flag.value)
