open OUnit2
open Codegen
open Ast

let test_codegen _ =
  let ast = (["x", IntLit 42], Binop (Var "x", Plus, IntLit 1)) in
  let code = Codegen.generate ast in
  assert_equal "x = 42\n(x + 1)" code

let suite =
  "Codegen Tests" >::: [
    "test_codegen" >:: test_codegen;
  ]

let _ = run_test_tt_main suite
