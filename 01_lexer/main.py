#!/usr/bin/env python3

import sys, ply.lex
import re
from decimal import *
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
        return t_IDENT(t)
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
    return t

def t_COORDINATE_IDENT(t):
    r'([A-Z]{1,2}[0-9]{1,3})'
    return t

def t_DECIMAL_LITERAL(t):
    r'-?\d+\.\d'
    t.value = Decimal(t.value)
    return t

def t_INT_LITERAL(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_IDENT(t):
    r'[a-z][a-zA-Z0-9_]+'
    t.type = "IDENT"
    return t

def t_RANGE_IDENT(t):
    r'_[a-zA-Z0-9_]+\s'
    return t


def t_FUNC_IDENT(t):
    r'[A-Z][a-z0-9_]+'
    return t

def t_SHEET_IDENT(t):
    r'[A-Z]+'
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

if __name__ == '__main__':
    import argparse, codecs
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()
    if ns.who == True:
        print( '292119 Nghia Duc Hong' )
    elif ns.file is None:
        parser.print_help()
    else:
        with codecs.open( ns.file, 'r', encoding='utf-8' ) as INFILE:
            data = INFILE.read() 
            
        #pre eliminate comments 
        data = re.sub(r"\.{3,3}([\s\S]*?)\.{3,3}","",data)
        lexer.input( data )

        while True:
            token = lexer.token()
            if token is None:
                break
            print( token )
