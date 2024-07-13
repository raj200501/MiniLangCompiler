open Aws_s3
open Aws_dynamodb

let upload_to_s3 bucket file content =
  let open Lwt.Infix in
  S3.put_object ~bucket ~key:file ~content ()
  >|= fun _ -> ()

let log_error table file message =
  let item = [
    "File", DynamoDB.string file;
    "Error", DynamoDB.string message;
  ] in
  DynamoDB.put_item ~table ~item ()
