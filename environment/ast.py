from environment.error import Error
class Ast():
    def __init__(self):
        self.instructions = []
        self.console = ""
        self.errors = []

    def setConsole(self, content):
        self.console += content + "\n"
    
    def getConsole(self):
        return self.console

    def addInstructions(self, instructions):
        self.instructions += instructions
    
    def getInstructions(self):
        return self.instructions
    
    def setErrors(self,linea,columna,tipo,mensaje):
        self.errors.append(Error(linea,columna,tipo,mensaje))
        print("llego al ast")
    
    def getErrors(self):
        return self.errors