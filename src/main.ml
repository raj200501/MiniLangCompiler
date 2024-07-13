open Lexer
open Parser
open Semant
open Codegen
open Aws_integration

let compile file =
  let lexbuf = Lexing.from_channel (open_in file) in
  let ast = Parser.program Lexer.read lexbuf in
  let _ = Semant.check ast in
  let code = Codegen.generate ast in
  Aws_integration.upload_to_s3 Config.s3_bucket file code;
  Printf.printf "Compilation successful! Compiled code uploaded to S3.\n"

let () =
  if Array.length Sys.argv <> 2 then
    Printf.printf "Usage: %s <source-file>\n" Sys.argv.(0)
  else
    let file = Sys.argv.(1) in
    try
      compile file
    with
    | e ->
      let msg = Printexc.to_string e in
      Aws_integration.log_error Config.dynamodb_table file msg;
      Printf.printf "Compilation failed: %s\n" msg
