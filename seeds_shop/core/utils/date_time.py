from datetime import datetime

from pytz import timezone


def get_date_time(
    tz: str | None = None,
    time_format: str = "%Y-%m-%d %H:%M:%S",
    as_string: bool = False,
) -> str | datetime:
    """Получаем текущую дату и время"""

    date_and_time = datetime.now(timezone(tz) if tz else None).replace(tzinfo=None).replace(microsecond=0)

    if as_string:
        date_and_time = date_and_time.strftime(time_format)

    return date_and_time


def get_current_timestamp() -> int:
    """Возвращаем текущий timestamp"""

    cur_date = get_date_time()
    return int(cur_date.timestamp())
