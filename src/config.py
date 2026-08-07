from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class AppConfig:
    name: str
    version: str


@dataclass
class InputConfig:
    sql_directory: str


@dataclass
class OutputConfig:
    output_directory: str
    excel_file: str


@dataclass
class EnvironmentConfig:
    environments: dict


@dataclass
class LoggingConfig:
    level: str
    file: str


class ConfigLoader:

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)

    def load(self):

        with open(self.config_path, "r") as file:
            config = yaml.safe_load(file)

        return {
            "application": AppConfig(**config["application"]),
            "input": InputConfig(**config["input"]),
            "output": OutputConfig(**config["output"]),
            "environment": EnvironmentConfig(
                environments=config["environments"]
            ),
            "logging": LoggingConfig(**config["logging"]),
            "metadata": config["metadata"],
        }
