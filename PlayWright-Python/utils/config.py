from pathlib import Path

import yaml


class Config:

    def __init__(self, environment: str):
        self.environment = environment

        config_file = (
            Path(__file__).parent.parent
            / "config"
            / f"{environment}.yaml"
        )

        if not config_file.exists():
            raise FileNotFoundError(
                f"Config tidak ditemukan: {config_file}"
            )

        with open(config_file, "r", encoding="utf-8") as file:
            self.data = yaml.safe_load(file)

    @property
    def base_url(self):
        return self.data["base_url"]