# AWS Integration

MiniLangCompiler can upload compiled bytecode to AWS S3 and log errors to AWS
DynamoDB. AWS integration is optional and is disabled by default to keep the
project deterministic and easy to run.

## Enabling AWS mode

1. Install boto3 (outside of `requirements.txt` so local runs stay dependency
   free):

   ```bash
   python -m pip install boto3
   ```

2. Configure credentials and region. For example:

   ```bash
   export AWS_ACCESS_KEY_ID=your-access-key
   export AWS_SECRET_ACCESS_KEY=your-secret
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. Enable AWS mode:

   ```bash
   export MINILANG_AWS_MODE=true
   ```

4. Optionally set bucket and table names:

   ```bash
   export MINILANG_BUCKET=my-artifacts
   export MINILANG_TABLE=MiniLangCompilerLogs
   ```

## Expected AWS resources

- **S3 bucket**: the compiler writes two objects per compilation: `<key>.mlc`
  (compiled bytecode) and `<key>.json` (metadata).
- **DynamoDB table**: the compiler inserts items with `Key`, `Message`, and
  `Timestamp` attributes when compilation fails.

Create these resources before running the compiler.

## Security notes

The compiler only requires permission to write to S3 and DynamoDB. Use IAM roles
and least privilege policies. Because the project can run without AWS, CI does
not attempt to connect to AWS resources.
