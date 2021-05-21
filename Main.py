# MAIN 
============================
import sys
from CompilerProject1 import comment_remover, start, tokenizer, inputlist, tokenlist
# from CompilerProject2 import start_parser
# from SemanticAnalyzer import start_parser
from testing import start_parser

if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    # line_printer(f)

    string = f.read()
    # print(string)

    # newS = string.replace(" ", "").replace('\n', '')

    temp_string = comment_remover(string)
    newS = temp_string.replace('\n', '')
    # print(newS)

    cleanString = comment_remover(newS).replace("\n", "").strip()
    slen = cleanString.replace('\n', '').__len__()
    start(cleanString, slen)
    tokens = tokenizer(inputlist)
    tokenlist.append("$")
    tokenlist.append("&")

    # for token in tokenlist:
    #     print(token)

    # P2
    start_parser(tokenlist)

===================================================================================================================
===================================================================================================================
