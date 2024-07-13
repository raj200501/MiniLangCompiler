open OUnit2
open Aws_integration

let test_upload_to_s3 _ =
  assert_equal () (Aws_integration.upload_to_s3 "test-bucket" "test-file" "content")

let test_log_error _ =
  assert_equal () (Aws_integration.log_error "test-table" "test-file" "error")

let suite =
  "AWS Integration Tests" >::: [
    "test_upload_to_s3" >:: test_upload_to_s3;
    "test_log_error" >:: test_log_error;
  ]

let _ = run_test_tt_main suite
