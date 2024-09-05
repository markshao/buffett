from datetime import datetime, date


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def str_2_date(date_str: str) -> date:
    exec = []
    for pattern in ["%Y-%m-%d", "%Y%m%d"]:
        try:
            trade_datetime = datetime.strptime(date_str, pattern)
            return trade_datetime
        except Exception as e:
            exec.append(e)
    raise exec[0]


def date_2_str(date_obj: date) -> str:
    return date_obj.strftime("%Y-%m-%d")
