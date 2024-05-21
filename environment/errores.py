from environment.error import Error
Errores = []

# Opcional: Definir una función para añadir elementos a la lista global
def agregar_error(linea,columna,descripcion,elemento):
    Errores.append([linea,columna,descripcion,elemento])
    print("Agregado a la lista de errores")

def extraer_datos():
    return Errores

def limpiar_errores():
    Errores.clear()
    print("Lista de errores limpiada")