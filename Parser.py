
# PARSER

token_list = []
token = ""
tokenlistNum = 0


def start_parser(tokenlist):
    global token, token_list
    token = tokenlist[tokenlistNum]
    token_list = tokenlist
    program()
    if token == "$":
        print("ACCEPT")
    else:
        print("REJECT")


def update():
    global token, tokenlistNum
    token = token_list[tokenlistNum]


def end():
    global token
    token = token_list[token_list.__len__() - 1]


def match(check):
    # print("match                               " + token + " VS " + check)
    global tokenlistNum
    if token == check:
        tokenlistNum = tokenlistNum + 1
        update()
    else:
        end()


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
    # print("declaration")
    if token == "int" or token == "void":
        type_specifier()
        if token == "ID":
            match("ID")
        if token == "(" or token == ";" or token == "[":
            B()
    # print("end of declaration")


def B():
    # print("B")
    if token == ";" or token == "[":
        C()
    if token == "(":
        match("(")
        if token == "int" or token == "void":
            params()
        match(")")
        if token == "{":
            compound_stmt()
    # print("end of B")


def var_declaration():
    # print("var_declaration")
    if token == "int" or token == "void":
        type_specifier()
        match("ID")
        if token == ";" or token == "[":
            C()
    # print("end of var_declaration")


def C():
    # print("C")
    if token == ";":
        match(";")
    else:
        match("[")
        match("NUM")
        match("]")
        match(";")
    # print("end of C")


def type_specifier():
    # print("type_specifier")
    if token == "int":
        match("int")
    if token == "void":
        match("void")
    # print("end of type_specifier")


def params():
    # print("params")
    if token == "int":
        match("int")
        if token == "ID":
            U()
    elif token == "void":
        match("void")
        if token == "ID":
            T()
    # print("end of params")


def T():
    # print("T")
    if token == "ID":
        U()
    # print("end of T")


def U():
    # print("U")
    if token == "ID":
        match("ID")
        if token in ["["]:
            E()
        if token in [","]:
            D()
    # print("end of U")


def param_list():
    # print("param_list")
    if token == "int" or token == "void":
        param()
        if token == ",":
            D()
    # print("end of param_list")


def D():
    # print("D")
    match(",")
    if token == "int" or token == "void":
        param()
        if token == ",":
            D()
    # print("end of D")


def param():
    # print("param")
    if token == "int" or token == "void":
        type_specifier()
        match("ID")
        if token == "[":
            E()
    # print("end of param")


def E():
    # print("E")
    match("[")
    match("]")
    if token == "[":
        E()
    # print("end of E")


def compound_stmt():
    # print("compound_stmt")
    match("{")
    if token == "int" or token == "void":
        local_declarations()
    if token in ["(", ";", "ID", "NUM", "if", "return", "while", "{"]:
        statement_list()
    match("}")
    # print("end of compound_stmt")


def local_declarations():
    # print("local_declarations")
    if token == "int" or token == "void":
        F()
    # print("end of local_declaration")


def F():
    # print("F")
    if token == "int" or token == "void":
        var_declaration()
        if token == "int" or token == "void":
            F()
    # print("end of F")


def statement_list():
    # print("statement_list")
    if token == "(" or token == ";" or token == "ID" or token == "NUM" or token == "if" or token == "return" or token == "while" or token == "{":
        G()
    # print("end of statement_list")


def G():
    # print("G")
    if token == "(" or token == ";" or token == "ID" or token == "NUM" or token == "if" or token == "return" or token == "while" or token == "{":
        statement()
        if token == "(" or token == ";" or token == "ID" or token == "NUM" or token == "if" or token == "return" or token == "while" or token == "{":
            G()
    # print("end of G")


def statement():
    # print("statement")
    if token in ["(", ";", "ID", "NUM"]:
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
    if token in ["(", "ID", "NUM"]:
        expression()
        match(";")
    else:
        match(";")
    # print("end of expression_stmt")


def selection_stmt():
    # print("selection_stmt")
    match("if")
    match("(")
    if token in ["(", "ID", "NUM"]:
        expression()
        match(")")
        if token in ['(', ';', 'ID', 'NUM', 'if', 'return', 'while', '{']:
            statement()
            if token in ["else"]:
                N()
    # print("end of selection_stmt")


def N():
    # print("N")
    match("else")
    if token in ['(', ';', 'ID', 'NUM', 'if', 'return', 'while', '{']:
        statement()
    # print("end of N")


def iteration_stmt():
    # print("iteration_stmt")
    match("while")
    match("(")
    if token in ["(", "ID", "NUM"]:
        expression()
        match(")")
        if token in ['(', ';', 'ID', 'NUM', 'if', 'return', 'while', '{']:
            statement()
    # print("end of iteration_stmt")


def return_stmt():
    # print("return_stmt")
    match("return")
    if token in ['(', ';', 'ID', 'NUM']:
        M()
    # print("end of return_stmt")


def M():
    if token in ["(", "ID", "NUM"]:
        expression()
        match(";")
    else:
        match(";")
    # print("end of M")


def expression():
    # print("expression")
    if token in ["ID"]:
        match("ID")
        W()
    if token in ["("]:
        match("(")
        if token in ["(", "ID", "NUM"]:
            expression()
            match(")")
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            R()
    if token in ["NUM"]:
        match("NUM")
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            R()
    # print("this is the token: " + token)
    # print("end of expression")


def W():
    # print("W")
    if token in ["["]:
        P()
    if token in ['!=', '*', '+', '-', '/', '<', '<=', '=', '==', '>', '>=']:
        Q()
    if token in ["("]:
        match("(")
        if token in ["(", "ID", "NUM"]:
            args()
        match(")")
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            R()
    # print("end of W")


def Q():
    # print("Q")
    if token in ["="]:
        match("=")
        if token in ["(", "ID", "NUM"]:
            expression()
    else:
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            R()
    # print("end of Q")


def R():
    # print("R")
    J()
    H()
    L()
    # print("end of R")


def var():
    # print("var")
    match("ID")
    if token in ["["]:
        P()
    # print("end of var")


def P():
    # print("P")
    if token in ["["]:
        match("[")
        if token in ["(", "ID", "NUM"]:
            expression()
        match("]")
    # print("end of P")


def simple_expression():
    # print("simple_expression")
    if token in ["(", "ID", "NUM"]:
        additive_expression()
        L()
    # print("end of simple_expression")


def L():
    # print("L")
    if token in ['!=', '<', '<=', '==', '>', '>=']:
        relop()
        if token in ["(", "ID", "NUM"]:
            additive_expression()
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
    # print("additive_expression")
    if token in ["(", "ID", "NUM"]:
        term()
        if token in ["-", "+"]:
            H()
    # print("end of additive_expression")


def H():
    # print("H")
    if token in ["+", "-"]:
        addop()
        if token in ["(", "ID", "NUM"]:
            term()
            if token in ["-", "+"]:
                H()
        else:
            end()
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
    # print("term")
    if token in ["(", "ID", "NUM"]:
        factor()
        J()
    # print("end of term")


def J():
    # print("J")
    if token in ["*", "/"]:
        mulop()
        if token in ["(", "ID", "NUM"]:
            factor()
            if token in ["*", "/"]:
                J()
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
    # print("factor")
    # print("current token in factor: " + token)
    if token in ["("]:
        match("(")
        if token in ["(", "ID", "NUM"]:
            expression()
        match(")")
    elif token in ["ID"]:
        match("ID")
        V()
    else:
        match("NUM")
    # print("end of factor")


def V():
    # print("V")
    if token in ["("]:
        match("(")
        args()
        match(")")
    else:
        P()
    # print("End of V")


def call():
    # print("call")
    match("ID")
    match("(")
    args()
    match(")")


def args():
    # print("args")
    if token in ["(", "ID", "NUM"]:
        arg_list()
    # print("end of args")


def arg_list():
    # print("arg_list")
    if token in ["(", "ID", "NUM"]:
        expression()
    if token in [","]:
        K()
    # print("end of arglist")


def K():
    # print("K")
    if token in [","]:
        match(",")
        if token in ["(", "ID", "NUM"]:
            expression()
            if token in [","]:
                K()
        else:
            end()
    # print("end of K")


======================================================================================================================
======================================================================================================================
