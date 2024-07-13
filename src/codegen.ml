open Ast

let rec generate_expr = function
  | IntLit i -> string_of_int i
  | Var id -> id
  | Binop (e1, op, e2) ->
    let op_str = match op with
      | Plus -> "+"
      | Minus -> "-"
      | Times -> "*"
      | Div -> "/"
    in
    "(" ^ generate_expr e1 ^ " " ^ op_str ^ " " ^ generate_expr e2 ^ ")"

let generate (decls, body) =
  let decls_str = List.map (fun (id, expr) -> id ^ " = " ^ generate_expr expr) decls in
  let body_str = generate_expr body in
  String.concat "\n" decls_str ^ "\n" ^ body_str
