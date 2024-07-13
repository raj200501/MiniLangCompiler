open Ast

exception TypeError of string

let check (decls, body) =
  let env = List.fold_left (fun env (id, expr) -> (id, expr) :: env) [] decls in
  let rec expr = function
    | IntLit _ -> ()
    | Var id -> if not (List.mem_assoc id env) then raise (TypeError ("Unbound variable: " ^ id))
    | Binop (e1, _, e2) -> expr e1; expr e2
  in
  expr body
