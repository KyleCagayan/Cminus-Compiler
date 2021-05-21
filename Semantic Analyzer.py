token_list = []
token = ""
tokenlistNum = 0

var_tab  = {}
func_tab = []


def is_ID(token):
     return isinstance(token, tuple) and token[0] == 'ID'
def is_NUM(token):
     return isinstance(token, tuple) and token[0] == 'NUM'
def start_parser(tokenlist):
    global token, token_list
    token = tokenlist[tokenlistNum]
    token_list = tokenlist
    try:
        program()
        if token == "$":
            print("ACCEPT")
            print("var_tab: ",var_tab,"\nfunc_tab: ", func_tab)
        else:
            print("REJECT")
            print("var_tab: ",var_tab,"\nfunc_tab: ", func_tab)
    except ValueError:
        print("REJECT")
        print("var_tab: ",var_tab,"\nfunc_tab: ", func_tab)
def update():
    global token, tokenlistNum
    token = token_list[tokenlistNum]
def matchID(check):
    global tokenlistNum, n
    if token[0] == check:
        # print("matched ID!")
        n = token[1]
        tokenlistNum = tokenlistNum + 1
        update()
    else:
        raise ValueError
def matchNUM(check):
    global tokenlistNum
    if token[0] == check:
        # print("matched NUM!")
        tokenlistNum += 1
        update()
    else:
        raise ValueError
def match(check):
    # print("match                               " + token + " VS " + check)
    global tokenlistNum
    if token == check:
        # print("matched token: ", token)
        tokenlistNum = tokenlistNum + 1
        update()
    else:
        raise ValueError


def program():
    # print("program")
    declaration_list()
    # print("end of program")


def declaration_list():
    # print("declaration_list")
    if token == "int" or token == "void":
        declaration()
        A()
    # print("end of declaration_list")


def A():
    # print("A")
    if token == "int" or token == "void":
        declaration()
        if token == "int" or token == "void":
            A()
    # print("end of A")


def declaration():
    n = ''
    # print("declaration")
    if token == "int" or token == "void":
        t = type_specifier()
        if is_ID(token):
            # print("match ID? ", token)
            n = token[1]
            # print(n)
            matchID("ID")

        if token == "(" or token == ";" or token == "[":
            B(n, t)
    # print("end of declaration")


def B(n, t):
    # print("B")
    if token == ";" or token == "[":
        C(n, t)
    if token == "(":
        match("(")
        if token == "int" or token == "void":
            param_items = params()
            # print(param_items)
            func_tab.append((n, t, param_items)) # name type (params)
        match(")")
        if token == "{":
            compound_stmt(n, t)
    # print("end of B")


def var_declaration(n, t):
    # print("var_declaration")
    if token == "int" or token == "void":
        t = type_specifier()
        if is_ID(token):
            # print("match ID?")
            n = token[1]
            matchID("ID")
        if token == ";" or token == "[":
            C(n, t)
    # print("end of var_declaration")


def C(n, t):
    # print("C")
    if token == ";":
        match(";")
        var_tab[n] = t
    else:
        match("[")
        if is_NUM(token):
            # print("match NUM?")
            matchNUM("NUM")
        match("]")
        match(";")
        var_tab[n] = "array"
        # TODO append to var_tab
    # print("end of C")


def type_specifier():
    # print("type_specifier")
    if token == "int":
        match("int")
        t = "int"
    if token == "void":
        match("void")
        t = "void"
    return t
    # print("end of type_specifier")


def params():
    param_items = [] # "param 1, param 2, etc..."
    temp = ''
    # print("params")
    if token == "int":
        # print("match ID?")
        temp = token
        match("int")
        if is_ID(token):
            U(param_items, temp)
    elif token == "void":
        temp = token
        match("void")
        param_items.append(temp)
        # if is_ID(token):
            # U(param_items, temp)
    #todo append to param_items
    return param_items

def U(param_items, temp):
    # print("U")
    if is_ID(token):
        # print("match ID?")
        matchID("ID")
        if token in ["["]:
            E()
            param_items.append(temp+"[]")
        else:
            param_items.append(temp)
        if token in [","]:
            D(param_items)

def D(param_items):
    # print("D")
    match(",")
    if token == "int" or token == "void":
        param(param_items)
        if token == ",":
            D(param_items)
    # print("end of D")

def param(param_items):
    # print("param")
    if token == "int" or token == "void":
        t = type_specifier()
        if is_ID(token):
            # print("match ID?")

            matchID("ID")
        if token == "[":
            E() # TODO array type
        param_items.append(t)
        # print("I appended: ", param_items)
    # print("end of param")

def E():
    # print("E")
    match("[")
    match("]")
    if token == "[":
        E()
    # print("end of E")

def compound_stmt(n, t):
    # print("compound_stmt")
    match("{")
    if token == "int" or token == "void":
        local_declarations(n, t)
    if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
        statement_list()
    match("}")
    # print("end of compound_stmt")

def local_declarations(n, t):
    # print("local_declarations")
    if token == "int" or token == "void":
        F(n, t)
    # print("end of local_declaration")

def F(n, t):
    # print("F")
    if token == "int" or token == "void":
        var_declaration(n, t)
        if token == "int" or token == "void":
            F(n, t)
    # print("end of F")

def statement_list():
    # print("statement_list")
    if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
        G()
    # print("end of statement_list")

def G():
    # print("G")
    if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
        statement()
        if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
            G()
    # print("end of G")

def statement():
    # print("statement")
    if token in ["(", ";"] or is_ID(token) or is_NUM(token):
        expression_stmt()
    if token in ["{"]:
        compound_stmt()
    if token in ["if"]:
        selection_stmt()
    if token in ["while"]:
        iteration_stmt()
    if token in ["return"]:
        return_stmt()
    # print("end of statement")

def expression_stmt():
    # print("expression_stmt")
    if token in ["("] or is_ID(token) or is_NUM(token):
        expression()
        match(";")
    else:
        match(";")
    # print("end of expression_stmt")

def selection_stmt():
    # print("selection_stmt")
    match("if")
    match("(")
    if token in ["("] or is_ID(token) or is_NUM(token):
        expression()
        match(")")
        if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
            statement()
            if token in ["else"]:
                N()
    # print("end of selection_stmt")

def N():
    # print("N")
    match("else")
    if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
        statement()
    # print("end of N")

def iteration_stmt():
    # print("iteration_stmt")
    match("while")
    match("(")
    if token in ["("] or is_ID(token) or is_NUM(token):
        expression()
        match(")")
        if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
            statement()
    # print("end of iteration_stmt")

def return_stmt():
    # print("return_stmt")
    match("return")
    # print(token)
    if token in ['(', ';'] or is_ID(token) or is_NUM(token):
        M()
    # print("end of return_stmt")


def M():
    if token in ["("] or is_ID(token) or is_NUM(token):
        expression()
        match(";")
    else:
        match(";")
        if not func_tab[-1][1] == 'void':
            raise ValueError
    # print("end of M")


def expression():
    lhs = ''
    rhs = ''
    # print("expression")
    if is_ID(token): # ID W
        is_array = False
        if var_tab[token[1]] == 'array':
            is_array = True
        save = token[1]
        matchID("ID") # in-line P
        if token in ["["] and is_array == True:
            match("[")
            if token in ["("] or is_ID(token) or is_NUM(token):
                temp = expression()
            match("]")
            lhs = temp
        else:
            lhs = var_tab[save]
            matchID("ID")
        # if var_tab[token[1]] == 'array':
        #     lhs = "int"
        # else:
        #     lhs = var_tab[token[1]]
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '=', '==', '>', '>=', '(']:
            rhs = W()
            if not lhs == rhs:
                raise ValueError
        return lhs

    if token in ["("]:
        match("(")
        if token in ["("] or is_ID(token) or is_NUM(token):
            lhs = expression()
            match(")")
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            R()
    if is_NUM(token):
        matchNUM("NUM")
        lhs = "int"
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            rhs = R()
            if not rhs == lhs:
                raise ValueError
        return lhs
    # print("this is the token: " + token)
    # print("end of expression")

def W():
    rhs = ''
    # print("W")
    # if token in ["["]: # P Q
    #     rhs = P()
    if token in ['!=', '*', '+', '-', '/', '<', '<=', '=', '==', '>', '>=']:
        rhs = Q()
        return rhs
    if token in ["("]: # ( args ) R
        match("(")
        if token in ["("] or is_ID(token) or is_NUM(token):
            args()
        match(")")
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            R()
        return rhs
    # print("end of W")


def Q():
    rhs = ''
    # print("Q")
    if token in ["="]:
        match("=")
        if token in ["("] or is_ID(token) or is_NUM(token):
            rhs = expression()
    else:
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            rhs = R()
    return rhs
    # print("end of Q")


def R():
    rhs = ''
    # print("R")
    if token in ["*", "/"]:
        rhs = J()
    if token in ["+", "-"]:
        rhs = H()
    if token in ['!=', '<', '<=', '==', '>', '>=']:
        rhs = L()
    return rhs
    # print("end of R")


# def var():
#     # print("var")
#     # print("match ID?")
#     matchID("ID")
#     if token in ["["]:
#         P()
#     # print("end of var")


def P():
    lhs = ''
    # print("P")
    if token in ["["]:
        match("[")
        if token in ["("] or is_ID(token) or is_NUM(token):
            lhs = expression()
        match("]")
        return lhs

    # print("end of P")


def simple_expression():
    # print("simple_expression")
    if token in ["("] or is_ID(token) or is_NUM(token):
        additive_expression()
        L()
    # print("end of simple_expression")


def L():
    lhs = ''
    # print("L")
    if token in ['!=', '<', '<=', '==', '>', '>=']:
        relop()
        if token in ["("] or is_ID(token) or is_NUM(token):
            lhs = additive_expression()
    return lhs
    # print("end of L")


def relop():
    # print("relop")
    if token in ["!="]:
        match("!=")
    elif token in ["<"]:
        match("<")
    elif token in ["<="]:
        match("<=")
    elif token in ["=="]:
        match("==")
    elif token in [">"]:
        match(">")
    else:
        match(">=")
    # print("end of relop")


def additive_expression():
    lhs = ''
    # print("additive_expression")
    if token in ["("] or is_ID(token) or is_NUM(token):
        lhs = term()
        if token in ["-", "+"]:
            rhs = H()
            if not lhs == rhs:
                raise ValueError
        return lhs
    # print("end of additive_expression")


def H():
    lhs = ''
    rhs = ''
    # print("H")
    if token in ["+", "-"]:
        addop()
        if token in ["("] or is_ID(token) or is_NUM(token):
            lhs = term()
            if token in ["-", "+"]:
                rhs = H()
                if not lhs == rhs:
                    raise ValueError
            return lhs
        else:
            raise ValueError

    # print("end of H")


def addop():
    # print("addop")
    # print("current token: " + token)
    if token in ["+"]:
        match("+")
    if token in ["-"]:
        match("-")
    # print("end of addop")


def term():
    lhs = ''
    rhs = ''
    # print("term")
    if token in ["("] or is_ID(token) or is_NUM(token):
        lhs = factor()
        if token in ["*", "/"]:
            rhs = J()
            if not lhs == rhs:
                raise ValueError
        return lhs
    # print("end of term")


def J():
    lhs = ''
    # print("J")
    if token in ["*", "/"]:
        mulop()
        if token in ["("] or is_ID(token) or is_NUM(token):
            lhs = factor()
            if token in ["*", "/"]:
                rhs = J()
                if rhs == lhs:
                    return lhs
                else:
                    raise ValueError
        return lhs
    # print("end of J")


def mulop():
    # print("mulop")
    if token in ["*"]:
        match("*")
    else:
        if token in ["/"]:
            match("/")
    # print("end of mulop")


def factor():
    lhs = ''
    # print("factor")
    # print("current token in factor: " + token)
    if token in ["("]:
        match("(")
        if token in ["("] or is_ID(token) or is_NUM(token):
            expression()
        match(")")
    elif is_ID(token):
        # print("match ID?")
        lhs = var_tab[token[1]]
        matchID("ID")
        is_array = V()
    else:
        if is_NUM(token):
            # print("match NUM?")
            matchNUM("NUM")
    if is_array == True:
        lhs = "array"
    return lhs
    # print("end of factor")


def V():
    is_array = False
    # print("V")
    if token in ["("]:
        match("(")
        args()
        match(")")
    else:
        is_array = P()
    return is_array
    # print("End of V")


def call():
    # print("call")
    if is_ID(token):
        # print("match ID?")
        matchID("ID")
    match("(")
    args()
    match(")")


def args():
    # print("args")
    if token in ["("] or is_ID(token) or is_NUM(token):
        arg_list()
    # print("end of args")


def arg_list():
    # print("arg_list")
    if token in ["("] or is_ID(token) or is_NUM(token):
        if token == 'void':
            raise ValueError
        expression()
    if token in [","]:
        K()
    # print("end of arglist")


def K():
    # print("K")
    if token in [","]:
        match(",")
        if token in ["("] or is_ID(token) or is_NUM(token):
            expression()
            if token in [","]:
                K()
        else:
            raise ValueError
    # print("end of K")
