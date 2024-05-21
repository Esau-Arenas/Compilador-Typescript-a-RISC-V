from interfaces.instruction import Instruction
from environment.ast import Ast
from environment.errores import agregar_error
from environment.table import agregar_simbolo

class MatrixDeclaration(Instruction):
    def __init__(self, line, col, id, type, matrix_exp, tipo_variable):
        self.line = line
        self.col = col
        self.id = id
        self.type = type
        self.matrix_exp = matrix_exp
        self.tipo_variable = tipo_variable

    def ejecutar(self, ast, env):
        # Crear la matriz
        dimension = obtener_dimen(self.matrix_exp)
        #DECLARACION DE MATRIZ DE UNA DIMENSION
        if dimension == 1:
            matrix = []
            #Recorrer el arreglo y agregarlo a la lista matrix
            for exp in self.matrix_exp:
                indexExp = exp.ejecutar(ast,env)
                matrix.append(indexExp) 
            # Agregar al entorno
            env.saveVariable(ast, self.id, matrix)
            if self.tipo_variable == "var":
                agregar_simbolo(self.id, "Variable", 8, env.id, self.line, self.col,self.tipo_variable)
            else:
                agregar_simbolo(self.id, "Constante", 8, env.id, self.line, self.col,self.tipo_variable)
        elif dimension == 2:
            matrix = []
            for row in self.matrix_exp:
                matrix_row = []
                for exp in row:
                    value = exp.ejecutar(ast, env)
                    matrix_row.append(value)
                matrix.append(matrix_row)
            # Agregar al entorno
            env.saveVariable(ast, self.id, matrix)
            if self.tipo_variable == "var":
                agregar_simbolo(self.id, "Variable", 8, env.id, self.line, self.col,self.tipo_variable)
            else:
                agregar_simbolo(self.id, "Constante", 8, env.id, self.line, self.col,self.tipo_variable)
        #DECLARACION DE MATRIZ DE TRES DIMENSIONES
        elif dimension == 3:
            matrix = []
            for matrix2d in self.matrix_exp:
                matrix_row = []
                for row in matrix2d:
                    matrix_col = []
                    for exp in row:
                        value = exp.ejecutar(ast, env)
                        matrix_col.append(value)
                    matrix_row.append(matrix_col)
                matrix.append(matrix_row)
            # Agregar al entorno
            env.saveVariable(ast, self.id, matrix)
        #DECLARACION DE MATRIZ DE CUATRO DIMENSIONES
        elif dimension == 4:
            matrix = []
            for matrix3d in self.matrix_exp:
                matrix_layer = []
                for matrix2d in matrix3d:
                    matrix_row = []
                    for row in matrix2d:
                        matrix_col = []
                        for exp in row:
                            value = exp.ejecutar(ast, env)
                            matrix_col.append(value)
                        matrix_row.append(matrix_col)
                    matrix_layer.append(matrix_row)
                matrix.append(matrix_layer)
            env.saveVariable(ast, self.id, matrix)
            if self.tipo_variable == "var":
                agregar_simbolo(self.id, "Variable", 8, env.id, self.line, self.col,self.tipo_variable)
            else:
                agregar_simbolo(self.id, "Constante", 8, env.id, self.line, self.col,self.tipo_variable)
        #DECLARACION DE MATRIZ DE CINCO DIMENSIONES
        elif dimension == 5:
            matrix = []
            for matrix4d in self.matrix_exp:
                matrix_layer = []
                for matrix3d in matrix4d:
                    matrix_cube = []
                    for matrix2d in matrix3d:
                        matrix_row = []
                        for row in matrix2d:
                            matrix_col = []
                            for exp in row:
                                value = exp.ejecutar(ast, env)
                                matrix_col.append(value)
                            matrix_row.append(matrix_col)
                        matrix_cube.append(matrix_row)
                    matrix_layer.append(matrix_cube)
                matrix.append(matrix_layer)
            env.saveVariable(ast, self.id, matrix)
            if self.tipo_variable == "var":
                agregar_simbolo(self.id, "Variable", 8, env.id, self.line, self.col,self.tipo_variable)
            else:
                agregar_simbolo(self.id, "Constante", 8, env.id, self.line, self.col,self.tipo_variable)
        else:
            agregar_error("Semantico","Cantidad de dimesiones superado",self.line, self.col)

#obtener dimesiones de la matriz
def obtener_dimen(lista):
    if not isinstance(lista, list):
        return 0
    return 1 + obtener_dimen(lista[0])