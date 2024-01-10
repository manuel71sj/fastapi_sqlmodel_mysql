

from datetime import datetime

from core.conf import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE):
        # self.tz_info = zoneinfo.ZoneInfo(tz)
        pass

    def now(self) -> datetime:
        """
        표준 시간대 시간 가져오기

        :return:
        """
        # return datetime.now(self.tz_info)
        return datetime.now()

    def f_datetime(self, dt: datetime) -> datetime:
        """
        datetime 표준 시간대 시간

        :param dt:
        :return:
        """
        # return dt.astimezone(self.tz_info)
        return dt.astimezone()

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        시간 문자열을 표준 시간대 시간으로 변환

        :param date_str:
        :param format_str:
        :return:
        """
        # return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)
        return datetime.strptime(date_str, format_str)


timezone = TimeZone()
