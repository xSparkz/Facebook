from datetime import datetime
import time
import sys # Used to supply argv to application
import gui # All of the GUI code independent from functional code
from PyQt4 import QtGui, QtCore # Library for working with GUI
from common import  *
from facebook import *
import webbrowser

class GuiCore(QtGui.QMainWindow, gui.Ui_MainWindow):

    def __init__(self, parent=None):

        super(GuiCore, self).__init__(parent)
        self.setupUi(self)

class Gui():

    def __init__(self):

        # Objects
        self.MainApp = QtGui.QApplication(sys.argv)  # Setup main application
        self.MainWindow = GuiCore()  # Setup main window
        self.Facebook = WWWConnection() # Setup the Facebook browser

        # Variables
        self.__StartDateTime = None # Hold the value of our date & time
        self.__EndDateTime = None # Hold the value of our date & time

        # Signals
        self.MainWindow.btnGetLocations.mouseReleaseEvent = self.btnGetLocations_Click
        self.MainWindow.btnLogin.mouseReleaseEvent = self.btnLogin_Click
        self.MainWindow.btnClear.mouseReleaseEvent = self.btnClear_Click
        self.MainWindow.listLocations.itemDoubleClicked.connect(self.listLocations_Item_DoubleClicked)

        # Connections
        self.Facebook.ConnectGUI(self.MainWindow.listStatus)

        # Default States
        self.MainWindow.btnGetLocations.setDisabled(True)
        self.MainWindow.btnSaveToFile.setDisabled(True)

    def Show(self):

        self.MainWindow.show()  # Show the Main Window
        self.MainApp.exec_()  # Run the GUI Framework

    def listLocations_Item_DoubleClicked(self, Item):

        GPSPoints = str(Item.text()).split(', ')

        # Craft URL
        url = str(URL_MAP).replace('<lat>', GPSPoints[0]).replace('<lon>', GPSPoints[1])

        webbrowser.open(url)

    def btnClear_Click(self, MouseEvent):

        self.MainWindow.btnClear.animateClick() # Fix the button from sticking after it's clicked
        self.MainWindow.listLocations.clear() # Clear list

    def btnGetLocations_Click(self, MouseEvent):

        self.MainWindow.btnGetLocations.animateClick() # Fix the button from sticking after it's clicked

        # Convert the Date & Time from the GUI into a Python usable format
        self.__StartDateTime = self.MainWindow.dateFrom.dateTime().toPyDateTime() # Store start date/time
        self.__EndDateTime = self.MainWindow.dateTo.dateTime().toPyDateTime() # Store end date/time

        GPSPoints = self.Facebook.GetSavedGPSPoints(self.__StartDateTime, self.__EndDateTime)

        self.MainWindow.listLocations.clear()

        for GPSPoint in GPSPoints:

            self.MainWindow.listLocations.addItem(GPSPoint)

        self.MainWindow.listLocations.scrollToBottom()

    def btnLogin_Click(self, MouseEvent):

        self.MainWindow.btnLogin.animateClick() # Fix the button from sticking after it's clicked

        self.MainWindow.btnGetLocations.setDisabled(True)
        self.MainWindow.btnSaveToFile.setDisabled(True)

        if self.Facebook.Login(self.MainWindow.txtUsername.text(), self.MainWindow.txtPassword.text()):

            # GOOD! We've connected to Facebook, We've logged in, and we now have the User ID
            # We can now enable the buttons that allow us to retrieve the locations under this account since we now
            # have enough information.

            self.MainWindow.btnGetLocations.setDisabled(False)
            self.MainWindow.btnSaveToFile.setDisabled(False)




class MainApp():

    def __init__(self):

        # Initiate our User Interface
        self.Gui = Gui() # Setup the GUI
        self.Gui.Show() # Show the GUI

if __name__ == '__main__':

    FaceBookExtractor = MainApp() # Main application