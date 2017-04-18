import datetime
import re

# Formats
FORMAT_TIME = '%I:%M (%S) %p' # ex: 12:34 (04) PM
FORMAT_DATE = '%d %b %Y - %A' # ex: 13 Nov 2014 - Monday

# RegEx Patterns
REGEX_USER_ID = re.compile('"USER_ID":"([\\s\\S]*?)",')
REGEX_GPS = re.compile('\\{"latitude":([\\s\\S]*?)"longitude":([\\s\\S]*?)\\},"([\\s\\S]*?)"')

# GPS Points
GPS_SHOW_TEXT = True

# Map Options
TYPE_NORMAL = 'm'
TYPE_SATELITE = 'k'
TYPE_HYBRID = 'h'
TYPE_TERRAIN = 'p'

MAP_ZOOM = '12'
MAP_TYPE = TYPE_SATELITE

# URL's
URL_FACEBOOK = 'https://www.facebook.com'
URL_GPS_POINTS = 'https://www.facebook.com/ajax/aura/travel_log_map.php?start_time=<from>&end_time=<to>&title=Today&dpr=1&__user=<userid>&__a=1&__af=iw&__req=l&__be=-1&__pc=EXP4:DEFAULT&__rev=2953805'
URL_MAP = 'http://maps.google.com/maps?z=' + MAP_ZOOM + '&t=' + MAP_TYPE + '&q=loc:<lat>+<lon>'

# Date / Time Functions
def TimeStamp(): return datetime.datetime.now().strftime(FORMAT_TIME)
def DateStamp(): return datetime.datetime.now().strftime(FORMAT_DATE)

# Echo function (Print msg to console with timestamp)
def Echo(LineToEcho, GuiOutput=None):

    Line = str(TimeStamp() + '- ' + LineToEcho) # Format the line with a timestamp
    print Line # Print the line to console

    if GuiOutput is not None:

        GuiOutput.addItem(Line) # Add the line to the GUI
        GuiOutput.scrollToBottom() # Scroll the list to the bottom
