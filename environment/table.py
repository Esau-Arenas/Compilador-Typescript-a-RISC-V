Tabla_simbolos = []

# Opcional: Definir una función para añadir elementos a la lista global
def agregar_simbolo(id,tipo_simbolo,tipo_dato,ambito,linea,columna,tipo_variable,value):
    Tabla_simbolos.append([id,tipo_simbolo,tipo_dato,ambito,linea,columna,tipo_variable,value])
    print("Agregado a la tabla de simbolos")

def extraer_datos_tabla():
    return Tabla_simbolos

def limpiar_tabla():
    Tabla_simbolos.clear()
    print("Tabla de simbolos limpiada")

def getId(id):
    for valor in Tabla_simbolos:
       #Devolver el tipo de dato de la variable
       if valor[0] == id:
           return valor[2]

def getNombreVar(id):
    for valor in Tabla_simbolos:
       #Devolver el tipo de dato de la variable
       if valor[0] == id:
           return valor[0]
def getValueVar(id):
    for valor in Tabla_simbolos:
       #Devolver el tipo de dato de la variable
       if valor[0] == id:
           return valor[7]
    
def getPushValue(id, new):
    for valor in Tabla_simbolos:
       #hacer push a los valores
       if valor[0] == id:
           valor[7].append(new)

def getPopValue(id):
    for valor in Tabla_simbolos:
       #hacer push a los valores
       if valor[0] == id:
           value=valor[7].pop()
           return value