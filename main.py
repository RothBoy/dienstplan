import tabula
import warnings
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

warnings.filterwarnings(action='ignore', category=FutureWarning)


def cal_init():
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print('An error occurred: %s' % error)


def cal_create_event(service, date_start, date_end, task,
                     calendar_id='ef578613e16942775fee16ca94d07cd000ffda40aa5101e7acd2f4875f57b485@group.calendar.google.com'):
    # tz = pytz.timezone('Europe/Berlin')
    event = {
        'summary': task,
        'start': {
            'dateTime': date_start.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/Berlin'
        },
        'end': {
            'dateTime': date_end.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/Berlin'
        },
    }
    try:
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)


def pdf_parse(filename="Dienstplanentwurf 2023-01-2023 Januar Stand 17.11.2022.pdf", employee="Mohr"):
    filename = "res/" + filename
    df = tabula.read_pdf(filename, pages="1", stream=True, guess=False, area=[50, 17.5, 470, 765],
                         columns=[98.5, 165.5, 229, 300.5, 362, 431, 499, 564, 641, 704])
    dates = []
    tasks = []
    for i in df[0][df[0].eq(employee).any(axis=1)].index:
        # print(str(df[0].iloc[i, 0] + ": " + df[0].columns[df[0].loc[i].eq(employee)]))
        [day_str, month_str, year_str] = df[0].iloc[i, 0][3:].split(".")
        date_start = datetime.datetime(int(year_str), int(month_str), int(day_str))
        dates.append(date_start)
        tasks.append(df[0].columns[df[0].loc[i].eq(employee)][0])
    return dates, tasks


[date_start_list, task_list] = pdf_parse()
cal_service = cal_init()
for date_start, task in zip(date_start_list, task_list):
    match task:
        case "I. Dienst" | "II. Dienst" | "III. Dienst":
            date_end = date_start + datetime.timedelta(days=1)
        case "Spätd.Stein":
            date_start += datetime.timedelta(hours=9,minutes=15)
            date_end = date_start + datetime.timedelta(hours=9,minutes=15)
        case "Spätd. 2":
            task = 'Spätd.Südend'
            date_start += datetime.timedelta(hours=10, minutes=30)
            date_end = date_start + datetime.timedelta(hours=9,minutes=15)
        case 'AHT/PSZ 8577':
            task = 'PSZ'
            date_start += datetime.timedelta(hours=7, minutes=30)
            date_end = date_start + datetime.timedelta(hours=9,minutes=15)
        case 'NEF Vinc.' | 'NEF Durlach':
            date_end = date_start + datetime.timedelta(days=1)
        case _:
            exit(1)

    # print(task + '  ' + date_start.strftime("%Y-%m-%dT%H:%M:%S") + ' - ' + date_end.strftime("%Y-%m-%dT%H:%M:%S"))
    cal_create_event(cal_service, date_start, date_end, task)

