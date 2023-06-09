from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.image import AsyncImage
from kivymd.uix.card import MDCard
from kivymd.uix.slider import MDSlider
from BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from datetime import datetime, timedelta
from kivy.clock import Clock
import requests
import string
import coverpy
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Day(MDBoxLayout):

    def __init__(self, **kwargs):
        
        super(Day, self).__init__(**kwargs)
        self.name = "Day"
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.padding = '40dp'
        self.spacing = '50dp'
        self.Event1 = DayEvent()
        self.Event2 = DayEvent()
        self.Event3 = DayEvent()
        self.creds = None

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/home/buzzlaiclere/.credentials/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.TodaysNbEvents = 0
        self.NowNbEvents = 0

        Clock.schedule_interval(self.update_calendar, 60)
        self.update_calendar()

    def update_calendar(self, *args):
        # Called once a second using the kivy.clock module
        print("updating calendar\n")
        self.NowNbEvents = 0
        self.now = datetime.utcnow()
        self.end_of_day = datetime(self.now.year, self.now.month, self.now.day, 23, 59, 59)

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Call the Calendar API
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=3, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return
            start = None
            # Prints the start and name of the next 10 events
            for event in events:
                self.NowNbEvents += 1

            self.Event1.Layout.Desc.text = events[0]['summary']
            start = events[0]['start']['dateTime']
            if 'T' in start:
                start = start.split('T')[1]  # Extract the time portion
                start = start.split('-')[0]  # Extract the time portion
                start = start[:-3]
            else:
                start = ''  # All-day event, no specific start time
            self.Event1.Layout.Time.text = start

            self.Event2.Layout.Desc.text = events[1]['summary']
            start = events[1]['start']['dateTime']
            if 'T' in start:
                start = start.split('T')[1]  # Extract the time portion
                start = start.split('-')[0]  # Extract the time portion
                start = start[:-3]
            else:
                start = ''  # All-day event, no specific start time
            self.Event2.Layout.Time.text = start

            self.Event3.Layout.Desc.text = events[2]['summary']
            start = events[2]['start']['dateTime']
            if 'T' in start:
                start = start.split('T')[1]  # Extract the time portion
                start = start.split('-')[0]  # Extract the time portion
                start = start[:-3]
            else:
                start = ''  # All-day event, no specific start time
            self.Event3.Layout.Time.text = start

        except HttpError as error:
            print('An error occurred: %s' % error)

        print("got events\n")
        #print(self.todays_events)
        print("\n")
        

        #for event in self.todays_events:
            #print(event)
            #print("\n")
            #self.NowNbEvents += 1
        
        if self.NowNbEvents != self.TodaysNbEvents:

            self.TodaysNbEvents = self.NowNbEvents

            for childs in self.children:
                self.remove_widget(childs)

            if self.NowNbEvents == 1:
                self.add_widget(self.Event1)

            if self.NowNbEvents == 2:
                self.add_widget(self.Event1)
                self.add_widget(self.Event2)

            if self.NowNbEvents == 3:
                self.add_widget(self.Event1)
                self.add_widget(self.Event2)
                self.add_widget(self.Event3)
        

            

class DayEvent(MDCard):
     
     def __init__(self, **kwargs):
        
        super(DayEvent, self).__init__(**kwargs)
        self.name = "DayEvent"
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        #self.padding = '40dp'
        #self.spacing = '50dp'
        self.set_style('outlined')
        self.Layout = EventCardLayout()
        self.add_widget(self.Layout)

class EventCardLayout(MDBoxLayout):

    def __init__(self, **kwargs):
        
        super(EventCardLayout, self).__init__(**kwargs)
        self.name = "EventCardLayout"
        self.orientation = 'horizontal'
        self.padding = (0, "100dp")
        self.Time = EventTime()
        self.add_widget(self.Time)
        self.Desc = EventDesc()
        self.add_widget(self.Desc)

class EventDesc(MDLabel):

    def __init__(self, **kwargs):
        
        super(EventDesc, self).__init__(**kwargs)
        self.name = "EventDesc"
        self.font_style = 'H5'
        self.halign = 'center'
        self.size_hint_x = 0.7

class EventTime(MDLabel):

    def __init__(self, **kwargs):
        
        super(EventTime, self).__init__(**kwargs)
        self.name = "EventTime"
        self.font_style = 'H4'
        self.halign = 'center'
        self.size_hint_x = 0.3

class MusicMainLayout(MDBoxLayout):

    def __init__(self, **kwargs):
        
        super(MusicMainLayout, self).__init__(**kwargs)
        self.name = "MusicMainLayout"
        self.orientation = 'horizontal'
        self.padding = "20dp"
        self.Artwork = MusicArtwork()
        self.add_widget(self.Artwork)
        self.InfoLayout = MusicInfoLayout()
        self.add_widget(self.InfoLayout)
        
        #self.size_hint_y = 0.25
        Clock.schedule_interval(self.Artwork.newArtwork, 1)

class MusicArtwork(AsyncImage):

    def __init__(self, **kwargs):
        
        super(MusicArtwork, self).__init__(**kwargs)
        self.name = "MusicArtwork"
        #self.size_hint = (1, 1)
        self.fit_mode = "contain"
        self.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.coverpy = coverpy.CoverPy()
        self.showntitle = ""
        self.source = 'no-artwork.png'

    def newArtwork(self, dt):
        if self.showntitle != self.parent.InfoLayout.Title.Text.text :
            self.showntitle = self.parent.InfoLayout.Title.Text.text
            try:
                self.Temp = self.parent.InfoLayout.Album.Text.text + " " + self.parent.InfoLayout.Artist.Text.text
                print(self.Temp)
                self.result = self.coverpy.get_cover(self.Temp, 1)
                print(self.result.name)
                print(self.result.artwork(100))
                # Set a size for the artwork (first parameter) and get the result url.
                self.source = self.result.artwork()
            except requests.exceptions.HTTPError as f:
                print("Could not execute GET request")
                print(f)
            except Exception as e:
            	print("Nothing found.")
            
class MusicInfoLayout(MDBoxLayout):

    def __init__(self, **kwargs):
        
        super(MusicInfoLayout, self).__init__(**kwargs)
        self.name = "MusicInfoLayout"
        self.orientation = 'vertical'
        self.padding = (0, "100dp")
        self.Title = MusicTitle()
        self.add_widget(self.Title)
        self.Album = MusicAlbum()
        self.add_widget(self.Album)
        self.Artist = MusicArtist()
        self.add_widget(self.Artist)

class MusicTitle(MDBoxLayout):

    def __init__(self, **kwargs):
        
        super(MusicTitle, self).__init__(**kwargs)
        self.name = "MusicTitle"
        self.orientation = 'horizontal'
        self.Text = DescText()
        self.add_widget(self.Text)

class DescText(MDLabel):

    def __init__(self, **kwargs):
        
        super(DescText, self).__init__(**kwargs)
        self.name = "DescText"
        self.font_style = 'H4'
        self.halign = 'center'
        self.size_hint_x = 0.7

class MusicAlbum(MDBoxLayout):

    def __init__(self, **kwargs):
        
        super(MusicAlbum, self).__init__(**kwargs)
        self.name = "MusicAlbum"
        self.orientation = 'horizontal'
        self.Text = DescText()
        self.add_widget(self.Text)

class DescText(MDLabel):

    def __init__(self, **kwargs):
        
        super(DescText, self).__init__(**kwargs)
        self.name = "DescText"
        self.font_style = 'H4'
        self.halign = 'center'
        self.size_hint_x = 0.7

class MusicArtist(MDBoxLayout):

    def __init__(self, **kwargs):
        
        super(MusicArtist, self).__init__(**kwargs)
        self.name = "MusicArtist"
        self.orientation = 'horizontal'
        self.Text = DescText()
        self.add_widget(self.Text)

class DescText(MDLabel):

    def __init__(self, **kwargs):
        
        super(DescText, self).__init__(**kwargs)
        self.name = "DescText"
        self.font_style = 'H4'
        self.halign = 'center'
        self.size_hint_x = 0.7