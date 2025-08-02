import mytime
from gcalendar import GCalendar
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    gcalendar = GCalendar(os.getenv("GCALENDAR_NAME"))
    mytime_shifts = mytime.scrape(os.getenv("MYTIME_URL"),
                                  os.getenv("MYTIME_USERNAME"),
                                  os.getenv("MYTIME_PASSWORD"),
                                  20)
    gcalendar_shifts = gcalendar.get_events(mytime_shifts[0].start)
    for mt in range(len(mytime_shifts)):
        mt_shift = mytime_shifts[mt]
        in_gcalendar = False
        for gc_shift in gcalendar_shifts:
            if mt_shift == gc_shift:
                in_gcalendar = True
                break
        if not in_gcalendar:
            gcalendar.insert_shift(mt_shift)
