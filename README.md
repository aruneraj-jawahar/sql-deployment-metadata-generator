# SQL Deployment Metadata Generator

A Python-based automation tool that extracts deployment metadata from SQL files, validates the extracted information, and generates a structured Excel deployment workbook.

The project is designed around a common SQL deployment workflow where multiple database objects need to be executed in a defined sequence and grouped by deployment batch.

---

##  Project Overview

In data engineering projects, SQL deployment files often need to be executed in a specific order.

When multiple SQL objects such as tables, views, and data-load statements are involved, maintaining deployment metadata manually can become repetitive and error-prone.

This project automates that process by extracting deployment information directly from SQL files and generating a structured Excel deployment artifact.

The application:

- Reads SQL files from an input directory
- Extracts deployment metadata
- Parses SQL statements
- Validates the extracted metadata
- Processes multiple SQL files in batch
- Sorts objects based on deployment group and sequence
- Generates a formatted Excel workbook
- Generates a deployment summary
- Provides automated test coverage

---

#  Problem Statement

Managing deployment metadata manually for a large number of SQL objects can be time-consuming and error-prone.

For each SQL file, information such as:

- Deployment group
- Execution sequence
- SQL operation
- Object type
- Object name
- SQL statement

may need to be captured and organized into a deployment artifact.

Manually maintaining this information can lead to:

- Incorrect execution sequences
- Missing metadata
- Duplicate or inconsistent information
- Manual Excel preparation
- Increased deployment preparation effort

This project automates the metadata extraction and Excel generation process.

---

#  Solution

The solution uses Python to extract deployment metadata from SQL files and convert it into a structured deployment workbook.

The overall workflow is:

```text
                    SQL Files
                       │
                       ▼
                SQL Batch Processor
                       │
                       ▼
                   SQL Parser
                       │
                       ▼
              Metadata Extraction
                       │
                       ▼
              Metadata Validation
                       │
                ┌──────┴──────┐
                │             │
             Invalid         Valid
                │             │
                ▼             ▼
         Stop Processing   Excel Writer
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
          Deployment Metadata             Summary
                Sheet                     Sheet
````

---

#  Application Flow

### 1. SQL Files

The application receives a directory containing SQL files.

Example:

```text
sample_sql/
├── customer_table.sql
├── customer_load.sql
└── policy_table.sql
```

Each SQL file contains deployment metadata in comments.

Example:

```sql
-- deployment_group: CUSTOMER_DATA
-- sequence: 10

CREATE TABLE customer (
    customer_id INT,
    customer_name VARCHAR(100)
);
```

---

### 2. SQL Batch Processor

The batch processor scans the input directory and identifies SQL files.

It processes multiple files and passes each file to the SQL parser.

```text
SQL Directory
     │
     ├── customer_table.sql
     ├── customer_load.sql
     └── policy_table.sql
              │
              ▼
       SQL Batch Processor
```

---

### 3. SQL Parser

The parser reads each SQL file and extracts the required metadata.

It identifies:

* File name
* Deployment group
* Sequence
* SQL operation
* Object type
* Object name
* SQL statement

The extracted information is represented using the `SQLMetadata` data model.

---

### 4. Metadata Validation

The extracted metadata is validated before Excel generation.

If validation errors are detected, the application stops the process and does not generate the Excel output.

This provides an additional validation layer before creating the deployment artifact.

Example:

```text
Invalid metadata
       │
       ▼
Validation Failure
       │
       ▼
Excel generation stopped
```

---

### 5. Sorting and Processing

Valid metadata records are processed and sorted using:

```text
Deployment Group
        ↓
Sequence
```

This allows SQL objects to appear in their intended deployment order.

Example:

```text
CUSTOMER_DATA
    Sequence 10
    Sequence 20
    Sequence 30

POLICY_DATA
    Sequence 10
    Sequence 20
```

---

### 6. Excel Generation

The validated metadata is passed to the Excel writer.

The Excel writer generates a structured workbook containing:

### Deployment Metadata Sheet

Contains detailed information about each SQL object.

### Summary Sheet

Contains high-level deployment information including:

* Deployment group
* Object count
* First sequence
* Last sequence

The workbook also includes:

* Excel tables
* Filters
* Frozen headers
* Readable column widths
* Wrapped SQL statements
* Structured formatting

---

#  Example Output

The generated workbook contains a **Deployment Metadata** sheet similar to:

| File Name          | Deployment Group | Sequence | Operation | Object Type | Object Name |
| ------------------ | ---------------- | -------: | --------- | ----------- | ----------- |
| customer_table.sql | CUSTOMER_DATA    |       10 | CREATE    | TABLE       | customer    |
| customer_load.sql  | CUSTOMER_DATA    |       20 | INSERT    | UNKNOWN     | customer    |
| policy_table.sql   | POLICY_DATA      |       10 | CREATE    | TABLE       | policy      |

The **Summary** sheet provides an overview:

| Deployment Group | Object Count | First Sequence | Last Sequence |
| ---------------- | -----------: | -------------: | ------------: |
| CUSTOMER_DATA    |            2 |             10 |            20 |
| POLICY_DATA      |            1 |             10 |            10 |

---

#  Key Features

* SQL file batch processing
* Deployment metadata extraction
* SQL operation detection
* SQL object type detection
* SQL object name extraction
* Metadata validation
* Deployment group and sequence handling
* Automated Excel generation
* Deployment summary generation
* Configurable input directory
* Configurable output file
* Command-line interface
* Error handling
* Automated testing
* Modular architecture

---

#  Project Architecture

The project follows a modular architecture where each component has a specific responsibility.

```text
                         main.py
                            │
                            ▼
                  SQLBatchProcessor
                            │
                            ▼
                       SQLParser
                            │
                            ▼
                      SQLMetadata
                            │
                            ▼
                   MetadataValidator
                            │
                            ▼
                      ExcelWriter
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
       Deployment Metadata          Summary
             Sheet                   Sheet
```

### Components

| Component         | Responsibility                                     |
| ----------------- | -------------------------------------------------- |
| `main.py`         | Application entry point and workflow orchestration |
| `metadata.py`     | Defines the SQL metadata data model                |
| `parser.py`       | Extracts metadata from SQL files                   |
| `processor.py`    | Processes multiple SQL files                       |
| `validator.py`    | Validates extracted metadata                       |
| `excel_writer.py` | Generates and formats Excel output                 |
| `tests/`          | Automated unit and integration tests               |

---

# 📁 Project Structure

```text
sql-deployment-metadata-generator/
│
├── main.py
├── README.md
├── requirements.txt
│
├── src/
│   ├── metadata.py
│   ├── parser.py
│   ├── processor.py
│   ├── validator.py
│   └── excel_writer.py
│
├── sample_sql/
│   ├── sample_table.sql
│   └── sample_load.sql
│
├── tests/
│   ├── test_parser.py
│   ├── test_processor.py
│   ├── test_validator.py
│   ├── test_excel_writer.py
│   └── test_main.py
│
└── output/
    └── deployment_metadata.xlsx
```

---

#  Metadata Format

SQL files contain deployment metadata using SQL comments.

Example:

```sql
-- deployment_group: CUSTOMER_DATA
-- sequence: 10

CREATE TABLE customer (
    customer_id INT,
    customer_name VARCHAR(100)
);
```

The application extracts:

| Metadata         | Example            |
| ---------------- | ------------------ |
| File Name        | customer_table.sql |
| Deployment Group | CUSTOMER_DATA      |
| Sequence         | 10                 |
| Operation        | CREATE             |
| Object Type      | TABLE              |
| Object Name      | customer           |

---

#  SQL Parsing

The parser currently identifies common SQL operations including:

```text
CREATE
INSERT
UPDATE
DELETE
ALTER
DROP
```

For supported `CREATE` statements, it can identify object types such as:

```text
TABLE
VIEW
MATERIALIZED VIEW
```

The parser also removes SQL comments before analyzing the SQL statement itself.

---

#  Validation

Metadata validation is performed before generating the Excel workbook.

The validation stage helps prevent invalid deployment metadata from being included in the final output.

The workflow is:

```text
SQL Files
    ↓
Parsing
    ↓
Metadata
    ↓
Validation
    ↓
Valid?
  /   \
No     Yes
│       │
Stop   Excel
```

If validation fails:

```text
Validation errors found:
- <validation error>

Excel generation stopped.
```

---

#  Command-Line Usage

The application can be executed using the command line.

## Display Help

```bash
python main.py --help
```

Example:

```text
usage: main.py [-h] --input INPUT --output OUTPUT

Generate deployment metadata Excel from SQL files.

options:
  -h, --help       show this help message
  --input INPUT    Directory containing SQL files.
  --output OUTPUT  Path of the output Excel file.
```

---

#  Running the Application

## 1. Clone the Repository

```bash
git clone https://github.com/aruneraj-jawahar/sql-deployment-metadata-generator.git
```

## 2. Navigate to the Project

```bash
cd sql-deployment-metadata-generator
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the Application

```bash
python main.py --input sample_sql --output output/deployment_metadata.xlsx
```

Example output:

```text
Starting SQL deployment metadata generation...
Processed X SQL files.
Metadata validation passed.

Excel file generated successfully:
output\deployment_metadata.xlsx
```

The generated workbook will be available at:

```text
output/deployment_metadata.xlsx
```

---

#  Error Handling

The application validates the input directory before processing.

### Missing Directory

```bash
python main.py --input does_not_exist --output output/test.xlsx
```

The application reports:

```text
Error: Input directory not found: does_not_exist
```

### Input Path Is a File

If a SQL file is provided instead of a directory:

```text
Error: Input path is not a directory: ...
```

The application also prevents Excel generation when metadata validation fails.

---

#  Testing

The project uses **Pytest** for automated testing.

Run the complete test suite:

```bash
python -m pytest
```

The current project contains:

```text
27 automated tests
```

All tests should pass successfully.

The tests cover:

* SQL metadata extraction
* SQL operation detection
* SQL object identification
* Batch processing
* Metadata validation
* Excel generation
* Excel formatting
* Summary sheet generation
* CLI execution
* Invalid input handling
* Validation failure handling
* End-to-end workflow

---

#  Testing Approach

The project follows a modular testing approach.

```text
Parser Tests
     ↓
Processor Tests
     ↓
Validator Tests
     ↓
Excel Writer Tests
     ↓
Main / CLI Tests
     ↓
End-to-End Workflow
```

This ensures that both individual components and the overall application workflow are tested.

---

#  Technologies Used

* **Python** – Application development
* **Pandas** – Data processing
* **OpenPyXL** – Excel workbook creation and formatting
* **Pytest** – Automated testing
* **SQL** – Input data/deployment scripts
* **Git** – Version control
* **GitHub** – Source code management

---

#  Design Principles

The project follows a modular design approach.

Each component has a clearly defined responsibility.

For example:

```text
Parser
→ Understands SQL

Processor
→ Handles multiple files

Validator
→ Checks metadata

Excel Writer
→ Generates deployment artifact

Main
→ Orchestrates the workflow
```

This separation makes the project easier to:

* Maintain
* Test
* Debug
* Extend
* Reuse

---

#  Real-World Inspiration

This project is inspired by SQL deployment automation workflows commonly used in data engineering environments.

In large data engineering projects, developers may work with a significant number of SQL objects that need to be organized and deployed in a controlled sequence.

Preparing deployment metadata manually can become repetitive.

This project demonstrates how Python can be used to automate that repetitive preparation process while incorporating:

* Metadata extraction
* Validation
* Batch processing
* Structured output
* Automated testing

The implementation in this repository is intentionally generalized and does not contain proprietary SQL, credentials, database information, or organization-specific implementation details.

---

#  Future Enhancements

Potential future improvements include:

* YAML-based configuration
* Support for additional SQL dialects
* More advanced SQL parsing
* Duplicate sequence detection
* Deployment dependency validation
* Structured application logging
* Configuration-driven validation rules
* CI/CD integration
* Additional Excel reporting
* CSV output
* JSON output
* Database integration
* Deployment dependency visualization

---

#  Portfolio Relevance

This project demonstrates practical skills relevant to Data Engineering roles, including:

* Python automation
* SQL processing
* ETL-style data transformation
* Data validation
* Batch processing
* File-based data pipelines
* Excel automation
* Software testing
* Git/GitHub
* Command-line application development
* Modular software design

---

#  Author

**Arun**

Data Engineer | SQL | Python | AWS | Data Engineering