from pathlib import Path

import pandas as pd

from src.metadata import SQLMetadata


class ExcelWriter:

    COLUMNS = [
        "File Name",
        "Deployment Group",
        "Sequence",
        "Operation",
        "Object Type",
        "Object Name",
        "SQL Statement",
    ]

    def write(
        self,
        metadata_records: list[SQLMetadata],
        output_file: str
    ) -> Path:

        if not metadata_records:
            raise ValueError(
                "No metadata records available for Excel generation."
            )

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        records = [
            {
                "File Name": metadata.file_name,
                "Deployment Group": metadata.deployment_group,
                "Sequence": metadata.sequence,
                "Operation": metadata.operation,
                "Object Type": metadata.object_type,
                "Object Name": metadata.object_name,
                "SQL Statement": metadata.sql_statement,
            }
            for metadata in metadata_records
        ]

        dataframe = pd.DataFrame(
            records,
            columns=self.COLUMNS
        )

        dataframe = dataframe.sort_values(
            by=[
                "Deployment Group",
                "Sequence",
            ]
        )

        dataframe.to_excel(
            output_path,
            index=False,
            engine="openpyxl"
        )

        return output_path