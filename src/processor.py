from pathlib import Path

from src.metadata import SQLMetadata
from src.parser import SQLParser


class SQLBatchProcessor:

    def __init__(self, sql_directory: str):
        self.sql_directory = Path(sql_directory)
        self.parser = SQLParser()

    def process(self) -> list[SQLMetadata]:

        if not self.sql_directory.exists():
            raise FileNotFoundError(
                f"SQL directory not found: {self.sql_directory}"
            )

        sql_files = sorted(
            self.sql_directory.glob("*.sql")
        )

        if not sql_files:
            raise ValueError(
                f"No SQL files found in: {self.sql_directory}"
            )

        metadata_records = []

        for sql_file in sql_files:
            metadata = self.parser.parse_file(sql_file)
            metadata_records.append(metadata)

        return metadata_records