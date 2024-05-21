from interfaces.instruction import Instruction

class Interface(Instruction):
    def __init__(self, line, col, id, attr):
        self.line = line
        self.col = col
        self.id = id
        self.attr = attr

    def ejecutar(self, ast, env):
        # Se guarda el struct en un diccionario
        ## El id es el nombre llave
        ## El valor es la lista de atributos que consta de diccionarios
        env.saveStruct(ast, self.id, self.attr)