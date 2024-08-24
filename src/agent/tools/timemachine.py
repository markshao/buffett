from datetime import datetime, timedelta
from ..utils import Singleton
from ..config import AbstractConfig


class TimeMachineConfig(AbstractConfig):
    CONF_FILE_NAME = "timemachine.yaml"
    CONF_KEYS = ("fallback_days",)


class TimeMachine(metaclass=Singleton):
    def __init__(self) -> None:
        self._config = TimeMachineConfig()

    def __set_start_date(self):
        now_date = datetime.now().date()
        self._start_date = now_date - timedelta(days=int(self._config.fallback_days))
