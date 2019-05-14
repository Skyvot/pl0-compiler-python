from core_code import yufa, cifa, interpreter


log = []            #错误信息表
token_list = []     # token表
symbol_list = []    # 符号表
pcode_list = []     # pcode表
error_flag = 0      # 编译错误标志位（后来没有用到）


def pl0compile():
    """
    编译函数入口
    通过传list的方式实现个步骤的结果获取（利用了python函数传参特性，list在函数中的修改会保留）
    """
    global error_flag                               # 这个后来没有用到
    error_flag += cifa.cifa_main(log, token_list)   # 词法分析
    error_flag += yufa.yufa_main(log, token_list, symbol_list, pcode_list)  # 语法分析、语义分析、目标代码生成等


def init():
    """
    初始化
    1.清空各list中的对象
    2.清空各output文件中的已有信息
    """
    log.clear()
    token_list.clear()
    symbol_list.clear()
    pcode_list.clear()
    token_file = open("../output/token.txt", "w")
    for token in token_list:
        print(str(token.symtype) + " " + str(token.line) + " " + token.value, file=token_file)
    symbol_file = open("../output/symbol.txt", "w")
    for symbol in symbol_list:
        print(str(symbol.symtype) + " " + str(symbol.value) + " " + str(symbol.level),
              str(symbol.address) + " " + str(symbol.size) + " " + symbol.name, file=symbol_file)
    pcode_file = open("../output/pcode.txt", "w")
    for pcode in pcode_list:
        print(pcode.pf + " " + str(pcode.pl) + " " + str(pcode.pa), file=pcode_file)
    log_file = open("../output/log.txt", "w")
    for error in log:
        print(str(error.error_type) + " " + str(error.line), file=log_file)


def output():
    """
    将token、symbol、pcode输出到指定文件中，每个对象一行，各元素用空格隔开
    """
    token_file = open("../output/token.txt", "w")
    for token in token_list:
        print(str(token.symtype) + " " + str(token.line) + " " + token.value, file=token_file)
    symbol_file = open("../output/symbol.txt", "w")
    for symbol in symbol_list:
        print(str(symbol.symtype) + " " + str(symbol.value) + " " + str(symbol.level),
              str(symbol.address) + " " + str(symbol.size) + " " + symbol.name, file=symbol_file)
    pcode_file = open("../output/pcode.txt", "w")
    for pcode in pcode_list:
        print(pcode.pf + " " + str(pcode.pl) + " " + str(pcode.pa), file=pcode_file)


def get_error_str(error_type):
    """
    错误号转化为错误信息字符串
    """
    if error_type == 0:
        return "Missing ';'"
    elif error_type == -1:
        return "A declaration statement should start with 'const' or 'var'."
    elif error_type == 1:
        return "Invalid Identifier used"
    elif error_type == 2:
        return "Invalid comparing symbol used"
    elif error_type == 3:
        return "should assign a constant with '=' "
    elif error_type == 4:
        return "Missing '('"
    elif error_type == 5:
        return "Missing ')'"
    elif error_type == 6:
        return "Missing 'begin'"
    elif error_type == 7:
        return "Missing 'end'"
    elif error_type == 8:
        return "Missing 'then'"
    elif error_type == 9:
        return "Missing 'do'"
    elif error_type == 10:
        return "Unsolved identifier"
    elif error_type == 11:
        return "Not a procedure"
    elif error_type == 12:
        return "Not a variable"
    elif error_type == 13:
        return "Not a variable"
    elif error_type == 14:
        return "Unsolved variable"
    elif error_type == 15:
        return "Duplicated defination"
    elif error_type == 16:
        return "Number of parameters incorrect"
    elif error_type == 17:
        return "Missing '.'"
    elif error_type == 18:
        return "Code after '.'"
    elif error_type == 19:
        return "Missing 'until'"
    elif error_type == 20:
        return "should use ':='"
    elif error_type == 21:
        return "useless ';' before 'end'"
    elif error_type == 22:
        return "useless ';' before 'until'"
    elif error_type == 23:
        return "missing ','"
    elif error_type == 24:
        return "should use ':='"
    elif error_type == 25:
        return "should assign a variable with ':='"
    elif error_type == 26:
        return "const declaration in wrong place"
    else:
        return "UNKNOWN ERROR"


def show_log():
    """
    输出log（报错信息）
    """
    log_file = open("../output/log.txt", "w")
    for error in log:
        error_str = get_error_str(error.error_type)
        print("Line " + str(error.line) + ": " + error_str + " at symbol '" + str(error.token_name) + "'", file=log_file)


if __name__ == '__main__':
    init()
    pl0compile()
    if len(log) == 0:   # 通过log的长度判断是否出错。如果len是0说明编译过程中没有遇到错误
        print("Compiler succeeded.")
        output()
        print("commit interpreter? [y/n]")
        flag_1 = input()
        if flag_1 == "y":
            print("show pcode? [y/n]")
            flag_2 = input()
            if flag_2 == "y":
                show_pcode = 1
            else:
                show_pcode = 0
            interpreter.interpreter(pcode_list, show_pcode)
    else:
        print("Compiler failed.")
        show_log()
        output()
