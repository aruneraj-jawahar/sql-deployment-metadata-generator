import re
from pathlib import Path

from metadata import SQLMetadata


class SQLParser:

    def parse_file(self, file_path: str) -> SQLMetadata:
        path = Path(file_path)

        sql_content = path.read_text(encoding="utf-8")

        deployment_group = self._extract_metadata(
            sql_content,
            "deployment_group"
        )

        sequence = self._extract_metadata(
            sql_content,
            "sequence"
        )

        sql_statement = self._remove_comments(sql_content).strip()

        operation = self._extract_operation(sql_statement)

        object_type = self._extract_object_type(sql_statement)

        object_name = self._extract_object_name(
            sql_statement,
            operation,
            object_type
        )

        return SQLMetadata(
            file_name=path.name,
            deployment_group=deployment_group,
            sequence=int(sequence),
            operation=operation,
            object_type=object_type,
            object_name=object_name,
            sql_statement=sql_statement,
        )

    @staticmethod
    def _extract_metadata(
        sql_content: str,
        metadata_name: str
    ) -> str:

        pattern = rf"{metadata_name}\s*:\s*(.+)"

        match = re.search(
            pattern,
            sql_content,
            re.IGNORECASE
        )

        if not match:
            raise ValueError(
                f"Missing metadata: {metadata_name}"
            )

        return match.group(1).strip()

    @staticmethod
    def _remove_comments(sql_content: str) -> str:

        sql_content = re.sub(
            r"/\*.*?\*/",
            "",
            sql_content,
            flags=re.DOTALL
        )

        sql_content = re.sub(
            r"--.*?$",
            "",
            sql_content,
            flags=re.MULTILINE
        )

        return sql_content

    @staticmethod
    def _extract_operation(sql_statement: str) -> str:

        match = re.match(
            r"\s*(CREATE|INSERT|UPDATE|DELETE|ALTER|DROP)",
            sql_statement,
            re.IGNORECASE
        )

        if not match:
            raise ValueError(
                "Unable to determine SQL operation"
            )

        return match.group(1).upper()

    @staticmethod
    def _extract_object_type(sql_statement: str) -> str:

        match = re.match(
            r"\s*CREATE\s+(TABLE|VIEW|MATERIALIZED\s+VIEW)",
            sql_statement,
            re.IGNORECASE
        )

        if match:
            return match.group(1).upper()

        return "UNKNOWN"

    @staticmethod
    def _extract_object_name(
        sql_statement: str,
        operation: str,
        object_type: str
    ) -> str:

        if operation == "CREATE":

            pattern = (
                rf"CREATE\s+{object_type}\s+"
                r"([A-Za-z0-9_.]+)"
            )

            match = re.search(
                pattern,
                sql_statement,
                re.IGNORECASE
            )

            if match:
                return match.group(1)

        return "UNKNOWN"
