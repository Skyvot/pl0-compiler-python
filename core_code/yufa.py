from core_code import classes, symbol_manager
error_flag = 0          # 出错标志位（实际上没有用到）
token_ptr = 0           # token指针，表示当前处理到token_list中的第几个token
level = 0               # 当前所在层次
address = 0             # 过程起始地址
address_increase = 1    # 地址增加量
first = ["begin", "write", "if", "while", "call", "read", "write", "repeat"]


def program(log, token_list, symbol_list, pcode_list):
    """
    程序分析子程序
    """
    # print("# program start")
    global token_ptr
    global address
    block(log, token_list, symbol_list, pcode_list)
    cnt_token = token_list[token_ptr]
    if cnt_token.value == ".":
        token_ptr += 1
        if token_ptr != len(token_list):
            error(log, 18, token_list)  # '.'后程序没有停止
    else:
        error(log, 17, token_list)      # 缺少 '.'


def block(log, token_list, symbol_list, pcode_list):
    """
    <分程序>::=[<常量说明部分>][<变量说明部分>][<过程说明部分>]<语句>
    """
    # print("# block start")
    global address
    pre_address = address
    start = len(symbol_list)
    address = 3
    pos: classes.Symbol = symbol_manager.get_level_proc(symbol_list, level)
    if start > 0:
        pos: classes.Symbol = symbol_manager.get_level_proc(symbol_list, level)
    temp_pcode_ptr = len(pcode_list)
    temp_pcode = classes.Pcode("JMP", 0, 0)
    pcode_list.append(temp_pcode)
    if token_list[token_ptr].value == "const":
        con_declare(log, token_list, symbol_list, pcode_list)
    if token_list[token_ptr].value == "var":
        var_declare(log, token_list, symbol_list, pcode_list)
        if token_list[token_ptr].value == "const":
            error(log, 26, token_list)
            con_declare(log, token_list, symbol_list, pcode_list)
    if token_list[token_ptr].value == "procedure":
        proc(log, token_list, symbol_list, pcode_list)
    pcode_list[temp_pcode_ptr].pa = len(pcode_list)
    temp_pcode = classes.Pcode("INT", 0, address)
    pcode_list.append(temp_pcode)
    if start != 0:
        pos.value = len(pcode_list) - 1 - pos.size
    statement(log, token_list, symbol_list, pcode_list)
    temp_pcode = classes.Pcode("OPR", 0, 0)
    pcode_list.append(temp_pcode)
    address = pre_address


def con_declare(log, token_list, symbol_list, pcode_list):
    """
    <常量说明部分>::=const <常量定义>{,<常量定义>}
    """
    # print("# con_declare start")
    global token_ptr
    global address
    token_ptr += 1
    con_handle(log, token_list, symbol_list, pcode_list)
    while token_list[token_ptr].value == "," or token_list[token_ptr].symtype == 2:
        if token_list[token_ptr].value == ",":
            token_ptr += 1
        else:
            error(log, 23, token_list)      # 缺少 ,
        con_handle(log, token_list, symbol_list, pcode_list)
    if token_list[token_ptr].value == ";":
        token_ptr += 1
    else:
        error(log, 0, token_list)           # 缺 .


def con_handle(log, token_list, symbol_list, pcode_list):
    """
    <常量定义>::=<标识符>=<无符号整数>
    """
    # print("# con_handle start")
    global token_ptr
    if token_list[token_ptr].symtype == 2:
        name = token_list[token_ptr].value
        token_ptr += 1
        if token_list[token_ptr].value == "=" or token_list[token_ptr].value == ":=":
            if token_list[token_ptr].value == ":=":
                error(log, 3, token_list)
            token_ptr += 1
            if token_list[token_ptr].symtype == 6:
                value = int(token_list[token_ptr].value)
                if symbol_manager.exist_now(symbol_list, name, level):
                    error(log, 15, token_list)
                symbol_manager.enter_const(symbol_list, name, level, value, address)
                token_ptr += 1
        else:
            error(log, 3, token_list)
    else:
        error(log, 1, token_list)


def var_declare(log, token_list, symbol_list, pcode_list):
    """
    <变量说明部分>::=var<标识符>{,<标识符>}
    """
    # print("# var_handle start")
    global token_ptr
    global address
    token_ptr += 1
    if token_list[token_ptr].symtype == 2:
        name = token_list[token_ptr].value
        if symbol_manager.exist_now(symbol_list, name, level):
            error(log, 15, token_list)
        symbol_manager.enter_var(symbol_list, name, level, address)
        address += address_increase
        token_ptr += 1
        while token_list[token_ptr].value == "," or token_list[token_ptr].symtype == 2:
            if token_list[token_ptr].value == ",":
                token_ptr += 1
            else:
                error(log, 23, token_list)
            if token_list[token_ptr].symtype == 2:
                name = token_list[token_ptr].value
                if symbol_manager.exist_now(symbol_list, name, level):
                    error(log, 15, token_list)
                symbol_manager.enter_var(symbol_list, name, level, address)     # 这里还应不应该加到符号表中去？
                address += address_increase
                token_ptr += 1
            else:
                error(log, 1, token_list)
                token_ptr += 1
        if token_list[token_ptr].value != ";":
            error(log, 0, token_list)
        else:
            token_ptr += 1
    else:
        error(log, 1, token_list)


def proc(log, token_list, symbol_list, pcode_list):
    """
    <过程说明部分>::=<过程首部><分程序>{;<过程说明部分>};     <过程首部>::=procedure<标识符>;
    """
    # print("# proc start")
    global token_ptr
    global level
    global address
    if token_list[token_ptr].value != "procedure":
        return
    token_ptr += 1
    if token_list[token_ptr].symtype == 2:
        name = token_list[token_ptr].value
        if symbol_manager.exist_now(symbol_list, name, level):
            error(log, 15, token_list)
        symbol_manager.enter_proc(symbol_list, name, level, address)
        # address += address_increase
        level += 1
        token_ptr += 1
        if token_list[token_ptr].value == ";":
            token_ptr += 1
        else:
            error(log, 0, token_list)
        block(log, token_list, symbol_list, pcode_list)
        while token_list[token_ptr].value == "procedure" or token_list[token_ptr].value == ";":
            if token_list[token_ptr].value == ";":
                token_ptr += 1
            else:
                error(log, 0, token_list)
            level -= 1
            proc(log, token_list, symbol_list, pcode_list)
    else:
        error(log, -1, token_list)


def body(log, token_list, symbol_list, pcode_list):
    """
    <复合语句>::=begin<语句>{;<语句>}end
    """
    # print("# body start")
    global token_ptr
    if token_list[token_ptr].value == "begin":
        token_ptr += 1
        statement(log, token_list, symbol_list, pcode_list)
        while token_list[token_ptr].value == ";" or is_head_of_statement(token_list):
            if token_list[token_ptr].value == ";":
                token_ptr += 1
            elif token_list[token_ptr].value != "end":
                error(log, 0, token_list)
            if token_list[token_ptr].value == "end":
                # error(log, 21, token_list)
                break
            statement(log, token_list, symbol_list, pcode_list)
        if token_list[token_ptr].value == "end":
            token_ptr += 1
        else:
            error(log, 7, token_list)
            return
    else:
        error(log, 6, token_list)


def statement(log, token_list, symbol_list, pcode_list):
    """
    <语句>::=<赋值语句> | <条件语句> | <当循环语句> | <过程调用语句> | <复合语句> | <读语句> | <写语句> | <空>
    no pcode part
    """
    # print("# statement start")
    global token_ptr
    if token_list[token_ptr].value == "if":
        token_ptr += 1
        condition(log, token_list, symbol_list, pcode_list)
        if token_list[token_ptr].value == "then":
            temp_pcode_1 = classes.Pcode("JPC", 0, 0)
            pcode_list.append(temp_pcode_1)
            token_ptr += 1
            statement(log, token_list, symbol_list, pcode_list)
            temp_pcode_1.pa = len(pcode_list)
            if token_list[token_ptr].value == "else":
                token_ptr += 1
                temp_pcode_2 = classes.Pcode("JMP", 0, 0)
                pcode_list.append(temp_pcode_2)
                statement(log, token_list, symbol_list, pcode_list)
                temp_pcode_2.pa = len(pcode_list)
        else:
            error(log, 8, token_list)
            return
    elif token_list[token_ptr].value == "while":
        """<当循环语句>::=while<条件>do<语句>"""
        pos_1 = len(pcode_list)
        token_ptr += 1
        condition(log, token_list, symbol_list, pcode_list)
        if token_list[token_ptr].value == "do":
            pos_2 = len(pcode_list)
            temp_pcode_2 = classes.Pcode("JPC", 0, 0)
            pcode_list.append(temp_pcode_2)
            token_ptr += 1
            statement(log, token_list, symbol_list, pcode_list)
            pcode_list.append(classes.Pcode("JMP", 0, pos_1))
            temp_pcode_2.pa = len(pcode_list)
        else:
            error(log, 9, token_list)
            return
    elif token_list[token_ptr].value == "call":
        """<过程调用语句>::=call<标识符>"""
        token_ptr += 1
        if token_list[token_ptr].symtype == 2:
            name = token_list[token_ptr].value
            if symbol_manager.exist_pre(symbol_list, name, level):
                if symbol_manager.get_symbol(symbol_list, name, level).symtype == 3:
                    # print("this is a call to procedure" + name)
                    pcode_list.append(classes.Pcode("CAL",
                                                    level - symbol_manager.get_symbol(symbol_list, name, level).level,
                                                    symbol_manager.get_symbol(symbol_list, name, level).value))
                else:
                    error(log, 11, token_list)
                    return
            else:
                error(log, 10, token_list)
                return
            token_ptr += 1
        else:
            error(log, 1, token_list)
            return
    elif token_list[token_ptr].value == "read":
        """<读语句>::=read'('<标识符>{,<标识符>}')'"""
        token_ptr += 1
        if token_list[token_ptr].value == "(":
            token_ptr += 1
            if token_list[token_ptr].symtype == 2:
                name = token_list[token_ptr].value
                if symbol_manager.exist_pre(symbol_list, name, level) == 0:
                    error(log, 10, token_list)
                    return
                else:
                    temp_symbol = symbol_manager.get_symbol(symbol_list, name, level)
                    if temp_symbol.symtype == 2:
                        # pcode_list.append(classes.Pcode("OPR", 0, 16))
                        pcode_list.append(classes.Pcode("RED", level - temp_symbol.level, temp_symbol.address))
                        # print("read something into a variable")
                    else:
                        error(log, 12, token_list)
                        return
            token_ptr += 1
            while token_list[token_ptr].value == ",":
                token_ptr += 1
                if token_list[token_ptr].symtype == 2:
                    name = token_list[token_ptr].value
                    if symbol_manager.exist_pre(symbol_list, name, level) == 0:
                        error(log, 10, token_list)
                        return
                    else:
                        temp_symbol = symbol_manager.get_symbol(symbol_list, name, level)
                        if temp_symbol.symtype == 2:
                            # pcode_list.append(classes.Pcode("OPR", 0, 16))
                            # pcode_list.append(classes.Pcode("STO", level - temp_symbol.level, temp_symbol.address))
                            pcode_list.append(classes.Pcode("RED", level - temp_symbol.level, temp_symbol.address))
                            # print("read something into a variable")
                        else:
                            error(log, 12, token_list)
                            return
                    token_ptr += 1
                else:
                    error(log, 1, token_list)
                    return
            if token_list[token_ptr].value == ")":
                token_ptr += 1
                # print("end of a read statement.")
            else:
                error(log, 5, token_list)
        else:
            error(log, 4, token_list)
    elif token_list[token_ptr].value == "write":
        """<写语句>::=write '('<表达式>{,<表达式>}')'"""
        token_ptr += 1
        if token_list[token_ptr].value == "(":
            token_ptr += 1
            expression(log, token_list, symbol_list, pcode_list)
            # pcode_list.append(classes.Pcode("OPR", 0, 14))
            pcode_list.append(classes.Pcode("WRT", 0, 0))
            while token_list[token_ptr].value == ",":
                token_ptr += 1
                expression(log, token_list, symbol_list, pcode_list)
                pcode_list.append(classes.Pcode("WRT", 0, 0))
            # pcode_list.append(classes.Pcode("OPR", 0, 15))
            if token_list[token_ptr].value == ")":
                token_ptr += 1
            else:
                error(log, 5, token_list)
                while token_list[token_ptr].value not in first and token_list[token_ptr].symtype != 2:
                    token_ptr += 1
                token_ptr -= 1
        else:
            error(log, 4, token_list)
    elif token_list[token_ptr].value == "begin":
        """复合语句"""
        body(log, token_list, symbol_list, pcode_list)
    elif token_list[token_ptr].symtype == 2:
        """<赋值语句>::=<标识符>:=<表达式>"""
        name = token_list[token_ptr].value
        token_ptr += 1
        if token_list[token_ptr].value == "=" or token_list[token_ptr].value == ":=" or token_list[token_ptr].value == ":":
            if token_list[token_ptr].value == "=" or token_list[token_ptr].value == ":":
                error(log, 24, token_list)
            token_ptr += 1
            expression(log, token_list, symbol_list, pcode_list)
            if symbol_manager.exist_pre(symbol_list, name, level) == 0:
                error(log, 14, token_list)
                return
            else:
                temp_symbol = symbol_manager.get_symbol(symbol_list, name, level)
                if temp_symbol.symtype == 2:
                    pcode_list.append(classes.Pcode("STO", level - temp_symbol.level, temp_symbol.address))
                    # print("fuzhi ok")
                else:
                    error(log, 13, token_list)
        else:
            error(log, 25, token_list)
    elif token_list[token_ptr].value == "repeat":
        """<重复语句> ::= repeat<语句>{;<语句>}until<条件>"""
        token_ptr += 1
        pos = len(pcode_list)
        statement(log, token_list, symbol_list, pcode_list)
        while token_list[token_ptr].value == ";" or is_head_of_statement(token_list):
            if is_head_of_statement(token_list) == 1:
                error(log, 1, token_list)
            else:
                token_ptr += 1
            if token_list[token_ptr].value == "until":
                error(log, 22, token_list)
            token_ptr += 1
            statement(log, token_list, symbol_list, pcode_list)
        if token_list[token_ptr].value == "until":
            token_ptr += 1
            condition(log, token_list, symbol_list, pcode_list)
            pcode_list.append("JPC", 0, pos)
        else:
            error(log, 19, token_list)
            return
        con_declare(log, token_list, symbol_list, pcode_list)
    else:
        error(log, 1, token_list)


def condition(log, token_list, symbol_list, pcode_list):
    """<条件>::=<表达式><关系运算符><表达式> | odd<表达式>"""
    # ("# condition start")
    global token_ptr
    if token_list[token_ptr].value == "odd":
        token_ptr += 1
        expression(log, token_list, symbol_list, pcode_list)
        pcode_list.append(classes.Pcode("OPR", 0, 6))
    else:
        expression(log, token_list, symbol_list, pcode_list)
        temp_token = token_list[token_ptr]
        token_ptr += 1
        expression(log, token_list, symbol_list, pcode_list)
        if temp_token.value == "=":
            pcode_list.append(classes.Pcode("OPR", 0, 8))
        elif temp_token.value == "<>":
            pcode_list.append(classes.Pcode("OPR", 0, 9))
        elif temp_token.value == "<":
            pcode_list.append(classes.Pcode("OPR", 0, 10))
        elif temp_token.value == ">=":
            pcode_list.append(classes.Pcode("OPR", 0, 11))
        elif temp_token.value == ">":
            pcode_list.append(classes.Pcode("OPR", 0, 12))
        elif temp_token.value == "<=":
            pcode_list.append(classes.Pcode("OPR", 0, 13))
        else:
            error(log, 2, token_list)


def expression(log, token_list, symbol_list, pcode_list):
    """<表达式>::=[+|-]<项>{<加法运算符><项>}        <加法运算符>::=+|-"""
    # print("# expression start")
    global token_ptr
    flag = ""
    if token_list[token_ptr].value == "+" or token_list[token_ptr].value == "-":
        flag = token_list[token_ptr].value
        token_ptr += 1
    term(log, token_list, symbol_list, pcode_list)
    if flag == "-":
        pcode_list.append(classes.Pcode("OPR", 0, 1))
        # print("this is a negative number.")
    while token_list[token_ptr].value == "+" or token_list[token_ptr].value == "-":
        flag = token_list[token_ptr].value
        token_ptr += 1
        term(log, token_list, symbol_list, pcode_list)
        if flag == "-":
            pcode_list.append(classes.Pcode("OPR", 0, 3))
        if flag == "+":
            pcode_list.append(classes.Pcode("OPR", 0, 2))


def term(log, token_list, symbol_list, pcode_list):
    """<项>::=<因子>{<乘法运算符><因子>}       <乘法运算符>::=*"""
    # print("# term start")
    global token_ptr
    factor(log, token_list, symbol_list, pcode_list)
    while token_list[token_ptr].value == "*" or token_list[token_ptr].value == "/":
        flag = token_list[token_ptr].value
        token_ptr += 1
        factor(log, token_list, symbol_list, pcode_list)
        if flag == "*":
            pcode_list.append(classes.Pcode("OPR", 0, 4))
            # print("this is *.")
        if flag == "/":
            pcode_list.append(classes.Pcode("OPR", 0, 5))
            # print("this is /.")


def factor(log, token_list, symbol_list, pcode_list):
    """<因子>::=<标识符> | <无符号整数> | '('<表达式>')'"""
    # print("# factor start")
    global token_ptr
    if token_list[token_ptr].symtype == 6:
        pcode_list.append(classes.Pcode("LIT", 0, int(token_list[token_ptr].value)))
        # print("这是个常数")
        token_ptr += 1
    elif token_list[token_ptr].value == "(":
        token_ptr += 1
        expression(log, token_list, symbol_list, pcode_list)
        if token_list[token_ptr].value == ")":
            token_ptr += 1
        else:
            error(log, 5, token_list)
    elif token_list[token_ptr].symtype == 2:
        name = token_list[token_ptr].value
        if symbol_manager.exist_pre(symbol_list, name, level) == 0:
            error(log, 10, token_list)
            token_ptr += 1
            return
        else:
            temp_symbol = symbol_manager.get_symbol(symbol_list, name, level)
            if temp_symbol.symtype == 2:
                pcode_list.append(classes.Pcode("LOD", level - temp_symbol.level, temp_symbol.address))
                # print("这是个变量")
            elif temp_symbol.symtype == 1:
                pcode_list.append(classes.Pcode("LIT", 0, temp_symbol.value))
                # print("这是个常量")
            else:
                error(log, 12, token_list)
                return
        token_ptr += 1
    else:
        error(log, 1, token_list)
        return


def is_head_of_statement(token_list):
    if token_list[token_ptr].value == "if":
        return 1
    if token_list[token_ptr].value == "while":
        return 1
    if token_list[token_ptr].value == "call":
        return 1
    if token_list[token_ptr].value == "repeat":
        return 1
    if token_list[token_ptr].value == "write":
        return 1
    if token_list[token_ptr].value == "begin":
        return 1
    if token_list[token_ptr].value == "read":
        return 1
    if token_list[token_ptr].symtype == 2:
        return 1
    return 0


def error(log, key, token_list):
    """
    报错函数
    """
    global token_ptr
    # print("* error start")
    log.append(classes.Error(token_list[token_ptr].line, key, token_list[token_ptr].value))


def yufa_main(log, token_list, symbol_list, pcode_list):
    """
    语法分析入口
    """
    # print("# yufa_main start")
    # print(len(token_list))
    program(log, token_list, symbol_list, pcode_list)
    return error_flag
