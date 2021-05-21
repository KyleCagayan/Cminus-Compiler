token_list = []
token = ""
tokenlistNum = 0

var_tab  = {}
func_tab = []

ttts = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11' 't12', 't13', 't14', 't15', 't16',
        't17', 't18', 't19']

ttts_cntr = 0
instruc_cntr = 1


def is_ID(token):
     return isinstance(token, tuple) and token[0] == 'ID'
def is_NUM(token):
     return isinstance(token, tuple) and token[0] == 'NUM'
def start_CodeGenerator(tokenlist):
    global token, token_list
    token = tokenlist[tokenlistNum]
    token_list = tokenlist
    try:
        program()
        if token == "$":
            pass
            # print("ACCEPT")
            # print("var_tab: ",var_tab,"\nfunc_tab: ", func_tab)
        else:
            pass
            # print("REJECT")
            # print("var_tab: ",var_tab,"\nfunc_tab: ", func_tab)
    except ValueError:
        print("REJECT")
        print("var_tab: ",var_tab,"\nfunc_tab: ", func_tab)
def update():
    global token, tokenlistNum
    token = token_list[tokenlistNum]
def matchID(check):
    global tokenlistNum, n
    if token[0] == check:
        n = token[1]
        tokenlistNum = tokenlistNum + 1
        update()
def matchNUM(check):
    global tokenlistNum
    if token[0] == check:
        tokenlistNum += 1
        update()
def match(check):
    global tokenlistNum
    if token == check:
        tokenlistNum = tokenlistNum + 1
        update()


def program():
    declaration_list()


def declaration_list():
    if token == "int" or token == "void":
        declaration()
        A()


def A():
    if token == "int" or token == "void":
        declaration()
        if token == "int" or token == "void":
            A()


def declaration():
    n = ''
    if token == "int" or token == "void":
        t = type_specifier()
        if is_ID(token):
            n = token[1]
            matchID("ID")

        if token == "(" or token == ";" or token == "[":
            B(n, t)


def B(n, t):
    global instruc_cntr
    if token == ";" or token == "[":
        C(n, t)
    if token == "(":
        match("(")
        if token == "int" or token == "void":
            param_items = params()
            func_tab.append((n, t, param_items)) # name type (params)
            print('{:10s} {:10s} {:10s} {:10s} {}'.format(str(instruc_cntr), 'func', n, t, len(param_items)))
            instruc_cntr += 1
            for item in param_items:
                if item == 'void':
                    break
                print('{:10s} {:10s} {:10s} {:10s} {}'.format(str(instruc_cntr), 'param', " ", " ", item))
                instruc_cntr += 1
            for item in param_items:
                if item == 'void':
                    break
                print('{:10s} {:10s} {:10s} {:10s} {}'.format(str(instruc_cntr), 'alloc', '4', " ", item))
                instruc_cntr += 1
        match(")")
        if token == "{":
            compound_stmt(n, t)
            print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), "end", "func", func_tab[-1][0], " "))



def var_declaration(n, t):
    if token == "int" or token == "void":
        t = type_specifier()
        if is_ID(token):
            n = token[1]
            matchID("ID")
        if token == ";" or token == "[":
            C(n, t)


def C(n, t):
    global instruc_cntr
    save = ''
    if token == ";":
        match(";")
        var_tab[n] = t
        print('{:10s} {:10s} {:10s} {:10s} {:10s}'.format(str(instruc_cntr), "alloc", "4", "          ", n))
        instruc_cntr += 1
    else:
        match("[")
        if is_NUM(token):
            save = token
            matchNUM("NUM")
        match("]")
        match(";")
        var_tab[n] = "array"
        arr_size = 4 * int(save[1])
        print('{:10s} {:10s} {:10s} {:10s} {:10s}'.format(str(instruc_cntr), "alloc", str(arr_size), "          ", n))
        instruc_cntr += 1
        # TODO append to var_tab


def type_specifier():
    if token == "int":
        match("int")
        t = "int"
    if token == "void":
        match("void")
        t = "void"
    return t


def params():
    param_items = [] # "param 1, param 2, etc..."
    if token == "int":
        temp = token
        match("int")
        if is_ID(token):
            U(param_items, temp)
    elif token == "void":
        temp = token
        match("void")
        param_items.append(temp)
    #todo append to param_items
    return param_items

def U(param_items, temp):
    if is_ID(token):
        param_name = token[1]
        var_tab[param_name] = temp
        matchID("ID")
        if token in ["["]:
            E()
            param_items.append(param_name)
        else:
            param_items.append(param_name)
        if token in [","]:
            D(param_items)

def D(param_items):
    match(",")
    if token == "int" or token == "void":
        param(param_items)
        if token == ",":
            D(param_items)

def param(param_items):
    if token == "int" or token == "void":
        t = type_specifier()
        if is_ID(token):
            param_name = token[1]
            var_tab[param_name] = t
            matchID("ID")
        if token == "[":
            E() # TODO array type
        param_items.append(param_name)

def E():
    match("[")
    match("]")
    if token == "[":
        E()

def compound_stmt(n, t):
    match("{")
    if token == "int" or token == "void":
        local_declarations(n, t)
    if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
        statement_list()
    match("}")

def local_declarations(n, t):
    if token == "int" or token == "void":
        F(n, t)

def F(n, t):
    if token == "int" or token == "void":
        var_declaration(n, t)
        if token == "int" or token == "void":
            F(n, t)

def statement_list():
    if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
        G()

def G():
    if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
        statement()
        if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
            G()

def statement():
    n = ' '
    t = ' '
    if token in ["(", ";"] or is_ID(token) or is_NUM(token):
        expression_stmt()
    elif token in ["{"]:
        print("{:10s} {:10s}".format(str(instruc_cntr), "block"))
        compound_stmt(n, t)
        print("{:10s} {:10s} {:10s}".format(str(instruc_cntr), "end", "block"))
    elif token in ["if"]:
        selection_stmt()
    elif token in ["while"]:
        iteration_stmt()
    elif token in ["return"]:
        return_stmt()

def expression_stmt():
    if token in ["("] or is_ID(token) or is_NUM(token):
        expression()
        match(";")
    else:
        match(";")

def selection_stmt():
    match("if")
    match("(")
    if token in ["("] or is_ID(token) or is_NUM(token):
        expression()
        match(")")
        if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
            statement()
            if token in ["else"]:
                N()

def N():
    match("else")
    if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
        statement()

def iteration_stmt():
    match("while")
    match("(")
    if token in ["("] or is_ID(token) or is_NUM(token):
        expression()
        match(")")
        if token in ['(', ';', 'if', 'return', 'while', '{'] or is_ID(token) or is_NUM(token):
            statement()

def return_stmt():
    global instruc_cntr
    match("return")
    if token in ['(', ';'] or is_ID(token) or is_NUM(token):
        operandB = M()
        print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), "return", " ", " ", operandB))
        instruc_cntr += 1


def M():
    if token in ["("] or is_ID(token) or is_NUM(token):
        operandB = expression()
        match(";")
        return operandB
    else:
        match(";")


def expression():
    global ttts_cntr, instruc_cntr
    if is_ID(token): # ID W
        is_array = False
        if var_tab[token[1]] == 'array':
            is_array = True
        operandA = token[1]
        matchID("ID") # in-line P
        if token in ["["] and is_array == True:
            match("[")
            if token in ["("] or is_ID(token) or is_NUM(token):
                expression()
            match("]")
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '=', '==', '>', '>=', '(']:
            thingy = True
            while thingy:
                operation, operandB = W()
                if operation == 'assign':
                    print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation, operandA, " ", operandB))
                    instruc_cntr += 1
                elif operation in ['bre', 'brge', 'brg', 'brne', 'brle', 'brl']:
                    print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), 'comp', operandA, operandB, ttts[ttts_cntr]))
                    ttts_cntr += 1
                    instruc_cntr += 1
                    print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation, operandA, operandB, " "))
                    instruc_cntr += 1
                else:
                    print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation, operandA, operandB, ttts[ttts_cntr]))
                    operandB = ttts[ttts_cntr]
                    ttts_cntr += 1
                    instruc_cntr += 1
                if not token in ['!=', '*', '+', '-', '/', '<', '<=', '=', '==', '>', '>=', '(']:
                    thingy = False
            return operation, operandB
        else:
            operandB = operandA
            operation = ' '
            return operation, operandB
    elif token in ["("]:
        match("(")
        if token in ["("] or is_ID(token) or is_NUM(token):
            operation, operandB = expression()
            match(")")
            return operandB
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            operation, operandB = R()
            return operandB
    elif is_NUM(token):
        operandA = token[1]
        matchNUM("NUM")
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            operation, operandB = R()
            if operation == 'assign':
                print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation, operandA, " ", operandB))
                instruc_cntr += 1
            elif operation in ['bre', 'brge', 'brg', 'brne', 'brle', 'brl']:
                print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), 'comp', operandA, operandB, ttts[ttts_cntr]))
                ttts_cntr += 1
                instruc_cntr += 1
                print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation, operandA, operandB, " "))
                instruc_cntr += 1
            else:
                print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation, operandA, operandB, ttts[ttts_cntr]))
                operandB = ttts[ttts_cntr]
                ttts_cntr += 1
                instruc_cntr += 1
            return operation, operandB
        else:
            operandB = operandA
            operation = ' '
            return operation, operandB

def W():
    if token in ['!=', '*', '+', '-', '/', '<', '<=', '=', '==', '>', '>=']:
        if token == '=':
            operation = 'assign'
            operationA, operandB = Q()
            if not (operationA == None or operandB == None):
                return operation, operandB
            else:
                return " ", " "
        operation, operandB = Q()
        return operation, operandB
    elif token in ["("]: # ( args ) R
        match("(")
        if token in ["("] or is_ID(token) or is_NUM(token):
            args()
        match(")")
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            operation, operandB = R()
            return operation, operandB


def Q():
    if token in ["="]:
        match("=")
        if token in ["("] or is_ID(token) or is_NUM(token):
            operation, operandB = expression()
            return operation, operandB
    else:
        if token in ['!=', '*', '+', '-', '/', '<', '<=', '==', '>', '>=']:
            operation, operandB = R()
            return operation, operandB


def R():
    if token in ["*", "/"]:
        operation, operandB = J()
        return operation, operandB
    elif token in ["+", "-"]:
        operation, operandB = H()
        return operation, operandB
    elif token in ['!=', '<', '<=', '==', '>', '>=']:
        operation, operandB = L()
        return operation, operandB


def P():
    if token in ["["]:
        match("[")
        if token in ["("] or is_ID(token) or is_NUM(token):
            lhs = expression()
        match("]")
        return lhs

def L():
    if token in ['!=', '<', '<=', '==', '>', '>=']:
        operation = relop()
        if token in ["("] or is_ID(token) or is_NUM(token):
            operandB = additive_expression()
        return operation, operandB


def relop():
    if token in ["!="]:
        operation = 'bre'
        match("!=")
    elif token in ["<"]:
        operation = 'brge'
        match("<")
    elif token in ["<="]:
        operation = 'brg'
        match("<=")
    elif token in ["=="]:
        operation = 'brne'
        match("==")
    elif token in [">"]:
        operation = 'brle'
        match(">")
    else:
        operation = 'brl'
        match(">=")
    return operation

def additive_expression():
    global ttts_cntr, instruc_cntr
    if token in ["("] or is_ID(token) or is_NUM(token):
        operandB = term()
        if token in ["-", "+"]:
            operation_2, operandB_2 = H()
            print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation, operandB, operandB_2, ttts[ttts_cntr]))
            operandB_2 = ttts[ttts_cntr]
            ttts_cntr += 1
            instruc_cntr += 1
            return operandB_2
        return operandB


def H():
    global instruc_cntr, ttts_cntr
    if token in ["+", "-"]:
        operation = addop()
        if token in ["("] or is_ID(token) or is_NUM(token):
            operandB = term()
            if token in ["-", "+"]:
                operation_2, operandB_2 = H()
                print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation_2, operandB, operandB_2, ttts[ttts_cntr]))
                operandB_2 = ttts[ttts_cntr]
                ttts_cntr += 1
                instruc_cntr += 1
                return operation, operandB_2
            return operation, operandB


def addop():
    if token in ["+"]:
        operation = "add"
        match("+")
        return operation
    if token in ["-"]:
        operation = 'sub'
        match("-")
        return operation


def term():
    global ttts_cntr, instruc_cntr
    if token in ["("] or is_ID(token) or is_NUM(token):
        operandB = factor()
        if token in ["*", "/"]:
            operation, operandB_2 = J()
            print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation, operandB, operandB_2, ttts[ttts_cntr]))
            operandB_2 = ttts[ttts_cntr]
            ttts_cntr += 1
            instruc_cntr += 1
            return operandB_2
        return operandB


def J():
    global instruc_cntr, ttts_cntr
    if token in ["*", "/"]:
        operation = mulop()
        if token in ["("] or is_ID(token) or is_NUM(token):
            operandB = factor()
            if token in ["*", "/"]:
                operation_2, operandB_2 = J()
                print("{:10s} {:10s} {:10s} {:10s} {}".format(str(instruc_cntr), operation_2, operandB, operandB_2, ttts[ttts_cntr]))
                operandB_2 = ttts[ttts_cntr]
                ttts_cntr += 1
                instruc_cntr += 1
                return operation, operandB_2
            return operation, operandB


def mulop():
    if token in ["*"]:
        operation = "mult"
        match("*")
        return operation
    else:
        if token in ["/"]:
         operation = "div"
        match("/")
        return operation


def factor():
    if token in ["("]:
        match("(")
        if token in ["("] or is_ID(token) or is_NUM(token):
            operation, operandB  = expression()
        match(")")
        return operandB
    elif is_ID(token):
        operandB = token[1]
        matchID("ID")
        V()
        return operandB
    else:
        if is_NUM(token):
            operandB = token[1]
            matchNUM("NUM")
            return operandB


def V():
    is_array = False
    if token in ["("]:
        match("(")
        args()
        match(")")
    else:
        is_array = P()
    return is_array


def call():
    if is_ID(token):
        matchID("ID")
    match("(")
    args()
    match(")")


def args():
    if token in ["("] or is_ID(token) or is_NUM(token):
        arg_list()


def arg_list():
    if token in ["("] or is_ID(token) or is_NUM(token):
        expression()
    if token in [","]:
        K()


def K():
    if token in [","]:
        match(",")
        if token in ["("] or is_ID(token) or is_NUM(token):
            expression()
            if token in [","]:
                K()
