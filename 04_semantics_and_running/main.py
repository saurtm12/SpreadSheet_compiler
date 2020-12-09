#!/usr/bin/env python3

import sys, ply.lex
import re
from decimal import *
import tree_print

reserved = {
        'sheet':'SHEET',
        'scalar':'SCALAR',
        'range':'RANGE',
        'do':'DO',
        'done':'DONE',
        'is':'IS',
        'while':'WHILE',
        'for':'FOR',
        'if':'IF',
        'then':'THEN',
        'else':'ELSE',
        'endif':'ENDIF',
        'function':'FUNCTION',
        'subroutine':'SUBROUTINE',
        'return':'RETURN',
        'end':'END',
        'print_sheet':'PRINT_SHEET',
        'print_scalar':'PRINT_SCALAR',
        'print_range':'PRINT_RANGE',
}

tokens = [
        #1-2 letter tokens
        'ASSIGN',
        'LPAREN', 'RPAREN',
        'LSQUARE','RSQUARE',
        'LCURLY', 'RCURLY',
        'COMMA',
        'DOTDOT',
        'SQUOTE',
        'COLON',
        'DOLLAR',
        'NUMBER_SIGN',
        'EQ',
        'NOTEQ',
        'LT', 'LTEQ',
        'GT', 'GTEQ',
        'PLUS',
        'MINUS',
        'MULT',
        'DIV',
        #long token
        'INFO_STRING',
        'COORDINATE_IDENT',
        'DECIMAL_LITERAL',
        'INT_LITERAL',
        'IDENT',
        'RANGE_IDENT',
        'SHEET_IDENT',
        'FUNC_IDENT',
        'ID'
        ] + list(reserved.values())

#check for reserved keywords
def t_ID(t):
    r'[a-z_]+'
    if (reserved.get(t.value) != None):
        t.type = reserved.get(t.value,'ID')
    else:
        if (t.value[0] != '_'):
            return t_IDENT(t)
        else:
            return t_RANGE_IDENT(t)
    return t

t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'{'
t_RCURLY = r'}'

t_COMMA = r','
t_DOTDOT = r'\.\.'
t_SQUOTE = r"'"
t_COLON = r':'
t_DOLLAR = r'\$'
t_NUMBER_SIGN = r'\#'

t_NOTEQ = r'!='
t_LTEQ = r'<='
t_GTEQ = r'>='
t_EQ = r'='
t_LT = r'<'
t_GT = r'>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

def t_INFO_STRING(t):
    r'!.*?!'
    t.value = t.value[1:-1]
    t.value = re.sub(r"\.{3,3}([\s\S]*?)\.{3,3}","",t.value)
    t.type = 'INFO_STRING'
    return t

def t_COORDINATE_IDENT(t):
    r'([A-Z]{1,2}[0-9]{1,3})'
    return t

def t_DECIMAL_LITERAL(t):
    r'-?\d+\.\d'
    t.value = Decimal(t.value)
    t.type = 'DECIMAL_LITERAL'
    return t

def t_INT_LITERAL(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
        t.type = 'INT_LITERAL'
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_IDENT(t):
    r'[a-z][a-zA-Z0-9_]+'
    t.type = "IDENT"
    return t

def t_RANGE_IDENT(t):
    r'\_[a-zA-Z0-9_]+\s'
    t.type = "RANGE_IDENT"
    return t


def t_FUNC_IDENT(t):
    r'[A-Z][a-z0-9_]+'
    t.type = 'FUNC_IDENT'
    return t

def t_SHEET_IDENT(t):
    r'[A-Z]+'
    t.type = 'SHEET_IDENT'
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_COMMENT(t):
    r"\.{3,3}([\s\S]*?)\.{3,3}"
    pass

def t_error(t):
    raise Exception("Illegal character '{}' at line {}".format( 
        t.value[0], t.lexer.lineno ) )

lexer = ply.lex.lex()

# ------------------------------------------------------------------------------
# Phase 2 AND 3
# Define the syntax_check:
from ply import yacc

### {a} : a_star
### [a] : a_opt
### <a+> : a_plus // if necessary

class Node:
    def __init__(self,type=None, value=None):
        self.setType(type)
        self.setValue(value)
        self.children_ = []
    
    def addChild(self, node):
        self.children_.append(node)

    def insertFirstChild(self, child):
        self.children_.insert(0,child)
    def setValue(self, value):
        self.value = value
    
    def setType(self, type):
        self.nodetype = type
    
    def assignChildren(self, children):
        self.children_ = children
    

def p_program(p):
    ''' program : function_or_variable_definition_star statement_list'''
    p[0] = Node("program")
    p[0].addChild(p[1])
    p[0].addChild(p[2])
    
def p_function_or_variable_definition_star(p):
    '''function_or_variable_definition_star  : function_or_variable_definition_star function_or_variable_definition
                                            | empty'''
    if len(p) == 2: #t2
        p[0] = Node("function_or_variable_definition_list")
        return
    p[0] = p[1]
    p[0].addChild(p[2])
def p_function_or_variable_definition(p):
    '''function_or_variable_definition   : variable_definition 
                                        | function_definition 
                                        | subroutine_definition'''
    p[0] = p[1]

def p_variable_definition_star(p):
    '''variable_definition_star : variable_definition_star variable_definition
                                | empty'''
    if len(p) == 2: #t2
        p[0] = Node("variable_definition_list")
        return
    #t1
    p[0] = p[1]
    p[0].addChild(p[2])
    
def p_variable_definition(p):
    '''variable_definition : scalar_definition 
                            | range_definition 
                            | sheet_definition'''
    p[0] = p[1]


def p_function_definition(p):
    '''function_definition : FUNCTION FUNC_IDENT LSQUARE formals_opt RSQUARE \
                            RETURN SCALAR IS \
                            variable_definition_star \
                            statement_list \
                            END 
                            | FUNCTION FUNC_IDENT LSQUARE formals_opt RSQUARE \
                            RETURN RANGE IS \
                            variable_definition_star \
                            statement_list \
                            END'''
    p[0] = Node("definition_function", p[2])
    p[0].addChild(Node('func',p[2]))
    p[0].addChild(p[4])
    p[0].addChild(Node('return',p[7]))
    p[0].addChild(p[9])
    p[0].addChild(p[10])                        
 
def p_subroutine_definition(p):
    '''subroutine_definition : SUBROUTINE FUNC_IDENT LSQUARE formals_opt RSQUARE IS \
                                variable_definition_star \
                                statement_list \
                                END'''
    p[0] = Node("definition_subroutine", p[2])
    p[0].addChild(Node('sub',p[2]))
    p[0].addChild(p[4])
    p[0].addChild(p[7])
    p[0].addChild(p[8])


def p_formals_opt(p):
    '''formals_opt : formals
                    | empty'''
    p[0] = p[1]    

def p_formals(p):
    '''formals : formals COMMA formal_arg
                | formal_arg'''
    if len(p) == 2: #t2
        p[0] = Node("formals")
        p[0].addChild(p[1])
        return
    p[0] = p[1]
    p[0].addChild(p[3]) 

def p_formal_arg(p):
    '''formal_arg :  IDENT COLON SCALAR
                    | RANGE_IDENT COLON RANGE
                    | SHEET_IDENT COLON SHEET'''
    if p[3] == 'scalar': #t1
        p[0] = Node('scalar',p[1])
        return
    if p[3] == 'range': #t2
        p[0] = Node('range',p[1])
        return
    #3
    p[0] = Node('sheet',p[1])

def p_sheet_definition(p):
    '''sheet_definition : SHEET SHEET_IDENT sheet_init_opt'''
    p[0] = Node("definition_sheet", p[2])
    p[0].addChild(Node('sheet',p[2]))
    if p[3] is not None:
        p[0].addChild(p[3])

def p_sheet_init_opt(p):
    '''sheet_init_opt : sheet_init
                        | empty'''
    p[0] = p[1]                    

def p_sheet_init(p):
    '''sheet_init : EQ sheet_init_list 
                    | EQ INT_LITERAL MULT INT_LITERAL'''
    if len(p) == 3: #t1
        p[0] = p[2]
        return
    #t2:
    p[0] = Node('sheet_init_size', (p[2], p[4]))

def p_sheet_init_list(p):
    '''sheet_init_list : LCURLY sheet_row_plus RCURLY'''
    p[0] = p[2]

def p_sheet_row_plus(p):
    '''sheet_row_plus : sheet_row_plus sheet_row
                        | sheet_row'''
    if len(p) == 2: #t2
        p[0] = Node('sheet_init_list')
        p[0].addChild(p[1])
        return
    #t1
    p[0] = p[1]
    p[0].addChild(p[2])
def p_sheet_row(p):
    '''sheet_row : sheet_row COMMA simple_expr
                | simple_expr'''
    if len(p) == 2: 
        p[0] = Node("sheet_row")
        p[0].addChild(p[1])
        return
    p[0] = p[1]
    p[0].addChild(p[3])

def p_range_definition(p):
    '''range_definition : RANGE RANGE_IDENT 
                        | RANGE RANGE_IDENT EQ range_expr'''
    p[0] = Node("definition_range",p[2])
    if len(p) == 3: #t1
        # define behaviour when range is not intialized
        p[0].addChild(None)
        return
    #t2
    p[0].addChild(p[4])

def p_scalar_definition(p):
    '''scalar_definition : SCALAR IDENT  
                            | SCALAR IDENT EQ scalar_expr'''
    p[0] = Node("definition_scalar",p[2])
    if len(p) == 3: #1
        # define behaviour when variable is not intialized
        p[0].addChild(Node('decimal',('+',0.0)))
        return
    #t2
    p[0].addChild(p[4])

def p_statement_list(p):
    '''statement_list : statement_list statement
                        | statement'''
    if len(p) == 2: #t2
        p[0] = Node("statement_list")
        p[0].addChild(p[1])
        return
    #t1
    p[0] = p[1]
    p[0].addChild(p[2])


def p_statement(p):
    '''statement : PRINT_SHEET info_string_opt SHEET_IDENT
                    | PRINT_RANGE info_string_opt range_expr
                    | PRINT_SCALAR info_string_opt scalar_expr
                    | IF scalar_expr THEN statement_list ENDIF
                    | IF scalar_expr THEN statement_list ELSE statement_list ENDIF
                    | WHILE scalar_expr DO statement_list DONE
                    | FOR range_list DO statement_list DONE
                    | subroutine_call
                    | RETURN scalar_expr
                    | RETURN range_expr
                    | assignment'''
    if p[1] == "print_sheet": #1
        p[0] = Node('print_sheet')
        p[0].addChild(p[2])
        p[0].addChild(Node('sheet',p[3]))
        return
    if p[1] == "print_range": #t2
        p[0] = Node('print_range')
        p[0].addChild(p[2])
        p[0].addChild(p[3])
        return
    if p[1] == "print_scalar": #t3
        p[0] = Node('print_scalar')
        p[0].addChild(p[2])
        p[0].addChild(p[3])
        return
    if p[1] == 'if' and len(p) == 6: #t4
        p[0] = Node('if')
        p[0].addChild(p[2])
        p[0].addChild(p[4])
        return
    if p[1] == 'if': #t5
        p[0] = Node('if_else')
        p[0].addChild(p[2])
        p[0].addChild(p[4])
        p[0].addChild(p[6])
        return
    if p[1] == 'while': #t6
        p[0] = Node('while')
        p[0].addChild(p[2])
        p[0].addChild(p[4])
        return
    if p[1] == 'for': #t7
        p[0] = Node('for')
        p[0].addChild(p[2])
        p[0].addChild(p[4])
        return
    if p[1] == 'return': #t9,10
        p[0] = Node('return')
        p[0].addChild(p[2])
        return
    #t8,11
    p[0] = p[1]
def p_info_string_opt(p):
    '''info_string_opt : INFO_STRING
                        | empty'''
    p[0] = Node("info_string",p[1])

def p_range_list(p):
    '''range_list : range_list COMMA range_expr
                    | range_expr'''
    if len(p) == 2: #t2
        p[0] = Node("range_list")
        p[0].addChild(p[1])
        return
    p[0] = p[1]
    p[1].addChild(p[3])

def p_arguments(p):
    '''arguments : arguments COMMA arg_expr
                    | arg_expr'''
    if len(p) == 2: #t2
        p[0] = Node("arguments")
        p[0].addChild(p[1])
        return
    #t1
    p[0] = p[1]
    print(len(p))
    p[0].addChild(p[3])


def p_arg_expr(p):
    '''arg_expr : scalar_expr 
                | range_expr 
                | SHEET_IDENT'''
    if not isinstance(p[1],Node): #t3
        p[0] = Node('sheet',p[1])
        return
    p[0] = p[1]

def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE RSQUARE
                        | FUNC_IDENT LSQUARE arguments RSQUARE'''
    p[0] = Node("subroutine_call")
    p[0].addChild(Node('sub',p[1]))
    if len(p) == 5: #t2
        p[0].addChild(p[3])

def p_assignment(p):
    '''assignment : IDENT ASSIGN scalar_expr
                    | cell_ref ASSIGN scalar_expr
                    | RANGE_IDENT ASSIGN range_expr
                    | SHEET_IDENT ASSIGN SHEET_IDENT'''
    if isinstance(p[1],Node): #t2
        p[0] = Node('cell_ref_assignment')
        p[0].addChild(p[1])
        p[0].addChild(p[3])
        return
    if not isinstance(p[3], Node): #t4
        p[0] = Node('sheet_assignment')
        p[0].addChild(Node('sheet',p[1]))
        p[0].addChild(Node('sheet',p[3]))
        return
    if p[3].nodetype == 'range_expr': #t3
        p[0] = Node('range_assign')
        p[0].addChild(Node('range',p[1]))
        p[0].addChild(p[3])
        return
    #t1
    p[0] = Node("scalar_assignment") 
    p[0].addChild(Node('scalar',p[1]))
    p[0].addChild(p[3])
    

def p_range_expr(p):
    '''range_expr : RANGE_IDENT
                    | RANGE cell_ref DOTDOT cell_ref
                    | LSQUARE function_call RSQUARE
                    | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''
    if len(p) == 2: #t1
        p[0] = Node("range_expr")
        p[0].addChild(Node('range',p[1]))
        return
    if len(p) == 4: #t3
        p[0] = Node("range_expr")
        p[0].addChild(p[2])
        return
    if len(p) == 5: #t2
        p[0] = Node("range_expr")
        p[0].addChild(p[2])
        p[0].addChild(p[4])
        return
    if len(p) == 7: #t4
        p[0] = p[1]
        p[0].addChild(Node('int',p[3]))
        p[0].addChild(Node('int',p[5]))

    
def p_cell_ref(p):
    '''cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR 
                | DOLLAR  COLON RANGE_IDENT'''
    p[0] = Node('cell_ref')
    if len(p) == 2: #t2
        p[0].addChild(Node('dollar',p[1]))
    else:
        if p[1] == '$': #t3
            p[0].addChild(Node('dollar',p[1]))
            p[0].addChild(Node('range',p[3]))
        else : #t1
            p[0].addChild(Node('sheet',p[1]))
            col = re.search('[A-Z]+',p[3])
            col = col.group(0)
            if len(col) == 1 :
                col = ord(col) - ord('A')
            else :
                col = (ord(col[0])- ord('A')+1)*26 + ord(col[1])-ord('A')
            row = re.search('[0-9]+',p[3])
            row = int(row.group(0))-1
            p[0].addChild(Node('coordinate',(col,row,p[3])))


def p_scalar_expr(p):
    '''scalar_expr : simple_expr
                    | scalar_expr compare simple_expr'''
    if len(p)== 2: #t1
        p[0] = p[1]
    else: #t2
        if p[1].nodetype != 'scalar_expr':
            p[0] = Node('scalar_expr')
            p[0].addChild(p[1])
        else :
            p[0] = p[1]
        p[0].addChild(p[2])
        p[0].addChild(p[3])

def p_compare(p):
    '''compare : EQ 
                | NOTEQ 
                | LT 
                | LTEQ 
                | GT 
                | GTEQ'''
    p[0] = Node('compare',p[1])

def p_simple_expr(p):
    '''simple_expr : simple_expr PLUS term
                    | simple_expr MINUS term
                    | term'''
    if len(p) == 2: #t3
        p[0] = p[1]
    else: #t1,2
        if p[1].nodetype != 'simple_expr':
            p[0] = Node('simple_expr')     
            p[0].addChild(p[1]) 
        else :
            p[0] = p[1]
        p[0].addChild(Node('oper',p[2]))
        p[0].addChild(p[3])

def p_term(p):
    '''term : term MULT factor
            | term DIV factor
            | factor'''
    if len(p) == 2: #t3
        p[0] = p[1]
    else: #t1,2
        if p[1].nodetype != 'term':
            p[0] = Node('term')
            p[0].addChild(p[1])
        else :
            p[0] = p[1]
        p[0].addChild(Node('oper',p[2]))
        p[0].addChild(p[3])
    

def p_factor(p):
    '''factor : atom
                | MINUS atom'''
    if (len(p) == 2): #t1
        p[0] = p[1]
        p[0].value = ('+', p[0].value)
    else: #t2
        p[0] = p[2]
        p[0].value = ('-', p[0].value)

def p_atom(p):
    '''atom : IDENT 
            | DECIMAL_LITERAL 
            | function_call
            | cell_ref 
            | NUMBER_SIGN range_expr
            | LPAREN scalar_expr RPAREN'''
    if len(p) == 2:
        if isinstance(p[1],Node):
            #t3,4
            p[0] = p[1]
            return
        else:
            if isinstance(p[1],Decimal):
                #t2
                p[0] = Node('decimal', p[1])
                return
            else:
                #t1
                p[0] = Node('scalar', p[1])
                return

    if len(p) == 3: #t5
        p[0] = Node("cell_length",p[2])
        return
    
    if len(p) == 4: #t6
        p[0] = p[2]
        return 
        

def p_function_call(p):
    '''function_call : FUNC_IDENT LSQUARE arguments RSQUARE
                        | FUNC_IDENT LSQUARE RSQUARE'''
    p[0] = Node('function_call')
    p[0].addChild(Node('func',p[1]))
    if (len(p) == 5): #t1
        p[0].addChild(p[3])

# define empty productions
def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print('Syntax error',p)
    raise SystemExit

parser = yacc.yacc()

# ------------------------------------------------------------------------------
# Phase 4

from semantics_common import visit_tree, SymbolData, SemData

def add_def(node, semdata):
    #skip if not a node
    if not isinstance(node, Node):
        return None
    
    nodetype = node.nodetype

    #if it is a defninition
    if nodetype.startswith("definition"):
        vtype = nodetype.split("_")[1]
        ident = node.value
        if ident in semdata.symtbl or ident in semdata.tempSymtbl:
            return f"Error, redefine {vtype} {ident}"
        else:
            symdata = SymbolData(vtype, node)
            semdata.symtbl[ident] = symdata
            node.symdata = symdata

    if nodetype == "definition_function" or nodetype == "definition_subroutine":
        formals = node.children_[1]
        if isinstance(formals, Node): #if formals is not empty
            list_formals = formals.children_
            for arg in list_formals:
                symdata = SymbolData(arg.nodetype, node)
                semdata.tempSymtbl[arg.value] = symdata
    #check usage
    TYPE = ['func', 'sub', 'range', 'sheet', 'scalar']
    if nodetype in TYPE:
        if not isinstance(node.value, str): #ident is in an expression as expression node value contain the sign of the value as well, eg (+, sum)
            ident = node.value[1]
        else:  
            ident = node.value
        if not (ident in semdata.symtbl or ident in semdata.tempSymtbl):
            return f"Error, no {nodetype} \"{ident}\""
        

    
def clear_temp(node, semdata):
    #skip if not a node
    if not isinstance(node, Node):
        return None
    
    if node.nodetype == "definition_function" or node.nodetype == "definition_function":
        semdata.tempSymtbl.clear()


# def check_range_expr(node):

def print_symbol_table(semdata, title):
    '''Print the symbol table in semantic data
  
     Parameters:
     semdata: A SemData data structure containing semantic data
     title: String printed at the beginning
    '''
    print(title)
    for name,data in semdata.symtbl.items():
        print(name, ":")
        for attr,value in vars(data).items():
            printvalue = value
            if hasattr(value, "nodetype"): # If the value seems to be a ASTnode
                printvalue = value.nodetype
                if hasattr(value, "lineno"):
                    printvalue = printvalue + ", line " + str(value.lineno)
            print("  ", attr, "=", printvalue)

    

def semantic_checks(tree, semdata):
    #check variable
    visit_tree(tree, add_def, clear_temp, semdata)


if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()
    if ns.who == True:
        print( '292119 Nghia Duc Hong' )
    elif ns.file is None:
        arg_parser.print_help()
    else:
        with codecs.open( ns.file, 'r', encoding='utf-8' ) as INFILE:
            data = INFILE.read() 
        
        lexer.input( data )
        tree = parser.parse(data, lexer=lexer, debug=False)
        tree_print.treeprint(tree)

        semdata = SemData()
        semdata.tempSymtbl = {}
        semantic_checks(tree, semdata)
        print_symbol_table(semdata, "Symbol table:")
        print("Semantics ok")
        
