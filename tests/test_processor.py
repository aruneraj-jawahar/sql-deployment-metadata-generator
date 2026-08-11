from pathlib import Path

import pytest

from src.processor import SQLBatchProcessor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_SQL_DIR = PROJECT_ROOT / "sample_sql"


def test_process_sql_directory():

    processor = SQLBatchProcessor(
        SAMPLE_SQL_DIR
    )

    results = processor.process()

    assert len(results) == 2

    file_names = {
        result.file_name
        for result in results
    }

    assert file_names == {
        "customer_hub.sql",
        "customer_load.sql",
    }


def test_process_returns_metadata_objects():

    processor = SQLBatchProcessor(
        SAMPLE_SQL_DIR
    )

    results = processor.process()

    assert results[0].deployment_group == "CUSTOMER_DATA"
    assert results[1].deployment_group == "CUSTOMER_DATA"


def test_missing_directory_raises_error(tmp_path):

    missing_directory = (
        tmp_path / "does_not_exist"
    )

    processor = SQLBatchProcessor(
        missing_directory
    )

    with pytest.raises(
        FileNotFoundError,
        match="SQL directory not found"
    ):
        processor.process()