from pathlib import Path

import pytest

from src.parser import SQLParser


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_SQL_DIR = PROJECT_ROOT / "sample_sql"


def test_parse_create_table():

    parser = SQLParser()

    result = parser.parse_file(
        SAMPLE_SQL_DIR / "customer_hub.sql"
    )

    assert result.file_name == "customer_hub.sql"
    assert result.deployment_group == "CUSTOMER_DATA"
    assert result.sequence == 10
    assert result.operation == "CREATE"
    assert result.object_type == "TABLE"
    assert result.object_name == "customer_hub"


def test_sql_comments_are_removed():

    parser = SQLParser()

    result = parser.parse_file(
        SAMPLE_SQL_DIR / "customer_hub.sql"
    )

    assert "deployment_group:" not in result.sql_statement
    assert "sequence:" not in result.sql_statement


def test_missing_metadata_raises_error(tmp_path):

    invalid_sql = tmp_path / "invalid.sql"

    invalid_sql.write_text(
        """
        CREATE TABLE customer_test (
            id INT
        );
        """,
        encoding="utf-8",
    )

    parser = SQLParser()

    with pytest.raises(ValueError, match="Missing metadata"):
        parser.parse_file(invalid_sql)
