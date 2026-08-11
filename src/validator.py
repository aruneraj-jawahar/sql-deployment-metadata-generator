from collections import Counter

from src.metadata import SQLMetadata


class MetadataValidator:

    def validate(
        self,
        metadata_records: list[SQLMetadata]
    ) -> list[str]:

        errors = []

        for metadata in metadata_records:
            errors.extend(
                self._validate_record(metadata)
            )

        errors.extend(
            self._validate_duplicate_sequences(
                metadata_records
            )
        )

        return errors

    @staticmethod
    def _validate_record(
        metadata: SQLMetadata
    ) -> list[str]:

        errors = []

        if not metadata.file_name.strip():
            errors.append(
                "File name is missing."
            )

        if not metadata.deployment_group.strip():
            errors.append(
                f"{metadata.file_name}: "
                "Deployment group is missing."
            )

        if metadata.sequence <= 0:
            errors.append(
                f"{metadata.file_name}: "
                "Sequence must be greater than zero."
            )

        if metadata.operation not in {
            "CREATE",
            "INSERT",
            "UPDATE",
            "DELETE",
            "ALTER",
            "DROP",
        }:
            errors.append(
                f"{metadata.file_name}: "
                f"Unsupported operation "
                f"'{metadata.operation}'."
            )

        if (
            not metadata.object_name.strip()
            or metadata.object_name == "UNKNOWN"
        ):
            errors.append(
                f"{metadata.file_name}: "
                "Object name is missing or unknown."
            )

        return errors

    @staticmethod
    def _validate_duplicate_sequences(
        metadata_records: list[SQLMetadata]
    ) -> list[str]:

        errors = []

        grouped_sequences = {}

        for metadata in metadata_records:

            group = metadata.deployment_group

            grouped_sequences.setdefault(
                group,
                []
            ).append(metadata.sequence)

        for group, sequences in grouped_sequences.items():

            counts = Counter(sequences)

            duplicates = [
                sequence
                for sequence, count in counts.items()
                if count > 1
            ]

            for sequence in duplicates:
                errors.append(
                    f"Deployment group '{group}' "
                    f"contains duplicate sequence "
                    f"number: {sequence}."
                )

        return errors