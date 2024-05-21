
class Generator:
    def __init__(self):
        self.Temporal = 0
        self.Label = 0
        self.Fin = 0
        self.Code = []
        self.Data = []
        self.FinalCode = []
        self.Natives = []
        self.FuncCode = []
        self.TempList = []
        self.PrintStringFlag = True
        self.ConcatStringFlag = True
        self.BreakLabel = ""
        self.ContinueLabel = ""
        self.MainCode = False
        self.tipos = False

    def get_code(self):
        return self.Code

    def get_final_code(self):
        outstring=""
        if len(self.Data) >= 1:
            self.add_data()
            outstring += "".join(self.Data)
        outstring += "\n"
        self.add_headers()
        self.add_footers()
        outstring += "".join(self.Code)
        outstring += "".join(self.FuncCode)
        return outstring

    def get_temps(self):
        return self.TempList

    def add_break(self, lvl):
        self.BreakLabel = lvl

    def add_code(self, code):
        self.Code.append(code)

    def add_continue(self, lvl):
        self.ContinueLabel = lvl

    def new_temp(self):
        self.Temporal += 4
        #self.TempList.append(self.Temporal)
        return self.Temporal

    def new_label(self):
        temp = self.Label
        self.Label += 1
        return "L" + str(temp)

    def new_fin(self):
        temp = self.Fin
        self.Fin += 1
        return "Fin" + str(temp)

    def add_br(self):
        self.Code.append("\n")
    
    def add_la(self, left, right):
        self.Code.append(f"\tla {left}, {right}\n")

    def add_li(self, left, right):
        self.Code.append(f"\tli {left}, {right}\n")
    
    def add_lw(self, left, right):
        self.Code.append(f"\tlw {left}, {right}\n")

    def add_sw(self, left, right):
        self.Code.append(f"\tsw {left}, {right}\n")

    def add_sb(self, left, right):
        self.Code.append(f"\tsb {left}, {right}\n")

    def add_slli(self, left, right, res):
        self.Code.append(f"\tslli {left}, {right}, {res}\n")

    def add_operation(self, operation, target, left, right):
        self.Code.append(f"\t{operation} {target}, {left}, {right}\n")

    def add_operation_not(self, operation, target, left):
        self.Code.append(f"\t{operation} {target}, {left}\n")
    
    def add_operation_simple(self, operation, target, left):
        self.Code.append(f"\t{operation} {target}, {left}\n")

    def add_variable_word(self, id, value):
        self.Data.append(f"{id}: .word {value}\n")
    
    def add_variable_asciz(self, id, value):
        self.Data.append(f"{id}: .asciz \"{value}\" \n")
    
    def add_type_of(self):
        if self.tipos:
            return
        else:
            self.Data.append("typeof_number: .asciz \"number\" \n")
            self.Data.append("typeof_char: .asciz \"char\" \n")
            self.Data.append("typeof_string: .asciz \"string\" \n")
            self.Data.append("typeof_float: .asciz \"float\" \n")
            self.Data.append("typeof_boolean: .asciz \"boolean\" \n")
            self.Data.append("typeof_array: .asciz \"array\" \n")
            self.Data.append("typeof_null: .asciz \"null\" \n")
            self.tipos = True
    
    def add_variable_byte(self, id, value):
        print(value)
        self.Data.append(f"{id}: .byte {value} \n")

    def add_jump(self, value):
        self.Code.append(f"\tj {value} \n")
    
    def add_suma_float(self):
        self.Data.append("f_exp_coef: .word 0xFF \n")
        self.Data.append("f_man_coef: .word 0x7FFFFF \n")
        self.Data.append("f_man_norm: .word 0x800000 \n")
        self.Data.append("f_exp_hex1: .word 0x0 \n")
        self.Data.append("f_exp_hex2: .word 0x0 \n")
        self.Data.append("f_exp_diff: .word 0x0 \n")
        self.Data.append("f_man_hex1: .word 0x0 \n")
        self.Data.append("f_man_hex2: .word 0x0 \n")
        self.Data.append("f_man_sum: .word 0x0 \n")
        self.Data.append("f_sign_hex1: .word 0x0 \n")
        self.Data.append("f_sign_hex2: .word 0x0 \n")
    
    def call_addf(self):
        self.Code.append("\tjal ra, addf\n\n")
    
    def addf(self):
        self.FuncCode.append("addf: \n")
	    # extract signs
        self.FuncCode.append("\tla t0, f_sign_hex1\n")
        self.FuncCode.append("\tslli t1, a0, 31\n")
        self.FuncCode.append("\tandi t1, t1, 0x1\n")
        self.FuncCode.append("\tsw t1, 0(t0) \n")
        self.FuncCode.append("\tla t0, f_sign_hex2 \n")
        self.FuncCode.append("\tslli t1, a1, 31\n")
        self.FuncCode.append("\tandi t1, t1, 0x1\n")
        self.FuncCode.append("\tsw t1, 0(t0)\n")
    
    	# extract exponents
        self.FuncCode.append("\tla t0, f_exp_hex1\n")
        self.FuncCode.append("\tlw t1, f_exp_coef\n")
        self.FuncCode.append("\tsrli t2, a0, 23\n")
        self.FuncCode.append("\tand t2, t2, t1\n")
        self.FuncCode.append("\taddi t2, t2, -127\n")
        self.FuncCode.append("\tsw t2, 0(t0)\n")
        self.FuncCode.append("\tla t0, f_exp_hex2\n")
        self.FuncCode.append("\tlw t1, f_exp_coef\n")
        self.FuncCode.append("\tsrli t2, a1, 23\n")
        self.FuncCode.append("\tand t2, t2, t1\n")
        self.FuncCode.append("\taddi t2, t2, -127\n")
        self.FuncCode.append("\tsw t2, 0(t0)\n")
 
    	# extract mantissas
        self.FuncCode.append("\tla t0, f_man_hex1\n")
        self.FuncCode.append("\tlw t1, f_man_coef\n")
        self.FuncCode.append("\tlw t2, f_man_norm\n")
        self.FuncCode.append("\tand t3, a0, t1\n")
        self.FuncCode.append("\tor t3, t3, t2\n")
        self.FuncCode.append("\tsw t3, 0(t0)\n")
        self.FuncCode.append("\tla t0, f_man_hex2\n")
        self.FuncCode.append("\tlw t1, f_man_coef\n")
        self.FuncCode.append("\tlw t2, f_man_norm\n")
        self.FuncCode.append("\tand t3, a1, t1\n")
        self.FuncCode.append("\tor t3, t3, t2\n")
        self.FuncCode.append("\tsw t3, 0(t0)\n")
    	# adjust exponents
        self.FuncCode.append("\tla t0, f_exp_diff\n")
        self.FuncCode.append("\tlw t1, f_exp_hex1\n")
        self.FuncCode.append("\tlw t2, f_exp_hex2\n")
        self.FuncCode.append("\tsub t2, t1, t2\n")
        self.FuncCode.append("\tsw t2, 0(t0)\n")
    
        self.FuncCode.append("\tlw t0, f_exp_diff\n")
        self.FuncCode.append("\tbgtz t0, f_exp_diff_gtz    \n\n")

        self.FuncCode.append("f_exp_diff_letz:\n")
        self.FuncCode.append("\tneg t0, t0\n")
        self.FuncCode.append("\tlw t1, f_man_hex1\n")
        self.FuncCode.append("\tla t2, f_man_hex1\n")
        self.FuncCode.append("\tsrl t3, t1, t0\n")
        self.FuncCode.append("\tsw t3, 0(t2)\n")
        self.FuncCode.append("\tla t0, f_exp_hex1\n")
        self.FuncCode.append("\tlw t1, f_exp_hex2\n")
        self.FuncCode.append("\tsw t1, 0(t0)\n")
        self.FuncCode.append("\tj f_exp_diff_gtz_end\n\n")

        self.FuncCode.append("f_exp_diff_gtz:\n")
        self.FuncCode.append("\tlw t0, f_exp_diff\n")
        self.FuncCode.append("\tlw t1, f_man_hex2\n")
        self.FuncCode.append("\tla t2, f_man_hex2\n")
        self.FuncCode.append("\tsrl t3, t1, t0 \n")
        self.FuncCode.append("\tsw t3, 0(t2)\n")
        self.FuncCode.append("\tla t0, f_exp_hex2\n")
        self.FuncCode.append("\tlw t1, f_exp_hex1\n")
        self.FuncCode.append("\tsw t1, 0(t0)\n\n")
    
        self.FuncCode.append("f_exp_diff_gtz_end:\n")
	    # adding mantissas
        self.FuncCode.append("\tla t0, f_man_sum\n")
        self.FuncCode.append("\tlw t1, f_man_hex1\n")
        self.FuncCode.append("\tlw t2, f_man_hex2\n")
        self.FuncCode.append("\tadd t2, t1, t2\n")
        self.FuncCode.append("\tsw t2, 0(t0)\n")
    
    	# check carry
        self.FuncCode.append("\tlw t0, f_man_sum\n")
        self.FuncCode.append("\tli t1, 0x1000000\n")
        self.FuncCode.append("\tand t2, t0, t1\n")
        self.FuncCode.append("\tbnez t2, sum_carry\n")
        self.FuncCode.append("\tj combine_result\n\n")
    
        self.FuncCode.append("sum_carry:\n")
        self.FuncCode.append("\tla t0, f_man_sum\n")
        self.FuncCode.append("\tlw t1, f_man_sum\n")
        self.FuncCode.append("\tsrli t1, t1, 1\n")
        self.FuncCode.append("\tsw t1, 0(t0)\n")
        self.FuncCode.append("\tla t0, f_exp_hex1\n")
        self.FuncCode.append("\tlw t1, f_exp_hex1\n")
        self.FuncCode.append("\taddi t1, t1, 1\n")
        self.FuncCode.append("\tsw t1, 0(t0)\n\n")
    
        self.FuncCode.append("combine_result:\n")
        self.FuncCode.append("\tlw t0, f_sign_hex1\n")
        self.FuncCode.append("\tslli t0, t0, 31\n")
        self.FuncCode.append("\tlw t1, f_exp_hex1\n")
        self.FuncCode.append("\taddi t1, t1, 127\n")
        self.FuncCode.append("\tslli t1, t1, 23\n")
        self.FuncCode.append("\tor t0, t0, t1\n")
        self.FuncCode.append("\tlw t2, f_man_sum\n")
        self.FuncCode.append("\tlw t3, f_man_coef\n")
        self.FuncCode.append("\tand t2, t2, t3\n")
        self.FuncCode.append("\tor t0, t0, t2\n")
        self.FuncCode.append("\tmv a0, t0\n")
        self.FuncCode.append("\tret\n")

    def add_system_call(self):
        self.Code.append('\tecall\n')

    def add_data(self):
        self.Data.insert(0,'.data\n')

    def add_headers(self):
        self.Code.insert(0,'.text\n.globl _start\n_start:\n\n')
            
    def add_footers(self):
        self.Code.append('\n\tli a0, 0\n')
        self.Code.append('\tli a7, 93\n')
        self.Code.append('\tecall\n')