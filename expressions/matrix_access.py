from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.errores import agregar_error
from environment.symbol import Symbol

class MatrixAccess(Expression):
    def __init__(self, line, col, matrix, indices):
        self.line = line
        self.col = col
        self.matrix = matrix
        self.indices = indices

    def ejecutar(self, ast, env):
        # Traer la lista matrix del entorno 
        matriz = self.matrix.ejecutar(ast, env)
        listamatrix = obtener_listaprimitiva(matriz)
        
        listaindices = []
        #Recorrer el arreglo y agregarlo a la lista matrix
        for exp in self.indices:
            indexExp = exp.ejecutar(ast,env)
            listaindices.append(indexExp) 
            print(listaindices)
        # LA LISTA VALUES ES PARA OBTENER EL VALOR O VALORES DE LOS INDICES A LOS QUE SE QUIERE ACCEDER.
        values = []
        # Iterar sobre cada Symbol y obtener el valor
        for symbol in listaindices:
            # Acceder al atributo 'value' de cada Symbol
            values.append(symbol.value)
        print(values)

        if listamatrix:
            for index in values:
                listamatrix = listamatrix[index]
            print(listamatrix)
        return Symbol(self.line, self.col, listamatrix, ExpressionType.INTEGER)


#FUNCION AUXILIAR PARA OBTENER DIMENSIONES DE LA MATRIZ
def obtener_dimensiones(lista):
    if not isinstance(lista, list):
        return 0
    return 1 + obtener_dimensiones(lista[0])

#FUNCION AUXILIAR PARA DEVOLVER UNA LISTA MATRIZ PRIMITIVA DE PYTHON
def obtener_listaprimitiva(matriz):
        #Obtener la dimension de la matriz
        dimension = obtener_dimensiones(matriz)
        print(dimension)
        #DECLARACION DE MATRIZ DE UNA DIMENSION
        if dimension == 1:
            listamatrix = []
            #Recorrer el arreglo y agregarlo a la lista matrix
            for symbol in matriz:
                listamatrix.append(symbol.value) 
            print(listamatrix)
            return listamatrix
        elif dimension == 2:
            listamatrix = []
            for row in matriz:
                matrix_row = []
                for exp in row:
                    matrix_row.append(exp.value)
                listamatrix.append(matrix_row)
                print(listamatrix)
            return listamatrix
        elif dimension == 3:
            listamatrix = []
            for matrix2d in matriz:
                matrix_row = []
                for row in matrix2d:
                    matrix_col = []
                    for exp in row:
                        matrix_col.append(exp.value)
                    matrix_row.append(matrix_col)
                listamatrix.append(matrix_row)
            return listamatrix
        elif dimension == 4:
            listamatrix = []
            for matrix3d in matriz:
                matrix_layer = []
                for matrix2d in matrix3d:
                    matrix_row = []
                    for row in matrix2d:
                        matrix_col = []
                        for exp in row:
                            matrix_col.append(exp.value)
                        matrix_row.append(matrix_col)
                    matrix_layer.append(matrix_row)
                listamatrix.append(matrix_layer)
            return listamatrix
        elif dimension == 5:
            listamatrix = []
            for matrix4d in matriz:
                matrix_layer = []
                for matrix3d in matrix4d:
                    matrix_cube = []
                    for matrix2d in matrix3d:
                        matrix_row = []
                        for row in matrix2d:
                            matrix_col = []
                            for exp in row:
                                matrix_col.append(exp.value)
                            matrix_row.append(matrix_col)
                        matrix_cube.append(matrix_row)
                    matrix_layer.append(matrix_cube)
                listamatrix.append(matrix_layer)
            return listamatrix
        else:
            print("Error matrix")

