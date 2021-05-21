
# LEXICAL ANALYZER

import re

def comment_remover(text):
    return re.sub(r"(//.*\n)|(/\*(.|\n)*\*/)", '', text)


# Lexical Conventions of C
keyword = re.compile(r'^else|if|int|return|void|while')
identification = re.compile(r'^[a-zA-Z]+')
numbers = re.compile(r'^[0-9]+')
operations = re.compile(r'^(\!=)|\==|\+|\-|\*|\/|(\<=)|\<|(\>=)|\>|\=|\;|\,|\(|\)|\[|\]|\{|\}')

metachar = re.compile(
    r'\+|\-|\*|\/|(\<=)|\<|(\>=)|\>|\==|\!|\=|\;|\,|\(|\)|\[|\]|\{|\}|\@|\#|\$|\%|\^|\&|\?|\.|\,|\'|\;|\||\\|\_')
regular = re.compile(r'\w')
inputlist = []
counter = 0

tokenlist = []

def isRegular(s, slen):
    global counter
    lexeme = ''
    while counter < slen:
        char = s[counter]
        if char.isspace():
            lexeme += char
            counter += 1
            continue
        if regular.search(char.strip()):
            lexeme += char
            counter += 1
            if counter == slen:
                inputlist.append(lexeme)
        else:
            inputlist.append(lexeme)
            isMeta(s, slen)


def isMeta(s, slen):
    global counter
    lexeme = ''
    while counter < slen:
        char = s[counter]
        if char.isspace():
            lexeme += char
            counter += 1
            continue
        if metachar.search(char.strip()):
            lexeme += char
            counter += 1
            if (counter == slen):
                inputlist.append(lexeme)
        else:
            inputlist.append(lexeme)
            isRegular(s, slen)


def start(s, slen):
    if s[0] == metachar.search(s[0]):
        isMeta(s, slen)
    else:
        isRegular(s, slen)


def tokenizer(inputlist):
    for item in inputlist:
        s = item.strip()
        itemStringCounter = 0
        a = s[itemStringCounter:]
        while itemStringCounter < s.__len__():
            if s[itemStringCounter].isspace():
                itemStringCounter += 1
                continue
            elif keyword.search(s[itemStringCounter:]):
                # print('KEYWORD: ' + keyword.search(s[itemStringCounter:])[0])
                tokenlist.append(keyword.search(s[itemStringCounter:])[0])
                itemStringCounter += keyword.search(s[itemStringCounter:])[0].__len__()
            elif identification.search(s[itemStringCounter:]):
                # print(identification.search(s[itemStringCounter:]))
                # print('IDENTIFIER: ' + identification.search(s[itemStringCounter:])[0])
                tokenlist.append(('ID', identification.search(s[itemStringCounter:])[0]))
                # tokenlist.append('ID')
                itemStringCounter += identification.search(s[itemStringCounter:])[0].__len__()
            elif numbers.search(s[itemStringCounter:]):
                # print('NUMBER: ' + numbers.search(s[itemStringCounter:])[0])
                tokenlist.append(("NUM",numbers.search(s[itemStringCounter:])[0]))
                # tokenlist.append("NUM")
                itemStringCounter += numbers.search(s[itemStringCounter:])[0].__len__()
            elif operations.search(s[itemStringCounter:]):
                # print(operations.search(s[itemStringCounter:])[0])
                tokenlist.append(operations.search(s[itemStringCounter:])[0])
                itemStringCounter += operations.search(s[itemStringCounter:])[0].__len__()
            else:
                # print('ERROR ' + s[itemStringCounter:][0])
                itemStringCounter += s[itemStringCounter:][0].__len__()


def line_printer(f):
    line = f.readline()
    while line:
        print('INPUT: ' + line)
        if not line:
            break
        line = f.readline()



=============================================================================================================================
=============================================================================================================================
