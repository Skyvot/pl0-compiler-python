from core_code import classes

'''
关键字 KEYWORDSY 1
标识符 IDSY 2
单字操作符 SINOPSY 3
双字操作符 DOUOPSY 4
分界符 SEPSY 5
数字 NUMSY 6
'''
error_flag = 0          # 标志是否出错（实际上没用到）
temp = ""               # 存储当前行的字符串
token = ""              # 存储当前分析出的token
line_num = 0            # 行号
cur_char = ''           # 存储当前字符
textptr = 0             # 分析位置指针
keywords = ["const", "var", "procedure", "odd", "if", "else", "then", "while", "do", "call",
            "begin", "end", "repeat", "until", "read", "write"]   # 关键字集


def cat_token():
    global token
    global cur_char
    token += cur_char


def retract():
    global textptr
    textptr -= 1


def clear_token():
    global token
    token = ""


def is_reserve():
    global token
    for keyword in keywords:
        if token == keyword:
            return 1
    return 0


def error(log):
    global line_num
    global error_flag
    global token
    error_flag = 1
    cnt_error = classes.Error(line_num, 1, token)
    log.append(cnt_error)


def tgetchar():
    global cur_char
    global textptr
    cur_char = temp[textptr]
    textptr += 1


def is_space():
    global cur_char
    if cur_char == ' ':
        return 1
    else:
        return 0


def is_endl():
    global cur_char
    if cur_char == '\n' or cur_char == '\t':
        return 1
    else:
        return 0


def is_tab():
    global cur_char
    if cur_char == "\tabl":
        return 1
    else:
        return 0


def is_letter():
    global cur_char
    if cur_char.isalpha():
        return 1
    else:
        return 0


def is_digit():
    global cur_char
    if cur_char.isdigit():
        return 1
    else:
        return 0


def is_colon():
    global cur_char
    if cur_char == ':':
        return 1
    else:
        return 0


def is_comma():
    global cur_char
    if cur_char == ',':
        return 1
    else:
        return 0


def is_semi():
    global cur_char
    if cur_char == ';':
        return 1
    else:
        return 0


def is_equ():
    global cur_char
    if cur_char == '=':
        return 1
    else:
        return 0


def is_plus():
    global cur_char
    if cur_char == '+':
        return 1
    else:
        return 0


def is_minus():
    global cur_char
    if cur_char == '-':
        return 1
    else:
        return 0


def is_div():
    global cur_char
    if cur_char == '/':
        return 1
    else:
        return 0


def is_mul():
    global cur_char
    if cur_char == '*':
        return 1
    else:
        return 0


def is_lpar():
    global cur_char
    if cur_char == '(':
        return 1
    else:
        return 0


def is_rpar():
    global cur_char
    if cur_char == ')':
        return 1
    else:
        return 0


def is_lar():
    global cur_char
    if cur_char == '>':
        return 1
    else:
        return 0


def is_les():
    global cur_char
    if cur_char == '<':
        return 1
    else:
        return 0


def is_poi():
    global cur_char
    if cur_char == '.':
        return 1
    else:
        return 0


def getsym(log, token_list):
    clear_token()
    tgetchar()
    while is_space() or is_tab():    # 跳过空格等空白字符
        tgetchar()
    if is_letter():                  # 如果是字母，组合单词
        while is_letter() or is_digit():
            cat_token()
            tgetchar()
        retract()
        if is_reserve() == 0:
            sym = 2              # 2 表示标识符
            new_token = classes.Token(sym, line_num, token)
        else:
            sym = 1              # 1 表示关键词
            new_token = classes.Token(sym, line_num, token)
        token_list.append(new_token)
    elif is_digit():                  # 组合数字
        while is_digit():
            cat_token()
            tgetchar()
        retract()
        sym = 6             # 6 表示数字
        new_token = classes.Token(sym, line_num, token)
        token_list.append(new_token)
    elif is_colon():    # 判断：=
        cat_token()
        tgetchar()
        if is_equ():
            cat_token()
            sym = 4
            new_token = classes.Token(sym, line_num, token)
            token_list.append(new_token)
        else:
            retract()
            error(log)
            sym = 4
            new_token = classes.Token(sym, line_num, token)
            token_list.append(new_token)
    elif is_lpar() or is_rpar() or is_comma() or is_semi() or is_poi():   # 分界符
        cat_token()
        sym = 5
        new_token = classes.Token(sym, line_num, token)
        token_list.append(new_token)
    elif is_plus() or is_minus() or is_equ() or is_div() or is_mul():    # 单字操作符
        cat_token()
        sym = 3
        new_token = classes.Token(sym, line_num, token)
        token_list.append(new_token)
    elif is_les():                                                       # 判断<= <>
        cat_token()
        tgetchar()
        if is_equ() or is_lar():
            cat_token()
            sym = 4
        else:
            retract()
            sym = 3
        new_token = classes.Token(sym, line_num, token)
        token_list.append(new_token)
    elif is_lar():                                                      # 判断>=
        cat_token()
        tgetchar()
        if is_equ():
            cat_token()
            sym = 4
        else:
            retract()
            sym = 3
        new_token = classes.Token(sym, line_num, token)
        token_list.append(new_token)
    elif is_endl():                                                      # 换行符表示单行处理结束，返回
        return
    else:
        error(log)


def cifa_main(log, token_list):
    f = open("../input/input.txt", "r")
    lines = f.readlines()             # 读取  "../input/input.txt" 到内存中
    for line in lines:                # readlines函数的缘故逐行处理。
        global line_num
        global cur_char
        global temp
        global textptr
        temp = line + '\n'            # 这里其实是因为出现了最后一行末尾没有换行符导致文件结尾为identifier或者number的时候
                                      # tgetchar函数越界，因此多加一个换行符在不影响词法分析结果的情况下解决了bug
        line_num += 1
        textptr = 0
        while textptr < len(temp):
            getsym(log, token_list)
    return error_flag
