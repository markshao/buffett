from abc import ABC
from pathlib import Path
import yaml

ROOT_DIR = Path(__file__).parent


class AbstractConfig(ABC):
    CONF_DIR = ROOT_DIR / "conf"
    CONF_FILE_NAME = ""

    # subclass impelement
    CONF_KEYS = ()  # lower case

    def __init__(self):
        conf_file_path = self.CONF_DIR / self.CONF_FILE_NAME
        if not conf_file_path.exists():
            raise FileNotFoundError(f"The file {conf_file_path} does not exist.")

        with conf_file_path.open("r") as f:
            self._config = yaml.safe_load(f)

    def __getattr__(self, name: str):
        if not name in self.CONF_KEYS:
            raise AttributeError(f"conf key = {name} not support")

        return self._config[name]


class LlmConfig(AbstractConfig):
    CONF_FILE_NAME = "llm.yaml"
    CONF_KEYS = ("base_url", "api_key", "model")
