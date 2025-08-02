from datetime import datetime, timedelta
from pytz import timezone


class Shift:
    default_timezone = timezone('US/Pacific')

    def __init__(self, name, dt_start, dt_end):
        self.name = name
        self.start = dt_start
        self.end = dt_end

    @staticmethod
    def create_from_mytime(date, start, end, name):
        date = datetime.strptime(date, "%A %B %d").replace(year=datetime.now(Shift.default_timezone).year)
        if date.month == 1 and datetime.now(Shift.default_timezone).month > 1:
            date.replace(year=date.year + 1)
        start = datetime.strptime(start, "%I:%M %p")
        end = datetime.strptime(end, "%I:%M %p")
        start = date + timedelta(hours=start.hour, minutes=start.minute)
        end = date + timedelta(hours=end.hour, minutes=end.minute)
        if end < start:
            end += timedelta(days=1)
        return Shift(name, Shift.default_timezone.localize(start), Shift.default_timezone.localize(end))

    @staticmethod
    def create_from_gcalendar(name, start, end, tz):
        tz = timezone(tz)
        start = datetime.fromisoformat(start)
        end = datetime.fromisoformat(end)
        return Shift(name, start, end)

    def to_gcalendar_event(self):
        return {
            'summary': self.name,
            'start': {
                'dateTime': self.start.isoformat(),
                'timeZone': Shift.default_timezone.zone
            },
            'end': {
                'dateTime': self.end.isoformat(),
                'timeZone': Shift.default_timezone.zone
            },
        }

    def __str__(self):
        val = 'from ' + self.start.isoformat() + ' to ' + self.end.isoformat()
        if self.name is not None:
            return self.name + ' ' + val
        return val

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
