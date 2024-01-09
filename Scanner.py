from enum import Enum
import re
import tkinter as tk
import pandas
import pandas as pd
import graphviz


class Token_type(Enum):
    # listing all tokens type
    OpenPrac = 1
    ClosedPrac = 2
    DoTimes = 3
    Else = 4
    When = 5
    If = 6
    Dot = 7
    Semicolon = 8
    EqualOp = 9
    LessThanOrEqualOp = 10
    GreaterThanOrEqualOp = 11
    NotEqualOp = 12
    PlusOp = 13
    MinusOp = 14
    MultiplyOp = 15
    DivideOp = 16
    Identifier = 17
    Constant = 18
    DoubleQuotation = 19
    Error = 20
    Mod = 21
    Rem = 22
    Incf = 23
    Decf = 24
    TRUE = 25
    FALSE = 26
    Setq = 27
    Read = 28
    Write = 29
    Comma = 30
    Writeline = 31
    Not = 32
    And = 33
    Or = 34
    Defconstant = 35
    String = 36


class Token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'Token_type': self.token_type
        }


# Reserved word Dictionary
ReservedWords = {
    "IF": Token_type.If,
    "DOTIMES": Token_type.DoTimes,
    "ELSE": Token_type.Else,
    "WHEN": Token_type.When,
    "T": Token_type.TRUE,
    "NIL": Token_type.FALSE,
    "READ": Token_type.Read,
    "WRITE": Token_type.Write,
    "SETQ": Token_type.Setq,
    "WRITELINE": Token_type.Writeline,
    "DEFCONSTANT": Token_type.Defconstant
}
# operators dictionary
Operators = {
    "(": Token_type.OpenPrac,
    ")": Token_type.ClosedPrac,
    ".": Token_type.Dot,
    ";": Token_type.Semicolon,
    "=": Token_type.EqualOp,
    "+": Token_type.PlusOp,
    "-": Token_type.MinusOp,
    "*": Token_type.MultiplyOp,
    "/": Token_type.DivideOp,
    "<=": Token_type.LessThanOrEqualOp,
    ">=": Token_type.GreaterThanOrEqualOp,
    "<>": Token_type.NotEqualOp,
    "MOD": Token_type.Mod,
    "REM": Token_type.Rem,
    "INCF": Token_type.Incf,
    "DECF": Token_type.Decf,
    ",": Token_type.Comma,
    "\"": Token_type.DoubleQuotation
}

# logic operators dictionary
Logic_operators = {
    "NOT": Token_type.Not,
    "AND": Token_type.And,
    "OR": Token_type.Or
}


def split(text):
    i = 0
    tokenlist = []
    while i < len(text):
        str = ""
        if text[i] == ' ' or text[i] == '\n':
            i += 1

        elif text[i] == '(' or text[i] == ')' or text[i] == "'":
            tokenlist.append(text[i])
            i += 1

        elif text[i] == '#':
            i += 1
            if text[i] == '|':
                i += 1
                while i + 1 < len(text) and (text[i] != '|' or text[i + 1] != '#'):
                    i += 1
                i += 2

        elif text[i] == ';':
            while i < len(text) and text[i] != '\n':
                i += 1

        elif text[i] == '\"':
            str += text[i]
            i += 1
            while i < len(text) and text[i] != '\"':
                str += text[i]
                i += 1
            str += text[i]
            tokenlist.append(str)
            i += 1

        elif (text[i] != '(') and (text[i] != ')') and (text[i] != '#') and (text[i] != '\'') and (text[i] != '\"') and \
                text[i] != ' ' and ((text[i] < '0') or (text[i] > '9')):

            while i < len(text) and (text[i] != '(') and (text[i] != ')') and (text[i] != '#') and (
                    text[i] != '\'') and (text[i] != '\"') and text[i] != ' ':
                str += text[i]

                i += 1

            tokenlist.append(str)

        elif (text[i] >= '0') and (text[i] <= '9'):
            while i < len(text) and (text[i] >= '0') and (text[i] <= '9'):
                str += text[i]
                i += 1
            tokenlist.append(str)

        else:
            i += 1

    return tokenlist


Tokens = []
graph = graphviz.Digraph(comment='dfa')


def find_token(text):
    lexeme = split(text)
    for l in lexeme:
        characters = list(l)
        upper_l = l.upper()

        # Reserved Words
        if upper_l in ReservedWords:
            t = Token(l, ReservedWords[upper_l])
            Tokens.append(t)
            currentpos = 'r0'
            for currentchar in characters:
                correctFormat(currentpos) if currentpos != 'reject' else wrongFormat(currentpos)
                currentpos = NextPosReservedWords(currentchar, currentpos)

            correctFormat('r0')
            graph.format = 'png'
            graph.render('dfa_ReservedWords')
            graph

        # operators
        elif upper_l in Operators:
            t = Token(l, Operators[upper_l])
            Tokens.append(t)
            currentpos = 'o0'
            for currentchar in characters:
                correctFormat(currentpos) if currentpos != 'reject' else wrongFormat(currentpos)
                currentpos = NextPosOperators(currentchar, currentpos)

            correctFormat('o0')
            graph.format = 'png'
            graph.render('dfa_Operators')
            graph

        # logic operators
        elif upper_l in Logic_operators:
            t = Token(l, Logic_operators[upper_l])
            Tokens.append(t)
            currentpos = 'l0'
            characters = list(l)
            for currentchar in characters:
                correctFormat(currentpos) if currentpos != 'reject' else wrongFormat(currentpos)
                currentpos = NextPosLogic_operators(currentchar, currentpos)
            graph.node('l00', shape='point', width='0.0002', height='0.0002')
            graph.node('l0')
            graph.node('l1')
            graph.node('l2')
            graph.node('l3')
            graph.node('l4')
            graph.node('l5')
            graph.node('l6', shape='doublecircle')
            graph.node('l99', 'reject')

            graph.edge('l00', 'l0', arrowhead='vee')
            graph.edge('l0', 'l1', label='a,A')
            graph.edge('l1', 'l2', label='n,N')
            graph.edge('l2', 'l6', label='d,D')
            graph.edge('l0', 'l3', label='n,N')
            graph.edge('l3', 'l4', label='o,O')
            graph.edge('l4', 'l6', label='t,T')
            graph.edge('l0', 'l5', label='o,O')
            graph.edge('l5', 'l6', label='r,R')
            graph.edge('l6', 'l99', label='*')
            graph.edge('l99', 'l99', label='*')

            correctFormat('l0')
            graph.format = 'png'
            graph.render('dfa_Logic_operators')
            graph


        # identefier
        elif re.match("^[a-zA-Z][_|-|+|!|@|#|$|%|&|/|<|>|=|,|.|a-zA-Z0-9]*$", l):
            t = Token(l, Token_type.Identifier)
            Tokens.append(t)
            currentpos = 'i0'
            for currentchar in characters:
                correctFormat(currentpos) if currentpos != 'reject' else wrongFormat(currentpos)
                currentpos = NextPosIdentifier(currentchar, currentpos)

            correctFormat('i0')
            graph.format = 'png'
            graph.render('dfa_Identifier')
            graph

        # Constant
        elif re.match("^([0-9]+(.[0-9]+)?)$|^((.[0-9]+)?)$", l):
            t = Token(l, Token_type.Constant)
            Tokens.append(t)
            currentpos = 'c0'
            for currentchar in characters:
                correctFormat(currentpos) if currentpos != 'reject' else wrongFormat(currentpos)
                currentpos = NextPosConstant(currentchar, currentpos)
            graph.node(str(currentpos))

            correctFormat('c0')
            graph.format = 'png'
            graph.render('dfa_Constant')
            graph
        elif re.match("^\".*\"$", l):
            t = Token(l, Token_type.String)
            Tokens.append(t)


        else:
            t = Token(l, Token_type.Error)
            Tokens.append(t)
        if currentpos == 'i1' or 'r21' or 'o14' or 'c2':
            correctFormat(currentpos)


# GUI
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)
x1 = entry1.get()


def Scan():
    global Tokens
    x1 = entry1.get()
    Tokens = []
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    print(df)
    label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)
    label4 = tk.Label(root, text="Token_type" + x1, font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(
    text='Scan',
    command=Scan,
    bg='brown',
    fg='white',
    font=('helvetica', 9, 'bold')
)
canvas1.create_window(200, 180, window=button1)
root.mainloop()


# DFA Implementation
def correctFormat(node):
    graph.node(str(node), fillcolor='green', style='filled')


def wrongFormat(node):
    graph.node(str(node), fillcolor='red', style='filled')


def NextPosReservedWords(currentchar, currentpos):
    r0_temp = ''
    if currentchar.lower() == 't':
        r0_temp = 'r21'
    elif currentchar.lower() == 'i':
        r0_temp = 'r1'
    elif currentchar.lower() == 'd':
        r0_temp = 'r2'
    elif currentchar.lower() == 'e':
        r0_temp = 'r8'
    elif currentchar.lower() == 'w':
        r0_temp = 'r11'
    elif currentchar.lower() == 'n':
        r0_temp = 'r14'
    elif currentchar.lower() == 'r':
        r0_temp = 'r16'
    elif currentchar.lower() == 's':
        r0_temp = 'r26'
    r2_temp = ''
    if currentchar.lower() == 'o':
        r2_temp = 'r3'
    if currentchar.lower() == 'e':
        r2_temp = 'r29'
    r11_temp = ''
    if currentchar.lower() == 'r':
        r11_temp = 'r19'
    elif currentchar.lower() == 'h':
        r11_temp = 'r12'
    elif currentchar.lower() == 'h':
        r11_temp = 'r12'
    pos = {
        'r0': r0_temp,
        'r1': 'r21' if currentchar.lower() == 'f' else 'r1',
        'r2': r2_temp,
        'r29': 'r30' if currentchar.lower() == 'f' else 'r29',
        'r30': 'r31' if currentchar.lower() == 'c' else 'r30',
        'r31': 'r32' if currentchar.lower() == 'o' else 'r31',
        'r32': 'r33' if currentchar.lower() == 'n' else 'r32',
        'r33': 'r34' if currentchar.lower() == 's' else 'r33',
        'r34': 'r35' if currentchar.lower() == 't' else 'r34',
        'r35': 'r36' if currentchar.lower() == 'a' else 'r35',
        'r36': 'r37' if currentchar.lower() == 'n' else 'r36',
        'r37': 'r21' if currentchar.lower() == 't' else 'r37',
        'r3': 'r4' if currentchar.lower() == 't' else 'r3',
        'r4': 'r5' if currentchar.lower() == 'i' else 'r4',
        'r5': 'r6' if currentchar.lower() == 'm' else 'r5',
        'r6': 'r7' if currentchar.lower() == 'e' else 'r6',
        'r7': 'r21' if currentchar.lower() == 's' else 'r7',
        'r8': 'r9' if currentchar.lower() == 'l' else 'r8',
        'r9': 'r10' if currentchar.lower() == 's' else 'r9',
        'r10': 'r22' if currentchar.lower() == 'e' else 'r10',
        'r22': 'r23' if currentchar.lower() == 'l' else 'r22',
        'r23': 'r24' if currentchar.lower() == 'i' else 'r23',
        'r24': 'r25' if currentchar.lower() == 'n' else 'r24',
        'r25': 'r21' if currentchar.lower() == 'e' else 'r25',
        'r26': 'r27' if currentchar.lower() == 'e' else 'r26',
        'r27': 'r28' if currentchar.lower() == 't' else 'r27',
        'r28': 'r21' if currentchar.lower() == 'q' else 'r28',
        'r11': r11_temp,
        'r12': 'r13' if currentchar.lower() == 'e' else 'r12',
        'r13': 'r21' if currentchar.lower() == 'n' else 'r13',
        'r14': 'r15' if currentchar.lower() == 'i' else 'r14',
        'r15': 'r21' if currentchar.lower() == 'l' else 'r15',
        'r16': 'r17' if currentchar.lower() == 'e' else 'r16',
        'r17': 'r18' if currentchar.lower() == 'a' else 'r17',
        'r18': 'r21' if currentchar.lower() == 'd' else 'r18',
        'r19': 'r20' if currentchar.lower() == 'i' else 'r19',
        'r20': 'r10' if currentchar.lower() == 't' else 'r20',
        'r99': 'r99'
    }
    return pos[currentpos]


def NextPosOperators(currentchar, currentpos):
    o0_temp = ''
    if currentchar == '>':
        o0_temp = 'o1'
    elif currentchar == '<':
        o0_temp = 'o2'
    elif currentchar in ['+', '-', '*', '/', ')', '\'', '(', '=', '.', ';', ',', ':', '"']:
        o0_temp = 'o14'
    elif currentchar.lower() == 'r':
        o0_temp = 'o3'
    elif currentchar.lower() == 'i':
        o0_temp = 'o5'
    elif currentchar.lower() == 'd':
        o0_temp = 'o8'
    elif currentchar.lower() in 'm':
        o0_temp = 'o12'

    pos = {
        'o0': o0_temp,
        'o1': 'o14' if currentchar == '=' else 'o1',
        'o2': 'o14' if currentchar == '>,=' else 'o2',
        'o3': 'o4' if currentchar.lower() == 'e' else 'o3',
        'o4': 'o14' if currentchar.lower() == 'm' else 'o4',
        'o5': 'o6' if currentchar.lower() == 'n' else 'o5',
        'o6': 'o7' if currentchar.lower() == 'c' else 'o6',
        'o7': 'o14' if currentchar.lower() == 'f' else 'o7',
        'o8': 'o6' if currentchar.lower() == 'e' else 'o8',
        'o12': 'o13' if currentchar.lower() == 'o' else 'o12',
        'o13': 'o14' if currentchar.lower() == 'm' else 'o13',
        'o99': 'o99'
    }
    return pos[currentpos]


def NextPosLogic_operators(currentchar, currentpos):
    l0_temp = ''
    if currentchar == 'a':
        l0_temp = 'l1'
    elif currentchar == 'n':
        l0_temp = 'l3'
    elif currentchar == 'o':
        l0_temp = 'l5'

    pos = {
        'l0': l0_temp,
        'l1': 'l2' if currentchar.lower() == 'n' else 'l1',
        'l2': 'l6' if currentchar.lower() == 'd' else 'l2',
        'l3': 'l4' if currentchar.lower() == 'o' else 'l3',
        'l4': 'l6' if currentchar.lower() == 't' else 'l4',
        'l5': 'l6' if currentchar.lower() == 'r' else 'l5',
        'l99': 'l99'
    }
    return pos[currentpos]


def NextPosIdentifier(currentchar, currentpos):
    pos = {
        'i0': 'i1' if currentchar >= 'A' and currentchar <= 'z' else 'i99',
        'i1': 'i1' if (currentchar >= 'A' and currentchar <= 'z') or
                      (currentchar >= '0' and currentchar <= '9') or
                      (currentchar in '_-+!@#$%&/<>=,.') else 'i99',
        'i99': 'i99'
    }
    return pos[currentpos]


def NextPosConstant(currentchar, currentpos):
    c0_temp = ''
    if currentchar >= '0' and currentchar <= '9':
        c0_temp = 'c0'
    elif currentchar == ".":
        c0_temp = 'c1'
    pos = {
        'c0': c0_temp,
        'c1': 'c2' if currentchar >= '0' and currentchar <= '9' else 'c99',
        'c2': 'c2' if currentchar >= '0' and currentchar <= '9' else 'c99',
        'c99': 'c99'
    }
    return pos[currentpos]


graph.node('r00', shape='point', width='0.0002', height='0.0002')
graph.node('r0')
graph.node('r1')
graph.node('r2')
graph.node('r3')
graph.node('r4')
graph.node('r5')
graph.node('r6')
graph.node('r7')
graph.node('r8')
graph.node('r9')
graph.node('r10')
graph.node('r11')
graph.node('r12')
graph.node('r13')
graph.node('r14')
graph.node('r15')
graph.node('r16')
graph.node('r17')
graph.node('r18')
graph.node('r19')
graph.node('r20')
graph.node('r21', shape='doublecircle')
graph.node('r22', shape='doublecircle')
graph.node('r23')
graph.node('r24')
graph.node('r25')
graph.node('r26')
graph.node('r27')
graph.node('r28')
graph.node('r29')
graph.node('r30')
graph.node('r31')
graph.node('r32')
graph.node('r33')
graph.node('r34')
graph.node('r35')
graph.node('r36')
graph.node('r37')
graph.node('r99', 'reject')

graph.edge('r00', 'r0', arrowhead='vee')
graph.edge('r0', 'r21', label='t,T')
graph.edge('r0', 'r1', label='i,I')
graph.edge('r1', 'r21', label='f,F')
graph.edge('r0', 'r2', label='d,D')
graph.edge('r2', 'r3', label='o,O')
graph.edge('r3', 'r4', label='t,T')
graph.edge('r4', 'r5', label='i,I')
graph.edge('r5', 'r6', label='m,M')
graph.edge('r6', 'r7', label='e,E')
graph.edge('r7', 'r21', label='s,S')
graph.edge('r0', 'r8', label='e,E')
graph.edge('r8', 'r9', label='l,L')
graph.edge('r9', 'r10', label='s,S')
graph.edge('r10', 'r22', label='e,E')
graph.edge('r22', 'r23', label='l,L')
graph.edge('r23', 'r24', label='i,I')
graph.edge('r24', 'r25', label='n,N')
graph.edge('r25', 'r21', label='e,E')
graph.edge('r0', 'r26', label='s,S')
graph.edge('r26', 'r27', label='e,E')
graph.edge('r27', 'r28', label='t,T')
graph.edge('r28', 'r21', label='q,Q')
graph.edge('r0', 'r11', label='w,W')
graph.edge('r11', 'r12', label='h,H')
graph.edge('r12', 'r13', label='e,E')
graph.edge('r13', 'r21', label='n,N')
graph.edge('r11', 'r19', label='r,R')
graph.edge('r19', 'r20', label='i,I')
graph.edge('r20', 'r10', label='t,T')
graph.edge('r0', 'r14', label='n,N')
graph.edge('r14', 'r15', label='i,I')
graph.edge('r15', 'r21', label='l,L')
graph.edge('r0', 'r16', label='r,R')
graph.edge('r16', 'r17', label='e,E')
graph.edge('r17', 'r18', label='a,A')
graph.edge('r18', 'r21', label='d|,D')
graph.edge('r2', 'r29', label='e,E')
graph.edge('r29', 'r30', label='f,F')
graph.edge('r30', 'r31', label='c,C')
graph.edge('r31', 'r32', label='o,O')
graph.edge('r32', 'r33', label='n,N')
graph.edge('r33', 'r34', label='s,S')
graph.edge('r34', 'r35', label='t,T')
graph.edge('r35', 'r36', label='a,A')
graph.edge('r36', 'r37', label='n,N')
graph.edge('r37', 'r21', label='t,T')
graph.edge('r21', 'r99', label='*')
graph.edge('r99', 'r99', label='*')

graph.node('o00', shape='point', width='0.0002', height='0.0002')
graph.node('o0')
graph.node('o1')
graph.node('o2')
graph.node('o3')
graph.node('o4')
graph.node('o5')
graph.node('o6')
graph.node('o7')
graph.node('o8')
graph.node('o12')
graph.node('o13')
graph.node('o14', shape='doublecircle')
graph.node('o99', 'reject')

graph.edge('o00', 'o0', arrowhead='vee')
graph.edge('o0', 'o1', label='>')
graph.edge('o1', 'o14', label='=')
graph.edge('o0', 'o2', label='<')
graph.edge('o2', 'o14', label='>,=')
graph.edge('o0', 'o14', label=' + - * / ) ( = . ; , : ')
graph.edge('o0', 'o3', label='r,R')
graph.edge('o3', 'o4', label='e,E')
graph.edge('o4', 'o14', label='m,M')
graph.edge('o0', 'o5', label='i,I')
graph.edge('o5', 'o6', label='n,N')
graph.edge('o6', 'o7', label='c,C')
graph.edge('o7', 'o14', label='f,F')
graph.edge('o0', 'o8', label='d,D')
graph.edge('o8', 'o6', label='e,E')
graph.edge('o0', 'o12', label='m,M')
graph.edge('o12', 'o13', label='o,O')
graph.edge('o13', 'o14', label='d,D')
graph.edge('o14', 'o99', label='*')
graph.edge('o99', 'o99', label='*')

graph.node('i00', shape='point', width='0.0002', height='0.0002')
graph.node('i0')
graph.node('i1', shape='doublecircle')
graph.node('i99', 'reject')

graph.edge('i00', 'i0', arrowhead='vee')
graph.edge('i0', 'i1', label='[a-zA-Z]')
graph.edge('i1', 'i1', label='[a-zA-Z0-9],[_|-|+|!|@|#|$|%|&|/|<|>|=|,|.]')
graph.edge('i0', 'i99', label='[0-9]')
graph.edge('i99', 'i99', label='*')

graph.node('c00', shape='point', width='0.0002', height='0.0002')
graph.node('c0', shape='doublecircle')
graph.node('c1')
graph.node('c2', shape='doublecircle')
graph.node('c99', 'reject')

graph.edge('c00', 'c0', arrowhead='vee')
graph.edge('c0', 'c0', label='[0-9]')
graph.edge('c0', 'c1', label='[.]')
graph.edge('c1', 'c2', label='[0-9]')
graph.edge('c2', 'c2', label='[0-9]')
graph.edge('c2', 'c99', label='[.]')
graph.edge('c99', 'c99', label='*')

graph
