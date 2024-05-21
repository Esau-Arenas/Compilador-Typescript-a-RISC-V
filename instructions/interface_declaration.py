from interfaces.instruction import Instruction
from environment.environment import Environment

class InterfaceDeclaration(Instruction):
    def __init__(self, line, col, id1, id2, content):
        self.line = line
        self.col = col
        self.id1 = id1
        self.id2 = id2
        self.content = content

    def ejecutar(self, ast, env):
        # Obtener Interface
        interfaceValue = env.getStruct(ast, self.id2)
        # Validar valor
        if interfaceValue == None:
            return
        # Crear entorno interface
        newEnv = Environment(None, 'INTERFACE_'+self.id1)
        # Validar expresiones
        for i in range(len(self.content)):
            # Guardando valores de interface
            id_param = list(interfaceValue[i].keys())[0]
            type_param = list(interfaceValue[i].values())[0]
            # Guardando valores de expresiones
            id_exp = list(self.content[i].keys())[0]
            valExp = list(self.content[i].values())[0].ejecutar(ast, env)
            # Validar tipos
            if type_param == valExp.type and id_param == id_exp:
                ## Se guarda una nueva variable con el nombre de la interfaz
                ## como valor se guarda un entorno con las variables guardadas
                newEnv.saveVariable(ast, id_param, valExp)
            else:
                ast.setErrors('El tipo o identificador de la interfaz es incorrecto')
                return None
        # Guardar variable
        env.saveVariable(ast, self.id1, newEnv)