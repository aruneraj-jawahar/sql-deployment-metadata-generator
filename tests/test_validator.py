from src.metadata import SQLMetadata
from src.validator import MetadataValidator


def create_metadata(
    file_name="customer.sql",
    deployment_group="CUSTOMER_DATA",
    sequence=10,
    operation="CREATE",
    object_type="TABLE",
    object_name="customer",
):

    return SQLMetadata(
        file_name=file_name,
        deployment_group=deployment_group,
        sequence=sequence,
        operation=operation,
        object_type=object_type,
        object_name=object_name,
        sql_statement="CREATE TABLE customer (...)",
    )


def test_valid_metadata_has_no_errors():

    metadata = create_metadata()

    validator = MetadataValidator()

    errors = validator.validate(
        [metadata]
    )

    assert errors == []


def test_missing_deployment_group():

    metadata = create_metadata(
        deployment_group=""
    )

    validator = MetadataValidator()

    errors = validator.validate(
        [metadata]
    )

    assert any(
        "Deployment group is missing" in error
        for error in errors
    )


def test_invalid_sequence():

    metadata = create_metadata(
        sequence=0
    )

    validator = MetadataValidator()

    errors = validator.validate(
        [metadata]
    )

    assert any(
        "Sequence must be greater than zero" in error
        for error in errors
    )


def test_unknown_object_name():

    metadata = create_metadata(
        object_name="UNKNOWN"
    )

    validator = MetadataValidator()

    errors = validator.validate(
        [metadata]
    )

    assert any(
        "Object name is missing or unknown" in error
        for error in errors
    )


def test_unsupported_operation():

    metadata = create_metadata(
        operation="TRUNCATE"
    )

    validator = MetadataValidator()

    errors = validator.validate(
        [metadata]
    )

    assert any(
        "Unsupported operation" in error
        for error in errors
    )


def test_duplicate_sequence_within_group():

    first = create_metadata(
        file_name="customer_hub.sql",
        sequence=10
    )

    second = create_metadata(
        file_name="customer_load.sql",
        sequence=10
    )

    validator = MetadataValidator()

    errors = validator.validate(
        [first, second]
    )

    assert any(
        "duplicate sequence number: 10" in error
        for error in errors
    )


def test_same_sequence_in_different_groups_is_valid():

    first = create_metadata(
        file_name="customer.sql",
        deployment_group="CUSTOMER_DATA",
        sequence=10
    )

    second = create_metadata(
        file_name="policy.sql",
        deployment_group="POLICY_DATA",
        sequence=10
    )

    validator = MetadataValidator()

    errors = validator.validate(
        [first, second]
    )

    assert errors == []