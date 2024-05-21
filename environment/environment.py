from environment.symbol import Symbol
from environment.types import ExpressionType
from environment.errores import agregar_error

class Environment():
    def __init__(self, previous, id):
        self.previous = previous
        self.id = id
        self.tabla = {}
        self.interfaces = {}
        self.functions = {}

    def saveVariable(self, ast, id, symbol):
        if id in self.tabla:
            agregar_error("Semantico",'La variable: '+id+" ya existe",0,0)
            return
        self.tabla[id] = symbol

    def getVariable(self, ast, id):
        tmpEnv = self
        while True:
            if id in tmpEnv.tabla:
                return tmpEnv.tabla[id]
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        agregar_error("Semantico",'La variable: '+id+" no existe",0,0)
        return Symbol(0, 0, None, ExpressionType.NULL)

    def setVariable(self, ast, id, symbol):
        tmpEnv = self
        while True:
            if id in tmpEnv.tabla:
                tmpEnv.tabla[id] = symbol
                return symbol
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        agregar_error("Semantico",'La variable: '+id+" no existe",0,0)
        return Symbol(0, 0, None, ExpressionType.NULL)
    
    def saveFunction(self, ast, id, function):
        if id in self.functions:
            agregar_error("Semantico",'Ya existe una funcion con el nombre: '+id,0,0)
            return
        self.functions[id] = function

    def getFunction(self, ast, id):
        tmpEnv = self
        while True:
            if id in tmpEnv.functions:
                return tmpEnv.functions[id]
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        agregar_error("Semantico",'La funcion: '+id+" no existe",0,0)
        return {}

    def saveStruct(self, ast, id, struct):
        if id in self.interfaces:
            agregar_error("Semantico",'Ya existe una interface con el nombre: '+id,0,0)
            return
        self.interfaces[id] = struct
    
    def getStruct(self, ast, id):
        tmpEnv = self
        while True:
            if id in tmpEnv.interfaces:
                return tmpEnv.interfaces[id]
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        agregar_error("Semantico",'La interfaz: '+id+" no existe",0,0)
        return None

    def LoopValidation(self):
        tmpEnv = self
        while True:
            if tmpEnv.id == 'WHILE' or tmpEnv.id == 'FOR':
                return True
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        return False
    
    def FunctionValidation(self):
        tmpEnv = self
        while True:
            if 'FUNCTION_' in tmpEnv.id:
                return True
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        return False
    
    def getGlobalEnvironment(self):
        tmpEnv = self
        while True:
            if tmpEnv.previous == None:
                return tmpEnv
            else:
                tmpEnv = tmpEnv.previous

    def getEnvironment(self, id):
        tmpEnv = self
        while True:
            if tmpEnv.id == id:
                return tmpEnv
            else:
                tmpEnv = tmpEnv.previous
