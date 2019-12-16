grammar MC;

@lexer::header {
from lexererr import *
}

@lexer::member {
def emit(self):
    tk = self.type
    if tk == UNCLOSE_STRING:       
        result = super.emit();
        raise UncloseString(result.text);
    elif tk == ILLEGAL_ESCAPE:
        result = super.emit();
        raise IllegalEscape(result.text);
    elif tk == ERROR_CHAR:
        result = super.emit();
        raise ErrorToken(result.text); 
    else:
        return super.emit();
}

options{
	language=Python3;
}

program: decl+ EOF;

decl: var_decl | func_decl;

var_decl: primi_type id_list SEMI;

primi_type: INTTYPE | BOOLTYPE | FLOATTYPE | STRINGTYPE;

id_list: identifier (COMMA identifier)*;

identifier: id_array | id_single;

id_array: ID LSB INTLIT RSB;

id_single: ID;

func_decl: (primi_type | VOIDTYPE | array_pointer_type) ID LB param_list? RB block_stmt;

array_pointer_type: primi_type LSB RSB;

param_list: param_decl (COMMA param_decl)*;

param_decl: primi_type (ID | ID LSB RSB);

statement
    : if_stmt
    | dowhile_stmt
    | for_stmt
    | break_stmt
    | continue_stmt
    | return_stmt
    | expression_stmt
    | block_stmt
    ;

if_stmt: IF LB expression RB statement (ELSE statement)?;

dowhile_stmt: DO statement+ WHILE expression SEMI;

for_stmt : FOR LB expression SEMI expression SEMI expression RB statement;

break_stmt: BREAK SEMI;

continue_stmt: CONTINUE SEMI;

return_stmt: RETURN expression? SEMI;

expression_stmt: expression SEMI;

block_stmt: LP blockmem* RP;

blockmem: var_decl | statement;

expression: expression1 ASSIGNOP expression | expression1;

expression1: expression1 OROP expression2 | expression2;

expression2: expression2 ANDOP expression3 | expression3;

expression3: expression4 (EQUALOP | NOTEQUALOP) expression4 | expression4;

expression4: expression5 (LESSOP | GREATEROP | LEOP | GEOP) expression5 | expression5;

expression5: expression5 (ADDOP | SUBOP) expression6 | expression6;

expression6: expression6 (DIVOP | MULOP | MODOP) expression7 | expression7;

expression7: (SUBOP | NOTOP) expression7 | expression8;

expression8: expression8 LSB expression RSB | expression9;

expression9 : LB expression RB | operand;

operand: literal | identifier | func_call;

literal: INTLIT | FLOATLIT | STRINGLIT | BOOLLIT;

func_call: ID LB param_list_call? RB;

param_list_call: param_call (COMMA param_call)*;

param_call : literal | identifier | expression;

// Literals
INTLIT: DIGIT+;

FLOATLIT: (DIGIT+ ('.'DIGIT*)?|('.'DIGIT+)) EXPONENT?;

BOOLLIT: TRUE | FALSE;

// Keywords
BOOLTYPE: 'boolean';

BREAK: 'break';

CONTINUE: 'continue';

ELSE: 'else';

FOR: 'for';

FLOATTYPE: 'float';

IF: 'if';

INTTYPE: 'int';

RETURN: 'return';

VOIDTYPE: 'void';

STRINGTYPE: 'string';

DO: 'do';

WHILE: 'while';

TRUE: 'true';

FALSE: 'false';

fragment LETTER: [a-zA-Z];

fragment DIGIT: [0-9];

fragment QUOTE: '"';

fragment EXPONENT: [Ee] '-'? DIGIT+;

// Character Set
WHITESPACE_CHARACTER: [ \b\t\f\r\n]+ -> skip;

// Comment
BLOCK_COMMENT: '/*' .*? '*/' -> skip;

LINE_COMMENT: '//' (~'\n')* -> skip;

// Operators
ADDOP: '+';

SUBOP: '-';

MULOP: '*';

DIVOP: '/';

NOTOP: '!';

MODOP: '%';

OROP: '||';

ANDOP: '&&';

NOTEQUALOP: '!=';

EQUALOP: '==';

LESSOP: '<';

GREATEROP: '>';

LEOP: '<=';

GEOP: '>=';

ASSIGNOP: '=';

// Separators
LSB: '[';

RSB: ']';

LP: '{';

RP: '}';

LB: '(';

RB: ')';

SEMI: ';';

COMMA: ',';

// Identifier
ID: (LETTER|'_') (DIGIT|LETTER|'_')*;

STRINGLIT: QUOTE ( '\\' [bfrnt"\\] | ~[\b\f\r\n\t"\\] )* QUOTE
    {self.text = self.text[1:-1]};

ILLEGAL_ESCAPE: '"' ( '\\' [bfnrt"\\] | ~[\b\f\n\r\t"\\] )* ('\\' ~[bfnrt"\\] | [\b\f\t"\\]) 
    {raise IllegalEscape(self.text[1:])};

UNCLOSE_STRING: QUOTE ( '\\' [bfnrt"\\] | ~[\b\f\n\r\t"\\] )*
    {raise UncloseString(self.text[1:])};

ERROR_CHAR: .
    {raise ErrorToken(self.text)};