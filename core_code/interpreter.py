import os
from core_code import classes


pcode_stack = []


def base(l, runtime_stack, b):
    while l > 0:
        b = runtime_stack[b]
        l -= 1
    return b


def interpreter(pcode_list, flag):
    runtime_stack = []
    cnt = 0
    while cnt <= 1000:
        runtime_stack.append(0)
        cnt += 1
    pc = 0
    sp = 0
    bp = 0
    while 1:
        pcode = pcode_list[pc]
        if flag == 1:
            print(pcode.pf + "  " + str(pcode.pl) + "  " + str(pcode.pa))
        pc += 1
        if pcode.pf == "LIT":
            runtime_stack[sp] = pcode.pa
            sp += 1
        elif pcode.pf == "OPR":
            if pcode.pa == 0:           # 返回
                sp = bp
                pc = runtime_stack[sp + 2]
                bp = runtime_stack[sp + 1]
            elif pcode.pa == 1:         # 取反
                runtime_stack[sp - 1] = -runtime_stack[sp - 1]
            elif pcode.pa == 2:         # 加法
                sp -= 1
                runtime_stack[sp - 1] += runtime_stack[sp]
            elif pcode.pa == 3:         # 减法
                sp -= 1
                runtime_stack[sp - 1] -= runtime_stack[sp]
            elif pcode.pa == 4:         # 乘法
                sp -= 1
                runtime_stack[sp - 1] *= runtime_stack[sp]
            elif pcode.pa == 5:         # 除法
                sp -= 1
                runtime_stack[sp - 1] /= runtime_stack[sp]
            elif pcode.pa == 8:         # =
                sp -= 1
                if runtime_stack[sp] == runtime_stack[sp - 1]:
                    runtime_stack[sp - 1] = 1
                else:
                    runtime_stack[sp - 1] = 0
            elif pcode.pa == 9:         # <>
                sp -= 1
                if runtime_stack[sp] != runtime_stack[sp - 1]:
                    runtime_stack[sp - 1] = 1
                else:
                    runtime_stack[sp - 1] = 0
            elif pcode.pa == 10:         # <
                sp -= 1
                if runtime_stack[sp - 1] < runtime_stack[sp]:
                    runtime_stack[sp - 1] = 1
                else:
                    runtime_stack[sp - 1] = 0
            elif pcode.pa == 11:         # >=
                sp -= 1
                if runtime_stack[sp - 1] >= runtime_stack[sp]:
                    runtime_stack[sp - 1] = 1
                else:
                    runtime_stack[sp - 1] = 0
            elif pcode.pa == 12:         # >
                sp -= 1
                if runtime_stack[sp - 1] > runtime_stack[sp]:
                    runtime_stack[sp - 1] = 1
                else:
                    runtime_stack[sp - 1] = 0
            elif pcode.pa == 13:         # <=
                sp -= 1
                if runtime_stack[sp - 1] <= runtime_stack[sp]:
                    runtime_stack[sp - 1] = 1
                else:
                    runtime_stack[sp - 1] = 0
            else:
                pass
        elif pcode.pf == "LOD":
            runtime_stack[sp] = runtime_stack[base(pcode.pl, runtime_stack, bp) + pcode.pa]
            sp += 1
        elif pcode.pf == "CAL":
            runtime_stack[sp] = base(pcode.pl, runtime_stack, bp)
            runtime_stack[sp + 1] = bp
            runtime_stack[sp + 2] = pc
            bp = sp
            pc = pcode.pa
        elif pcode.pf == "STO":
            sp -= 1
            runtime_stack[base(pcode.pl, runtime_stack, bp) + pcode.pa] = runtime_stack[sp]
        elif pcode.pf == "INT":
            sp += pcode.pa
        elif pcode.pf == "JMP":
            pc = pcode.pa
        elif pcode.pf == "JPC":
            sp -= 1
            if runtime_stack[sp] == 0:
                pc = pcode.pa
        elif pcode.pf == "WRT":
            sp -= 1
            print(runtime_stack[sp])
        elif pcode.pf == "RED":
            stri = input()
            runtime_stack[base(pcode.pl, runtime_stack, bp) + pcode.pa] = int(stri)
        if pc == 0:
            break


