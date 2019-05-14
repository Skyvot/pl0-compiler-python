from core_code import classes
"""符号表管理类"""


def enter_const(symbol_list, name, level, value, address):  # 向符号表中插入常量
    symbol = classes.Symbol(1, value, level, address, 0, name)
    symbol_list.append(symbol)


def enter_var(symbol_list, name, level, address):   # 向符号表中插入变量
    symbol = classes.Symbol(2, -1, level, address, 0, name)
    symbol_list.append(symbol)


def enter_proc(symbol_list, name, level, address):  # 向符号表中插入过程
    symbol = classes.Symbol(3, -1, level, address, 0, name)
    symbol_list.append(symbol)


def exist_now(symbol_list, name, level):    # 判断该符号在当前层是否存在（冲突检查）
    for symbol in symbol_list:
        if symbol.name == name and symbol.level == level:
            return 1
    return 0


def exist_pre(symbol_list, name, level):    # 判断该符号在符号表中是否存在（判断是否有定义或声明）
    for symbol in symbol_list:
        if symbol.name == name and symbol.level <= level:
            return 1
    return 0


def get_symbol(symbol_list, name, level):  # 根据符号名称返回符号对象（进而对对象进行修改）
    for symbol in reversed(symbol_list):
        if symbol.name == name and symbol.level <= level:
            return symbol


def get_level_proc(symbol_list, level): # 返回该层的起始过程对象
    for symbol in reversed(symbol_list):
        if symbol.symtype == 3:
            return symbol
