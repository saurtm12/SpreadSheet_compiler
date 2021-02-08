#!/usr/bin/env python3

from ply import yacc
import lexer # previous phase example snippet code

import tree_print # syntax tree pretty-printer

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = lexer.tokens

# Simple class to store syntax tree nodes, by default only contains the type of the node as string
# (more stuff will be added in BNF actions)
class ASTnode:
  def __init__(self, typestr):
    self.nodetype = typestr

# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce 
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce 
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors

def p_program1(p):
    '''program : assign'''
    # Create a program node, with a child list containing a single expression
    p[0] = ASTnode("program")
    p[0].children_assigns = [ p[1] ]

def p_program2(p):
    '''program : program COMMA assign'''
    # For longer lists, we just use the already created "program" (containing all exprs except the last)
    # and append the last expression there
    # (Note: we switched the order of 'program' and 'assign')
    p[0] = p[1]
    p[0].children_assigns.append(p[3])

def p_assign(p):
    '''assign : ID ASSIGN expr'''
    p[0] = ASTnode("assign")
    p[0].value = p[1]
    p[0].child_expr = p[3]
    p[0].lineno = p.lineno(2) # Record the line number

def p_expr1(p):
    '''expr : expr PLUS term
            | expr MINUS term'''
    # Create a new tree node describing the operation
    p[0] = ASTnode("oper "+p[2])
    p[0].child_left = p[1] # Store left operand as a child node, tree_print() can print child_* fields as a tree
    p[0].child_right = p[3] # Store right operand as a child node, tree_print() can print child_* fields as a tree
    p[0].lineno = p.lineno(2) # Record the line number

def p_expr2(p):
    '''expr : term'''
    # Nothing todo, just pass the node onwards
    p[0] = p[1]

def p_term1(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    # Create a new tree node describing the operation
    p[0] = ASTnode("oper "+p[2])
    p[0].child_left = p[1] # Store left operand as a child node, tree_print() can print child_* fields as a tree
    p[0].child_right = p[3] # Store right operand as a child node, tree_print() can print child_* fields as a tree
    p[0].lineno = p.lineno(2) # Record the line number

def p_term2(p):
    '''term : factor'''
    # Nothing todo, just pass the node onwards
    p[0] = p[1]

def p_factor1(p):
    '''factor : NUMBER'''
    # Create a new node for the number literal
    p[0] = ASTnode("number")
    p[0].value = p[1] # Store the value of the literal, tree_print() can print the "value" field nicely
    p[0].lineno = p.lineno(1) # Record the line number

def p_factor2(p):
    '''factor : ID'''
    # Create a new node for the number literal
    p[0] = ASTnode("variable")
    p[0].value = p[1] # Store the value of the literal, tree_print() can print the "value" field nicely
    p[0].lineno = p.lineno(1) # Record the line number

def p_factor3(p):
    '''factor : LPAREN expr RPAREN'''
    # Nothing todo, just pass the node onwards
    p[0] = p[2]

# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print( 'syntax error @', p )
    raise SystemExit

parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    outformat="unicode"
    if ns.treetype:
      outformat = ns.treetype

    if ns.who == True:
        # identify who wrote this
        print( '88888 Ahto Simakuutio' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)
        # Pretty print the resulting tree
        tree_print.treeprint(result, outformat)
