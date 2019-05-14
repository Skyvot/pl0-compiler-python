"""
定义了一些用得到的类。
"""


class Symbol(object):   # 符号类（符号表项）
    def __init__(self, symtype, value, level, address, size, name):
        self.symtype = symtype                  # 符号类型 const: 1 var: 2 proc: 3 (int)
        self.value = value                      # 符号值 const: value var: -1 proc: Pcode address (int)
        self. level = level                     # 层数 level of block (int)
        self.address = address                  # 地址 address (int)
        self.size = size                        # 大小 (int) 实际上没用到
        self.name = name                        # 符号名称 name of the symbol (string)


class Token(object):    # 字符类（存储词法分析结果）
    def __init__(self, symtype, line, value):
        self.symtype = symtype  # 字符类型（详见cifa.py开头注释）
        self.line = line        # token所在行号
        self.value = value      # 字符值（string）


class Error(object):    # 错误类（代表一条错误信息）
    def __init__(self, line, error_type, token_name):
        self.error_type = error_type    # 错误类型（int，错误号）
        self.line = line                # 出错行号
        self.token_name = token_name         # 出错处字符（string）


class Pcode(object):
    pa: int

    def __init__(self, pf, pl, pa):
        self.pf = pf                    # 指令名称
        self.pl = pl                    # 层次差
        self.pa = pa                    # A 具体含义需要参考指令名称
