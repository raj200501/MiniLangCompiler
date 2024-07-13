#!/bin/bash

# Set up AWS CLI
aws configure

# Deploy to AWS S3
aws s3 cp _build/default/src/miniLangCompiler s3://your-s3-bucket-name/

# Deploy logs and errors to DynamoDB
aws dynamodb put-item --table-name MiniLangCompilerLogs --item file://error.json
