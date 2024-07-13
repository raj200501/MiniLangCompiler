open OUnit2
open Parser
open Lexer
open Lexing
open Ast

let test_parse _ =
  let lexbuf = Lexing.from_string "let x = 42 in x + 1" in
  let ast = Parser.program Lexer.read lexbuf in
  assert_equal ([], Binop (Var "x", Plus, IntLit 1)) ast

let suite =
  "Parser Tests" >::: [
    "test_parse" >:: test_parse;
  ]

let _ = run_test_tt_main suite
