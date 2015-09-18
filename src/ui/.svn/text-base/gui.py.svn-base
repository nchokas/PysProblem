#Py's Problem GUI
#Zach Olbrys
#5/2/09

#Import statements
import time
import pygame
import sys  
import socket
import os
import random

sys.path.append('..\\eng')
sys.path.append('..\\net')

from game import Game
from player import Player
from pgu import gui
from pgu import high
from pygame.locals import *
from socket_struct import *
from socket import *


#Sets up the screen and window title
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((700,720),HWSURFACE)
pygame.display.set_caption("Py's Problem")

#Font stuff
china_font = pygame.font.SysFont("CHINESETAKEAWAY", 15)
china_font_small = pygame.font.SysFont("CHINESETAKEAWAY", 12)
china_font_bold = pygame.font.SysFont("CHINESETAKEAWAY", 15)
china_font_bold.set_bold(True)
china_font_big = pygame.font.SysFont("CHINESETAKEAWAY", 18)

##### GLOBALS
#Used for profile name display/updating, size required because the label cannot be resized when it's value is reassigned.
nameLabel = gui.Label("                                 ",font=china_font)

#Main menu container, made global so the profile menu can have access to it
cx = gui.Container()

#Button height for the various buttons used, so the font is displayed correctly
buttonHeight = 21

#Data files
profilesFileName = "profiles.txt"
historyFileName = "history.txt"

#High Score Lists
pointsList = high.High('points.txt',limit=10)
timeList = high.High('time.txt',limit=10)

#Music/Image Stuff
imageDir = "../res/graphics/"
musicDir = "../res/sound/"
levelMusic = ["Retrospect","Harvest Tunes","Fuer Py","8 Bit Anthem","Chip Tune","Bolo the Brute"]
numSongs = len(levelMusic)
backgroundMusic = "8 Bit Anthem.ogg"

#Option variables
value = [0,0]
selectedValue = [0]
switchValue = [False,False]
userOptions = [[""],value,selectedValue,switchValue]

defaultValue = [25,25]
defaultSelectedValue = [0]
defaultSwitchValue = [False,False]
defaultOptions = [["Default"],defaultValue,defaultSelectedValue,defaultSwitchValue]

#Statistics variables 
#* means derived stats, not variables
#1   0 Total Games Played
#2   1 Multiplayer Wins
#3   2 Multiplayer Losses (As single player games count towards total games played, cannot just do a Total-Win calcualtion here)
#4   3 Total Points
#5       * Average Points Per game (Total Points/Total Games Played)
#6   4 Total time played
#7        * Average Time per game (Total Time/Total Games Played)
#8   5 Number of Items Bought
#9   6 Highest points scored
#10  7 Longest time survived
stats = [0,0,0,0,0,0,0,0]
defaultStats = [0,0,0,0,0,0,0,0]
multiStats = [0,0,0,0,0,0,0,0]

#Menu for displaying to the user that there is no controller installed
#Opens when options are loaded and the user has the controller enabled but is not installed
#or when the user sets the option in the options menu and the controller is not installed
def noControllerMenu():
    c = gui.Container(width=100,height=60)
    menu = gui.Dialog(gui.Label("Error",font=china_font),c)
    errorLabel = gui.Label("No Controller Found, Using Default Buttons",font=china_font)
    okayButton = gui.Button("Continue",font=china_font,height=buttonHeight)
    okayButton.connect(gui.CLICK,menu.close,None)
    c.add(errorLabel,0,0)
    c.add(okayButton,135,30)
    menu.open()
    
def setStats(gameType,gameStats):
    if(not gameStats==None):
        try:
            player1Name = gameStats[0]['player'].name
            player2Name = gameStats[1]['player'].name
        except:
            player2Name = ""
        
        if(gameType=="single"):
            stats[0] = str(int(stats[0]) + 1)
            #Single player game so do not update wins
            stats[3] = str(int(stats[3]) + int(float(gameStats[0]['points'])))
            stats[4] = str(int(stats[4]) + int(float(gameStats[0]['time_elapsed'])))
            stats[5] = str(int(stats[5]) + int(float(gameStats[0]['purchases_made'])))
            
            if(int(float(gameStats[0]['points'])) > int(stats[6])):
                stats[6] = str(int(float(gameStats[0]['points'])))
            pointsList.submit(int(float(gameStats[0]['points'])),player1Name)
                
            if(int(float(gameStats[0]['time_elapsed'])) > int(stats[7])):
                stats[7] = str(int(float(gameStats[0]['time_elapsed'])))
            timeList.submit(int(float(gameStats[0]['time_elapsed'])),player1Name)
            
        elif(gameType=="multinetwork"):
            stats[0] = str(int(stats[0]) + 1)
            
            if(gameStats[0]['won_game']):
                stats[1] = str(int(stats[1]) + 1)
            else:
                stats[2] = str(int(stats[2]) +1)
            
            stats[3] = str(int(stats[3]) + int(float(gameStats[0]['points'])))
            stats[4] = str(int(stats[4]) + int(float(gameStats[0]['time_elapsed'])))
            stats[5] = str(int(stats[5]) + int(float(gameStats[0]['purchases_made'])))
            
            if(int(float(gameStats[0]['points'])) > int(stats[6])):
                stats[6] = str(int(float(gameStats[0]['points'])))
            pointsList.submit(int(float(gameStats[0]['points'])),player1Name)
                
            if(int(float(gameStats[0]['time_elapsed'])) > int(stats[7])):
                stats[7] = str(int(float(gameStats[0]['time_elapsed'])))
            timeList.submit(int(float(gameStats[0]['time_elapsed'])),player1Name)
            
        elif(gameType=="multilocal"):
            stats[0] = str(int(stats[0]) + 1)
            multiStats[0] = str(int(multiStats[0]) + 1)
            
            if(gameStats[0]['won_game']):
                stats[1] = str(int(stats[1]) + 1)
                multiStats[2] = str(int(multiStats[2]) + 1)
            else:
                stats[2] = str(int(stats[2]) +1)
                multiStats[1] = str(int(multiStats[1]) + 1)
    
            stats[3] = str(int(stats[3]) + int(float(gameStats[0]['points'])))
            multiStats[3] = str(int(multiStats[3]) + int(float(gameStats[1]['points'])))
            
            stats[4] = str(int(stats[4]) + int(float(gameStats[0]['time_elapsed'])))
            multiStats[4] = str(int(multiStats[4]) + int(float(gameStats[1]['time_elapsed'])))
            
            stats[5] = str(int(stats[5]) + int(float(gameStats[0]['purchases_made'])))
            multiStats[5] = str(int(multiStats[5]) + int(float(gameStats[1]['purchases_made'])))
            
            if(int(float(gameStats[0]['points'])) > int(stats[6])):
                stats[6] = str(int(float(gameStats[0]['points'])))
            pointsList.submit(int(float(gameStats[0]['points'])),player1Name)
           
            if(int(float(gameStats[1]['points'])) > int(multiStats[6])):
                multiStats[6] = str(int(float(gameStats[1]['points'])))
            pointsList.submit(int(float(gameStats[1]['points'])),player2Name)
                
            if(int(float(gameStats[0]['time_elapsed'])) > int(stats[7])):
                stats[7] = str(int(float(gameStats[0]['time_elapsed'])))
            timeList.submit(int(float(gameStats[0]['time_elapsed'])),player1Name)
            
            if(int(float(gameStats[1]['time_elapsed'])) > int(multiStats[7])):
                multiStats[7] = str(int(float(gameStats[1]['time_elapsed'])))
            timeList.submit(int(float(gameStats[1]['time_elapsed'])),player2Name)
            
        pointsList.save()
        timeList.save()
            
        buffer = []
        
        profilesFile = open(profilesFileName,"r")
        numUsers = int(profilesFile.readline())
        for x in range(numUsers):
            userConfig = profilesFile.readline()
            userConfigSplit = userConfig.split('|')
            #Once you find the target profile, rewrite it with default values
            if(userConfigSplit[0]==player1Name):
                userConfigSplit[6] = stats[0]
                userConfigSplit[7] = stats[1]
                userConfigSplit[8] = stats[2]
                userConfigSplit[9] = stats[3]
                userConfigSplit[10] = stats[4]
                userConfigSplit[11] = stats[5]
                userConfigSplit[12] = stats[6]
                #Of course, the last line will need a newline character 
                userConfigSplit[13] = str(stats[7]) + "\n"
            if(userConfigSplit[0]==player2Name):
                userConfigSplit[6] = multiStats[0]
                userConfigSplit[7] = multiStats[1]
                userConfigSplit[8] = multiStats[2]
                userConfigSplit[9] = multiStats[3]
                userConfigSplit[10] = multiStats[4]
                userConfigSplit[11] = multiStats[5]
                userConfigSplit[12] = multiStats[6]
                #Of course, the last line will need a newline character 
                userConfigSplit[13] = str(multiStats[7]) + "\n"

            buffer.append(userConfigSplit)
    
        profilesFile.close()
    
        #Now write everything back to the file
        profilesFile2 = open(profilesFileName,"w")
        profilesFile2.write(str(numUsers)+"\n")
        for field in buffer:
            for element in field:
                if (str(element).find("\n") == -1):
                    profilesFile2.write(str(element))
                    profilesFile2.write("|")
                else:
                    profilesFile2.write(str(element))
        profilesFile2.close()

#Profile selection menu (initial window when game starts)
#Custom dialog.py file needed to make sure the dialog windows are not closeable
class ProfileMenu(gui.Dialog):
    
    #Global profile variables - not all are used through multiple methods,
    #But are necessary to be global so they can be persistent.
    profileNum = -1
    newProfileNum = -1
    profileList = gui.Select(font=china_font)
    profileNames = []
    profileNames2 = []
    userNum = 0
    delete = False
    c = gui.Container(width=420,height=185)
    inputError = False

    def __init__(self,mainMenu,**params):
        
        self.mainMenu = mainMenu
        
        #Obtains the last user who played
        historyFile = open(historyFileName,"r")
        lastUser = historyFile.readline().rpartition("\n")[0]
        historyFile.close()
        
        #Ensures that the last user is a valid selection choice, if not, sets last user to the default profile
        profileFile = open(profilesFileName,"r")
        numUsers = int(profileFile.readline())
        profileFile.close()
        
        if int(lastUser) > numUsers:
            lastUser = "0"
        
        #Menu widgets
        profileLabel = gui.Label("Select or create your profile",font=china_font)        
        selectProfileButton = gui.Button("Select Profile",font=china_font, height=buttonHeight)
        selectProfileButton.connect(gui.CLICK,self.closeMenu)        
        makeProfileButton = gui.Button("Create a New Profile",font=china_font, height=buttonHeight)
        makeProfileButton.connect(gui.CLICK,self.createMenu)  
        deleteProfileButton = gui.Button("Delete Profile",font=china_font, height=buttonHeight)
        deleteProfileButton.connect(gui.CLICK,self.deleteProfile)
        editProfileButton = gui.Button("Edit Profile Name",font=china_font, height=buttonHeight)
        editProfileButton.connect(gui.CLICK,self.editProfileMenu)
        self.profileList = gui.Select(value=lastUser,font=china_font)
    
        #Add widgets to container
        self.c.add(profileLabel,85,10)
        self.c.add(selectProfileButton,80,50)
        self.c.add(deleteProfileButton,80,80)
        self.c.add(makeProfileButton,80,110)
        self.c.add(editProfileButton,80,140)
        self.c.add(self.profileList,250,50)
        
        #Load the default profile names when originally creating the menu
        self.loadProfileNames()
        
        #Initializes the dialog window menu
        title = gui.Label("Welcome to Py's Problem",font=china_font) 

        gui.Dialog.__init__(self,title,self.c)
    
    #Loads the appropriate menu options configuration
    def loadOptions(self,profileNumber):
        profileNum = int(profileNumber)
        profilesFile = open(profilesFileName,"r")
        numUsers = int(profilesFile.readline())
        for x in range(numUsers):
            userConfig = profilesFile.readline()
            userConfigSplit = userConfig.split('|')
            if (profileNum == x):
                #load options, checks for errors in options and fixes them
                #If there are indexErrors, then that field does not exist, so fix the profile (i.e. if options are not present for a given line)
                try:
                    userOptions[0][0] = userConfigSplit[0]
                except:
                    userOptions[0][0] = "Default"
                    
                try:
                    userConfigSplit[1] = int(userConfigSplit[1])
                    if(userConfigSplit[1] >= 0 and userConfigSplit[1] <= 100):
                        value[0] = userConfigSplit[1]
                    else:
                        value[0] = defaultValue[0]
    
                    userConfigSplit[2] = int(userConfigSplit[2])
                    if(userConfigSplit[2] >= 0 and userConfigSplit[2] <= 100):
                        value[1] = userConfigSplit[2]
                    else:
                        value[1] = defaultValue[1]
    
                    userConfigSplit[3] = int(userConfigSplit[3])
                    if(userConfigSplit[3] >= 0 and userConfigSplit[3] <= numSongs):
                        selectedValue[0] = userConfigSplit[3]
                    else:
                        selectedValue[0] = defaultSelectedValue[0]
                
                    if(userConfigSplit[4]=="False"):
                        switchValue[0] = False
                    elif(userConfigSplit[4]=="True"):
                        switchValue[0] = True
                    else:
                        switchValue[0] = defaultSwitchValue[0]
               
                    if(userConfigSplit[5]=="False"):
                        switchValue[1] = False
                    elif(userConfigSplit[5]=="True"):
                        switchValue[1] = True
                    else:
                        switchValue[1] = defaultSwitchValue[1]
                    
                    #No need to check for incorrect values here...
                    #Crafty users could change their score on purpose
                    #READ: Nick!
                    stats[0] = userConfigSplit[6]
                    stats[1] = userConfigSplit[7]
                    stats[2] = userConfigSplit[8]
                    stats[3] = userConfigSplit[9]
                    stats[4] = userConfigSplit[10]
                    stats[5] = userConfigSplit[11]
                    stats[6] = userConfigSplit[12]
                    #The last field in the profile will always have a new line character at the end, so remove this when saving it to a variable
                    stats[7] = userConfigSplit[13].rpartition("\n")[0]
                    
                #If any errors are found, rewrite the profile line with the default values, keep the profile name.
                except:
                   self.fixProfs(profileNumber)  
                      
        profilesFile.close()
            
    #If this is called, a given profile that is selected has missing fields
    #So we need to rewrite the profile with the default values
    def fixProfs(self,profileNumber):
        buffer = []
        profilesFile2 = open(profilesFileName,"r")
        numUsers = int(profilesFile2.readline())
        for x in range(numUsers):
            userConfig = profilesFile2.readline()
            #Once you find the target profile, rewrite it with default values
            if(x==profileNumber):
                userConfigSplit = ['','','','','','','','','','','','']
                userConfigSplit[0] = userOptions[0][0]
                userConfigSplit[1] = defaultOptions[1][0]
                userConfigSplit[2] = defaultOptions[1][1]
                userConfigSplit[3] = defaultOptions[2][0]
                userConfigSplit[4] = defaultOptions[3][0]
                userConfigSplit[5] = defaultOptions[3][1]
                userConfigSplit[6] = defaultStats[0]
                userConfigSplit[7] = defaultStats[1]
                userConfigSplit[8] = defaultStats[2]
                userConfigSplit[9] = defaultStats[3]
                userConfigSplit[10] = defaultStats[4]
                userConfigSplit[11] = defaultStats[5]
                userConfigSplit[12] = defaultStats[6]
                #Of course, the last line will need a newline character 
                userConfigSplit[13] = str(defaultStats[7]) + "\n"
                
            else:
                userConfigSplit = userConfig.split('|')
            buffer.append(userConfigSplit)
        profilesFile2.close()
        
        #Now write everything back to the file
        profilesFile3 = open(profilesFileName,"w")
        profilesFile3.write(str(numUsers)+"\n")
        for field in buffer:
            for element in field:
                if (str(element).find("\n") == -1):
                    profilesFile3.write(str(element))
                    profilesFile3.write("|")
                else:
                    profilesFile3.write(str(element))
        profilesFile3.close()
        
        #Now that the profile the user selected has its values fixed, load these values
        self.loadOptions(profileNumber)

    
    def noProfSelectedMenu(self):
        c = gui.Container(width=100,height=60)
        defaultLabel = gui.Label("No Profile Selected",font=china_font)
        okayButton = gui.Button("Continue",font=china_font, height=buttonHeight)
        okayButton.connect(gui.CLICK,self.closeMenus,4)
        c.add(defaultLabel,0,0)
        c.add(okayButton,40,30)
        self.menu4 = gui.Dialog(gui.Label("Error",font=china_font),c)
        self.menu4.open()
     
    #Check for valid input
    def checkInput(self,input,menuNum):
        if (""==input):
            self.inputError = True
            c = gui.Container(width=40,height=90)
            errorLabel = gui.Label("Invalid User Name",font=china_font)
            tryAgainButton = gui.Button("Try Again",font=china_font, height=buttonHeight)
            cancelButton = gui.Button("Cancel",font=china_font, height=buttonHeight)
            tryAgainButton.connect(gui.CLICK,self.closeMenus,5)
            if menuNum == 1:
                cancelButton.connect(gui.CLICK,self.closeMenus,15)
            if menuNum == 3:
                cancelButton.connect(gui.CLICK,self.closeMenus,35)
            c.add(errorLabel,0,0)
            c.add(tryAgainButton,28,30)
            c.add(cancelButton,35,60)
            self.menu5 = gui.Dialog(gui.Label("Error",font=china_font),c)
            self.menu5.open()
         
    #Load the profiles that exist into a selection list for the user to browse through
    def loadProfileNames(self):
        #when creating a new profile, you should not blank out the profile
        #name array, or else all the new ones will be added
        #however, if you are loading in names after a profile deletion or edit,
        #you need to blank it out.
        if(self.delete):
            self.profileNames = []
            self.userNum = 0
        
        #For each user in the profiles file, load the first name into the array
        #and load that name into the list.
        #Take appropriate actions if the name is a repeat, etc.
        profilesFile = open(profilesFileName,"r")
        numUsers = int(profilesFile.readline())
        for x in range(numUsers):
            self.profileNames.append("")
            userConfig = profilesFile.readline()
            userConfigSplit = userConfig.split('|')
            if(not userConfigSplit[0] in self.profileNames):
                self.profileNames[self.userNum] = userConfigSplit[0]
                self.profileList.add(self.profileNames[self.userNum],str(self.userNum))
                self.userNum = self.userNum + 1
            else:
                self.profileNames.pop(-1)
        profilesFile.close()
    
    #When the delete button is clicked, create a confirm dialog, and proceed with the delete action if the user confirms the deletion, else cancel it
    def deleteProfile(self):
        error = False
        try:
            int(self.profileList.value)
        except TypeError:
            error = True
            self.noProfSelectedMenu()
        
        if(not error):
            c = gui.Container(width=105,height=90)
            
            defaultLabel = gui.Label("Delete Profile",font=china_font)
            deleteButton = gui.Button("Delete",font=china_font, height=buttonHeight)
            cancelButton = gui.Button("Cancel",font=china_font, height=buttonHeight)
            deleteButton.connect(gui.CLICK,self.delProf)
            cancelButton.connect(gui.CLICK,self.closeMenus,2)
            
            c.add(defaultLabel,0,0)
            c.add(deleteButton,20,30)
            c.add(cancelButton,20,60)
            
            self.menu2 = gui.Dialog(gui.Label("Confirm Delete",font=china_font),c)
            self.menu2.open()        
    
    #The delete algorithm is:
    #1) Remove the select list from the screen, load in all the data in the profiles file to a buffer
    #2) Write back all the profiles except for the one you have chosen to delete
    #3) Reload the profiles to the profile menu so that the select list is updated
    #4) Add the select list back onto the screen (now that is is updated)
    def delProf(self):
        self.delete = True
        self.closeMenus(2)
        
        target = int(self.profileList.value)
            
        #1
        buffer = []
        self.c.remove(self.profileList)
        self.profileList = gui.Select(font=china_font)
        profilesFile = open(profilesFileName,"r")
        numUsers = int(profilesFile.readline())
        for x in range(numUsers):
            userConfig = profilesFile.readline()
            userConfigSplit = userConfig.split('|')
            buffer.append(userConfigSplit)
        profilesFile.close()
        
        #2
        profilesFile2 = open(profilesFileName,"w")
        profilesFile2.write(str(numUsers-1)+"\n")
        z = 0
        for field in buffer:
            if(not target == z):
                for element in field:
                    if (element.find("\n") == -1):
                        profilesFile2.write(str(element))
                        profilesFile2.write("|")
                    else:
                        profilesFile2.write(str(element))
            z = z+1
        profilesFile2.close()   
        
        #3
        self.loadProfileNames()
        
        #4
        self.c.add(self.profileList,250,50)

    #Closes the menu
    #This occurs when a user selects a profile from the list
    #So if no profile is selected, let the user known an error has occured
    def closeMenu(self):
        error = False
        try:
            self.profileNum = int(self.profileList.value)
        except TypeError:
            error = True
            self.noProfSelectedMenu()
        
        #When a profile is selected from the list indicate that a  
        #profile has not been removed
        if(not error):
            self.close()
            self.newProfileNum = -1
            self.delete = False
            
            #Set the value of the name label to the selected profile
            profilesFile = open(profilesFileName,"r")
            numUsers = int(profilesFile.readline())
            for x in range(numUsers):
                userConfig = profilesFile.readline()
                userConfigSplit = userConfig.split('|')
                if(x==self.profileNum):
                    nameLabel.value = userConfigSplit[0]
            profilesFile.close()
            
            #This updates the last selected user to the history file
            buffer = []
            historyFile = open(historyFileName,"r")

            for x in range(6):
                historyLine = historyFile.readline()
                
                if type(historyLine) == type(""):
                    buffer.append(historyLine)
                else:
                    break
                    
            historyFile.close()
            
            buffer[0] = str(self.profileNum) + "\n"
            
            historyFile2 = open(historyFileName,"w")
            for element in buffer:
                historyFile2.write(element)
            historyFile2.close()
            
            #Now apply the profile's selected options!
            self.loadOptions(self.profileNum)
            self.setUserOptions(userOptions)
    
    def setUserOptions(self,options):
        #[0][0] == Name
        #Obviously do nothing with this now
        
        #[1][0] == Sound Volume
        #Do Nothing here, handled by game code
        
        #[1][1] == Music Volume
        pygame.mixer.music.set_volume(userOptions[1][1]/100.0)
        
        #[2][0] == music selection
        #Do nothing here, play background music while in main menu
        
        #[3][0] == Full screen T/F
        if(options[3][0]):
            screen = pygame.display.set_mode((700,720),pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((700,720),HWSURFACE)
        
        self.repaint()
    
        #[3][1] == Controller T/F
        if(options[3][1]):
            try:
                controller = pygame.joystick.Joystick(0)
                controller.init()
            except:
                options[3][1] = False
                noControllerMenu()
        
    def createMenu(self):        
        #Menu widgets
        profileLabel = gui.Label("Enter your Profile Name",font=china_font)
        profileName = gui.Input(value="",size=20,font=china_font)   
        createButton = gui.Button("Create Profile",font=china_font, height=buttonHeight)
        createButton.connect(gui.CLICK,self.createProfile,profileName)
        
        #Add widgets to container
        c = gui.Container(width=40,height=110)
        c.add(profileLabel,10,10)
        c.add(profileName,0,40)
        c.add(createButton,40,80)   
        
        #Initializes the dialog window menu
        title = gui.Label("Create Profile Menu",font=china_font)
        self.menu1 = gui.Dialog(title,c)
        self.menu1.open()

    #Loads the profile names in the profile file, in order to see if a 
    #duplicate name is trying to be created
    #Also checks to make sure profile has space (max 15 allowed)
    def loadProfileNames_2(self):
        limit = False
        userNum1 = 0
        profilesFile = open(profilesFileName,"r")
        numUsers = int(profilesFile.readline())
        
        if(numUsers >= 15):
            limit = True
        
        for x in range(numUsers):
            self.profileNames2.append("")
            userConfig = profilesFile.readline()
            userConfigSplit = userConfig.split('|')
            if(not userConfigSplit[0] in self.profileNames2):
                self.profileNames2[userNum1] = userConfigSplit[0]
                userNum1 = userNum1 + 1 
            else:
                self.profileNames2.pop(-1)
        profilesFile.close()
        
        return limit
        
    #Method for creating profiles
    def createProfile(self,input):
        #When create a profile, you need to first load a list of the names already existing
        #so that you can see if an existing profile already has the same desired name
        match = False
        first = True
        
        #Check for valid input first
        self.inputError = False
        self.checkInput(input.value,1)
        
        #If there is an input error, don't do anything else but allow
        #the user to re-attempt to enter a new profile name, or exit the
        #create profile menu
        if(not self.inputError):
            if(not self.loadProfileNames_2()):

                for element in self.profileNames2:
                    if(element==input.value):
                        match = True
                        break
                    
                #If no match is found, then the profile is a new profile (and not an existing user),
                #so append the new information to the end of the profile.txt file
                if(not match):
                    defaultOptions[0][0] = input.value
                    profilesFile = open(profilesFileName,"a")
                
                    for field in defaultOptions:
                        for element in field:
                            if(not first):
                                profilesFile.write("|")
                            first = False
                            profilesFile.write(str(element))
                
                    first = True
                    for field in defaultStats:
                        profilesFile.write("|")
                        profilesFile.write(str(field))
                
                    profilesFile.write("\n") 
                    profilesFile.close()
                    
                    nameLabel.value = defaultOptions[0][0]
                    
                    userOptions = defaultOptions
                
                    #As this is a new user, we have to also update the numUsers field, which this does
                    buffer = []
                    profilesFile2 = open(profilesFileName,"r")
                    numUsers = int(profilesFile2.readline())
                    numUsers = numUsers+1
                    self.newProfileNum = numUsers
                    for x in range(numUsers):
                        userConfig = profilesFile2.readline()
                        userConfigSplit = userConfig.split('|')
                        buffer.append(userConfigSplit)
                    profilesFile2.close()
                    
                    profilesFile3 = open(profilesFileName,"w")
                    profilesFile3.write(str(numUsers)+"\n")
                    for field in buffer:
                        for element in field:
                            if (element.find("\n") == -1):
                                profilesFile3.write(str(element))
                                profilesFile3.write("|")
                            else:
                                profilesFile3.write(str(element))
                    profilesFile3.close()
                   
                    self.closeMenus(1)
                    self.close()

                    self.loadProfileNames()
                    
                    self.loadOptions(self.newProfileNum-1)

                    #This updates the last selected user to the history file
                    buffer = []
                    historyFile = open(historyFileName,"r")
        
                    for x in range(6):
                        historyLine = historyFile.readline()
                        
                        if type(historyLine) == type(""):
                            buffer.append(historyLine)
                        else:
                            break
                            
                    historyFile.close()
                    
                    buffer[0] = str(self.newProfileNum-1) + "\n"
                    
                    historyFile2 = open(historyFileName,"w")
                    for element in buffer:
                        historyFile2.write(element)
                    historyFile2.close()

                #If there is a match found, then let the user know the name already
                #exists, and give them the option to try again or leave the menu
                elif(match):
                    c = gui.Container(width=40,height=95)
                    errorLabel = gui.Label("Profile Already Exists",font=china_font)
                    tryAgainButton = gui.Button("Try Again",font=china_font, height=buttonHeight)
                    cancelButton = gui.Button("Cancel",font=china_font, height=buttonHeight)
                    tryAgainButton.connect(gui.CLICK,self.closeMenus,6)
                    cancelButton.connect(gui.CLICK,self.closeMenus,16)
                    c.add(errorLabel,0,0)
                    c.add(tryAgainButton,43,30)
                    c.add(cancelButton,50,60)
                    self.menu6 = gui.Dialog(gui.Label("Error"),c)
                    self.menu6.open()
            
            else:
                c = gui.Container(width=40,height=65)
                errorLabel = gui.Label("Profile Limit Reached",font=china_font)
                cancelButton = gui.Button("Continue",font=china_font, height=buttonHeight)
                cancelButton.connect(gui.CLICK,self.closeMenus,16)
                c.add(errorLabel,0,0)
                c.add(cancelButton,38,30)
                self.menu6 = gui.Dialog(gui.Label("Error",font=china_font),c)
                self.menu6.open()
                
    def editProfileMenu(self):
        error = False
        try:
            int(self.profileList.value)
        except TypeError:
            error = True
            self.noProfSelectedMenu()
        
        if(not error):
            #Menu widgets
            profileLabel = gui.Label("Enter your New Profile Name",font=china_font)
            profileInput = gui.Input(value="",size=20,font=china_font)   
            createButton = gui.Button("Change Profile Name",font=china_font, height=buttonHeight)
            createButton.connect(gui.CLICK,self.editProfileName,profileInput)
            cancelButton = gui.Button("Cancel",font=china_font, height=buttonHeight)
            cancelButton.connect(gui.CLICK,self.closeMenus,3)
            
            #Add widgets to container
            c = gui.Container(width=40,height=140)
            c.add(profileLabel,5,10)
            c.add(profileInput,15,40)
            c.add(createButton,29,80)
            c.add(cancelButton,75,110)  
            
            #Initializes the dialog window menu
            title = gui.Label("Edit Profile Menu",font=china_font)
            self.menu3 = gui.Dialog(title,c)
            self.menu3.open()
        
    def editProfileName(self,profileName):
        #check if new name is good or not
        self.checkInput(profileName.value,3)
        
        if(not self.inputError):
            buffer = []
            profilesFile = open(profilesFileName,"r")
            numUsers = int(profilesFile.readline())
            for x in range(numUsers):
                userConfig = profilesFile.readline()
                userConfigSplit = userConfig.split('|')
                if(str(x) == self.profileList.value):
                    userConfigSplit[0] = profileName.value
                buffer.append(userConfigSplit)
            profilesFile.close()
            
            profilesFile2 = open(profilesFileName,"w")
            profilesFile2.write(str(numUsers)+"\n")
            for field in buffer:
                for element in field:
                    if (element.find("\n") == -1):
                        profilesFile2.write(str(element))
                        profilesFile2.write("|")
                    else:
                        profilesFile2.write(str(element))
            profilesFile2.close()
            
            self.closeMenus(3)
    
            self.c.remove(self.profileList)
            self.profileList = gui.Select(font=china_font)
            self.delete = True
            
            self.loadProfileNames()
            
            self.c.add(self.profileList,250,50)
            
    #Method for closing the various error menus and such
    def closeMenus(self,menuNum):
        if menuNum == 1:
            self.menu1.close()
        elif menuNum == 15:
            self.menu1.close()
            self.menu5.close()
        elif menuNum == 16:
            self.menu1.close()
            self.menu6.close()
        elif menuNum == 2:
            self.menu2.close()
        elif menuNum == 3:
            self.menu3.close()
        elif menuNum == 35:
            self.menu3.close()
            self.menu5.close()
        elif menuNum == 37:
            self.menu3.close()
            self.menu7.close()
        elif menuNum == 4:
            self.menu4.close()
        elif menuNum == 5:
            self.menu5.close()
        elif menuNum == 6:
            self.menu6.close()
        else:
            print menuNum

#Quick play menu
class SinglePlayerGame():
    
    def __init__(self,mainMenu):
            
        self.menu = mainMenu
    
    def start(self):
        #movements
        #gun controls: left, right, shoot, shoot barrel cannon
        #buy controls: up, down, spinner, barrel cannon,  upgrade spinner, upgrade max bullet, upgrade reload, confirm
        #confirm build, cancel build            
        if(userOptions[3][1]):
            try:
                controller = pygame.joystick.Joystick(0)
                controller.init()
            except:
                controller = None
                noControllerMenu()
        else:
            controller = None
        
        player1 = Player(userOptions[0][0],0,K_a,K_d,K_w,K_SPACE,K_r, K_f,K_RETURN, K_RSHIFT,controller,userOptions[1][0]/100.0)
        
        players = [player1]
        
        game = Game(players,userOptions[3][0],userOptions[2][0],None,None)
        gameStats = game.start()
        
        setStats("single",gameStats)
        
        #As the game changes the window size/etc, reformat the screen when control comes back
        if(userOptions[3][0]):
            screen = pygame.display.set_mode((700,720),pygame.FULLSCREEN)
        else:        
            screen = pygame.display.set_mode((700,720),HWSURFACE)

        self.menu.repaint()
        
        pygame.mixer.music.load(musicDir+backgroundMusic)
        pygame.mixer.music.play(-1)
        
#Local multiplayer menu
class LocalMultiplayerGame():
    
    def __init__(self,mainMenu):
        
        self.player2Name = ""
        self.mainMenu = mainMenu
        self.player2ControlOption = ""
    
    #Provides the user interface needed for selecting the second player for the local multiplayer game    
    def select2Player(self):
        profileNames = []
        userNum = 0
        profileList = gui.Select(font=china_font)
           
        #Menu widgets
        c = gui.Container(width=300,height=100)
        profileLabel = gui.Label("Select player two profile",font=china_font)        
        selectProfileButton = gui.Button("Select Profile",font=china_font, height=buttonHeight)
        selectProfileButton.connect(gui.CLICK,self.checkSelect,profileList)
        
        #Load the profile list with the availble user names (all but the currently selected profile)
        profilesFile = open(profilesFileName,"r")
        numUsers = int(profilesFile.readline())
        for x in range(numUsers):
            profileNames.append("")
            userConfig = profilesFile.readline()
            userConfigSplit = userConfig.split('|')
            if((not userConfigSplit[0] in profileNames) and (userConfigSplit[0] != userOptions[0][0])):
                profileNames[userNum] = userConfigSplit[0]
                profileList.add(profileNames[userNum],userNum)
                userNum = userNum + 1
            elif(userConfigSplit[0]==userOptions[0][0]):
                userNum = userNum + 1
            else:
                profileNames.pop(-1)
        
        profilesFile.close()

        #Add widgets to container
        c.add(profileLabel,40,10)
        c.add(selectProfileButton,30,50)
        c.add(profileList,190,50)
        
        title = gui.Label("Local Multiplayer",font=china_font)

        self.menu = gui.Dialog(title,c)
        
        self.menu.open()

    #Ensure that the user selects a valid second player profile
    def checkSelect(self,list):
        error = False
        
        try:
            #although the list values are already ints, you need to cast as int again to check if its valid (as otherwise no exception would occur)
            profileNum = int(list.value)
            profilesFile = open(profilesFileName,"r")
            numUsers = int(profilesFile.readline())
            for x in range(numUsers):
                userConfig = profilesFile.readline()
                userConfigSplit = userConfig.split('|')
                if (profileNum == x):
                    self.player2Name = userConfigSplit[0]
                    self.player2ControlOption = userConfigSplit[5]
                    multiStats[0] = userConfigSplit[6]
                    multiStats[1] = userConfigSplit[7]
                    multiStats[2] = userConfigSplit[8]
                    multiStats[3] = userConfigSplit[9]
                    multiStats[4] = userConfigSplit[10]
                    multiStats[5] = userConfigSplit[11]
                    multiStats[6] = userConfigSplit[12]
                    #The last field in the profile will always have a new line character at the end, so remove this when saving it to a variable
                    multiStats[7] = userConfigSplit[13].rpartition("\n")[0]
            
        #If anything bad happens, then the user has not selected a second player
        except:
            error = True
            c = gui.Container(width=100,height=60)
            self.menu4 = gui.Dialog(gui.Label("Error",font=china_font),c)
            defaultLabel = gui.Label("No Profile Selected",font=china_font)
            okayButton = gui.Button("Continue",font=china_font, height=buttonHeight)
            okayButton.connect(gui.CLICK,self.menu4.close,None)
            c.add(defaultLabel,0,0)
            c.add(okayButton,40,30)
            self.menu4.open()
        
        #If everything works, start the two player game
        if(not error):
            self.preStart()
                
    def noControllerMenu(self,userName):
        c = gui.Container(width=100,height=90)
        self.errorMenu = gui.Dialog(gui.Label("Error",font=china_font),c)
        errorLabel1 = gui.Label("No Controller Found",font=china_font)
        errorLabel2 = gui.Label("Default Buttons Set For " + userName + ".",font=china_font)
        okayButton = gui.Button("Continue",font=china_font,height=buttonHeight)
        okayButton.connect(gui.CLICK,self.startGame)
        c.add(errorLabel1,40,0)
        c.add(errorLabel2,0,30)
        c.add(okayButton,85,60)
        self.errorMenu.open()
        
    def preStart(self):            
        #Close the 2 player select menu, as the game will be starting
        self.menu.close()
        
        error = False
        self.controller1 = None
        self.controller2 = None
        
        if userOptions[3][1] and self.player2ControlOption=="True":
            try:
                self.controller1 = pygame.joystick.Joystick(0)
                self.controller1.init()
            except:
                error = True
                self.noControllerMenu(userOptions[0][0])
                self.controller1 = None
            
            try:
                self.controller2 = pygame.joystick.Joystick(1)
                self.controller2.init()
            except:
                error = True
                self.noControllerMenu(self.player2Name)
                self.controller2 = None
        
        elif userOptions[3][1]:
            try:
                self.controller1 = pygame.joystick.Joystick(0)
                self.controller1.init()
            except:
                error = True
                self.noControllerMenu(userOptions[0][0])
                self.controller1 = None
                
        elif self.player2ControlOption=="True":
            try:
                self.controller2 = pygame.joystick.Joystick(0)
                self.controller2.init()
            except:
                error = True
                self.noControllerMenu(self.player2Name)
                self.controller2 = None
        
        if not error:
            self.startGame()
            
    #Responsible for starting the game when ready
    def startGame(self):
        try:
            self.errorMenu.close()
        except:
            pass
        
        #Create the two players (default sound volume is player 1's settings)
        player1 = Player(userOptions[0][0],0,K_a,K_d,K_w,K_SPACE,K_r, K_f,K_RETURN, K_RSHIFT,self.controller1,userOptions[1][0])
        player2 = Player(self.player2Name,1,K_LEFT,K_RIGHT,K_UP, K_KP0,K_KP_MINUS, K_KP_PLUS,K_KP_ENTER, K_KP_PERIOD,self.controller2,userOptions[1][0])

        #Add the players to a player list, as the game needs this format
        players = [player1,player2]
        
        #Create the game object
        game = Game(players,userOptions[3][0],userOptions[2][0],None, None)
        
        #The game returns the stats obtained during the game
        gameStats = game.start()
        
        setStats("multilocal",gameStats)
#       
        #As the game changes the window size/etc, reformat the screen when control comes back
        if(userOptions[3][0]):
            screen = pygame.display.set_mode((700,720),pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((700,720),HWSURFACE)

        self.mainMenu.repaint()
        
        pygame.mixer.music.load(musicDir+backgroundMusic)
        pygame.mixer.music.play(-1)

#Network multiplayer host menu
class NetworkMultiHostMenu(gui.Desktop):

    menu = gui.Desktop()
    soc = socObject("")
    openConnection = False
    
    def __init__(self,mainMenu,**params):
        
        self.menu = mainMenu

        gui.Desktop.__init__(self)
    
    def start(self):
        c = gui.Container()
         
        menuLabel = gui.Label("Network Multiplayer Host Menu",font=china_font)
        ipLabel = gui.Label("Your IP Address is: ",font=china_font)
        ipAddr = gui.Label(str(gethostbyname(gethostname())),font=china_font)
#        ipAddr = gui.Label("x.x.x.x",font=china_font)
        
        hostButton = gui.Button("Host a new Game",font=china_font, height=buttonHeight)
        hostButton.connect(gui.CLICK,self.hostGame)
        
        returnButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        returnButton.connect(gui.CLICK,self.leave)
        
        bgImage = gui.Image(imageDir+'hostMenu.png')
        color = gui.Color("white",height=800,width=800)
        
        c.add(color,0,0)
        c.add(bgImage,0,0)
        c.add(menuLabel,110,30)
        c.add(hostButton,150,200)
        c.add(ipLabel,100,255)
        c.add(ipAddr,260,255)
        c.add(returnButton,140,300)
        self.run(c)

    def hostGame(self):
        self.openConnection = True
        
        self.soc = socObject("")
        self.soc.create_server_socket()
        
        self.accept = acceptConn(self.soc)
        self.accept.start()
        self.accept.accept()
        #self.accept.fun = self.startGame

    #def startGame(self):        
        get_data = self.accept.getDataThread
        send_data = self.accept.sendDataThread
        print get_data
        print send_data

        if(userOptions[3][1]):
            try:
                controller = pygame.joystick.Joystick(0)
                controller.init()
            except:
                controller = None
                noControllerMenu()
        else:
            controller = None
        
        player1 = Player(userOptions[0][0],0,K_a,K_d,K_w,K_SPACE,K_r, K_f,K_RETURN, K_RSHIFT,controller,userOptions[1][0]/100.0)
        
        players = [player1]
    
        game = Game(players,userOptions[3][0],userOptions[2][0], get_data, send_data)
        
        gameStats = game.start()
        
        setStats("multinetwork",gameStats)
        
        #As the game changes the window size/etc, reformat the screen when control comes back
        if(userOptions[3][0]):
            screen = pygame.display.set_mode((700,720),pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((700,720),HWSURFACE)
        
        self.repaintall()
    
        pygame.mixer.music.load(musicDir+backgroundMusic)
        pygame.mixer.music.play(-1)
    
    #Leave method: this will close the single player menu, and then repaint the main menu to make it appear again
    def leave(self):
        if self.openConnection == True:
            try:
                self.accept.soc.TCPSock.close()
                #self.testy = socket(AF_INET,SOCK_STREAM)
                #self.testy.connect(('localhost',12345))  
                #self.accept.running = False
            except error, (value,message): 
                print "Host socket is closed!!!!"
        self.quit()
        
        self.menu.repaint()
        
#Networking multiplayer menu
class NetworkMultiJoinMenu(gui.Desktop):

    menu = gui.Desktop()
    soc = socObject("")
    openConnection = False
    
    def __init__(self,mainMenu,**params):
        
        self.menu = mainMenu   
    
        gui.Desktop.__init__(self)
    
    def start(self):
        c = gui.Container()
        
        historySelect = gui.Select(font=china_font)
        historySelect.connect(gui.CHANGE,self.updateLabel,historySelect)
                
        ipHistory = []
        historyFile = open(historyFileName,"r")
        historyFile.readline()
        for x in range(5):
            ipAddr = historyFile.readline().rpartition("\n")[0]
            historySelect.add(ipAddr,ipAddr)
        historyFile.close()
        
        menuLabel = gui.Label("Network Multiplayer Join Menu",font=china_font)
        inputLabel = gui.Label("Input or select the Host's IP Address",font=china_font)
        
        self.ipInput = gui.Input(value="",size=20,font=china_font)
        
        connectButton = gui.Button("Connect to Host",font=china_font, height=buttonHeight)
        connectButton.connect(gui.CLICK,self.openConnection,self.ipInput)
        
        returnButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        returnButton.connect(gui.CLICK,self.leave)
        
        bgImage = gui.Image(imageDir+'joinMenu.png')
        color = gui.Color("white",width=800,height=800)
        
        c.add(color,0,0)
        c.add(bgImage,0,0)
        c.add(menuLabel,335,30)
        c.add(inputLabel,310,200)
        c.add(self.ipInput,355,250)
        c.add(historySelect,380,300)
        c.add(connectButton,385,350)
        c.add(returnButton,370,400)
        
        self.run(c)
    
    def updateLabel(self,label):
        self.ipInput.value = label.value
    
    def openConnection(self,inputField):
        ip = ""
        ip = str(inputField.value)
        
        #Update the ip history
        buffer = []
        historyFile = open(historyFileName,"r")

        for x in range(6):
            historyLine = historyFile.readline()
            
            if type(historyLine) == type(""):
                buffer.append(historyLine)
            else:
                break
                
        historyFile.close()
        
        if not (buffer.__contains__(ip+"\n")):
            buffer[5] = buffer[4]
            buffer[4] = buffer[3]
            buffer[3] = buffer[2]
            buffer[2] = buffer[1]
            buffer[1] = ip+"\n"
            
            historyFile2 = open(historyFileName,"w")
            for element in buffer:
                historyFile2.write(element)
            historyFile2.close()
                    
        self.openConnection = True
        self.soc = socObject(ip)
        self.soc.create_client_socket()
        
        get_data = getData(self.soc, 'client')
        get_data.start()
        send_data = sendData(self.soc, 'client')
        send_data.start()

        if(userOptions[3][1]):
                try:
                    controller = pygame.joystick.Joystick(0)
                    controller.init()
                except:
                    controller = None
                    noControllerMenu()
        else:
            controller = None
        
        player1 = Player(userOptions[0][0],0,K_a,K_d,K_w,K_SPACE,K_r, K_f,K_RETURN, K_RSHIFT,controller,userOptions[1][0]/100.0)
        
        players = [player1]
    
        game = Game(players,userOptions[3][0],userOptions[2][0], get_data, send_data)
    
        gameStats = game.start()
        
        setStats("multinetwork",gameStats)
        
        #As the game changes the window size/etc, reformat the screen when control comes back
        if(userOptions[3][0]):
            screen = pygame.display.set_mode((700,720),pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((700,720),HWSURFACE)
        
        self.repaintall()
        
        pygame.mixer.music.load(musicDir+backgroundMusic)
        pygame.mixer.music.play(-1)
        
    #Leave method: this will close the single player menu, and then repaint the main menu to make it appear again
    def leave(self):
        if self.openConnection == True:
            try:
                self.soc.TCPSock.close()
            except error, (value,message): 
                print "Client socket is closed!!!!"
        self.quit()
        
        self.menu.repaint()
  
#Options Menu
class OptionsMenu(gui.Dialog):
    
    profileNum = -1
    playedSong = False
    
    def __init__(self,**params):
        title = gui.Label("Options Menu",font=china_font)
        
        #Plays the user's current selected song initially
        if not userOptions[2][0] == 0:
            pygame.mixer.music.load(musicDir+levelMusic[int(userOptions[2][0])-1]+".ogg")
            pygame.mixer.music.play(-1)
        else:
            pass

        #Creates the options menu
        c = gui.Container(width=300,height=370)
    
        ###BEGIN OPTION MENU WIDGETS###
        ##Game Options
        gameOptionsLabel = gui.Label("Game Options",font=china_font)
        c.add(gameOptionsLabel,130,10)
        
        #Windowed Mode
        fullscreenSwitchLabel = gui.Label("Fullscreen ",font=china_font)
        fullscreenSwitch = gui.Switch(userOptions[3][0])
        fullscreenSwitch.connect(gui.CHANGE,self.updateSwitch,(0,fullscreenSwitch))
       
        c.add(fullscreenSwitchLabel,50,50)
        c.add(fullscreenSwitch,280,50)
                
        #Controller Mode T/F
        controllerSwitchLabel = gui.Label("In Game Controller Support",font=china_font)
        controllerSwitch = gui.Switch(userOptions[3][1])
        controllerSwitch.connect(gui.CHANGE,self.updateSwitch,(1,controllerSwitch))
        
        c.add(controllerSwitchLabel,50,80)
        c.add(controllerSwitch,280,80)
        
        ##Sound Options
        soundOptionsLabel = gui.Label("Sound Options",font=china_font)
        c.add(soundOptionsLabel,130,150)
        
        #Sound Volume
        #The sound and music volume sliders work so that they update their labels when they change value.
        #This is achieved by having the value of the slider held in a class-wide variable 'value', which is
        #a list with 2 entries: 1 for each slider.
        soundVolumeSliderLabel = gui.Label("Sound Volume",font=china_font)
        soundVolumeSlider = gui.HSlider(value=userOptions[1][0],min=0,max=100,size=20,height=16,width=120)
        soundVolumeSliderValueLabel = gui.Label(str(userOptions[1][0]) + "%       ",font=china_font)
        soundVolumeSlider.connect(gui.CHANGE,self.updateLabel, (0,soundVolumeSlider),soundVolumeSliderValueLabel)

        c.add(soundVolumeSliderLabel,50,190)
        c.add(soundVolumeSlider,180,190)
        c.add(soundVolumeSliderValueLabel,310,190)
        
        #Music Volume
        musicVolumeSliderLabel = gui.Label("Music Volume",font=china_font)
        musicVolumeSlider = gui.HSlider(value=userOptions[1][1],min=0,max=100,size=20,height=16,width=120)
        musicVolumeSliderValueLabel = gui.Label(str(userOptions[1][1]) + "%       ",font=china_font)
        musicVolumeSlider.connect(gui.CHANGE,self.updateLabel, (1,musicVolumeSlider),musicVolumeSliderValueLabel)
                
        c.add(musicVolumeSliderLabel,50,220)
        c.add(musicVolumeSlider,180,220)
        c.add(musicVolumeSliderValueLabel,310,220)
       
        #Song selection
        songSelectLabel = gui.Label("Select Music",font=china_font)
        songSelect = gui.Select(value=str(userOptions[2][0]),font=china_font)
        songSelect.add("Random","0")
        
        x = 1
        for element in levelMusic:
            songSelect.add(element,str(x))
            x = x+1

        songSelect.connect(gui.CHANGE,self.updateSelection,songSelect)
        
        c.add(songSelectLabel,50,280)    
        c.add(songSelect,215,280)      
        
        okayButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        okayButton.connect(gui.CLICK,self.closeMenu)
        
        c.add(okayButton,95,330)
        
        ###END OPTIONS MENU WIDGETS###
        
        gui.Dialog.__init__(self,title,c)
    
    #Changed the way this works - play any song the user selects, but do nothing for random, as it will randomly play all of these songs
    #Pass this option into the game when it is created, will handle game playback then.
    def playSong(self):
        self.playedSong = True
        
        if(userOptions[2][0] == 0):
            pygame.mixer.music.stop()
        else:            
            songNum = levelMusic[userOptions[2][0]-1]
            pygame.mixer.music.load(musicDir+str(songNum)+".ogg")
            pygame.mixer.music.play(-1)

    def closeMenu(self):
        self.writeOptions()
        self.close()

        #Begin playing the background music again, as the user is going to the main menu
        if self.playedSong:
            pygame.mixer.music.load(musicDir+backgroundMusic)
            pygame.mixer.music.play(-1)
        
    #Update method, used by the volume sliders to update their labels
    #slideNum,slider identifies the slider number (sound or music) and the actual reference to the sliders
    #label is the label to be updated
    #The value of the slider is first saved to the class wide variable for that slider, then the label updated
    def updateLabel(self,slider,label):      
        slideNum,slider = slider
        label = label
        userOptions[1][slideNum] = slider.value       
        label.value = str(slider.value) + "%"
        self.repaint()
        
        if(slideNum==0):
          #change sound volume
          pass
        elif(slideNum==1):  
            pygame.mixer.music.set_volume(userOptions[1][1]/100.0)
    
    #Updates the selected music to play
    def updateSelection(self,selector):
        userOptions[2][0] = int(selector.value)
        self.playSong()
    
    #Updates the selected game modes for full screen and controller
    def updateSwitch(self,switch):
        switchNum,switch = switch
        userOptions[3][switchNum] = switch.value
        
        if(switchNum==0):
            if(userOptions[3][0]):
                screen = pygame.display.set_mode((700,720),pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((700,720),HWSURFACE)
        
            self.repaint()
                
        elif(switchNum==1): #Attempt to create a joystick object just to know whether or not one is installed on the system
            if(userOptions[3][1]):
                try:
                    controller = pygame.joystick.Joystick(0)
                    controller.init()
                except:
                    userOptions[3][1] = False
                    switch.value = False
                    noControllerMenu()
            else:
                pass

    #Writes the options the user has specified to their profile when the menu is closed
    def writeOptions(self):
        #In order to update the user's options, first load all the data into a buffer
        #and if the match of the user whos updating their profile is found, edit the data
        #then write it back to the file
        buffer = []
        profilesFile = open(profilesFileName,"r")
        numUsers = int(profilesFile.readline())
        for x in range(numUsers):
            userConfig = profilesFile.readline()
            userConfigSplit = userConfig.split('|')
            if(userConfigSplit[0] == userOptions[0][0]):
                userConfigSplit[1] = userOptions[1][0]
                userConfigSplit[2] = userOptions[1][1]
                userConfigSplit[3] = userOptions[2][0] 
                if(userOptions[3][0]==False):
                    userConfigSplit[4] = False
                elif(userOptions[3][0]==True):
                    userConfigSplit[4] = True    
                if(userOptions[3][1]==False):
                    userConfigSplit[5] = False
                elif(userOptions[3][1]==True):
                   userConfigSplit[5] = True
            buffer.append(userConfigSplit)
        profilesFile.close()

        profilesFile2 = open(profilesFileName,"w")
        profilesFile2.write(str(numUsers)+"\n")
        for field in buffer:
            for element in field:
                if (str(element).find("\n") == -1):
                    profilesFile2.write(str(element))
                    profilesFile2.write("|")
                else:
                    profilesFile2.write(str(element))
        profilesFile2.close()
            
#Statistics menu
class StatsMenu(gui.Desktop):

    menu = gui.Desktop()
    
    def __init__(self,mainMenu,**params):
        
        self.menu = mainMenu
    
        gui.Desktop.__init__(self)
    
    #Start the statistics profile menu, which means load the stats!
    def start(self):        
        #Labels used to describe the table columns
        profileNameLabel = gui.Label("Profile Name",font=china_font_small)
        numberofGamesLabel = gui.Label("# of Games Played",font=china_font_small)
        numberOfWinsLabel = gui.Label("# of Wins",font=china_font_small)
        numberOfLossesLabel = gui.Label("# of Losses",font=china_font_small)
        totalPointsLabel = gui.Label("Total Credits",font=china_font_small)
        highestPointsLabel = gui.Label("Credit Highscore",font=china_font_small)
        avePointsLabel = gui.Label("Credits/Game",font=china_font_small)
        totalTimeLabel = gui.Label("Total Time",font=china_font_small)
        highestTimeLabel = gui.Label("Time Highscore",font=china_font_small)
        aveTimeLabel = gui.Label("Time/Game",font=china_font_small)
        numItemsLabel = gui.Label("# of Items Bought",font=china_font_small)
        
        #creates the statistics holding table
        statTable = gui.Table()
        statTable2 = gui.Table()
        
        #Create a new row
        statTable.tr()
        statTable2.tr()
        
        #Load the columns labels into the initial row
        statTable.td(profileNameLabel)
        statTable.td(gui.Label(" "))
        statTable.td(numberofGamesLabel)
        statTable.td(gui.Label(" "))
        statTable.td(numberOfWinsLabel)
        statTable.td(gui.Label(" "))
        statTable.td(numberOfLossesLabel)
        statTable.td(gui.Label(" "))
        statTable.td(totalPointsLabel)
        statTable.td(gui.Label(" "))
        statTable.td(totalTimeLabel)
        
        #One table is too big to hold all the values in 1 row, so two tables are used
        statTable2.td(profileNameLabel)
        statTable2.td(gui.Label(" "))
        statTable2.td(numItemsLabel)
        statTable2.td(gui.Label(" "))
        statTable2.td(avePointsLabel)
        statTable2.td(gui.Label(" "))
        statTable2.td(aveTimeLabel)
        statTable2.td(gui.Label(" "))
        statTable2.td(highestPointsLabel)
        statTable2.td(gui.Label(" "))
        statTable2.td(highestTimeLabel)
        
        #Read in the statistics from the profile file
        profilesFile = open(profilesFileName,"r")
        numUsers = int(profilesFile.readline())
        for x in range(numUsers):
            
            #Create a new row for each profile
            statTable.tr()
            statTable2.tr()
        
            
            userConfig = profilesFile.readline()
            userConfigSplit = userConfig.split('|')
            
            #First try to load these profile stats
            try:
                userConfigSplit[0]
                userConfigSplit[6]
                userConfigSplit[7]
                userConfigSplit[8]
                userConfigSplit[9]
                userConfigSplit[10]
                userConfigSplit[11]
                userConfigSplit[12]
                userConfigSplit[13]

            #If any errors, tell the user that an error has occured with this profile by display "Error" for values
            #This makes it so profiles with errors will not mess up any other profile's stats.
            except:
                userConfigSplit = ["Error",'','','','','',"Error","Error","Error","Error","Error","Error","Error","Error\n"]

            #Add the stats to the tables
            statTable.td(gui.Label(userConfigSplit[0],font=china_font_small))             #Name
            statTable.td(gui.Label("   "))
            statTable.td(gui.Label(userConfigSplit[6],font=china_font_small))             #Games Played
            statTable.td(gui.Label("   "))
            statTable.td(gui.Label(userConfigSplit[7],font=china_font_small))             # Games won
            statTable.td(gui.Label("   "))
            statTable.td(gui.Label(userConfigSplit[8],font=china_font_small))             # Games Lost
            statTable.td(gui.Label("   "))
            statTable.td(gui.Label(userConfigSplit[9],font=china_font_small))             #Total Points
            statTable.td(gui.Label("   "))
            statTable.td(gui.Label(userConfigSplit[10],font=china_font_small))            #Total Time
            
            statTable2.td(gui.Label(userConfigSplit[0],font=china_font_small))            #Name
            statTable2.td(gui.Label("   "))
            statTable2.td(gui.Label(userConfigSplit[11],font=china_font_small))           # # of items bought
            statTable2.td(gui.Label("   "))
            try:
                statTable2.td(gui.Label(str(round((float(userConfigSplit[9]) / float(userConfigSplit[6])),2)),font=china_font_small))  #Ave Points/Game
            except:
                statTable2.td(gui.Label("0",font=china_font_small))
            statTable2.td(gui.Label("   "))
            try:
                statTable2.td(gui.Label(str(round((float(userConfigSplit[10]) / float(userConfigSplit[6])),2)),font=china_font_small))  #Ave Time/Game
            except:
                statTable2.td(gui.Label("0",font=china_font_small))
            statTable2.td(gui.Label("   "))
            statTable2.td(gui.Label(userConfigSplit[12],font=china_font_small))                                  #Credits High Score## Items Bought
            statTable2.td(gui.Label("   "))
            statTable2.td(gui.Label(userConfigSplit[13].rpartition("\n")[0],font=china_font_small))            #Highest time scored
                
        profilesFile.close()
        
        menuLabel = gui.Label("Statistics Menu",font=china_font_big)
        returnButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        returnButton.connect(gui.CLICK,self.leave)
        color = gui.Color("white",width=800,height=800)
        bgImage = gui.Image(imageDir+'sortedNuts.png')
        
        c = gui.Container()
        c.add(color,0,0)
        c.add(bgImage,0,0)
        c.add(menuLabel,270,30)
        c.add(returnButton,250,690)
        c.add(statTable,30,90)
        c.add(statTable2,30,405)
        self.run(c)

    #Leave method: this will close the single player menu, and then repaint the main menu to make it appear again
    def leave(self):
        self.quit()
        self.menu.repaint()
        
#Stats menu
class HighScoreMenu(gui.Desktop):

    menu = gui.Desktop()
    
    def __init__(self,mainMenu,**params):
        
        self.menu = mainMenu
    
        gui.Desktop.__init__(self)
    
    def start(self):        
        #Labels used to describe the table columns
        rankLabel = gui.Label("Rank",font=china_font_bold)
        profileNameLabel = gui.Label("Profile Name",font=china_font_bold)
        pointsLabel = gui.Label("Credits Earned",font=china_font_bold)
        timeLabel = gui.Label("Time Survived",font=china_font_bold)
        pointsTableLabel = gui.Label("Most Credits Earned in One Game",font=china_font)
        timeTableLabel = gui.Label("Longest Survival Time",font=china_font)
        
        #creates the high scores table
        pointsTable = gui.Table()
        timeTable = gui.Table()
        
        #Create a new row
        pointsTable.tr()
        timeTable.tr()
        
        #Load the columns labels into the initial row
        pointsTable.td(rankLabel)
        pointsTable.td(gui.Label("   "))
        pointsTable.td(profileNameLabel)
        pointsTable.td(gui.Label("   "))
        pointsTable.td(pointsLabel)
        
        timeTable.td(rankLabel)
        timeTable.td(gui.Label("   "))
        timeTable.td(profileNameLabel)
        timeTable.td(gui.Label("   "))
        timeTable.td(timeLabel)
    
        x = 1
        for e in pointsList:
            #Create a new row for each entry
            pointsTable.tr()
            
            pointsTable.td(gui.Label(str(x),font=china_font))
            pointsTable.td(gui.Label("   "))
            pointsTable.td(gui.Label(e.name,font=china_font))
            pointsTable.td(gui.Label("   "))
            pointsTable.td(gui.Label(str(e.score),font=china_font))
            x = x+1
            
        x = 1
        for e in timeList:
            #Create a new row for each entry
            timeTable.tr()
            
            timeTable.td(gui.Label(str(x),font=china_font))
            timeTable.td(gui.Label("   "))
            timeTable.td(gui.Label(e.name,font=china_font))
            timeTable.td(gui.Label("   "))
            timeTable.td(gui.Label(str(e.score),font=china_font))
            x = x+1
            
        bgImage = gui.Image(imageDir+'pyking.png',height=487,width=390)
        
        menuLabel = gui.Label("High score Menu",font=china_font_big)
        returnButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        returnButton.connect(gui.CLICK,self.leave)
        color = gui.Color("white",width=800,height=800)
        
        c = gui.Container()
        c.add(color,0,0)
        c.add(bgImage,5,100)
        c.add(menuLabel,275,30)
        c.add(returnButton,250,690)
        c.add(pointsTableLabel,400,100)
        c.add(pointsTable,385,130)
        c.add(timeTableLabel,435,380)
        c.add(timeTable,385,410)
        self.run(c)

    #Leave method: this will close the single player menu, and then repaint the main menu to make it appear again
    def leave(self):
        self.quit()
        self.menu.repaint()

class StoryMenu(gui.Desktop):
    
    menu = gui.Desktop()
    
    def __init__(self,mainMenu,**params):
        
        self.menu = mainMenu
    
        gui.Desktop.__init__(self)
        
    def start(self):
        storyLabel1 = gui.Label("Welcome to Py\'s Problem, a game that takes place in another world and is unlike any other. In Py\'s",font=china_font_small)
        storyLabel2 = gui.Label("Problem you join our hero Py, a gatherer of food for his colony. While gathering food may seem like",font=china_font_small)
        storyLabel3 = gui.Label("a simple task, it is actually extremely difficult and only the most skilled gatherers are given this",font=china_font_small)
        storyLabel4 = gui.Label("job.",font=china_font_small)
        spaceLabel = gui.Label(" ")
        storyLabel5 = gui.Label("The food itself is a large nut like object that grows off vines inside large caves. The plant that",font=china_font_small)
        storyLabel6 = gui.Label("produces these nuts becomes fully matured when all of its stems are occupied with nuts, leaving no",font=china_font_small)
        storyLabel7 = gui.Label("room for it to grow. It also has a very unique property in that once it has fully matured, it will",font=china_font_small)
        storyLabel8 = gui.Label("never sprout nuts again. The plant also tries to mature itself faster and faster as time goes by which",font=china_font_small)
        storyLabel9 = gui.Label("makes the process of stopping it from maturing even harder. So, as you can see a good gatherer is",font=china_font_small)
        storyLabel10 = gui.Label("needed to make effective use out of the plant and get the most amount of food out of it. The nuts",font=china_font_small)
        storyLabel11 = gui.Label("themselves also grow in a peculiar fashion. When the first nut grows out of the vine, thre other",font=china_font_small)
        storyLabel12 = gui.Label("smaller nuts can grow out of that one. Two even smaller nuts can grow out of the latter. While",font=china_font_small)
        storyLabel13 = gui.Label("the nuts can be used no matter what for food, it is ideal to keep them together as the bond between",font=china_font_small)
        storyLabel14 = gui.Label("them keeps them fresher and helps retain the nutritional value.",font=china_font_small)
        storyLabel15 = gui.Label("Since the food Py is harvesting is high up, Py and the other gatherers must utilize a special cannon",font=china_font_small)
        storyLabel16 = gui.Label("-like apparatus to knock them down. In return, he is awarded with money for the food he collects.",font=china_font_small)
        storyLabel17 = gui.Label("He can use this money to have advancements made to his cannon, or even purchase an additional cannon",font=china_font_small)
        storyLabel18 = gui.Label("to help collect food faster. While the colonies on this planet are usually peaceful, they become",font=china_font_small)
        storyLabel19 = gui.Label("very self-conscious about who has the most food. Because of this gatherers often employ",font=china_font_small)
        storyLabel20 = gui.Label("spinners, an obtrusive object that makes it hard to collect nuts, on other gathers.",font=china_font_small)
        storyLabel21 = gui.Label("At the end of the day though, no gatherer can keep a plant growing forever. But, the ones that keep",font=china_font_small)
        storyLabel22 = gui.Label("it going the longest are seen as heroes! So, join Py and the other gatherers and test your nut",font=china_font_small)
        storyLabel23 = gui.Label("collecting skills!",font=china_font_small)
        
        bgImage = gui.Image(imageDir+'nutPile.png')
        menuLabel = gui.Label("Background Story",font=china_font_big)
        returnButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        returnButton.connect(gui.CLICK,self.leave)
        color = gui.Color("white",width=800,height=800)
        labelDiff = 20
        initLabelY = 60
        c = gui.Container()
        c.add(color,0,0)
        c.add(bgImage,0,120)
        c.add(storyLabel1,10,initLabelY+labelDiff)
        c.add(storyLabel2,10,initLabelY+labelDiff*2)
        c.add(storyLabel3,10,initLabelY+labelDiff*3)
        c.add(storyLabel4,10,initLabelY+labelDiff*4)
        c.add(storyLabel5,10,initLabelY+labelDiff*7)
        c.add(storyLabel6,10,initLabelY+labelDiff*8)
        c.add(storyLabel7,10,initLabelY+labelDiff*9)
        c.add(storyLabel8,10,initLabelY+labelDiff*10)
        c.add(storyLabel9,10,initLabelY+labelDiff*11)
        c.add(storyLabel10,10,initLabelY+labelDiff*12)
        c.add(storyLabel11,10,initLabelY+labelDiff*13)
        c.add(storyLabel12,10,initLabelY+labelDiff*14)
        c.add(storyLabel13,10,initLabelY+labelDiff*15)
        c.add(storyLabel14,10,initLabelY+labelDiff*16)
        c.add(storyLabel15,10,initLabelY+labelDiff*19)
        c.add(storyLabel16,10,initLabelY+labelDiff*20)
        c.add(storyLabel17,10,initLabelY+labelDiff*21)
        c.add(storyLabel18,10,initLabelY+labelDiff*22)
        c.add(storyLabel19,10,initLabelY+labelDiff*23)
        c.add(storyLabel20,10,initLabelY+labelDiff*24)
        c.add(storyLabel21,10,initLabelY+labelDiff*25)
        c.add(storyLabel22,10,initLabelY+labelDiff*26)
        c.add(storyLabel23,10,initLabelY+labelDiff*27)
        c.add(menuLabel,270,30)
        c.add(returnButton,250,690)
        self.run(c)
    
    def leave(self):
        self.quit()
        self.menu.repaint()

class GamePlayMenu(gui.Desktop):
    
    menu = gui.Desktop()
    #        basic premise
#        controls
#        color menu
#        upgrades
    
    def __init__(self,mainMenu,**params):
        
        self.menu = mainMenu
    
        gui.Desktop.__init__(self)
        
    def start(self):
        gamePlayLabel1 = gui.Label("In single player mode the objective is to stop the plant from having 30 nuts connected to it by vines.",font=china_font_small)
        gamePlayLabel2 = gui.Label("If there are 30 nuts, then the game ends. Two player mode is very similar, but a player wins when",font=china_font_small)
        gamePlayLabel3 = gui.Label("their opponent allows 30 nuts to accumulate.",font=china_font_small)
        spaceLabel = gui.Label("",font=china_font_small)
        gamePlayLabel4 = gui.Label("You knock nuts down by shooting at them with the gun located at the bottom of the screen. Each nut",font=china_font_small)
        gamePlayLabel5 = gui.Label("you knock down earns you credits, with bonuses for large groups of nuts.  The gun can rotate left",font=china_font_small)
        gamePlayLabel6 = gui.Label("to right and the player can attempt to bounce the bullets off the top of side of the stage for an",font=china_font_small)
        gamePlayLabel7 = gui.Label("advantageous angle. The player should use their bullets wisely however as the gun only has a limited",font=china_font_small)
        gamePlayLabel8 = gui.Label("bullet capacity of three bullets initially and it takes some time to reload.",font=china_font_small)
        gamePlayLabel9 = gui.Label("With credits you can buy an assortment of upgrades or items that can help you keep the plant growing.",font=china_font_small)
        gamePlayLabel10 = gui.Label("The barrel cannon costs 15,000 credits.  This upgrade spins around, moving back and forth",font=china_font_small)
        gamePlayLabel11 = gui.Label("autonomously, collecting projectiles from the gun and can shoot out its own projectile(s) ",font=china_font_small)
        gamePlayLabel12 = gui.Label("if loaded. Initially the cannon only shoots out one projectile. The barrel cannon can be",font=china_font_small)
        gamePlayLabel13 = gui.Label("upgraded twice. Each upgrade adds two more projectiles to the cannon\'s shot and also",font=china_font_small)
        gamePlayLabel14 = gui.Label("gives it more power behind the shot.",font=china_font_small)
        gamePlayLabel15 = gui.Label("Spinners cost 25,000 credits, and greatly hinder the opponent",font=china_font_small)
        gamePlayLabel16 = gui.Label("from making a successful by blocking the cannon shots.",font=china_font_small)
        gamePlayLabel17 = gui.Label("The spinner upgrades increase the size of the spinners and can",font=china_font_small)
        gamePlayLabel18 = gui.Label("also be purchased for a total of three times. Spinners are",font=china_font_small)
        gamePlayLabel19 = gui.Label("only available in multiplayer games.",font=china_font_small)
        gamePlayLabel20 = gui.Label("The gun\'s capacity can be upgraded three times, each time increasing the",font=china_font_small)
        gamePlayLabel21 = gui.Label("capacity by one. Each upgrade to the capacity costs 20,000 credits.",font=china_font_small)
        gamePlayLabel22 = gui.Label("The reload rate of the gun can be upgraded three times, each time",font=china_font_small)
        gamePlayLabel23 = gui.Label("reducing the time it takes to reload a bullet. Each upgrade to the",font=china_font_small)
        gamePlayLabel24 = gui.Label("reload rate costs 30,000 credits.",font=china_font_small)
        
        #Image creation
        pyPlay = gui.Image(imageDir+'pyplay.png',width=288,height=314)
        barrelCannon = gui.Image(imageDir+'BCloaded.png')
        spinner = gui.Image(imageDir+'spinner.png')
        
        menuLabel = gui.Label("About The Game",font=china_font_big)
        returnButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        returnButton.connect(gui.CLICK,self.leave)
        color = gui.Color("white",width=800,height=800)
        labelDiff = 20
        initLabelY = 60
        
        c = gui.Container()
        c.add(color,0,0)
        c.add(pyPlay,5,400)
        c.add(gamePlayLabel1,10,initLabelY+labelDiff)
        c.add(gamePlayLabel2,10,initLabelY+labelDiff*2)
        c.add(gamePlayLabel3,10,initLabelY+labelDiff*3)
        c.add(spaceLabel,10,initLabelY+labelDiff*4)
        
        c.add(gamePlayLabel4,10,initLabelY+labelDiff*5)
        c.add(gamePlayLabel5,10,initLabelY+labelDiff*6)
        c.add(gamePlayLabel6,10,initLabelY+labelDiff*7)
        c.add(gamePlayLabel7,10,initLabelY+labelDiff*8)
        c.add(gamePlayLabel8,10,initLabelY+labelDiff*9)
        c.add(spaceLabel,10,initLabelY+labelDiff*10)
        
        c.add(gamePlayLabel9,10,initLabelY+labelDiff*11)
        c.add(spaceLabel,10,initLabelY+labelDiff*12)
        c.add(barrelCannon,15,initLabelY+labelDiff*13)
        c.add(gamePlayLabel10,70,initLabelY+labelDiff*13)
        c.add(gamePlayLabel11,70,initLabelY+labelDiff*14)
        c.add(gamePlayLabel12,70,initLabelY+labelDiff*15)
        c.add(gamePlayLabel13,70,initLabelY+labelDiff*16)
        c.add(gamePlayLabel14,150,initLabelY+labelDiff*17)
        c.add(spaceLabel,10,initLabelY+labelDiff*18)
        
        c.add(spinner,175,initLabelY+labelDiff*19)
        c.add(gamePlayLabel15,250,initLabelY+labelDiff*19)
        c.add(gamePlayLabel16,250,initLabelY+labelDiff*20)
        c.add(gamePlayLabel17,250,initLabelY+labelDiff*21)
        c.add(gamePlayLabel18,250,initLabelY+labelDiff*22)
        c.add(gamePlayLabel19,250,initLabelY+labelDiff*23)
        c.add(spaceLabel,10,initLabelY+labelDiff*24)
        
        c.add(gamePlayLabel20,215,initLabelY+labelDiff*25)
        c.add(gamePlayLabel21,215,initLabelY+labelDiff*26)
        c.add(spaceLabel,10,initLabelY+labelDiff*27)
        
        c.add(gamePlayLabel22,215,initLabelY+labelDiff*28)
        c.add(gamePlayLabel23,215,initLabelY+labelDiff*29)
        c.add(gamePlayLabel24,215,initLabelY+labelDiff*30)
        
        c.add(menuLabel,270,30)
        c.add(returnButton,250,690)
        self.run(c)
    
    def leave(self):
        self.quit()
        self.menu.repaint()
        
class AboutTeamMenu(gui.Desktop):
    
    menu = gui.Desktop()
    
    def __init__(self,mainMenu,**params):
        
        self.menu = mainMenu
    
        gui.Desktop.__init__(self)
        
    def start(self):
        teamInfoLabel1 = gui.Label("Nick Chokas",font=china_font)
        teamInfoLabel2 = gui.Label("Rob Duval",font=china_font)
        teamInfoLabel3 = gui.Label("Zach Olbrys",font=china_font)
        teamInfoLabel4 = gui.Label("Matt Zheng",font=china_font)        
        teamInfoLabel5 = gui.Label("Contact us at CDOZsd@gmail.com",font=china_font)
        
        nickPic = gui.Image(imageDir+'nick.jpg')
        robPic = gui.Image(imageDir+'rob.jpg')
        zachPic = gui.Image(imageDir+'zach.jpg')
        mattPic = gui.Image(imageDir+'matt.jpg')
        
        menuLabel = gui.Label("The Team",font=china_font_big)
        returnButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        returnButton.connect(gui.CLICK,self.leave)
        color = gui.Color("white",width=800,height=800)
        
        c = gui.Container()
        c.add(color,0,0)
        c.add(teamInfoLabel1,145,80)
        c.add(nickPic,35,110)
        c.add(teamInfoLabel2,475,80)
        c.add(robPic,395,110)
        c.add(teamInfoLabel3,145,280)
        c.add(zachPic,75,310)
        c.add(teamInfoLabel4,475,340)
        c.add(mattPic,395,370)
        c.add(menuLabel,290,30)
        c.add(returnButton,250,690)
        self.run(c)
    
    def leave(self):
        self.quit()
        self.menu.repaint()

#    
class ControlMenu(gui.Desktop):
    
    menu = gui.Desktop()
    
    def __init__(self,mainMenu,**params):
        
        self.menu = mainMenu
    
        gui.Desktop.__init__(self)
        
    def start(self):
        controlLabel = gui.Label("Controls",font=china_font)
        
        spaceLabel = gui.Label(" ",font=china_font)
        
        keyboardLabel = gui.Label("Keyboard",font=china_font_bold)
        keyboardAltLabel = gui.Label("Alternate Keyboard",font=china_font_bold)
        controllerLabel = gui.Label("Controller",font=china_font_bold)
        
        ###
        cannonLabel = gui.Label("Main Cannon",font=china_font_bold)
        cannonShootLabel = gui.Label("Shoot",font=china_font)
        moveCannonLLabel = gui.Label("Aim Left",font=china_font)
        moveCannonRLabel = gui.Label("Aim Right",font=china_font)
        #
        cannonShoot = gui.Label("W",font=china_font)
        cannonShootAlt = gui.Label("Up Arrow",font=china_font)
        cannonShootController = gui.Label("A / Button 0",font=china_font)
        
        moveCannonL = gui.Label("A",font=china_font)
        moveCannonLAlt = gui.Label("Left Arrow",font=china_font)
        moveCannonLController = gui.Label("Left",font=china_font)
        
        moveCannonR = gui.Label("D",font=china_font)
        moveCannonRAlt = gui.Label("Right Arrow",font=china_font)
        moveCannonRController = gui.Label("Right",font=china_font)
        
        ###
        upgradeLabel = gui.Label("Upgrade Menu",font=china_font_bold)
        upgradeUpLabel = gui.Label("Up",font=china_font)
        upgradeDownLabel = gui.Label("Down",font=china_font)
        upgradeBuyLabel = gui.Label("Buy",font=china_font)
        #
        upgradeUp = gui.Label("R",font=china_font)
        upgradeUpAlt = gui.Label("Keypad +",font=china_font)
        upgradeUpController = gui.Label("Left Shoulder",font=china_font)
        
        upgradeDown = gui.Label("F",font=china_font)
        upgradeDownAlt = gui.Label("Keypad -",font=china_font)
        upgradeDownController = gui.Label("Right Shoulder",font=china_font)
        
        buyUpgrade = gui.Label("Enter",font=china_font)
        buyUpgradeAlt = gui.Label("Keypad Enter",font=china_font)
        buyUpgradeController = gui.Label("B / Button 1",font=china_font)
        
        ###
        otherLabel = gui.Label("Other Controls",font=china_font_bold)
        moveUpgradeUpLabel = gui.Label("Move Upgrade Up",font=china_font)
        moveUpgradeDownLabel = gui.Label("Move Upgrade Down",font=china_font)
        buildUpgradeLabel = gui.Label("Build Upgrade",font=china_font)
        cancelUpgradeLabel = gui.Label("Cancel Build",font=china_font)
        shootBarrelLabel = gui.Label("Shoot Barrel Cannon",font=china_font)
        quitGameLabel = gui.Label("Exit Game",font=china_font)
        #
        moveUpgradeUp = gui.Label("R",font=china_font)
        moveUpgradeUpAlt = gui.Label("Keypad +",font=china_font)
        moveUpgradeUpController = gui.Label("Left Shoulder",font=china_font)
        
        moveUpgradeDown = gui.Label("F",font=china_font)
        moveUpgradeDownAlt = gui.Label("Keypad -",font=china_font)
        moveUpgradeDownController = gui.Label("Right Shoulder",font=china_font)
        
        buildUpgrade = gui.Label("Enter",font=china_font)
        buildUpgradeAlt = gui.Label("Keypad Enter",font=china_font)
        buildUpgradeController = gui.Label("B / Button 1",font=china_font)
        
        cancelUpgrade = gui.Label("Shift",font=china_font)
        cancelUpgradeAlt = gui.Label("Del",font=china_font)
        cancelUpgradeController = gui.Label("Y / Button 3",font=china_font)
        
        shootBarrel = gui.Label("Space",font=china_font)
        shootBarrelAlt = gui.Label("Keypad 0",font=china_font)
        shootBarrelController = gui.Label("X / Button 2",font=china_font)
        
        quitGame = gui.Label("Esc",font=china_font)
        
        ###
        mainCannonTable = gui.Table()
        mainCannonTable.tr()
        
        #First Row
        mainCannonTable.td(cannonLabel)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(keyboardLabel)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(keyboardAltLabel)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(controllerLabel)
        
        mainCannonTable.tr()
        
        #Second Row
        mainCannonTable.td(cannonShootLabel)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(cannonShoot)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(cannonShootAlt)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(cannonShootController)  
        
        mainCannonTable.tr()
        
        #Third Row
        mainCannonTable.td(moveCannonLLabel)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(moveCannonL)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(moveCannonLAlt)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(moveCannonLController)       
        
        mainCannonTable.tr()
        
        #Fourth Row
        mainCannonTable.td(moveCannonRLabel)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(moveCannonR)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(moveCannonRAlt)
        mainCannonTable.td(spaceLabel)
        mainCannonTable.td(moveCannonRController)

        ###
        upgradeMenuTable = gui.Table()
        upgradeMenuTable.tr()
        
        #First Row
        upgradeMenuTable.td(upgradeLabel)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(keyboardLabel)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(keyboardAltLabel)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(controllerLabel)
        
        upgradeMenuTable.tr()
        
        #Second Row
        upgradeMenuTable.td(upgradeUpLabel)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(upgradeUp)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(upgradeUpAlt)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(upgradeUpController)
        
        upgradeMenuTable.tr()
        
        #Third Row
        upgradeMenuTable.td(upgradeDownLabel)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(upgradeDown)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(upgradeDownAlt)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(upgradeDownController)       
        
        upgradeMenuTable.tr()
        
        #Fourth Row
        upgradeMenuTable.td(upgradeBuyLabel)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(buyUpgrade)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(buyUpgradeAlt)
        upgradeMenuTable.td(spaceLabel)
        upgradeMenuTable.td(buyUpgradeController)
        
        ###
        otherTable = gui.Table()
        otherTable.tr()
        
        #First Row
        otherTable.td(otherLabel)
        otherTable.td(spaceLabel)
        otherTable.td(keyboardLabel)
        otherTable.td(spaceLabel)
        otherTable.td(keyboardAltLabel)
        otherTable.td(spaceLabel)
        otherTable.td(controllerLabel)
        
        otherTable.tr()
        
        #Second Row
        otherTable.td(moveUpgradeUpLabel)
        otherTable.td(spaceLabel)
        otherTable.td(moveUpgradeUp)
        otherTable.td(spaceLabel)
        otherTable.td(moveUpgradeUpAlt)
        otherTable.td(spaceLabel)
        otherTable.td(moveUpgradeUpController)
        
        otherTable.tr()
        
        #Third Row
        otherTable.td(moveUpgradeDownLabel)
        otherTable.td(spaceLabel)
        otherTable.td(moveUpgradeDown)
        otherTable.td(spaceLabel)
        otherTable.td(moveUpgradeDownAlt)
        otherTable.td(spaceLabel)
        otherTable.td(moveUpgradeDownController)       
        
        otherTable.tr()
        
        #Fourth Row
        otherTable.td(buildUpgradeLabel)
        otherTable.td(spaceLabel)
        otherTable.td(buildUpgrade)
        otherTable.td(spaceLabel)
        otherTable.td(buildUpgradeAlt)
        otherTable.td(spaceLabel)
        otherTable.td(buildUpgradeController)
        
        otherTable.tr()
        
        #Fifth Row
        otherTable.td(cancelUpgradeLabel)
        otherTable.td(spaceLabel)
        otherTable.td(cancelUpgrade)
        otherTable.td(spaceLabel)
        otherTable.td(cancelUpgradeAlt)
        otherTable.td(spaceLabel)
        otherTable.td(cancelUpgradeController)
        
        otherTable.tr()
        
        #Sixth Row
        otherTable.td(shootBarrelLabel)
        otherTable.td(spaceLabel)
        otherTable.td(shootBarrel)
        otherTable.td(spaceLabel)
        otherTable.td(shootBarrelAlt)
        otherTable.td(spaceLabel)
        otherTable.td(shootBarrelController)
        
        otherTable.tr()
        
        #Seventh Row
        otherTable.td(quitGameLabel)
        otherTable.td(spaceLabel)
        otherTable.td(quitGame)
        otherTable.td(spaceLabel)
        otherTable.td(gui.Label(" -- ",font=china_font))
        otherTable.td(spaceLabel)
        otherTable.td(gui.Label(" -- ",font=china_font))
        ######
        
        hintLabel = gui.Label("Game Hints",font=china_font)
        
        nut1 = gui.Image(imageDir+'nut1.png')
        nut2 = gui.Image(imageDir+'nut2.png')
        nut3 = gui.Image(imageDir+'nut3.png')
        nut4 = gui.Image(imageDir+'nut4.png')
        nut5 = gui.Image(imageDir+'nut5.png')
        nut6 = gui.Image(imageDir+'nut6.png')
        
        nutTableLabel = gui.Label("Nuts",font=china_font)
        numHitsLabel = gui.Label("Number of Hits Required To Knock Down",font=china_font)
        nut1Label = gui.Label("6",font=china_font)
        nut2Label = gui.Label("5",font=china_font)
        nut3Label = gui.Label("4",font=china_font)
        nut4Label = gui.Label("3",font=china_font)
        nut5Label = gui.Label("2",font=china_font)
        nut6Label = gui.Label("1",font=china_font)
        
        
        nutTable = gui.Table()
        nutTable.tr()
        
        nutTable.td(nutTableLabel)
        nutTable.td(spaceLabel)
        nutTable.td(nut1)
        nutTable.td(spaceLabel)
        nutTable.td(nut2)
        nutTable.td(spaceLabel)
        nutTable.td(nut3)
        nutTable.td(spaceLabel)
        nutTable.td(nut4)
        nutTable.td(spaceLabel)
        nutTable.td(nut5)
        nutTable.td(spaceLabel)
        nutTable.td(nut6)
        
        nutTable.tr()
        
        nutTable.td(numHitsLabel)
        nutTable.td(spaceLabel)
        nutTable.td(nut1Label)
        nutTable.td(spaceLabel)
        nutTable.td(nut2Label)
        nutTable.td(spaceLabel)
        nutTable.td(nut3Label)
        nutTable.td(spaceLabel)
        nutTable.td(nut4Label)
        nutTable.td(spaceLabel)
        nutTable.td(nut5Label)
        nutTable.td(spaceLabel)
        nutTable.td(nut6Label)

        hint1 = gui.Label("Each nut knocked down will earn the player 600 credits. However if a nut is directly attached to a",font=china_font_small)
        hint2 = gui.Label("higher level nut, the player will be awarded with 900 credits. Furthermore if a nut is attached",font=china_font_small)
        hint3 = gui.Label("a nut that is two levels higher, it will award them with 1200 credits.",font=china_font_small)
        hint4 = gui.Label("You can only have one barrel cannon and three spinners maximum!",font=china_font_small)
        menuLabel = gui.Label("How To Play",font=china_font_big)
        returnButton = gui.Button("Return to Main Menu",font=china_font, height=buttonHeight)
        returnButton.connect(gui.CLICK,self.leave)
        color = gui.Color("white",width=800,height=800)
        
        hintY = 570
        hintYInc = 20
        
        c = gui.Container()
        c.add(color,0,0)
        c.add(controlLabel,290,70)
        c.add(mainCannonTable,100,100)
        c.add(upgradeMenuTable,90,190)
        c.add(otherTable,60,300)
        c.add(hintLabel,290,450)
        c.add(nutTable,20,480)
        c.add(hint1,10,hintY)
        c.add(hint2,10,hintY+hintYInc)
        c.add(hint3,10,hintY+hintYInc*2)
        c.add(gui.Label(" ",font=china_font_small),10,hintY+hintYInc*3)
        c.add(hint4,10,hintY+hintYInc*4)
        c.add(menuLabel,270,30)
        c.add(returnButton,250,690)
        self.run(c)
    
    def leave(self):
        self.quit()
        self.menu.repaint()

#Main menu
def main():   
    #This code manages the themes used for the GUI skinning
    buttonHeight = 21
    theme = gui.Theme("asian")
    
    #Container for main menu
    c = gui.Container()
    
    #Creates the main application window
    mainMenu = gui.Desktop(theme=theme)
            
    #Sub menu creation
    profileMenu = ProfileMenu(mainMenu)
    singlePlayerGame = SinglePlayerGame(mainMenu)
    localMultiplayerGame = LocalMultiplayerGame(mainMenu)
    networkMultiHostMenu = NetworkMultiHostMenu(mainMenu)
    networkMultiJoinMenu = NetworkMultiJoinMenu(mainMenu)
    highScoreMenu = HighScoreMenu(mainMenu)
    statsMenu = StatsMenu(mainMenu)
    storyMenu = StoryMenu(mainMenu)
    gamePlayMenu = GamePlayMenu(mainMenu)
    aboutTeamMenu = AboutTeamMenu(mainMenu)
    controlMenu = ControlMenu(mainMenu)

    ##Main menu methods start here
    def openOptionMenu():
        optionsMenu = OptionsMenu()
        optionsMenu.open()
        
    ##Game mode methods and selection menus
    def localMulti(self):
        multiplayerSelectMenu.close()
        localMultiplayerGame.select2Player()
        
    def networkMultiHost(self):
        multiplayerSelectMenu.close()
        networkMultiSelectMenu.close()
        networkMultiHostMenu.start()
        
    def networkMultiJoin(self):
        multiplayerSelectMenu.close()
        networkMultiSelectMenu.close()
        networkMultiJoinMenu.start()
        
    def viewScores(self):
        extrasMenu.close()
        highScoreMenu.start()
        
    def viewStats(self):
        extrasMenu.close()
        statsMenu.start()
        
    def viewStory(self):
        aboutMenu.close()
        storyMenu.start()
        
    def viewGamePlay(self):
        aboutMenu.close()
        gamePlayMenu.start()
        
    def viewControls(self):
        aboutMenu.close()
        controlMenu.start()
        
    def viewAboutTeam(self):
        aboutMenu.close()
        aboutTeamMenu.start()
        
    def playBGMusic():
        pygame.init()
        pygame.mixer.music.load(musicDir+backgroundMusic)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
    
    ## Methods End
    
    ## Sub menu creation here
    #Network Multiplayer Game Type Selection
    c2 = gui.Container(height=100)
    networkMultiSelectMenu = gui.Dialog(gui.Label("Join or Host Network Game",font=china_font),c2)
    hostButton = gui.Button("Host",font=china_font, height=buttonHeight)
    hostButton.connect(gui.CLICK,networkMultiHost,None)
    joinButton = gui.Button("Join",font=china_font, height=buttonHeight)
    joinButton.connect(gui.CLICK,networkMultiJoin,None)
    cancelButton2 = gui.Button("Cancel",font=china_font, height=buttonHeight)
    cancelButton2.connect(gui.CLICK,networkMultiSelectMenu.close,None)
    c2.add(hostButton,6,10)
    c2.add(joinButton,9,40)
    c2.add(cancelButton2,0,70)    
    
    #Multiplayer Game Type Selection
    c1 = gui.Container(height=100)
    multiplayerSelectMenu = gui.Dialog(gui.Label("Select Multiplayer Mode",font=china_font),c1)
    localButton = gui.Button("Local",font=china_font, height=buttonHeight)
    localButton.connect(gui.CLICK,localMulti,None)
    networkButton = gui.Button("Network",font=china_font, height=buttonHeight)
    networkButton.connect(gui.CLICK,networkMultiSelectMenu.open)
    cancelButton = gui.Button("Cancel",font=china_font, height=buttonHeight)
    cancelButton.connect(gui.CLICK,multiplayerSelectMenu.close,None)
    c1.add(localButton,21,10)
    c1.add(networkButton,9,40)
    c1.add(cancelButton,15,70)

    #Extras menu selection
    c3 = gui.Container(height=100)
    extrasMenu = gui.Dialog(gui.Label("Extras Menu",font=china_font),c3)
    highScoreButton = gui.Button("View High Scores",font=china_font, height=buttonHeight)
    highScoreButton.connect(gui.CLICK,viewScores,None)
    statsButton = gui.Button("View Profile Statistics",font=china_font, height=buttonHeight)
    statsButton.connect(gui.CLICK,viewStats,None)
    cancelButton3 = gui.Button("Cancel",font=china_font, height=buttonHeight)
    cancelButton3.connect(gui.CLICK,extrasMenu.close,None)
    c3.add(highScoreButton,23,10)
    c3.add(statsButton,5,40)
    c3.add(cancelButton3,65,70)
    
    #About menu selection
    c4 = gui.Container(height=165)
    aboutMenu = gui.Dialog(gui.Label("About Menu",font=china_font),c4)
    storyButton = gui.Button("Story",font=china_font,height=buttonHeight)
    storyButton.connect(gui.CLICK,viewStory,None)
    gamePlayButton = gui.Button("About The Game",font=china_font,height=buttonHeight)
    gamePlayButton.connect(gui.CLICK,viewGamePlay,None)
    aboutTeamButton = gui.Button("About Development Team",font=china_font,height=buttonHeight)
    aboutTeamButton.connect(gui.CLICK,viewAboutTeam,None)
    controlsButton = gui.Button("How To Play",font=china_font,height=buttonHeight)
    controlsButton.connect(gui.CLICK,viewControls,None)
    cancelButton4 = gui.Button("Cancel",font=china_font,height=buttonHeight)
    cancelButton4.connect(gui.CLICK,aboutMenu.close,None)
    c4.add(storyButton,75,10)
    c4.add(controlsButton,47,40)
    c4.add(gamePlayButton,35,70)
    c4.add(aboutTeamButton,0,100)
    c4.add(cancelButton4,70,130)
    

    ## Sub menu creation end
    
    #Button positioning variables
    buttonWidth = 110
    button_height = 60
    buttonXPos = 555
    buttonYPos = 245
    buttonYPosDiff = 67

    #Button creation/connecting
    buttonProfile = gui.Button("Select another profile",font=china_font, height=buttonHeight)
    buttonProfile.connect(gui.CLICK,profileMenu.open)
    
    buttonSinglePlayer = gui.Button("Single Player",width=buttonWidth,height=button_height,font=china_font)
    buttonSinglePlayer.connect(gui.CLICK,singlePlayerGame.start)
    
    buttonMultiPlayer = gui.Button("Multiplayer",width=buttonWidth,height=button_height,font=china_font)
    buttonMultiPlayer.connect(gui.CLICK,multiplayerSelectMenu.open)
    
    buttonOptions = gui.Button("Options",width=buttonWidth,height=button_height,font=china_font)
    buttonOptions.connect(gui.CLICK,openOptionMenu)
    
    buttonExtras = gui.Button("Extras",width=buttonWidth,height=button_height,font=china_font)
    buttonExtras.connect(gui.CLICK,extrasMenu.open)
    
    buttonQuit = gui.Button("Quit",width=buttonWidth,height=button_height,font=china_font)
    buttonQuit.connect(gui.CLICK,mainMenu.quit,None)
    
    buttonAbout = gui.Button("About",width=buttonWidth,height=button_height,font=china_font)
    buttonAbout.connect(gui.CLICK,aboutMenu.open)
    
    #Image creation
    gamePic = gui.Image(imageDir+'mainMenu.png')
    borderPic = gui.Image(imageDir+'buttonbg.png')

    #Play the background music
    playBGMusic()
    
    #Sets the background color of the container to white
    color = gui.Color("white",width=800,height=800)
    cx.add(color,0,0)
    
    #Creates a container to hold all the widgets in, and then adds all of the widgets
    cx.add(gamePic,0,0)
    cx.add(borderPic,buttonXPos-35,buttonYPos-65)
    cx.add(nameLabel,250,660)
    cx.add(buttonProfile,170,690)
    cx.add(buttonSinglePlayer,buttonXPos,buttonYPos)
    cx.add(buttonMultiPlayer,buttonXPos,buttonYPos+buttonYPosDiff)
    cx.add(buttonOptions,buttonXPos,buttonYPos+2*buttonYPosDiff)
    cx.add(buttonExtras,buttonXPos,buttonYPos+3*buttonYPosDiff)
    cx.add(buttonAbout,buttonXPos,buttonYPos+4*buttonYPosDiff)
    cx.add(buttonQuit,buttonXPos,buttonYPos+5*buttonYPosDiff)
    

    #Allows for profile selection menu to open when the game is started
    mainMenu.connect(gui.INIT,profileMenu.open,None)
    
    #Run the program
    mainMenu.run(cx)
    
if __name__ in '__main__':
    main()