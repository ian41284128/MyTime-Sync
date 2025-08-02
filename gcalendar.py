import datetime
import os.path
from shift import Shift

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GCalendar:
    def __init__(self, calendar_name):
        print("Initializing Google Calendar API...")
        # If modifying these scopes, delete the file token.json.
        SCOPES = ["https://www.googleapis.com/auth/calendar"]

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.service = build("calendar", "v3", credentials=creds)
            self.calendar_id = self._get_work_calendar(calendar_name)
        except HttpError as error:
            print(error)
            exit(1)

    def _get_work_calendar(self, name):
        print("Finding work calendar '" + name + "'...")
        for calendar in self.service.calendarList().list().execute().get('items'):
            if calendar.get('summary') == name:
                return calendar.get('id')
        raise ValueError("Could not find a calendar named " + name)

    def get_events(self, after):
        events = (self.service.events()
                  .list(
                        calendarId=self.calendar_id,
                        timeMin=after.isoformat(),
                        singleEvents=True,
                        orderBy="startTime",
                  ).execute()
        ).get("items", [])
        if not events:
            print("No upcoming events found")
            return []
        result = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            tz = event['start'].get('timeZone')
            name = event['summary']
            result.append(Shift.create_from_gcalendar(name, start, end, tz))
        return result

    def insert_shift(self, shift):
        event = self.service.events().insert(calendarId=self.calendar_id, body=shift.to_gcalendar_event()).execute()
        print('Event created: ' + (event.get('htmlLink')))
