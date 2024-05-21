from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from environment.errores import agregar_error
from environment.value import Value
from environment.table import getValueVar
import re
import struct

dominant_table = [
    [ExpressionType.INTEGER, ExpressionType.FLOAT,  ExpressionType.STRING, ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.FLOAT,   ExpressionType.FLOAT,  ExpressionType.STRING, ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.STRING,  ExpressionType.STRING, ExpressionType.STRING, ExpressionType.STRING,  ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.STRING, ExpressionType.BOOLEAN, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
]

class Operation(Expression):
    def __init__(self, line, col, operador, opL, opR):
        self.line = line
        self.col = col
        self.operador = operador
        self.opL = opL
        self.opR = opR

    def ejecutar(self, ast, env, gen):
        # Ejecución de operandos
        print("empieza operacion")
        print(f"op1: {self.opL}")
        print(f"op2: {self.opR}")
        op1 = self.opL.ejecutar(ast, env, gen)
        #print(f"valor op1: {op1.type}")
        if self.opR != None:
            op2 = self.opR.ejecutar(ast, env, gen)
            #print(f"valor op1: {op2.type}")
        else:
            op2 = Value("", 0, ExpressionType.NULL, [], [], [])

        # Validar tipos
        if op1.type == ExpressionType.INTEGER and op2.type == ExpressionType.INTEGER:
            gen.add_br()
            gen.add_li('t3', str(op1.value))
            gen.add_lw('t1', '0(t3)')
            gen.add_li('t3', str(op2.value))
            gen.add_lw('t2', '0(t3)')
            temp = gen.new_temp()

            if self.operador == "+":
                gen.add_operation('add', 't0', 't1', 't2')
                newVal = op1.intValue + op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
        
            if self.operador == "-":
                gen.add_operation('sub', 't0', 't1', 't2')
                newVal = op1.intValue - op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "*":
                gen.add_operation('mul', 't0', 't1', 't2')
                newVal = op1.intValue * op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "/":
                if op2.intValue == 0:
                    agregar_error("Semantico", f"Division entre 0", self.line, self.col)
                    return Value("", 0, ExpressionType.NULL, [], [], [])
                else:
                    gen.add_operation('div', 't0', 't1', 't2')
                    newVal = op1.intValue / op2.intValue
                    gen.add_li('t3', str(temp))
                    gen.add_sw('t0', '0(t3)')
                    return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "==":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('beq', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (op1.intValue == op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "!=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bne', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (op1.intValue != op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == ">":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bgt', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (op1.intValue > op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "<":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('blt', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (op1.intValue < op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == ">=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bge', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (op1.intValue >= op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "<=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('sub', 't0', 't1', 't2')
                gen.add_operation_simple('blez', 't0', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (op1.intValue <= op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
        
            if self.operador == "&&":
                gen.add_operation('and', 't0', 't1', 't2')
                newVal = op1.intValue and op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "||":
                gen.add_operation('or', 't0', 't1', 't2')
                newVal = op1.intValue or op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
        elif op1.type == ExpressionType.FLOAT and op2.type == ExpressionType.FLOAT:
            gen.add_br()
            gen.add_suma_float()
            gen.add_li('t3', str(op1.value))
            gen.add_lw('a0', '0(t3)')
            gen.add_li('t3', str(op2.value))
            gen.add_lw('a1', '0(t3)')
            gen.call_addf()
            gen.addf()
            newVal = op1.intValue  + op2.intValue
            temp = gen.new_temp()
            print("retorno: ", str(newVal))
            return  Value(str(temp), newVal, ExpressionType.FLOAT, [], [], [])

        elif op1.type == "ACCESS" and op2.type == ExpressionType.INTEGER:
            gen.add_br()
            gen.add_lw('t1', str(op1.value))
            print("condicion: ",op1.value)
            #gen.add_lw('t1', '0(t3)')
            gen.add_li('t3', str(op2.value))
            gen.add_lw('t2', '0(t3)')
            temp = gen.new_temp()
            valor_variable = getValueVar(op1.value)

            if self.operador == "+":
                gen.add_operation('add', 't0', 't1', 't2')
                newVal = valor_variable + op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
        
            if self.operador == "-":
                gen.add_operation('sub', 't0', 't1', 't2')
                newVal = valor_variable - op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "*":
                gen.add_operation('mul', 't0', 't1', 't2')
                newVal = valor_variable * op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "/":
                if op2.intValue == 0:
                    agregar_error("Semantico", f"Division entre 0", self.line, self.col)
                    return Value("", 0, ExpressionType.NULL, [], [], [])
                else:
                    gen.add_operation('div', 't0', 't1', 't2')
                    newVal = valor_variable / op2.intValue
                    gen.add_li('t3', str(temp))
                    gen.add_sw('t0', '0(t3)')
                    return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "%":
                
                newVal = valor_variable % op2.intValue
                gen.add_li('t0', newVal)
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "==":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('beq', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor_variable == op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "!=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bne', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor_variable != op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            

            if self.operador == ">":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bgt', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor_variable > op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "<":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('blt', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor_variable < op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == ">=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bge', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor_variable >= op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "<=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('sub', 't0', 't1', 't2')
                gen.add_operation_simple('blez', 't0', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor_variable <= op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "&&":
                gen.add_operation('and', 't0', 't1', 't2')
                newVal = valor_variable and op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "||":
                gen.add_operation('or', 't0', 't1', 't2')
                newVal = valor_variable or op2.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

        elif op1.type == ExpressionType.INTEGER and op2.type == "ACCESS":
            gen.add_br()
            gen.add_li('t3', str(op1.value))
            gen.add_lw('t1', '0(t3)')
            gen.add_lw('t2', str(op2.value))
            #gen.add_lw('t2', '0(t3)')
            temp = gen.new_temp()
            valor_variable = getValueVar(op2.value)

            if self.operador == "+":
                gen.add_operation('add', 't0', 't1', 't2')
                newVal = op1.intValue + valor_variable
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
        
            if self.operador == "-":
                gen.add_operation('sub', 't0', 't1', 't2')
                newVal = op1.intValue - valor_variable
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "*":
                gen.add_operation('mul', 't0', 't1', 't2')
                newVal = valor_variable * op1.intValue
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "/":
                gen.add_operation('div', 't0', 't1', 't2')
                newVal = op2.intValue / valor_variable
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "==":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('beq', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor_variable == op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "!=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bne', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor_variable != op2.intValue):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "&&":
                gen.add_operation('and', 't0', 't1', 't2')
                newVal = op1.intValue and valor_variable
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "||":
                gen.add_operation('or', 't0', 't1', 't2')
                newVal = op1.intValue or valor_variable
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

        elif op1.type == "ACCESS" and op2.type == "ACCESS":
            gen.add_br()
            gen.add_lw('t1', str(op1.value))
            gen.add_lw('t2', str(op2.value))
            temp = gen.new_temp()

            #Valores de las variables
            valor1 = getValueVar(op1.value)
            valor2 = getValueVar(op2.value)
            print("entre access 2")

            if self.operador == "+":
                gen.add_operation('add', 't0', 't1', 't2')
                if es_hexadecimal(str(valor1)):
                    gen.add_br()
                    gen.add_suma_float()
                    gen.add_lw('a0', str(op1.value))
                    gen.add_lw('a1', str(op2.value))
                    gen.call_addf()
                    gen.addf()
                    h1 = float.fromhex(valor1)
                    h2 = float.fromhex(valor2)
                    
                    # Sumar los valores
                    suma = h1 + h2
                    
                    # Convertir el resultado de vuelta a hexadecimal
                    resultado_hex = struct.pack('!f', suma).hex()
                    
                    # Retornar el resultado en formato hexadecimal con el prefijo "0x"
                    newVal = "0x"+resultado_hex
                    #newVal = op1.intValue  + op2.intValue
                    temp = gen.new_temp()
                    print("retorno: ", str(newVal))
                    return  Value(str(temp), newVal, ExpressionType.FLOAT, [], [], [])

                else:
                    newVal = valor1 + valor2
                    print("valor suma: ", newVal)
                    gen.add_li('t3', str(temp))
                    gen.add_sw('t0', '0(t3)')

                    return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
        
            if self.operador == "-":
                gen.add_operation('sub', 't0', 't1', 't2')
                newVal = valor1 - valor2
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "*":
                gen.add_operation('mul', 't0', 't1', 't2')
                newVal = valor1 * valor2
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "/":
                gen.add_operation('div', 't0', 't1', 't2')
                newVal = valor1 / valor2
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "==":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('beq', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor1 == valor2):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "!=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bne', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor1 != valor2):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == ">":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bgt', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor1 > valor2):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "<":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('blt', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor1 < valor2):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == ">=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('bge', 't1', 't2', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor1 >= valor2):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

            if self.operador == "<=":
                final = gen.new_fin()
                case = gen.new_label()
                case2 = gen.new_label()
                gen.add_operation('sub', 't0', 't1', 't2')
                gen.add_operation_simple('blez', 't0', case)
                gen.add_jump(case2)

                #etiqueta verdadera
                gen.add_code(f"{case}: \n")
                gen.add_li('t0','1')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)
                
                #etiqueta falsa
                gen.add_code(f"{case2}: \n")
                gen.add_li('t0','0')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(final)

                if (valor1 <= valor2):
                    newVal = 1
                else:
                    newVal = 0
                
                #sale del ciclo
                gen.add_code(f"{final}: \n")
                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
        
            if self.operador == "&&":
                gen.add_operation('and', 't0', 't1', 't2')
                newVal = valor1 and valor2
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])
            
            if self.operador == "||":
                gen.add_operation('or', 't0', 't1', 't2')
                newVal = valor1 or valor2
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')

                return  Value(str(temp), newVal, ExpressionType.INTEGER, [], [], [])

        elif op1.type == "ACCESS":
            gen.add_br()
            gen.add_lw('t1', str(op1.value))
            temp = gen.new_temp()

            if self.operador == "!":
                gen.add_operation_not('not', 't0', 't1')
                valor_variable = getValueVar(op1.value)
                newVal = not valor_variable
                if newVal:
                    newVal = 1
                else:
                    newVal = 0
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                return  Value(str(temp), newVal, ExpressionType.BOOLEAN, [], [], [])
        
        elif op1.type == ExpressionType.BOOLEAN:
            gen.add_br()
            gen.add_li('t3', str(op1.value))
            gen.add_lw('t1', '0(t3)')
            temp = gen.new_temp()

            if self.operador == "!":
                gen.add_operation_not('not', 't1', 't1')
                newVal = not op1.intValue
                if newVal:
                    newVal = 1
                else:
                    newVal = 0
                
                gen.add_li('t2', '2')
                gen.add_operation('add', 't0', 't1', 't2')
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                retorno = Value(str(temp), newVal, ExpressionType.BOOLEAN, [], [], [])
                print(retorno.type)
                return  retorno

        else:
            print("Error de tipos")
            print("op1: ", op1)
            return op1
        
def es_hexadecimal(valor):
    # Expresión regular para verificar si la cadena es un número hexadecimal
    patron = r'^0x[0-9a-fA-F]+$'
    
    # Verificar si la cadena cumple con el patrón
    if re.match(patron, valor):
        return True
    else:
        return False
        #return None