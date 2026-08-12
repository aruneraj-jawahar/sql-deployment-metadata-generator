import argparse
import sys
from pathlib import Path

from src.excel_writer import ExcelWriter
from src.processor import SQLBatchProcessor
from src.validator import MetadataValidator


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Generate deployment metadata Excel "
            "from SQL files."
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Directory containing SQL files."
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path of the output Excel file."
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    sql_directory = Path(args.input)
    output_file = Path(args.output)

    print("Starting SQL deployment metadata generation...")

    if not sql_directory.exists():
        print(
            f"Error: Input directory not found: "
            f"{sql_directory}"
        )
        return 1

    if not sql_directory.is_dir():
        print(
            f"Error: Input path is not a directory: "
            f"{sql_directory}"
        )
        return 1

    try:
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

            print("\nExcel generation stopped.")

            return 1

        print("Metadata validation passed.")

        # Step 3: Generate Excel
        writer = ExcelWriter()

        generated_file = writer.write(
            metadata_records,
            output_file
        )

        print(
            "\nExcel file generated successfully:"
        )
        print(generated_file)

        return 0

    except Exception as error:
        print(
            f"\nError during metadata generation: "
            f"{error}"
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())