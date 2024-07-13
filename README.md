# MiniLangCompiler

**MiniLangCompiler** is an OCaml-based compiler for a domain-specific language (DSL) named **MiniLang**. The project involves parsing, semantic analysis, and code generation. The compiled code is uploaded to an AWS S3 bucket, and logs and errors are stored in an AWS DynamoDB table for analysis.

## Features

- Lexical analysis, parsing, and semantic analysis for MiniLang
- Code generation for MiniLang
- Integration with AWS S3 for storing compiled code
- Integration with AWS DynamoDB for logging and error reporting

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/MiniLangCompiler.git
    cd MiniLangCompiler
    ```

2. Install dependencies and build the project:
    ```bash
    opam install dune aws-s3 aws-dynamodb
    dune build
    ```

## Usage

1. Compile MiniLang source files:
    ```bash
    dune exec ./miniLangCompiler <source-file>
    ```

2. The compiled code will be uploaded to an AWS S3 bucket, and logs and errors will be stored in an AWS DynamoDB table.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
