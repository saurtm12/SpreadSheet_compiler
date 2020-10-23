#!/usr/bin/env python3

import sys, ply.lex
import re

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
    try:
        t.value = float(t.value)
    except ValueError:
        print('Float is too large')
        t.value =0
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

# ------------------------------------------------------------------------------
# Phase 2
# Define the syntax_check:
from ply import yacc

### {a} : a_star
### [a] : a_opt
### <a+> : a_plus // if necessary 
def p_program(p):
    ''' program : function_or_vaiable_definition_star statement_list'''

def p_function_or_vaiable_definition_star(p):
    '''function_or_vaiable_definition_star  : function_or_vaiable_definition_star function_or_vaiable_definition
                                            | empty'''

def p_function_or_vaiable_definition(p):
    '''function_or_vaiable_definition   : variable_definition 
                                        | function_definition 
                                        | subroutine_definition'''

def p_variable_definition_star(p):
    '''variable_definition_star : variable_definition_star variable_definition
                                | empty'''

def p_variable_definition(p):
    '''variable_definition : scalar_definition 
                            | range_definition 
                            | sheet_definition'''

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
 
def p_subroutine_definition(p):
    '''subroutine_definition : FUNC_IDENT LSQUARE formals_opt RSQUARE IS \
                                variable_definition_star \
                                statement_list \
                                END'''

def p_formals_opt(p):
    '''formals_opt : formals
                    | empty'''

def p_formals(p):
    '''formals : formals COMMA formal_arg
                | formal_arg'''

def p_formal_arg(p):
    '''formal_arg :  IDENT COLON SCALAR
                    | RANGE_IDENT COLON RANGE
                    | SHEET_IDENT COLON SHEET'''

def p_sheet_definition(p):
    '''sheet_definition : SHEET SHEET_IDENT sheet_init_opt'''

def p_sheet_init_opt(p):
    '''sheet_init_opt : sheet_init
                        | empty'''

def p_sheet_init(p):
    '''sheet_init : EQ sheet_init_list 
                    | EQ INT_LITERAL MULT INT_LITERAL'''

def p_sheet_init_list(p):
    '''sheet_init_list : LCURLY sheet_row_plus RCURLY'''

def p_sheet_row_plus(p):
    '''sheet_row_plus : sheet_row_plus sheet_row
                        | sheet_row'''

def p_sheet_row(p):
    '''sheet_row : sheet_row COMMA simple_expr
                | simple_expr'''

def p_range_definition(p):
    '''range_definition : RANGE RANGE_IDENT 
                        | RANGE RANGE_IDENT EQ range_expr'''

def p_scalar_definition(p):
    '''scalar_definition : SCALAR IDENT  
                            | SCALAR IDENT EQ scalar_expr'''

def p_statement_list(p):
    '''statement_list : statement_list statement
                        | statement'''

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

def p_info_string_opt(p):
    '''info_string_opt : INFO_STRING
                        | empty'''

def p_range_list(p):
    '''range_list : range_list COMMA range_expr
                    | range_expr'''

def p_arguments(p):
    '''arguments : arguments COMMA arg_expr
                    | arg_expr'''

def p_arg_expr(p):
    '''arg_expr : scalar_expr 
                | range_expr 
                | SHEET_IDENT'''

def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE empty RSQUARE
                        | FUNC_IDENT LSQUARE arguments RSQUARE'''

def p_assignment(p):
    '''assignment : IDENT ASSIGN scalar_expr
                    | cell_ref ASSIGN scalar_expr
                    | RANGE_IDENT ASSIGN range_expr
                    | SHEET_IDENT ASSIGN SHEET_IDENT'''

def p_range_expr(p):
    '''range_expr : RANGE_IDENT
                    | RANGE cell_ref DOTDOT cell_ref
                    | LSQUARE function_call RSQUARE
                    | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''

def p_cell_ref(p):
    '''cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR 
                | DOLLAR  COLON RANGE_IDENT'''

def p_scalar_expr(p):
    '''scalar_expr : scalar_expr compare simple_expr
                    | simple_expr'''

def p_compare(p):
    '''compare : EQ 
                | NOTEQ 
                | LT 
                | LTEQ 
                | GT 
                | GTEQ'''

def p_simple_expr(p):
    '''simple_expr : simple_expr PLUS term
                    | simple_expr MINUS term
                    | term'''

def p_term(p):
    '''term : term MULT factor
            | term DIV factor
            | factor'''

def p_factor(p):
    '''factor : empty atom
                | MINUS atom'''

def p_atom(p):
    '''atom : IDENT 
            | DECIMAL_LITERAL 
            | function_call
            | cell_ref 
            | NUMBER_SIGN range_expr
            | LPAREN scalar_expr RPAREN'''

def p_function_call(p):
    '''function_call : FUNC_IDENT LSQUARE arguments RSQUARE
                        | FUNC_IDENT LSQUARE empty RSQUARE'''

# define empty productions
def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print('Syntax error',p)
    raise SystemExit


parser = yacc.yacc()




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

        rTokens = lexer.tokens
