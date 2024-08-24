from pathlib import Path
import yaml
import os

from .utils import Singleton

ROOT_DIR = Path(__file__).parent


class AbstractConfig(metaclass=Singleton):
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

        value = self._config.get(name, None)
        if not value:
            env_name = "%s.%s" % (self.CONF_FILE_NAME, name)
            value = os.environ.get(env_name, None)

        if value:
            return value
        else:
            raise AttributeError(f"conf key = {name} not found")


class LlmConfig(AbstractConfig):
    CONF_FILE_NAME = "llm.yaml"
    CONF_KEYS = ("base_url", "api_key", "model")
