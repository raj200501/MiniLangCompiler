%{
open Ast
%}

%token LET IN IDENT INT PLUS MINUS TIMES DIV EQ
%start program
%type <Ast.program> program

%%

program:
  | LET decl IN expr { ([], $3) }

decl:
  | IDENT EQ expr { ($1, $3) }

expr:
  | INT { IntLit $1 }
  | IDENT { Var $1 }
  | expr PLUS expr { Binop ($1, Plus, $3) }
  | expr MINUS expr { Binop ($1, Minus, $3) }
  | expr TIMES expr { Binop ($1, Times, $3) }
  | expr DIV expr { Binop ($1, Div, $3) }
