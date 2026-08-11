from pathlib import Path

from src.processor import SQLBatchProcessor
from src.validator import MetadataValidator
from src.excel_writer import ExcelWriter


def main():

    project_root = Path(__file__).resolve().parent

    sql_directory = project_root / "sample_sql"
    output_file = (
        project_root
        / "output"
        / "deployment_metadata.xlsx"
    )

    print("Starting SQL deployment metadata generation...")

    # Step 1: Process SQL files
    processor = SQLBatchProcessor(
        sql_directory
    )

    metadata_records = processor.process()

    print(
        f"Processed {len(metadata_records)} SQL files."
    )

    # Step 2: Validate metadata
    validator = MetadataValidator()

    validation_errors = validator.validate(
        metadata_records
    )

    if validation_errors:

        print("\nValidation errors found:")

        for error in validation_errors:
            print(f"- {error}")

        print(
            "\nExcel generation stopped."
        )

        return

    print("Metadata validation passed.")

    # Step 3: Generate Excel
    writer = ExcelWriter()

    generated_file = writer.write(
        metadata_records,
        output_file
    )

    print(
        f"\nExcel file generated successfully:"
    )

    print(generated_file)


if __name__ == "__main__":
    main()