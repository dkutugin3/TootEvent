import datetime as dt


class DateManager:
    format = "%d.%m.%Y %H:%M %Z %z"  # DD.MM.YYYY HH:MM UTC +HHMM

    @classmethod
    def date_to_string(cls, date: dt.datetime):
        return dt.datetime.strftime(date, cls.format)

    @classmethod
    def string_to_date(cls, string: str):
        return dt.datetime.strptime(string, cls.format)
