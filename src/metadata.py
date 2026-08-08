from dataclasses import dataclass


@dataclass
class SQLMetadata:
    file_name: str
    deployment_group: str
    sequence: int
    operation: str
    object_type: str
    object_name: str
    sql_statement: str
