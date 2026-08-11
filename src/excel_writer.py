from pathlib import Path

import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

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

        self._format_workbook(output_path)

        return output_path

    @staticmethod
    def _format_workbook(output_path: Path) -> None:

        from openpyxl import load_workbook

        workbook = load_workbook(output_path)
        worksheet = workbook.active

        # Freeze the header row
        worksheet.freeze_panes = "A2"

        # Enable filtering through an Excel table
        table_reference = (
            f"A1:{get_column_letter(worksheet.max_column)}"
            f"{worksheet.max_row}"
        )

        table = Table(
            displayName="DeploymentMetadata",
            ref=table_reference
        )

        table_style = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )

        table.tableStyleInfo = table_style
        worksheet.add_table(table)

        # Format header
        for cell in worksheet[1]:
            cell.font = Font(
                bold=True
            )
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

        # Format data cells
        for row in worksheet.iter_rows(
            min_row=2
        ):
            for cell in row:
                cell.alignment = Alignment(
                    vertical="top",
                    wrap_text=True
                )

        # Set useful column widths
        column_widths = {
            "A": 28,
            "B": 24,
            "C": 12,
            "D": 14,
            "E": 22,
            "F": 30,
            "G": 70,
        }

        for column, width in column_widths.items():
            worksheet.column_dimensions[column].width = width

        # Make the SQL statement column easier to read
        for cell in worksheet["G"][1:]:
            cell.alignment = Alignment(
                vertical="top",
                wrap_text=True
            )

        workbook.save(output_path)