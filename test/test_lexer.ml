open OUnit2
open Lexer
open Lexing

let test_lex _ =
  let lexbuf = Lexing.from_string "let x = 42 in x + 1" in
  assert_equal LET (Lexer.read lexbuf);
  assert_equal (IDENT "x") (Lexer.read lexbuf);
  assert_equal EQ (Lexer.read lexbuf);
  assert_equal (INT 42) (Lexer.read lexbuf);
  assert_equal IN (Lexer.read lexbuf);
  assert_equal (IDENT "x") (Lexer.read lexbuf);
  assert_equal PLUS (Lexer.read lexbuf);
  assert_equal (INT 1) (Lexer.read lexbuf)

let suite =
  "Lexer Tests" >::: [
    "test_lex" >:: test_lex;
  ]

let _ = run_test_tt_main suite
