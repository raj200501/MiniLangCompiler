open OUnit2
open Semant
open Ast

let test_semant _ =
  let ast = (["x", IntLit 42], Binop (Var "x", Plus, IntLit 1)) in
  assert_equal () (Semant.check ast)

let suite =
  "Semant Tests" >::: [
    "test_semant" >:: test_semant;
  ]

let _ = run_test_tt_main suite
