from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType
from environment.environment import Environment
from environment.execute import StatementExecuter
from expressions.continue_statement import Continue
from environment.errores import agregar_error
from environment.table import agregar_simbolo

class Call(Expression):
    def __init__(self, line, col, id, params):
        self.line = line
        self.col = col
        self.id = id
        self.params = params

    def ejecutar(self, ast, env, gen):
        # Buscar la función
        func = env.getFunction(ast, self.id)
        if func == {}:
            return
        # Validar cantidad de parámetros
        if len(self.params) != len(func['params']):
            agregar_error("Sintactico",f"La función esperaba {len(func['params'])} parámetros, pero se obtuvieron {len(self.params)}",self.line, self.col)
            return Symbol(line=self.line, col=self.col, value=None, type=ExpressionType.NULL)
        # Crear entorno de funcion
        function_env = Environment(env.getGlobalEnvironment(), 'FUNCTION_'+self.id)
        # Validar parámetros
        if len(self.params) > 0:
            symbolList = []
            # Lista de parámetros
            for i in range(len(self.params)):
                # Obteniendo simbolo del parámetro
                symParam = self.params[i].ejecutar(ast, env, gen)
                print(symParam)
                symbolList.append(symParam)
                # Guardando valores de funcion
                print("Parametro: ",list(func['params'][i].keys())[0],func['params'][i].values())
                
                id_param = list(func['params'][i].keys())[0]
                type_param = list(func['params'][i].values())[0]
                print("id_param: ",id_param)
                print("type_param: ",type_param)
                # Validando tipos
                if type_param != symParam.type:
                    agregar_error("Sintactico","Los tipos de parámetros son incorrectos",self.line, self.col)
                    return Symbol(line=self.line, col=self.col, value=None, type=ExpressionType.NULL)
                # Agregar parámetros al entorno
                gen.add_variable_word(str(id_param),0)
                agregar_simbolo(str(id_param) , "Variable", type_param.value, env.id, self.line, self.col, type_param.value,0)
                #function_env.saveVariable(ast, id_param, symParam)

        # Ejecutar bloque
        returnValue = StatementExecuter(func['block'], ast, function_env, gen)
        if returnValue != None:
            if returnValue.type != func['type']:
                agregar_error("Semantico","El tipo de retorno: "+returnValue.value+" es incorrecto",self.line, self.col)
                return Symbol(line=self.line, col=self.col, value=None, type=ExpressionType.NULL)  
            return returnValue        
        return None

