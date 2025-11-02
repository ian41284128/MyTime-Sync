# Setup
* [Google API Access](#google-api-access)
* [Python Virtual Environment and Packages](#python-virtual-environment-and-packages)
* [Run `main.py`](#run-main)
## Google API Access
For more detailed instructions please refer to the [Google Calendar API Python Quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python)
### 1. Enable Google Calendar API access [here](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com).
### 2. Configure the Google OAuth consent screen
- Go to [Google Branding](https://console.cloud.google.com/auth/branding)
- Under **App Information**, in **App name**, enter `MyTime Sync` or any name of your choosing.
- In **User support email**, enter your email.
- Click **Next**.
- Under **Audience**, select **Internal** (or external if internal doesn't work).
- Click **Next**.
- Under **Contact Information**, enter an **Email address** where you can be notified about any changes to your project.
- Click **Next**.
- Under **Finish**, review the Google API Services User Data Policy and if you agree, select **I agree to the Google API Services: User Data Policy**.
- Click **Continue**.
- Click **Create**.
### 3. Authorize credentials for a desktop application
- In the Google Cloud console, go to [Clients](https://console.cloud.google.com/auth/clients)
- Click **Create Client.**
- Click **Application type > Desktop app.**
- In the **Name** field, type a name for the credential. This name is only shown in the Google Cloud console.
- Click **Create.**
- Save the downloaded JSON file as `credentials.json`, and move the file next to `main.py`.

## Python Virtual Environment and Packages
1. Setup venv
```
python -m venv .venv
source .venv/bin/activate
```
2. Download dependencies
```
pip install -r requirements.txt
```
3. Configure environment variables
- Open .env
- Fill in the username and password you use to login to MyTime
- Modify the `MYTIME_URL` to match your MyTime schedule url
- Change `GCALENDAR_NAME` to match your desired calendar, or put `primary` if you want to use your main google calendar

## Run Main
```
python main.py
```
This will attempt to authenticate with Google Calendar and compare the events in the calendar to your shifts in MyTime.
If any shifts in MyTime don't have events in your calendar, they will be created.
(Optional) Run this script on a set interval to automatically update your google calendar when your shifts change.
