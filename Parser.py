import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *


class Token_type(Enum):  # listing all tokens type
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
    WriteLine = 31
    LessThanOp = 32
    GreaterThanOp = 33
    NOT = 34
    AND = 35
    OR = 36
    NIL = 37
    T = 38
    String = 39
    Defconst = 40


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Reserved word Dictionary
ReservedWords = {"if": Token_type.If,
                 "dotimes": Token_type.DoTimes,
                 "setq": Token_type.Setq,
                 "when": Token_type.When,
                 "write": Token_type.Write,
                 "write-line": Token_type.WriteLine,
                 "read": Token_type.Read,
                 "nil": Token_type.NIL,
                 "t": Token_type.T,
                 "defconst":Token_type.Defconst
                 }

Operators = { "(": Token_type.OpenPrac,
              ")": Token_type.ClosedPrac,
              ".": Token_type.Dot,
              ";": Token_type.Semicolon,
              "=": Token_type.EqualOp,
              "+": Token_type.PlusOp,
              "-": Token_type.MinusOp,
              "*": Token_type.MultiplyOp,
              "/": Token_type.DivideOp,
              ">": Token_type.GreaterThanOp,
              "<": Token_type.LessThanOp,
              "<=": Token_type.LessThanOrEqualOp,
              ">=": Token_type.GreaterThanOrEqualOp,
              "<>": Token_type.NotEqualOp,
              "mod": Token_type.Mod,
              "rem": Token_type.Rem,
              "incf": Token_type.Incf,
              "decf": Token_type.Decf,
              ",": Token_type.Comma,
              "\"": Token_type.DoubleQuotation
}

LogicalOperators = {"and": Token_type.AND,
                    "or": Token_type.OR,
                    "not": Token_type.NOT
                   }


Tokens = []
errors = []


def split(text):
    i=0
    tokenlist = []
    while i < len(text):
        str = ""
        if text[i] == ' ' or text[i] == '\n':
            i +=1

        elif text[i] == '(' or text[i] == ')' or text[i] == "'" :
            tokenlist.append(text[i])
            i+=1

        elif text[i] == '#':
            i+=1
            if text[i] == '|' :
                i +=1
                while text[i] != '|' or text[i+1] != '#':
                    i += 1
                i+=2

        elif text[i] == ';':
            while text[i] != '\n':
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

        elif (text[i] != '(') and (text[i] != ')') and (text[i] != '#') and (text[i] != '\'') and (text[i] != '\"') and text[i] != ' ' and ((text[i] < '0') or (text[i] > '9')):
            while i < len(text) and (text[i] != '(') and (text[i] != ')') and (text[i] != '#') and (text[i] != '\'') and (text[i] != '\"') and text[i] != ' ': #Lisp has only ~7 special characters: (, ), #, ', ", ` and wite-space. All others are valid as part of an identifier, alone or together.
                str +=text[i]
                i+=1
            tokenlist.append(str)

        elif (text[i] >= '0') and (text[i] <= '9' ):
            while i < len(text) and ((text[i] >= '0') and (text[i] <= '9')) or (text[i] == '.'):
                str += text[i]
                i += 1
            tokenlist.append(str)


        else:
            i += 1

    return tokenlist


def find_token(tokens):

    for word in tokens:

        if word in ReservedWords:
            Tokens.append(token(word, ReservedWords[word]))

        elif word in Operators:
            Tokens.append(token(word, Operators[word]))

        elif word in LogicalOperators:
            Tokens.append(token(word, LogicalOperators[word]))

        elif re.match("^[a-zA-Z][a-zA-Z0-9]*$", word):
            Tokens.append(token(word, Token_type.Identifier))

        elif re.match("^[0-9]\.?[0-9]*?$", word):
            Tokens.append(token(word, Token_type.Constant))

        elif re.match("^\".*\"$", word):
            Tokens.append(token(word, Token_type.String))

        else:
            new_token=token(word, Token_type.Error)
            errors.append("Lexical error " + word)


# complete
def Valid_const(Tokens_Dict):
    return re.match("^[0-9]\.?[0-9]*?$", Tokens_Dict['Lex'])


def Valid_Iden(Tokens_Dict):
    return re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex'])


def Valid_String(Tokens_Dict):
    return re.match("^\".*\"$", Tokens_Dict['Lex'])


def Valid_ArthOperators(Tokens_Dict):
    return (Tokens_Dict['Lex'] == '+' or Tokens_Dict['Lex'] == '-' or Tokens_Dict['Lex'] == '*' or Tokens_Dict['Lex'] == '/'
            or Tokens_Dict['Lex'] == 'mod' or Tokens_Dict['Lex'] == 'rem')


def Valid_RelOperators(Tokens_Dict):
    return (Tokens_Dict['Lex'] == '>' or Tokens_Dict['Lex'] == '<' or Tokens_Dict['Lex'] == '=' or Tokens_Dict['Lex'] == '>=' or Tokens_Dict['Lex'] == '<=')


def Valid_IncOperators(Tokens_Dict):
    return (Tokens_Dict['Lex'] == 'incf' or Tokens_Dict['Lex'] == 'decf')


def Valid_Symbols(Tokens_Dict):
    return (Tokens_Dict['Lex'] == '(' or Tokens_Dict['Lex'] == ')' or Tokens_Dict['Lex'] == ";")


def Parse():
    j = 0
    Children = []

    Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Valid_String(Tokens_Dict):
        String_dict = Match(Token_type.String, j)
        Children.append(String_dict["node"])

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == '(':
        Statements_dict = Statements(j)
        Children.append(Statements_dict["node"])

    else:
        errors.append("Syntax error: empty program")
        Children.append(errors[len(errors)-1])



    Node = Tree('Program', Children)

    return Node


def Statements(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == '(':
        List_Dict = List(j)
        Children.append(List_Dict["node"])
        out1 = Statements(List_Dict["index"])
        if out1:
            Children.append(out1["node"])
            output["index"] = out1["index"]
        else:
            output["index"] = List_Dict["index"]

    else:
        return

    node = Tree('Statements', Children)
    output["node"] = node

    return output


def List(j):
    Children = []
    output = dict()

    out1 = Match(Token_type.OpenPrac, j)
    Children.append(out1["node"])

    ListItem_Dict = ListItem(out1["index"])
    if ListItem_Dict:
        Children.append(ListItem_Dict["node"])
        index = ListItem_Dict["index"]
    else:
        index = out1["index"]

    out2 = Match(Token_type.ClosedPrac, index)
    Children.append(out2["node"])

    node = Tree('List', Children)
    output["node"] = node
    output["index"] = out2["index"]
    return output


def ListItem(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if (Valid_String(Tokens_Dict) or Valid_const(Tokens_Dict)):
            Atom_Dict = Atom(j)
            Children.append(Atom_Dict["node"])
            output["index"] = Atom_Dict["index"]

        elif (
                Tokens_Dict['Lex'] == 'setq' or
                Tokens_Dict['Lex'] == 'write-line' or
                Tokens_Dict['Lex'] == 'write' or
                Tokens_Dict['Lex'] == 'when' or
                Tokens_Dict['Lex'] == 'dotimes' or
                Tokens_Dict['Lex'] == 'defconst' or
                Tokens_Dict['Lex'] == 'read' or
                Valid_Iden(Tokens_Dict) or
                Valid_ArthOperators(Tokens_Dict) or
                Valid_RelOperators(Tokens_Dict) or
                Valid_IncOperators(Tokens_Dict) or
                Tokens_Dict['Lex'] in LogicalOperators
        ):
            Statement_Dict = Statement(j)
            Children.append(Statement_Dict["node"])
            output["index"] = Statement_Dict["index"]

        else:
            return

    node = Tree('ListItem', Children)
    output["node"] = node

    return output


def Atom(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Valid_String(Tokens_Dict):
            String_dict = Match(Token_type.String, j)
            Children.append(String_dict["node"])
            output["index"] = String_dict["index"]

        elif Valid_const(Tokens_Dict):
            const_Dict= Match(Token_type.Constant,j)
            Children.append(const_Dict["node"])
            output["index"] = const_Dict["index"]

        else:
            return

    node = Tree('ListItem', Children)
    output["node"] = node

    return output


def Statement(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex']=='setq':
            out1 = Match(Token_type.Setq, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.Identifier,out1["index"])
            Children.append(out2["node"])
            Terms_Dict = Terms(out2["index"])
            Children.append(Terms_Dict["node"])
            output["index"] = Terms_Dict["index"]

        elif Tokens_Dict['Lex']=='defconst':
            out1 = Match(Token_type.Defconst, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.Identifier, out1["index"])
            Children.append(out2["node"])
            out3 = Match(Token_type.Constant, out2["index"])
            Children.append(out3["node"])
            output["index"] = out3["index"]

        elif Tokens_Dict['Lex'] == 'write-line':
            out1 = Match(Token_type.WriteLine, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.String, out1["index"])
            Children.append(out2["node"])
            output["index"] = out2["index"]

        elif Tokens_Dict['Lex'] == 'write':
            out1 = Match(Token_type.Write, j)
            Children.append(out1["node"])
            Terms_Dict = Terms(out1["index"])
            Children.append(Terms_Dict["node"])
            output["index"] = Terms_Dict["index"]

        elif Tokens_Dict['Lex'] == 'read':
            out1 = Match(Token_type.Read, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.Identifier, out1["index"])
            Children.append(out2["node"])
            output["index"] = out2["index"]

        elif Tokens_Dict['Lex'] == 'when':
            out1 = Match(Token_type.When, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.OpenPrac, out1["index"])
            Children.append(out2["node"])
            WhenTerm_Dict = WhenTerm(out2["index"])
            Children.append(WhenTerm_Dict["node"])
            out3 = Match(Token_type.ClosedPrac, WhenTerm_Dict["index"])
            Children.append(out3["node"])
            Stmts_Dict = Statements(out3["index"])
            if Stmts_Dict:
                Children.append(Stmts_Dict["node"])
                output["index"] = Stmts_Dict["index"]
            else:
                output["index"] = out3["index"]

        elif Tokens_Dict['Lex'] == 'dotimes':
            out1 = Match(Token_type.DoTimes, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.OpenPrac, out1["index"])
            Children.append(out2["node"])
            out3 = Match(Token_type.Identifier,out2["index"])
            Children.append(out3["node"])
            Factor_Dict = Factor(out3["index"])
            Children.append(Factor_Dict["node"])
            out3 = Match(Token_type.ClosedPrac, Factor_Dict["index"])
            Children.append(out3["node"])
            Stmts_Dict = Statements(out3["index"])
            if Stmts_Dict:
                Children.append(Stmts_Dict["node"])
                output["index"] = Stmts_Dict["index"]
            else:
                output["index"] = out3["index"]

        elif (Valid_IncOperators(Tokens_Dict)):
            Inc_Dict = Incrementation(j)
            Children.append(Inc_Dict["node"])
            out1 = Match(Token_type.Identifier, Inc_Dict["index"])
            Children.append(out1["node"])
            IncVar_Dict = IncrementVar(out1["index"])

            if IncVar_Dict:
                Children.append(IncVar_Dict["node"])
                index = IncVar_Dict["index"]
            else:
                index = out1["index"]
            output["index"] = index

        elif (Valid_ArthOperators(Tokens_Dict)):
            Exp_Dict = Expression(j)
            Children.append(Exp_Dict["node"])
            output["index"] = Exp_Dict["index"]

        elif (Valid_RelOperators(Tokens_Dict)):
            Cond_Dict = Condition(j)
            Children.append(Cond_Dict["node"])
            output["index"] = Cond_Dict["index"]

        elif (Tokens_Dict['Lex'] in LogicalOperators):
            Bool_Dict = BoolExp(j)
            Children.append(Bool_Dict["node"])
            output["index"] = Bool_Dict["index"]

        elif Valid_Iden(Tokens_Dict):
            out1 = Match(Token_type.Identifier, j)
            Children.append(out1["node"])
            Factors_Dict = Factors(out1["index"])
            Children.append(Factors_Dict["node"])
            output["index"] = Factors_Dict["index"]

    else:
        errors.append("Syntax error: Expected Statement")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('Statement', Children)
    output["node"] = node

    return output


def Terms(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Valid_String(Tokens_Dict):
            out1 = Match(Token_type.String, j)
            Children.append(out1["node"])
            output["index"] = out1["index"]

        else:
            Term_Dict = Term(j)
            Children.append(Term_Dict["node"])
            output["index"] = Term_Dict["index"]

    else:
        errors.append("Syntax error: Expected string or term")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('Terms', Children)
    output["node"] = node

    return output


def Term (j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if(Valid_Iden(Tokens_Dict) or Valid_const(Tokens_Dict)):
            Factor_Dict = Factor(j)
            Children.append(Factor_Dict["node"])
            output["index"] = Factor_Dict["index"]

        elif Tokens_Dict['Lex'] == '(':
            out = Match(Token_type.OpenPrac, j)
            Children.append(out["node"])
            BoolItem_Dict = BoolItem(out["index"])
            Children.append(BoolItem_Dict["node"])
            out1 = Match(Token_type.ClosedPrac, BoolItem_Dict["index"])
            Children.append(out1["node"])
            output["index"] = out1["index"]

    else:
        errors.append("Syntax error: Expected id or constant or (boolExp)")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('Term', Children)
    output["node"] = node

    return output


def WhenTerm(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if (Valid_RelOperators(Tokens_Dict)):
            Cond_Dict = Condition(j)
            Children.append(Cond_Dict["node"])
            output["index"] = Cond_Dict["index"]

        elif (Tokens_Dict['Lex'] in LogicalOperators):
            Bool_Dict = BoolExp(j)
            Children.append(Bool_Dict["node"])
            output["index"] = Bool_Dict["index"]

    else:
        errors.append("Syntax error: Expected WhenTerm")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('WhenTerm', Children)
    output["node"] = node

    return output


def Incrementation(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex'] == 'incf':
            out = Match(Token_type.Incf, j)
            Children.append(out["node"])
            output["index"] = out["index"]

        elif Tokens_Dict['Lex'] == 'decf':
            out = Match(Token_type.Decf, j)
            Children.append(out["node"])
            output["index"] = out["index"]

    else:
        errors.append("Syntax error: Expected Incrementation")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('Incrementation', Children)
    output["node"] = node

    return output


def Condition(j):
    Children = []
    output = dict()

    RelOp_Dict = RelOp(j)
    Children.append(RelOp_Dict["node"])

    ExpDash_Dict1 = ExpDash(RelOp_Dict["index"])
    Children.append(ExpDash_Dict1["node"])

    ExpDash_Dict2 = ExpDash(ExpDash_Dict1["index"])
    Children.append(ExpDash_Dict2["node"])

    node = Tree('Condition', Children)
    output["node"] = node
    output["index"] = ExpDash_Dict2["index"]
    return output


def Factor(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Valid_const(Tokens_Dict):
            out1 = Match(Token_type.Constant, j)
            Children.append(out1["node"])
            output["index"] = out1["index"]

        elif Valid_Iden(Tokens_Dict):
            out2 = Match(Token_type.Identifier, j)
            Children.append(out2["node"])
            output["index"] = out2["index"]

    else:
        errors.append("Syntax error: Expected identifier or constant")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('Factor', Children)
    output["node"] = node

    return output


def Factors(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Valid_Iden(Tokens_Dict) or Valid_const(Tokens_Dict):
            Factor_Dict = Factor(j)
            Children.append(Factor_Dict["node"])
            Facsss_Dict = Factors(Factor_Dict["index"])
            if Facsss_Dict:
                Children.append(Facsss_Dict["node"])
                output["index"] = Facsss_Dict["index"]
            else:
                output["index"] = Factor_Dict["index"]

        else:
            return

    node = Tree('Factors', Children)
    output["node"] = node

    return output


def Op(j):
    Children = []
    output = dict()


    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex'] == "+":
            out1 = Match(Token_type.PlusOp, j)
            Children.append(out1["node"])
            output["index"] = out1["index"]

        elif Tokens_Dict['Lex'] == "-":
            out2 = Match(Token_type.MinusOp, j)
            Children.append(out2["node"])
            output["index"] = out2["index"]

        elif Tokens_Dict['Lex'] == "*":
            out3 = Match(Token_type.MultiplyOp, j)
            Children.append(out3["node"])
            output["index"] = out3["index"]

        elif Tokens_Dict['Lex'] == "/":
            out4 = Match(Token_type.DivideOp, j)
            Children.append(out4["node"])
            output["index"] = out4["index"]

        elif Tokens_Dict['Lex'] == "mod":
            out5 = Match(Token_type.Mod, j)
            Children.append(out5["node"])
            output["index"] = out5["index"]

        elif Tokens_Dict['Lex'] == "rem":
            out6 = Match(Token_type.Rem, j)
            Children.append(out6["node"])
            output["index"] = out6["index"]

    else:
        errors.append("Syntax error: Expected operator")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('Op', Children)
    output["node"] = node
    return output


def RelOp(j):

    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex'] == "=":
            out1 = Match(Token_type.EqualOp, j)
            Children.append(out1["node"])
            output["index"] = out1["index"]

        elif Tokens_Dict['Lex'] == ">":
            out2 = Match(Token_type.GreaterThanOp, j)
            Children.append(out2["node"])
            output["index"] = out2["index"]

        elif Tokens_Dict['Lex'] == "<":
            out3 = Match(Token_type.LessThanOp, j)
            Children.append(out3["node"])
            output["index"] = out3["index"]

        elif Tokens_Dict['Lex'] == "<=":
            out4 = Match(Token_type.LessThanOrEqualOp, j)
            Children.append(out4["node"])
            output["index"] = out4["index"]

        elif Tokens_Dict['Lex'] == ">=":
            out5 = Match(Token_type.GreaterThanOrEqualOp, j)
            Children.append(out5["node"])
            output["index"] = out5["index"]

    else:
        errors.append("Syntax error: Expected Reloperator")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('RelOp', Children)
    output["node"] = node

    return output


def Incrementation(j):

    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex'] == "incf":
            out1 = Match(Token_type.Incf, j)
            Children.append(out1["node"])
            output["index"] = out1["index"]

        elif Tokens_Dict['Lex'] == "decf":
            out2 = Match(Token_type.Decf, j)
            Children.append(out2["node"])
            output["index"] = out2["index"]

    else:
        errors.append("Syntax error: Expected Incoperator")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('Incrementation', Children)
    output["node"] = node
    return output


def IncrementVar(j):

    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Valid_Iden(Tokens_Dict) or Valid_const(Tokens_Dict):
            Factor_dict = Factor(j)
            Children.append(Factor_dict["node"])

        else:
            return

    node = Tree('IncrementVar', Children)
    output["node"] = node
    output["index"] = Factor_dict["index"]
    return output


def LogicalOp(j):

    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex'] == "not":
            out1 = Match(Token_type.NOT, j)
            Children.append(out1["node"])
            output["index"] = out1["index"]

        elif Tokens_Dict['Lex'] == "and":
            out2 = Match(Token_type.AND, j)
            Children.append(out2["node"])
            output["index"] = out2["index"]

        elif Tokens_Dict['Lex'] == "or":
            out3 = Match(Token_type.OR, j)
            Children.append(out3["node"])
            output["index"] = out3["index"]

    else:
        errors.append("Syntax error: Expected Logicaloperator")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('LogicalOp', Children)
    output["node"] = node

    return output


def BoolExp(j):
    Children = []
    output = dict()

    Logic_Dict = LogicalOp(j)
    Children.append(Logic_Dict["node"])

    BoolDash_Dict1 = BoolExpDash(Logic_Dict["index"])
    if BoolDash_Dict1:
        Children.append(BoolDash_Dict1["node"])
        index = BoolDash_Dict1["index"]
    else:
        index = Logic_Dict["index"]

    BoolDash_Dict2 = BoolExpDash(index)
    if BoolDash_Dict2:
        Children.append(BoolDash_Dict2["node"])
        index2 = BoolDash_Dict2["index"]
    else:
        index2 = index

    node = Tree('BoolExp', Children)
    output["node"] = node
    output["index"] = index2

    return output


def BoolExpDash(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex'] == '(':
            out1 = Match(Token_type.OpenPrac, j)
            Children.append(out1["node"])
            BoolItem_Dict = BoolItem(out1["index"])
            Children.append(BoolItem_Dict["node"])
            out2 = Match(Token_type.ClosedPrac, BoolItem_Dict["index"])
            Children.append(out2["node"])
            output["index"] = out2["index"]

        elif Valid_Iden(Tokens_Dict) or Valid_const(Tokens_Dict):
            Factor_dict = Factor(j)
            Children.append(Factor_dict["node"])
            output["index"] = Factor_dict["index"]

        elif Tokens_Dict['Lex'] == 'nil':
            out = Match(Token_type.NIL, j)
            Children.append(out["node"])
            output["index"] = out["index"]

        elif Tokens_Dict['Lex'] == 't':
            out = Match(Token_type.T, j)
            Children.append(out["node"])
            output["index"] = out["index"]

        else:
            return

    node = Tree('BoolExpDash', Children)
    output["node"] = node

    return output


def BoolItem(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if (Valid_ArthOperators(Tokens_Dict) or Valid_RelOperators(Tokens_Dict)):
            logExp_Dict = LogicExp(j)
            Children.append(logExp_Dict["node"])
            output["index"] = logExp_Dict["index"]

        elif Tokens_Dict['Lex'] in LogicalOperators:
            BoolExp_Dict = BoolExp(j)
            Children.append(BoolExp_Dict["node"])
            output["index"] = BoolExp_Dict["index"]

    else:
        errors.append("Syntax error: Expected Logical Expression or Boolean Expression")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('BoolItem', Children)
    output["node"] = node

    return output


def LogicExp(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Valid_ArthOperators(Tokens_Dict):
            Exp_Dict = Expression(j)
            Children.append(Exp_Dict["node"])
            output["index"] = Exp_Dict["index"]

        elif Valid_RelOperators(Tokens_Dict):
            Cond_Dict = Condition(j)
            Children.append(Cond_Dict["node"])
            output["index"] = Cond_Dict["index"]

    else:
        errors.append("Syntax error: Expected Logical Expression")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('LogicExp', Children)
    output["node"] = node

    return output


def Expression(j):
    Children = []
    output = dict()

    Op_Dict = Op(j)
    Children.append(Op_Dict["node"])

    ExpDash_Dict1 = ExpDash(Op_Dict["index"])
    Children.append(ExpDash_Dict1["node"])

    ExpDash_Dict2 = ExpDash(ExpDash_Dict1["index"])
    Children.append(ExpDash_Dict2["node"])

    Exps_dict = Expressions(ExpDash_Dict2["index"])
    if Exps_dict:
        Children.append(Exps_dict["node"])
        output["index"] = Exps_dict["index"]
    else:
        output["index"] = ExpDash_Dict2["index"]

    node = Tree('Expression', Children)
    output["node"] = node

    return output


def Expressions(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex'] == '(' or Valid_Iden(Tokens_Dict) or Valid_const(Tokens_Dict):
            ExpDash_dict = ExpDash(j)
            Children.append(ExpDash_dict["node"])
            Exps_dict = Expressions(ExpDash_dict["index"])
            if Exps_dict:
                Children.append(Exps_dict["node"])
                output["index"] = Exps_dict["index"]
            else:
                output["index"] = ExpDash_dict["index"]

        else:
            return

    node = Tree('Expressions', Children)
    output["node"] = node

    return output


def ExpDash(j):
    Children = []
    output = dict()

    if(j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

        if Tokens_Dict['Lex'] == '(':
            out1 = Match(Token_type.OpenPrac, j)
            Children.append(out1["node"])
            Exp_Dict = Expression(out1["index"])
            Children.append(Exp_Dict["node"])
            out2 = Match(Token_type.ClosedPrac, Exp_Dict["index"])
            Children.append(out2["node"])
            output["index"] = out2["index"]

        elif Valid_Iden(Tokens_Dict) or Valid_const(Tokens_Dict):
            Factor_dict = Factor(j)
            Children.append(Factor_dict["node"])
            output["index"] = Factor_dict["index"]

    else:
        errors.append("Syntax error: Expected Expression or identifier or constant")
        Children.append(errors[len(errors)-1])
        output["index"] = j

    node = Tree('ExpDash', Children)
    output["node"] = node

    return output


def Match(a, j):
    output = dict()
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output
        elif ((Temp['token_type'] != a) and ((Temp['Lex'] in ReservedWords) or Valid_ArthOperators(Temp) or Valid_RelOperators(Temp) or (Temp['Lex'] in LogicalOperators) or Valid_IncOperators(Temp))):
            output["node"] = ["Syntax error : " + " Expected " + str(a.name)]
            output["index"] = j + 1
            errors.append("Syntax error : " + " Expected " + str(a.name))
            return output
        else:
            output["node"] = ["Syntax error : "+ " Expected "+str(a.name)]
            output["index"] = j
            errors.append("Syntax error : " +  " Expected "+str(a.name))
            return output
    else:
        output["node"] = ["Syntax error: Close Bracket expected"]
        errors.append("Syntax error: Close Bracket expected")
        output["index"] = j +1
        return output


# GUI
root = tk.Tk()
root.title('Scanner')
root.geometry("800x600")


my_Text = tk.Text(root, width=90, height= 25, bg="white")
my_Text.pack(pady=10)

x1 = my_Text.get(1.0, tk.END)


def Scan():
    x1 = my_Text.get(1.0, tk.END)
    x1 = x1.lower()
    tokens = split(x1)
    find_token(tokens)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)


btn_scan = tk.Button(root, text="Scan", command=Scan ,bg="#00B1F7", fg="white",
                    font=("Arial", 14), relief="solid", borderwidth=0, padx=10, pady=5)
btn_scan.pack(pady=10)

root.mainloop()
