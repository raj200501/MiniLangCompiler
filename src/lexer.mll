{
  open Parser
  exception Eof
}

rule read = parse
  | [' ' '\t' '\r' '\n'] { read lexbuf }
  | "let"                { LET }
  | "in"                 { IN }
  | ['a'-'z' 'A'-'Z']+ as id { IDENT id }
  | ['0'-'9']+ as num   { INT (int_of_string num) }
  | '+'                 { PLUS }
  | '-'                 { MINUS }
  | '*'                 { TIMES }
  | '/'                 { DIV }
  | '='                 { EQ }
  | eof                 { raise Eof }
  | _                   { failwith "Unexpected character" }
