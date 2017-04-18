import mechanize, cookielib, re
from bs4 import BeautifulSoup
from common import *
import re # Regex functions (Pattern Matching)
import time
import datetime



class WWWConnection():

    def __init__(self):

        # Browser
        self.__Browser = mechanize.Browser()

        # Cookie Jar
        # Needed to handle sessions
        self.__CookieJar = cookielib.LWPCookieJar()
        self.__Browser.set_cookiejar(self.__CookieJar)

        # Browser Options
        self.__Browser.set_handle_equiv(True)
        self.__Browser.set_handle_redirect(True)
        self.__Browser.set_handle_referer(True)
        self.__Browser.set_handle_robots(False)
        self.__Browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1) # For redirects

        # Setup Headers to appear like a regular browser. Without this step the browser may be confused as a BOT and denied service from a website
        self.__Browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        # Gui Connections
        self.__GuiOutput = None # Holds the pointer to a Textbox to output text to the gui when something happens

        # Facebook Credentials
        self.__Username = None # Holds the Username
        self.__Password = None # Holds the password
        self.__UserID = None # Facebook User ID

    def __GetPageSource(self, WebsiteURL):

        # Connect to website
        Echo('Connecting to ' + WebsiteURL, self.__GuiOutput)
        self.__Browser.open(WebsiteURL)

        # Check response
        Response = self.__Browser.response()
        ResponseCode = Response.code

        # Make sure response is good
        if not ResponseCode == 200:  # Look for an 'OK' code (200)

            Echo('Uh Oh! Not sure what happened.. Hmmm...', GuiOutput=self.__GuiOutput)
            Echo('\t- Received response: ' + ResponseCode + ' from server', GuiOutput=self.__GuiOutput)
            Echo('\t - ERROR!!', GuiOutput=self.__GuiOutput)

            raise Exception('Unable to connect to website. Unknown error. Maybe you did something wrong.')  # No point going any further

        # Store page source
        PageSource = Response.read()

        return PageSource

    def __SubmitForm(self):

        # Submit Form
        self.__Browser.submit()

        # Check response
        Response = self.__Browser.response()
        ResponseCode = Response.code

        # Make sure response is good
        if not ResponseCode == 200:  # Look for an 'OK' code (200)

            Echo('Uh Oh! Not sure what happened.. Hmmm...', GuiOutput=self.__GuiOutput)
            Echo('\t- Received response: ' + ResponseCode + ' from server', GuiOutput=self.__GuiOutput)
            Echo('\t - ERROR!!', GuiOutput=self.__GuiOutput)

            raise Exception(
                'Unable to connect to website. Unknown error. Maybe you did something wrong.')  # No point going any further

        # Store page source
        PageSource = Response.read()

        return PageSource

    def __GetUserID(self, PageSource):

        Echo('Obtaining User ID', self.__GuiOutput)

        Matches = re.findall(REGEX_USER_ID, PageSource) # Find the User ID

        if len(Matches) >= 1:

            self.__UserID = Matches[0] # First match (Should only be one)
            return  True

        return False # Something went wrong, we didn't get the User ID

    def ConnectGUI(self, GuiOutput):

        self.__GuiOutput = GuiOutput

    def Login(self, Username, Password):

        # Save Username & Password
        self.__Username = str(Username).strip() # Remove spaces
        self.__Password = str(Password).strip() # Remove spaces

        # Generate the URL
        WebsiteURL = URL_FACEBOOK

        # Get website
        self.__GetPageSource(WebsiteURL)

        # Login
        Echo('Logging in..', self.__GuiOutput)

        self.__Browser.select_form(nr=0) # Select the first <form> Login Form
        self.__Browser.form['email'] = self.__Username # Fill in the username/email
        self.__Browser.form['pass'] = self.__Password # Fill in the password

        PageSource = self.__SubmitForm() # Login and grab Page Source

        # Get the User ID
        if self.__GetUserID(PageSource):

            # GOOD! We've connected to Facebook, We've logged in, and we now have the User ID
            # We can now enable the buttons that allow us to retrieve the locations under this account since we now
            # have enough information.

            Echo('User ID Found: ' + self.__UserID, self.__GuiOutput)

            return True # Able to proceed

        else:

            return False # Something went wrong

    def GetSavedGPSPoints(self, From, To):

        From = str(time.mktime(From.timetuple()))
        To = str(time.mktime(To.timetuple()))

        # Craft the URL
        url = str(URL_GPS_POINTS).replace('<from>', From).replace('<to>', To).replace('<userid>', str(self.__UserID))

        PageSource = self.__GetPageSource(url)

        Matches = re.findall(REGEX_GPS, PageSource)

        GPSPoints = [] # Create a new list to store all of our GPS Points that we found

        for Match in Matches:

            String = '' # New empty string

            Items = str(Match).strip('(').strip(')').split(', ', 2)

            Lat = str(Items[0]).strip('\'').strip(',')
            Lon = str(Items[1]).strip('\'').strip(',')
            Text = str(Items[2]).strip('\'').strip(',')

            if not GPS_SHOW_TEXT:

                TextSplit = str(Text).split(' - ')
                Text = TextSplit[0]

            String = Lat + ', ' + Lon + ', ' + Text

            GPSPoints.append(String)


        return GPSPoints


