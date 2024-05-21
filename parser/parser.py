# PLY ImportsToString
import parser.ply.lex as Lex
import parser.ply.yacc as yacc

# Expressions imports
from environment.types import ExpressionType
from environment.errores import agregar_error
from expressions.primitive import Primitive
from expressions.operation import Operation
from expressions.access import Access
from expressions.array import Array
from expressions.array_access import ArrayAccess
from expressions.matrix_access import MatrixAccess
from expressions.break_statement import Break
from expressions.continue_statement import Continue
from expressions.ternario import Ternario
from expressions.call import Call
from expressions.return_statement import Return

# Instructions imports
from instructions.print import Print
from instructions.declaration import Declaration
from instructions.assignment import Assignment
from instructions.operator_assigment import OperatorAssignment
from instructions.array_declaration import ArrayDeclaration
from instructions.lower import Lower
from instructions.upper import Upper
from instructions.to_string import ToString
from instructions.parse_int import ParseInt
from instructions.parse_float import ParseFloat
from instructions.typeof import Typeof
from instructions.if_instruction import If
from instructions.for_instruction import For
from instructions.while_instruction import While
from instructions.switch import Switch
from instructions.case import Case
from instructions.function import Function
from instructions.options_array import OptionArray


class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column

#LEXICO
reserved_words = {
    'console': 'CONSOLE', 
    'log': 'LOG', 
    'var': 'VAR',
    'const': 'CONST',
    'let': 'LET',
    'float': 'FLOAT',
    'number': 'NUMBER',
    'string': 'STRING',
    'char': 'CHAR',
    'boolean': 'BOOL',
    'if' : 'IF',
    'for' : 'FOR',
    'else' : 'ELSE',
    'switch' : 'SWITCH',
    'case' : 'CASE',
    'default' : 'DEFAULT',
    'while' : 'WHILE',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'RETURN',
    'function' : 'FUNC',
    'toLowerCase' : 'TOLOWER',
    'toUpperCase' : 'TOUPPER',
    'toString' : 'TOSTRING',
    'parseInt' : 'PARSEINT',
    'parseFloat' : 'PARSEFLOAT',
    'typeof' : 'TYPEOF',
    'push' : 'PUSH',
    'pop' : 'POP',
    'length' : 'LENGTH',
    'indexOf' : 'INDEXOF',
    'join' : 'JOIN'
}

# Listado de tokens
tokens = [
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'PUNTO',
    'DOSPTS',
    'COMA',
    'PYC',
    'BOOLEANO',
    'CADENA',
    'CARACTER',
    'ENTERO',
    'DECIMAL',
    'IG',
    'IGIG',
    'DIF',
    'CORIZQ',
    'CORDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'MAYOR',
    'MENOR',
    'MAYORIG',
    'MENORIG',
    'AND',
    'OR',
    'NOT',
    'TERN',
    'ID'
] + list(reserved_words.values())

t_MAYOR         = r'>'
t_MENOR         = r'<'
t_MAYORIG       = r'>='
t_MENORIG       = r'<='
t_PARIZQ        = r'\('
t_PARDER        = r'\)'
t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIVIDIDO      = r'/'
t_MODULO        = r'%'
t_PUNTO         = r'\.'
t_DOSPTS        = r':'
t_COMA          = r','
t_PYC           = r';'
t_IGIG          = r'=='
t_IG            = r'='
t_DIF           = r'!='
t_CORIZQ        = r'\['
t_CORDER        = r'\]'
t_LLAVEIZQ      = r'\{'
t_LLAVEDER      = r'\}'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'
t_TERN          = r'\?'

#Función de reconocimiento
def t_BOOLEANO(t):
    r'true|false'
    try:
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        if t.value == 'true':
            t.value = Primitive(line, column, True, ExpressionType.BOOLEAN)
        else:
            t.value = Primitive(line, column, False, ExpressionType.BOOLEAN)
    except ValueError:
        print("Error al convertir boolean %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t

def t_CADENA(t):
    r'\"(.+?)\"'
    try:
        strValue = str(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, strValue.replace('"', ''), ExpressionType.STRING)
    except ValueError:
        print("Error al convertir string %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t

def t_CARACTER(t):
    r'\'.?\''
    try:
        charValue = str(t.value[1:-1])
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, charValue, ExpressionType.CHAR)
        print("Se reconcio caracter: ", t.value)
    except ValueError:
        print("Error al convertir caracter %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        floatValue = float(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, floatValue, ExpressionType.FLOAT)
    except ValueError:
        print("Error al convertir a decimal %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t

def t_ENTERO(t):
    r'\d+'
    params = get_params(t)
    try:
        intValue = int(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, intValue, ExpressionType.INTEGER)
    except ValueError:
        print("Error al convertir a entero %d", t.value)
        agregar_error("Lexico", "Error al convertir a entero %d"+str(t.value[0]),params.line, params.column)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_words.get(t.value,'ID')
    return t

t_ignore = " \t"

t_ignore_COMMENTLINE = r'\/\/.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_ignore_COMMENTBLOCK(t):
    r'\/\*[^*]*\*+(?:[^/*][^*]*\*+)*\/'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    params = get_params(t)
    agregar_error("Lexico", "Caracter ilegal "+str(t.value[0]),params.line, params.column)
    print("Error Léxico '%s'" % t.value[0])
    t.lexer.skip(1)

#SINTACTICO
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGIG', 'DIF'),
    ('left', 'MENOR', 'MAYOR'),
    ('left', 'MENORIG', 'MAYORIG'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO')
)

#START
def p_start(t):
    '''s : block'''
    t[0] = t[1]

def p_instruction_block(t):
    '''block : block instruccion
            | instruccion '''
    if 2 < len(t):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

#Listado de instrucciones
def p_instruction_list(t):
    '''instruccion : print
                | ifinstruction
                | forinstruction
                | switchinstruction
                | whileinstruction 
                | declaration
                | arraydeclaration
                | assignment
                | assignmentsuma
                | assignmentresta
                | breakstmt
                | continuestmt
                | functionstmt
                | call
                | returnstmt
                | toLowerinstruction
                | toUpperinstruction
                | parseintinstruction
                | parsefloatinstruction
                | pushinstruction'''
    t[0] = t[1]

#-----------

#Listado de instrucciones
    
# Impresion en consola ----------------------------------------------------------------------------------
def p_instruccion_console(t):
    'print : CONSOLE PUNTO LOG PARIZQ expressionList PARDER PYC'
    params = get_params(t)
    t[0] = Print(params.line, params.column, t[5])

# Ciclo IF -----------------------------------------------------------------------------------------------
def p_instruction_if(t):
    '''ifinstruction : IF PARIZQ expression PARDER LLAVEIZQ block LLAVEDER
                    | IF PARIZQ expression PARDER LLAVEIZQ block LLAVEDER ELSE LLAVEIZQ block LLAVEDER
                    | IF PARIZQ expression PARDER LLAVEIZQ block LLAVEDER ELSE block
                    '''
    params = get_params(t)
    if len(t)==12:
        t[0] = If(params.line, params.column, t[3], t[6],t[10])
    elif len(t)==10:
        t[0] = If(params.line, params.column, t[3], t[6],t[9])
    else:
        t[0] = If(params.line, params.column, t[3], t[6],[])
    print(len(t))

# FOR --------------------------------------------------------------------------------------------------
def p_instruction_for(t):
    '''forinstruction : FOR PARIZQ declaration expression PYC Recurinstruction PARDER LLAVEIZQ block LLAVEDER'''
    params = get_params(t)
    t[0] = For(params.line, params.column, t[3], t[4], t[6], t[9])

def p_instruction_for_assign(t):
    '''Recurinstruction : ID MAS MAS
                        | ID MENOS MENOS'''
    arr = []
    arr.append([t[1],t[2],t[3]])
    t[0] = arr

# Switch -----------------------------------------------------------------------------------------------
def p_instruction_switch(t):
    'switchinstruction : SWITCH PARIZQ expression PARDER LLAVEIZQ caseinstruction LLAVEDER'
    params = get_params(t)
    t[0] = Switch(params.line, params.column, t[3], t[6])

def p_instruction_mul_case(t):
    '''caseinstruction : caseinstruction caseindividual
                       | caseindividual'''
    params = get_params(t)
    if 2 < len(t):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_instruction_case(t):
    '''caseindividual : cases DOSPTS block BREAK PYC'''
    params = get_params(t)
    t[0] = Case(params.line, params.column,t[1], t[3])

def p_instruction_case_default(t):
    '''cases : CASE expression
              | DEFAULT '''
    if len(t) > 2:
        t[0] = t[2]
    else:
        t[0] = t[1]

# While -----------------------------------------------------------------------------------------------
def p_instruction_while(t):
    'whileinstruction : WHILE PARIZQ expression PARDER LLAVEIZQ block LLAVEDER'
    params = get_params(t)
    t[0] = While(params.line, params.column, t[3], t[6])

# DECLARACION DE VARIABLES -------------------------------------------------------------------------------
def p_instruccion_declaration(t):
    '''declaration : VAR ID DOSPTS type IG expression PYC
                    | VAR ID IG expression PYC
                    | CONST ID DOSPTS type IG expression PYC
                    | CONST ID IG expression PYC'''
    params = get_params(t)
    if len(t) > 7:
        t[0] = Declaration(params.line, params.column, t[2], t[4], t[6],t[1])
    else:
        t[0] = Declaration(params.line, params.column, t[2], t[4].type, t[4],t[1])

# DECLARACION DE ARREGLOS --------------------------------------------------------------------------------
def p_instruccion_array_declaration(t):
    'arraydeclaration : VAR ID DOSPTS type CORIZQ CORDER IG expression PYC'
    params = get_params(t)
    t[0] = ArrayDeclaration(params.line, params.column, t[2], t[4], t[8],t[1])


# Asignacion de valores --------------------------------------------------------------------------------
def p_instruccion_assignment(t):
    'assignment : ID  IG expression PYC'
    params = get_params(t)
    t[0] = Assignment(params.line, params.column, t[1],t[3])

# Asignacion de valores con operadores ----------------------------------------------------------------
def p_instruccion_assignment_suma(t):
    'assignmentsuma : ID MAS IG expression PYC'
    params = get_params(t)
    t[0] = OperatorAssignment(params.line, params.column, t[1], "+",t[4])

def p_instruccion_assignment_resta(t):
    'assignmentresta : ID MENOS IG expression PYC'
    params = get_params(t)
    t[0] = OperatorAssignment(params.line, params.column, t[1], "-",t[4])

# Operaciones ternarias --------------------------------------------------------------------------------
def p_instruction_return(t):
    '''returnstmt : RETURN expression PYC
                | RETURN PYC'''
    params = get_params(t)
    if len(t) > 3:
        t[0] = Return(params.line, params.column, t[2])
    else:
        t[0] = Return(params.line, params.column, None)

# Llamada a funciones --------------------------------------------------------------------------------
def p_instruction_call_function(t):
    '''call : ID PARIZQ expressionList PARDER PYC
            | ID PARIZQ PARDER PYC'''
    params = get_params(t)
    if len(t) > 5:
        t[0] = Call(params.line, params.column, t[1], t[3])
    else:
        t[0] = Call(params.line, params.column, t[1], [])
    
    
# Definicion de funciones --------------------------------------------------------------------------------
def p_instruction_function(t):
    'functionstmt : FUNC ID funcparams functype LLAVEIZQ block LLAVEDER'
    params = get_params(t)
    t[0] = Function(params.line, params.column, t[2], t[3], t[4], t[6])

def p_instruction_function_params_list(t):
    '''funcparams : PARIZQ paramsList PARDER
                |  PARIZQ PARDER'''
    if len(t) > 3:
        t[0] = t[2]
    else:
        t[0] = []

def p_expression_param_list(t):
    '''paramsList : paramsList COMA ID DOSPTS type
                | ID DOSPTS type
                | paramsList ID DOSPTS type CORIZQ CORDER
                | ID DOSPTS type CORIZQ CORDER'''
    arr = []
    if len(t) > 5:
        if t[2] == ",":
            param = {t[3] : t[5]}
            arr = t[1] + [param]
        else:
            param = {t[1] : ExpressionType.ARRAY}
            arr.append(param)
    elif len(t) > 6:
        param = {t[2] : ExpressionType.ARRAY}
        arr = t[1] + [param]
    else:
        param = {t[1] : t[3]}
        arr.append(param)
    t[0] = arr

def p_instruction_function_type(t):
    '''functype : DOSPTS type
                | '''
    if len(t) > 2:
        t[0] = t[2]
    else:
        t[0] = ExpressionType.NULL

def p_instruction_break(t):
    'breakstmt : BREAK PYC'
    params = get_params(t)
    t[0] = Break(params.line, params.column)

def p_instruction_continue(t):
    'continuestmt : CONTINUE PYC'
    params = get_params(t)
    t[0] = Continue(params.line, params.column)


# Funciones embebidas --------------------------------------------------------------------------------
def p_instruccion_toLowerCase(t):
    'toLowerinstruction : CONST ID DOSPTS type IG ID PUNTO TOLOWER PARIZQ PARDER PYC'
    params = get_params(t)
    print("Reconoci bien lexico")
    valor = Lower(params.line, params.column,t[6])
    if valor != None:
        t[0] = Declaration(params.line, params.column, t[2], t[4], valor, t[1])
    else:
        print("Error en la instrucción toLowerCase")

def p_instruccion_toUpperCase(t):
    'toUpperinstruction : CONST ID DOSPTS type IG ID PUNTO TOUPPER PARIZQ PARDER PYC'
    params = get_params(t)
    valor = Upper(params.line, params.column,t[6])
    if valor != None:
        t[0] = Declaration(params.line, params.column, t[2], t[4], valor, t[1])
    else:
        print("Error en la instrucción toUpperCase")

def p_instruccion_parseInt(t):
    'parseintinstruction : CONST ID DOSPTS type IG PARSEINT PARIZQ expression PARDER PYC'
    params = get_params(t)
    valor = ParseInt(params.line, params.column,t[8])
    if valor != None:
        t[0] = Declaration(params.line, params.column, t[2], t[4], valor, t[1])
    else:
        print("Error en la instrucción parseInt")
    
def p_instruccion_parseFloat(t):
    'parsefloatinstruction : CONST ID DOSPTS type IG PARSEFLOAT PARIZQ expression PARDER PYC'
    params = get_params(t)
    print("entre parse float")
    valor = ParseFloat(params.line, params.column,t[8])
    if valor != None:
        t[0] = Declaration(params.line, params.column, t[2], t[4], valor, t[1])
    else:
        print("Error en la instrucción parseFloat")
    
def p_instruccion_push(t):
    'pushinstruction : ID PUNTO PUSH PARIZQ expression PARDER PYC'
    params = get_params(t)
    t[0] = OptionArray(params.line, params.column, t[1],"push", [t[5]])

def p_type_prod(t):
    '''type : NUMBER
            | FLOAT
            | STRING
            | CHAR
            | BOOL'''
    if t[1] == 'number':
        t[0] = ExpressionType.INTEGER
    if t[1] == 'float': 
        t[0] = ExpressionType.FLOAT
    if t[1] == 'string':
        t[0] = ExpressionType.STRING
    if t[1] == 'char':
        t[0] = ExpressionType.CHAR
    if t[1] == 'boolean':
        t[0] = ExpressionType.BOOLEAN

# Expressions
def p_expression_list(t):
    '''expressionList : expressionList COMA expression
                    | expression '''
    arr = []
    if len(t) > 2:
        arr = t[1] + [t[3]]
    else:
        arr.append(t[1])
    t[0] = arr

def p_expression_add(t):
    'expression : expression MAS expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "+", t[1], t[3])

def p_expression_sub(t):
    'expression : expression MENOS expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "-", t[1], t[3])

def p_expression_mult(t):
    'expression : expression POR expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "*", t[1], t[3])

def p_expression_div(t):
    'expression : expression DIVIDIDO expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "/", t[1], t[3])

def p_expression_mod(t):
    'expression : expression MODULO expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "%", t[1], t[3])

def p_expression_mayor(t):
    'expression : expression MAYOR expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, ">", t[1], t[3])

def p_expression_menor(t):
    'expression : expression MENOR expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "<", t[1], t[3])

def p_expression_mayor_igual(t):
    'expression : expression MAYORIG expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, ">=", t[1], t[3])

def p_expression_menor_igual(t):
    'expression : expression MENORIG expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "<=", t[1], t[3])

def p_expression_igual(t):
    'expression : expression IGIG expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "==", t[1], t[3])

def p_expression_diferente(t):
    'expression : expression DIF expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "!=", t[1], t[3])

def p_expression_and(t):
    'expression : expression AND expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "&&", t[1], t[3])

def p_expression_or(t):
    'expression : expression OR expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "||", t[1], t[3])

def p_expression_not(t):
    'expression : NOT expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "!", t[2], None)

def p_expression_agrupacion(t):
    'expression : PARIZQ expression PARDER'
    t[0] = t[2]

def p_expression_ternario(t):
    'expression : expression TERN expression DOSPTS expression'
    params = get_params(t)
    t[0] = Ternario(params.line, params.column, t[1], t[3], t[5])


def p_expression_primitiva(t):
    '''expression   : ENTERO
                    | DECIMAL
                    | BOOLEANO
                    | CADENA 
                    | CARACTER
                    | listArray'''
    
    params = get_params(t)
    if len(t) > 2:
        params = get_params(t)
        t[0] = Primitive(params.line, params.column, t[2], ExpressionType.INTEGER)
    else:
        t[0] = t[1]

def p_expression_array_primitiva(t):
    '''expression : CORIZQ expressionList CORDER'''
    params = get_params(t)
    t[0] = Array(params.line, params.column, t[2])

def p_expression_call_function(t):
    '''expression : ID PARIZQ expressionList PARDER
            | ID PARIZQ PARDER'''
    params = get_params(t)
    if len(t) > 4:
        t[0] = Call(params.line, params.column, t[1], t[3])
    else:
        t[0] = Call(params.line, params.column, t[1], [])


def p_expression_list_array(t):
    '''listArray : listArray PUNTO INDEXOF PARIZQ expression PARDER 
                | listArray PUNTO POP PARIZQ PARDER
                | listArray PUNTO JOIN PARIZQ PARDER
                | listArray PUNTO TOSTRING PARIZQ PARDER
                | listArray CORIZQ expression CORDER
                | listArray PUNTO LENGTH
                | listArray PUNTO ID
                | ID'''
    params = get_params(t)
    if len(t) > 6:
        t[0] = OptionArray(params.line, params.column, t[1], 'index', t[5])
    elif len(t) > 5:
        if t[3] == 'join':
            t[0] = OptionArray(params.line, params.column, t[1], 'join', None)
        elif t[3] == 'pop':
            t[0] = OptionArray(params.line, params.column, t[1], 'pop', None)
        elif t[3] == 'toString':
            t[0] = ToString(params.line, params.column,t[1])
    elif len(t) > 4:
        t[0] = ArrayAccess(params.line, params.column, t[1], t[3])
    elif len(t) > 3:
        if t[3] == 'length':
            t[0] = OptionArray(params.line, params.column, t[1], 'length', None)
        
    else:
        t[0] = Access(params.line, params.column, t[1])

def p_instruccion_typeof(t):
    'expression : TYPEOF ID'
    params = get_params(t)
    t[0] = Typeof(params.line, params.column,t[2])

def p_error(p):
    if p:
        agregar_error("Sintactico", "Token inesperado "+str(p.value),str(p.lineno), str(p.lexpos))
    else:
        agregar_error("Sintactico", "Error de sintaxis",0,0)

def get_params(t):
    line = t.lexer.lineno  # Obtener la línea actual desde el lexer
    lexpos = t.lexpos if isinstance(t.lexpos, int) else 0  # Verificar si lexpos es un entero
    column = lexpos - t.lexer.lexdata.rfind('\n', 0, lexpos) 
    return codeParams(line, column)

class Parser:
    def __init__(self):
        pass

    def interpretar(self, input, ast):
        lexer = Lex.lex()
        parser = yacc.yacc()
        result = parser.parse(input)
        return result
