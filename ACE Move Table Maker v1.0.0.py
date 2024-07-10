import os
import sys
import platform
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as stxt
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from subprocess import call, Popen

# ------------------------------------------------------------
# Set Platform Variable
# ------------------------------------------------------------
if(platform.system() == 'Darwin'): # This is a Mac
    OnAMac = True
else:
    OnAMac = False

PyVersion = sys.version_info[1]

# ------------------------------------------------------------
# Define file explorer menu
# ------------------------------------------------------------
def OpenFileDirectory():
    CurrentDirectory = os.getcwd()

    if OnAMac:
        call(["open", CurrentDirectory])
    else:
        Popen('explorer "{}"'.format(CurrentDirectory))

def ConvertToHex(N): # N = decimal integer
    B = hex(N).upper()[2:] # Removes the leading '0x' and makes uppercase

    if N < 16: # Adds a leading zero if it's less than 0x10
        B = "0" + B

    return B

#------------------------------------------------------------
# Global stuff
#------------------------------------------------------------

FileTypes = [("text files", "*.txt")]
Table = []
MoveNameList = []

CurrentOpenFile = ""

HexBytes = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F", \
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1A", "1B", "1C", "1D", "1E", "1F", \
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "2A", "2B", "2C", "2D", "2E", "2F", \
            "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "3A", "3B", "3C", "3D", "3E", "3F", \
            "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "4A", "4B", "4C", "4D", "4E", "4F", \
            "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "5A", "5B", "5C", "5D", "5E", "5F", \
            "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "6A", "6B", "6C", "6D", "6E", "6F", \
            "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "7A", "7B", "7C", "7D", "7E", "7F", \
            "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "8A", "8B", "8C", "8D", "8E", "8F", \
            "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "9A", "9B", "9C", "9D", "9E", "9F", \
            "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "AA", "AB", "AC", "AD", "AE", "AF", \
            "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "BA", "BB", "BC", "BD", "BE", "BF", \
            "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "CA", "CB", "CC", "CD", "CE", "CF", \
            "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "DA", "DB", "DC", "DD", "DE", "DF", \
            "E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "EA", "EB", "EC", "ED", "EE", "EF", \
            "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "FF"]

TextToBytes = {'A': 'BB', 'B': 'BC', 'C': 'BD', 'D': 'BE', 'E': 'BF', 'F': 'C0', 'G': 'C1', 'H': 'C2',
               'I': 'C3', 'J': 'C4', 'K': 'C5', 'L': 'C6', 'M': 'C7', 'N': 'C8', 'O': 'C9', 'P': 'CA',
               'Q': 'CB', 'R': 'CC', 'S': 'CD', 'T': 'CE', 'U': 'CF', 'V': 'D0', 'W': 'D1', 'X': 'D2',
               'Y': 'D3', 'Z': 'D4', 'a': 'D5', 'b': 'D6', 'c': 'D7', 'd': 'D8', 'e': 'D9', 'f': 'DA',
               'g': 'DB', 'h': 'DC', 'i': 'DD', 'j': 'DE', 'k': 'DF', 'l': 'E0', 'm': 'E1', 'n': 'E2',
               'o': 'E3', 'p': 'E4', 'q': 'E5', 'r': 'E6', 's': 'E7', 't': 'E8', 'u': 'E9', 'v': 'EA',
               'w': 'EB', 'x': 'EC', 'y': 'ED', 'z': 'EE', ' ': '00', '!': 'AB', '?': 'AC', '.': 'AD',
               "'": 'B4', ',': 'B8', ':': 'F0', '\n': 'FE', '0': 'A1', '1': 'A2', '2': 'A3', '3': 'A4',
               '4': 'A5', '5': 'A6', '6': 'A7', '7': 'A8', '8': 'A9', '9': 'AA'}

TypeConversion = {"Normal":"00", "Fighting":"01", "Flying":"02",
                  "Poison":"03", "Ground":"04", "Rock":"05",
                  "Bug":"06", "Ghost":"07", "Steel":"08",
                  "Fairy":"09", "Fire":"0A", "Water":"0B",
                  "Grass":"0C", "Electric":"0D", "Psychic":"0E",
                  "Ice":"0F", "Dragon":"10", "Dark":"11"}

RangeConversion = {"User":"10", "Target":"00", "My Side":"40",
                   "Foe Side":"08", "All But User":"20",
                   "Random":"04", "Last Attacker":"01", "Everyone":"30",
                   "Target Or Partner":"02", "User Or Partner":"80"}

KindConversion = {"Physical":"00", "Special":"01", "Status":"02"}

TestMenuBox = {"Heading 1": ["This is the first sentence",
                          "This is the second one",
                          "This is the third",
                          "You get the point by now",
                          "The end"],
            "Heading 2": ["This is another example of some text",
                          "But this one is shorte than the other one."]}

DefaultLists = os.path.join(os.getcwd(), "Default Lists")

# Make the Move Script Dictionary
def MakeDictionary(File):
    D = {}
    
    NewFile = open(os.path.join(DefaultLists, File), "r")
    NewList = NewFile.read().split("\n\n")

    for Entry in NewList:
        Entry = Entry.split("\n")
        Name = Entry[0]
        Text = Entry[1:]

        while len(Text) < 5:
            Text.append("")

        D[Name] = Text

    return D
    
MoveScriptText = MakeDictionary("Move Scripts.txt")
MoveScriptArgText = MakeDictionary("Move Script Arguments.txt")

def DebugMakeTable():
    global Table, CurrentOpenFile

    Table = [["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]]
    CurrentOpenFile = os.path.realpath(os.path.join(os.getcwd(), "Test Table.txt"))
    CurrentLabel.configure(text = "Open File: Test Table.txt")
    EnableEverything()
    Refresh()

#------------------------------------------------------------
# Make GUI
#------------------------------------------------------------

Root = tk.Tk()
Root.title("Move Table Maker v1.0.0")
Root.resizable(False, False)
Root.configure(bg = "Black")

s = ttk.Style()
s.theme_use('alt')

SmallSize = 16

# This is what the widgets look like when not disabled
s.configure("TCombobox", background = "white", foreground = "black")
s.configure("TCheckbutton", background = "black", foreground = "white", indicatorcolor = "white", font = ('Menlo', SmallSize - 2))
s.configure("TLabel", background = "black", foreground = "white", font = ('Courier', SmallSize, 'bold'))
s.configure("TButton", background = "black", foreground = "white", font = ('Arial', SmallSize))

# This is what the widgets look like when disabled or hovered over (active)
s.map("TCombobox", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")])
s.map("TCheckbutton", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")], indicatorcolor = [("selected", "blue")])
s.map("TButton", background = [("active", "white"), ("disabled", "black")], foreground = [("active", "black"), ("disabled", "grey")])

# -------------------------------------------------------
# Make Frames
# -------------------------------------------------------

IconFrame = tk.Frame(Root, bg = "Black")
IconFrame.pack(fill = tk.X, padx = 10, pady = 10)

ButtonFrame = tk.Frame(Root, bg = "Black")
ButtonFrame.pack(fill = tk.X, padx = 10, pady = 10)

EditorFrame = tk.Frame(Root, bg = "Black")
EditorFrame.pack(side = tk.LEFT, padx = 10, pady = 10)

#------------------------------------------------------------
# Set Index and Tkinter Variables
#------------------------------------------------------------

MoveNameIndex = 0
MoveScriptIndex = 1
BasePowerIndex = 2
TypeIndex = 3
AccuracyIndex = 4
PowerPointIndex = 5
EffectChanceIndex = 6
RangeIndex = 7
PriorityIndex = 8
MoveFlagIndex = 9
DamageFormulaIndex = 10
MoveKindIndex = 11
ScriptArgIndex = 12
DescriptionIndex = 13

MoveName = StringVar()
MoveScript = StringVar()
BasePower = IntVar()
Type = StringVar()
Accuracy = IntVar()
PowerPoints = IntVar()
EffectChance = IntVar()
Range = StringVar()
Priority = IntVar()

Parity = IntVar()
Parity.set(0)

A = IntVar()    # Ability Bypass
B = IntVar()    # Self Effect
C = IntVar()    # King's Rock
D = IntVar()    # Mirror Move
E = IntVar()    # Snatch
F = IntVar()    # Magic Coat
G = IntVar()    # Protect
H = IntVar()    # Direct Contact 

DamageFormula = StringVar()
MoveKind = StringVar()
ScriptArgument = IntVar()
Description = StringVar()

CurrentMoveNumber = IntVar()
CurrentMoveNumber.set(0)

CurrentMove = StringVar()

MoveTemplate = {"Move Script": "0", "Base Power": 0, "Type": "Normal", \
                "Accuracy": 0, "Power Points": 0, "Effect Chance": 0, \
                "Range": "Target", "Priority": 0, \
                "Move Flags": {"Bypass Ability": 0, \
                               "Self Effect": 0, \
                               "King's Rock": 0, \
                               "Mirror Move": 0, \
                               "Snatch Flag": 0, \
                               "Protect Flag": 0, \
                               "Direct Contact": 0}, \
                "Damage Formula": "0", \
                "Kind": "Status", \
                "Script Argument": 0}

#------------------------------------------------------------
# Make Box Functions
#------------------------------------------------------------

def MakeInfoBox(Title, Header, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = tk.X, pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = tk.X, pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = tk.X, pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = W)

    def QuitBox():
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = QuitBox)
    OkayButton.pack()

    Top.wait_window()

def MakeYesNoBox(Title, Header, Var, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = tk.X, pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = tk.X, pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = tk.X, pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Arial", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Arial", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = W)

    def SetYes():
        Var.set(True)
        Top.destroy()

    def SetNo():
        Var.set(False)
        Top.destroy()

    YesButton = ttk.Button(OkayFrame, text = "Yes", command = SetYes)
    YesButton.pack()

    NoButton = ttk.Button(OkayFrame, text = "No", command = SetNo)
    NoButton.pack()

    Top.wait_window()

# The Type argument is the data type that the input needs to be
# The function will convert the input to the same type as the Type variable
# If the input cannot be converted, it will delete it and you must try again
# If you want only integers, put 1 (or another integer) as Type
# If you don't care, use "1" so convert it to a string
def MakeEntryBox(Title, Header, Var, Type, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = tk.X, pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = tk.X, pady = 10)

    PromptFrame = tk.Frame(Top, bg = "Black")
    PromptFrame.pack(fill = tk.X, pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = tk.X, pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Arial", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Arial", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = W)
    
    def ProcessEntry(Text):
        try:
            N = type(Type)(Text)
            OkayButton.configure(state = "normal")
            
        except:
            PromptEntry.delete(1.0, "end-1c")
            PromptEntry.insert(1.0, Text[:-1])           
    
    PromptEntry = tk.Text(PromptFrame, width = 20, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    PromptEntry.bind("<KeyRelease>", (lambda event: ProcessEntry(PromptEntry.get(1.0, "end-1c"))))
    PromptEntry.pack()

    def SetValue():
        PromptNumber = PromptEntry.get(1.0, "end-1c")
        Var.set(PromptNumber)
        Top.destroy()

    def Cancel():
        Var.set(None)
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = SetValue)
    OkayButton.configure(state = "disabled")
    OkayButton.pack()

    CancelButton = ttk.Button(OkayFrame, text = "Cancel", command = Cancel)
    CancelButton.pack()

    Top.wait_window()

# Make an entry box but this takes an address
def MakeAddressEntryBox(Title, Header, Var, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = tk.X, pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = tk.X, pady = 10)

    PromptFrame = tk.Frame(Top, bg = "Black")
    PromptFrame.pack(fill = tk.X, pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = tk.X, pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Arial", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Arial", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = W)

    def ProcessEntry(Text):
        Text = Text.upper()
        Hex = "1234567890ABCDEF"

        if Text[-1] not in Hex or len(Text) > 8:
            Text = Text[:-1]
            PromptEntry.delete(1.0, "end-1c")
            PromptEntry.insert(1.0, Text)
            
        else:
            PromptEntry.delete(1.0, "end-1c")
            PromptEntry.insert(1.0, Text)

        if len(Text) != 8:
            OkayButton.configure(state = "disabled")
        else:
            OkayButton.configure(state = "normal")
    
    PromptEntry = tk.Text(PromptFrame, width = 20, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    PromptEntry.bind("<KeyRelease>", (lambda event: ProcessEntry(PromptEntry.get(1.0, "end-1c"))))
    PromptEntry.pack()

    PromptEntry.delete(1.0, "end-1c")
    PromptEntry.insert(1.0, "08")

    def SetValue():
        PromptNumber = PromptEntry.get(1.0, "end-1c")
        Var.set(PromptNumber)
        Top.destroy()

    def Cancel():
        Var.set(None)
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = SetValue)
    OkayButton.configure(state = "disabled")
    OkayButton.pack()

    CancelButton = ttk.Button(OkayFrame, text = "Cancel", command = Cancel)
    CancelButton.pack()

    Top.wait_window()

# Text is a list with each entry being a line of text
# MenuText is a dictionary with keys being the combobox options
# and the paired values being a list of text to display
# Maximum of up to five lines
def MakeInfoBoxWithMenu(Title, Header, Text, MenuText):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = tk.X, pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = tk.X, pady = 10)

    MenuTextFrame = tk.Frame(Top, bg = "Black")
    MenuTextFrame.pack(fill = tk.X, pady = 10)

    MenuFrame = tk.Frame(Top, bg = "Black")
    MenuFrame.pack(fill = tk.X, pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = tk.X, pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = W)

    DoLine = ttk.Label(MenuTextFrame, text = "-----", font = ("Courier", SmallSize))
    
    Line1Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))
    Line2Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))
    Line3Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))
    Line4Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))
    Line5Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))

    DoLine.pack(side = tk.TOP)
    Line1Label.pack(side = tk.TOP)
    Line2Label.pack(side = tk.TOP)
    Line3Label.pack(side = tk.TOP)
    Line4Label.pack(side = tk.TOP)
    Line5Label.pack(side = tk.TOP)

    Values = []
    for Key in MenuText:
        Values.append(Key)

    Option = StringVar()
    Option.set("-")
    
    def ChangeText(self):
        List = MenuText[Option.get()]

        while len(List) < 5:
            List.append("")

        Line1Label.configure(text = List[0])
        Line2Label.configure(text = List[1])
        Line3Label.configure(text = List[2])
        Line4Label.configure(text = List[3])
        Line5Label.configure(text = List[4])        

    MenuDropDown = ttk.Combobox(MenuFrame, textvariable = Option, width = 20, values = Values, font = ("Courier", SmallSize))      
    MenuDropDown.bind("<<ComboboxSelected>>", ChangeText)
    MenuDropDown.pack()

    def QuitBox():
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Done", command = QuitBox)
    OkayButton.pack()

    Top.wait_window()

# This makes a menu with a dropdown but this one saves to a variable
def MakeMultiChoiceBox(Title, Header, Var, Text, MenuText):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = tk.X, pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = tk.X, pady = 10)

    MenuTextFrame = tk.Frame(Top, bg = "Black")
    MenuTextFrame.pack(fill = tk.X, pady = 10)

    MenuFrame = tk.Frame(Top, bg = "Black")
    MenuFrame.pack(fill = tk.X, pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = tk.X, pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = W)

    DoLine = ttk.Label(MenuTextFrame, text = "-----", font = ("Courier", SmallSize))
    
    Line1Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))
    Line2Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))
    Line3Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))
    Line4Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))
    Line5Label = ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize))

    DoLine.pack(side = tk.TOP)
    Line1Label.pack(side = tk.TOP)
    Line2Label.pack(side = tk.TOP)
    Line3Label.pack(side = tk.TOP)
    Line4Label.pack(side = tk.TOP)
    Line5Label.pack(side = tk.TOP)

    Values = []
    for Key in MenuText:
        Values.append(Key)

    Option = StringVar()
    Option.set("-")
    
    def ChangeText(self):
        List = MenuText[Option.get()]

        while len(List) < 5:
            List.append("")

        Line1Label.configure(text = List[0])
        Line2Label.configure(text = List[1])
        Line3Label.configure(text = List[2])
        Line4Label.configure(text = List[3])
        Line5Label.configure(text = List[4])

        Var.set(Option.get())

    MenuDropDown = ttk.Combobox(MenuFrame, textvariable = Option, width = 20, values = Values, font = ("Courier", SmallSize))      
    MenuDropDown.bind("<<ComboboxSelected>>", ChangeText)
    MenuDropDown.pack()

    def QuitBox():
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = QuitBox)
    OkayButton.pack()

    Top.wait_window()

#------------------------------------------------------------
# Top of the screen stuff
#------------------------------------------------------------

LabelFrame = tk.Frame(IconFrame, bg = "Black")
MenuFrame = tk.Frame(IconFrame, bg = "Black")

MainLabel = ttk.Label(LabelFrame, text = "ACE Move Table Maker", font = ("Arial", int(1.5 * SmallSize), "bold"))

CurrentLabel = ttk.Label(MenuFrame, text = "{}".format(CurrentOpenFile))

CopyrightLabel = ttk.Label(LabelFrame, text = "Program by AkameTheBulbasaur, v1.0.0", font = ("Arial", SmallSize - 2))

# Make Help Menu
def ShowHelpMenu():
    MakeInfoBox("Help", "Shortcuts",
                ["Cmd/Ctrl N: Make new table file",
                 "Cmd/Ctrl O: Open saved table file",
                 "Cmd/Ctrl S: Save current table file",
                 "Cmd/Ctrl E: Save current table as new file",
                 "Cmd/Ctrl 0: Show next Move in table",
                 "Cmd/Ctrl 9: Show previous Move in table",
                 "Cmd/Ctrl H: Open shortcut menu",
                 "Cmd/Ctrl Q: Quit program"])

ShowHelp = IntVar()
ShowHelp.set(0)

def DisplayHelp():
    ShowHelp.set(0)
    ShowHelpMenu()

ShowHelpButton = ttk.Checkbutton(MenuFrame, text = "?", variable = ShowHelp, command = DisplayHelp)

# Jump to Move
def JumpToMove(self):
    # Gets the Move Number
    MoveNumber = int(CurrentMove.get().split("-")[0].strip()) - 1

    CurrentMoveNumber.set(MoveNumber)
    Refresh()

MoveFinder = ttk.Combobox(MenuFrame, textvariable = CurrentMove, width = 18, values = MoveNameList, font = ("Courier", SmallSize))
MoveFinder.bind("<<ComboboxSelected>>", JumpToMove)

LabelFrame.pack(pady = 10)
MainLabel.pack()
CopyrightLabel.pack()

MenuFrame.pack()
CurrentLabel.pack(side = tk.LEFT, padx = 20)
ShowHelpButton.pack(side = tk.LEFT, padx = (20,0))
MoveFinder.pack(side = tk.LEFT, padx = (0,20))

#------------------------------------------------------------
# Edit Move Name
#------------------------------------------------------------

MoveNameFrame = tk.Frame(EditorFrame, bg = "Black")

def EditName(Name):
    if MoveNameEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        Name = Name[0:12]
        Table[i][MoveNameIndex] = Name
        
        Refresh()

MoveNameLabel = ttk.Label(MoveNameFrame, text = "Move Name:")
MoveNameEntry = tk.Text(MoveNameFrame, width = 12, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
MoveNameEntry.bind("<KeyRelease>", (lambda event: EditName(MoveNameEntry.get(1.0, "end-1c"))))

NameHelp = IntVar()
NameHelp.set(0)

def MoveNameHelp():
    NameHelp.set(0)
    MakeInfoBox("Help", "Move Name", \
                ["This is the name of the Move.",
                 "This does not appear in the compiled Attack Data Table.",
                 "Instead, Move Names are compiled to a separate Move Name Table."])

MoveNameHelpButton = ttk.Checkbutton(MoveNameFrame, text = "?", variable = NameHelp, command = MoveNameHelp)

MoveNameFrame.grid(row = 0, column = 0, padx = 15, pady = 5, sticky = W)
MoveNameHelpButton.pack(side = tk.LEFT)
MoveNameLabel.pack(side = tk.LEFT, padx = (0,5))
MoveNameEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Move Script
#------------------------------------------------------------

MoveScriptFrame = tk.Frame(EditorFrame, bg = "Black")

def EditMoveScript(self):
    global Table
    i = CurrentMoveNumber.get()

    Table[i][MoveScriptIndex] = MoveScript.get()

    Refresh()

MoveScriptLabel = ttk.Label(MoveScriptFrame, text = "Move Script:")
MoveScriptEntry = ttk.Combobox(MoveScriptFrame, textvariable = MoveScript, width = 2, values = HexBytes, font = ("Courier", SmallSize))
MoveScriptEntry.bind("<<ComboboxSelected>>", EditMoveScript)

ScriptHelp = IntVar()
ScriptHelp.set(0)

def MoveScriptHelp():
    ScriptHelp.set(0)

    MakeInfoBoxWithMenu("Help", "Move Scripts",
                        ["The Move Script is a Battle Script that is specifically",
                         "executed by a Move when it is selected in battle.",
                         "Select a script from the dropdown menu to see what it does.",
                         "Note: these are the defaults for ACE, your scripts may vary."],
                        MoveScriptText)

MoveScriptHelpButton = ttk.Checkbutton(MoveScriptFrame, text = "?", variable = ScriptHelp, command = MoveScriptHelp)

MoveScriptFrame.grid(row = 0, column = 1, padx = 15, pady = 5, sticky = W)
MoveScriptHelpButton.pack(side = tk.LEFT)
MoveScriptLabel.pack(side = tk.LEFT, padx = (0,5))
MoveScriptEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Base Power
#------------------------------------------------------------

BasePowerFrame = tk.Frame(EditorFrame, bg = "Black")

def EditBasePower(Power):
    if BasePowerEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            Power = int(Power)
        except:
            Power = 0

        if Power > 255:
            Power = 255

        if Power < 0:
            Power = 0

        Table[i][BasePowerIndex] = Power
        
        Refresh()

BasePowerLabel = ttk.Label(BasePowerFrame, text = "Base Power:")
BasePowerEntry = tk.Text(BasePowerFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
BasePowerEntry.bind("<KeyRelease>", (lambda event: EditBasePower(BasePowerEntry.get(1.0, "end-1c"))))

PowerHelp = IntVar()
PowerHelp.set(0)

def BasePowerHelp():
    PowerHelp.set(0)
    MakeInfoBox("Help", "Base Power",
                ["The Base Power of a Move generally indicates its strength.",
                 "This value can range from 0 to 255.",
                 "Setting this value to zero means the Move is Non-Damaging."])

BasePowerHelpButton = ttk.Checkbutton(BasePowerFrame, text = "?", variable = PowerHelp, command = BasePowerHelp)

BasePowerFrame.grid(row = 0, column = 2, padx = 15, pady = 5, sticky = W)
BasePowerHelpButton.pack(side = tk.LEFT)
BasePowerLabel.pack(side = tk.LEFT, padx = (0,5))
BasePowerEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Move Type
#------------------------------------------------------------

Types = ["Normal", "Flying", "Fighting", "Poison", "Ground", "Rock", \
         "Bug", "Ghost", "Steel", "Fairy", "Fire", "Water", "Grass", \
         "Electric", "Psychic", "Ice", "Dragon", "Dark"]

TypeFrame = tk.Frame(EditorFrame, bg = "Black")

def EditType(self):
    global Table
    i = CurrentMoveNumber.get()

    Table[i][TypeIndex] = Type.get()

    Refresh()
    
TypeLabel = ttk.Label(TypeFrame, text = "Type:")
TypeEntry = ttk.Combobox(TypeFrame, textvariable = Type, width = 8, values = Types, font = ("Courier", SmallSize))
TypeEntry.bind("<<ComboboxSelected>>", EditType)

TypeHelp = IntVar()
TypeHelp.set(0)

def MoveTypeHelp():
    TypeHelp.set(0)
    MakeInfoBox("Help", "Move Type",
                ["This is the base Type of the Move."
                 "The actual Type when used in Battle may be different,"
                 "but will, by default, be the one given here."])

TypeHelpButton = ttk.Checkbutton(TypeFrame, text = "?", variable = TypeHelp, command = MoveTypeHelp)

TypeFrame.grid(row = 1, column = 0, padx = 15, pady = 5, sticky = W)
TypeHelpButton.pack(side = tk.LEFT)
TypeLabel.pack(side = tk.LEFT, padx = (0,5))
TypeEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Accuracy
#------------------------------------------------------------

AccuracyFrame = tk.Frame(EditorFrame, bg = "Black")

def EditAccuracy(Accuracy):
    if AccuracyEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            Accuracy = int(Accuracy)
        except:
            Accuracy = 0

        if Accuracy > 100:
            Accuracy = 100

        if Accuracy < 0:
            Accuracy = 0

        Table[i][AccuracyIndex] = Accuracy
        
        Refresh()
    
AccuracyLabel = ttk.Label(AccuracyFrame, text = "Accuracy:")
AccuracyEntry = tk.Text(AccuracyFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
AccuracyEntry.bind("<KeyRelease>", (lambda event: EditAccuracy(AccuracyEntry.get(1.0, "end-1c"))))

AccHelp = IntVar()
AccHelp.set(0)

def AccuracyHelp():
    AccHelp.set(0)
    MakeInfoBox("Help", "Accuracy",
                ["This is the base Accuracy of the Move.",
                 "This value can range from 0 to 100.",
                 "A higher Accuracy means the Move will hit more often.",
                 "An Accuracy of 0 means the Move bypasses Accuracy checks."])

AccuracyHelpButton = ttk.Checkbutton(AccuracyFrame, text = "?", variable = AccHelp, command = AccuracyHelp)

AccuracyFrame.grid(row = 1, column = 1, padx = 15, pady = 5, sticky = W)
AccuracyHelpButton.pack(side = tk.LEFT)
AccuracyLabel.pack(side = tk.LEFT, padx = (0,5))
AccuracyEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Power Points
#------------------------------------------------------------

PowerPointFrame = tk.Frame(EditorFrame, bg = "Black")

def EditPowerPoints(PowerPoints):
    if PowerPointEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            PowerPoints = int(PowerPoints)
        except:
            PowerPoints = 0

        if PowerPoints > 99:
            PowerPoints = 99

        if PowerPoints < 0:
            PowerPoints = 0

        Table[i][PowerPointIndex] = PowerPoints
        
        Refresh()
    
PowerPointLabel = ttk.Label(PowerPointFrame, text = "Power Points:")
PowerPointEntry = tk.Text(PowerPointFrame, width = 2, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
PowerPointEntry.bind("<KeyRelease>", (lambda event: EditPowerPoints(PowerPointEntry.get(1.0, "end-1c"))))

PPHelp = IntVar()
PPHelp.set(0)

def PowerPointHelp():
    PPHelp.set(0)
    MakeInfoBox("Help", "Power Points",
                ["This is the default amount of Power Points that the Move can have.",
                 "This value can range from 0 to 99.",
                 "More Power Points means the Move can be used more.",
                 "This does not include the amount added by using Items such as PPUp or PPMax."])

PowerPointHelpButton = ttk.Checkbutton(PowerPointFrame, text = "?", variable = PPHelp, command = PowerPointHelp)

PowerPointFrame.grid(row = 1, column = 2, padx = 15, pady = 5, sticky = W)
PowerPointHelpButton.pack(side = tk.LEFT)
PowerPointLabel.pack(side = tk.LEFT, padx = (0,5))
PowerPointEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Effect Chance
#------------------------------------------------------------

EffectChanceFrame = tk.Frame(EditorFrame, bg = "Black")

def EditEffectChance(Chance):
    if EffectChanceEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            Chance = int(Chance)
        except:
            Chance = 0

        if Chance > 100:
            Chance = 100

        if Chance < 0:
            Chance = 0

        Table[i][EffectChanceIndex] = Chance
        
        Refresh()
    
EffectChanceLabel = ttk.Label(EffectChanceFrame, text = "Effect Chance:")
EffectChanceEntry = tk.Text(EffectChanceFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
EffectChanceEntry.bind("<KeyRelease>", (lambda event: EditEffectChance(EffectChanceEntry.get(1.0, "end-1c"))))

ChanceHelp = IntVar()
ChanceHelp.set(0)

def EffectChanceHelp():
    ChanceHelp.set(0)
    MakeInfoBox("Help", "Effect Chance",
                ["This is the chance of the Move Script's effect activating (if it has one).",
                 "This values ranges from 0 to 100.",
                 "A higher value means the effect will occur more often.",
                 "Setting this to zero makes the effect always activate."])

EffectChanceHelpButton = ttk.Checkbutton(EffectChanceFrame, text = "?", variable = ChanceHelp, command = EffectChanceHelp)

EffectChanceFrame.grid(row = 2, column = 0, padx = 15, pady = 5, sticky = W)
EffectChanceHelpButton.pack(side = tk.LEFT)
EffectChanceLabel.pack(side = tk.LEFT, padx = (0,5))
EffectChanceEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Attack Range
#------------------------------------------------------------

RangeList = ["Target", "User", "Foe Side", "My Side", "All But User", "Everyone", "Random", "Last Attacker", "User Or Partner", "Target Or Partner"]

RangeFrame = tk.Frame(EditorFrame, bg = "Black")

def EditRange(self):
    global Table
    i = CurrentMoveNumber.get()

    Table[i][RangeIndex] = Range.get()

    Refresh()
    
RangeLabel = ttk.Label(RangeFrame, text = "Range:")
RangeEntry = ttk.Combobox(RangeFrame, textvariable = Range, width = 13, values = RangeList, font = ("Courier", SmallSize))
RangeEntry.bind("<<ComboboxSelected>>", EditRange)

RHelp = IntVar()
RHelp.set(0)

def RangeHelp():
    RHelp.set(0)
    MakeInfoBox("Help", "Range",
                ["This is the range of Pokemon who can be targeted by the Move.",
                 "This only has an effect in a Double Battle.",
                 "If the Move targets one Pokemon, the Move Script runs once.",
                 "If the Move targets multiple, the Move Script runs once per Pokemon.",
                 "Global Effect Moves (i.e. Sandstorm) should target the User."
                 "\n",
                 "Target = Single target, can select any Pokemon besides themselves.",
                 "User = Single target, can only select themselves.",
                 "My Side = Both the user and their partner are selected.",
                 "Foe Side = Both the opposing Pokemon are selected.",
                 "All But User = All Pokemon except the user are selected.",
                 "Everyone = All Pokemon including the user are selected.",
                 "User or Partner = Single target, can select themselves or their partner.",
                 "Target or Partner = Single target, can select either opponent but not both.",
                 "Last Attacker = Single target, selects last Pokemon to attack the user.",
                 "Random = Single target, randomly picks a Pokemon besides the user."])

RangeHelpButton = ttk.Checkbutton(RangeFrame, text = "?", variable = RHelp, command = RangeHelp)

RangeFrame.grid(row = 2, column = 1, padx = 15, pady = 5, sticky = W)
RangeHelpButton.pack(side = tk.LEFT)
RangeLabel.pack(side = tk.LEFT, padx = (0,5))
RangeEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Priority
#------------------------------------------------------------

PriorityFrame = tk.Frame(EditorFrame, bg = "Black")

def EditPriority(Priority):
    if PriorityEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            Priority = int(Priority)
        except:
            Priority = 0

        if Priority > 127:
            Priority = 127

        if Priority < 0:
            Priority = 0

        if Parity.get() == 1: # Negative Priority
            Priority = -Priority

        Table[i][PriorityIndex] = Priority
        
        Refresh()
    
PriorityLabel = ttk.Label(PriorityFrame, text = "Priority:")
PriorityEntry = tk.Text(PriorityFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
PriorityEntry.bind("<KeyRelease>", (lambda event: EditPriority(PriorityEntry.get(1.0, "end-1c"))))

PriHelp = IntVar()
PriHelp.set(0)

def PriorityHelp():
    PriHelp.set(0)
    MakeInfoBox("Help", "Priority",
                ["Moves with higher Priority will go before those which have a lower Priority.",
                 "This values ranges from -127 to 127.",
                 "The default is zero, with higher values moving first and negative values moving later."])

PriorityHelpButton = ttk.Checkbutton(PriorityFrame, text = "?", variable = PriHelp, command = PriorityHelp)

X = IntVar()
X.set(0)

def EditParity():
    global Table
    i = CurrentMoveNumber.get()
    X.set(0)

    if Parity.get() == 0: # +
        ParityButton.configure(text = "-")
        Parity.set(1)
        Table[i][PriorityIndex] = -Table[i][PriorityIndex]
        
    else:
        ParityButton.configure(text = "+")
        Parity.set(0)
        Table[i][PriorityIndex] = -Table[i][PriorityIndex]

    Refresh()

ParityButton = ttk.Checkbutton(PriorityFrame, text = "+", variable = X, command = EditParity)

PriorityFrame.grid(row = 2, column = 2, padx = 15, pady = 5, sticky = W)
PriorityHelpButton.pack(side = tk.LEFT)
PriorityLabel.pack(side = tk.LEFT, padx = (0,5))
ParityButton.pack(side = tk.LEFT)
PriorityEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Move Flags
#------------------------------------------------------------

MoveFlagLabelFrame = tk.Frame(EditorFrame, bg = "Black")
MoveFlagFrame = tk.Frame(EditorFrame, bg = "Black")

MoveFlagLabel = ttk.Label(MoveFlagLabelFrame, text = "Move Flags")

def SetMoveFlag(CheckVar, X):
    global Table
    i = CurrentMoveNumber.get()

    Table[i][MoveFlagIndex][X] = CheckVar.get()

    Refresh()

SetAbilityFlag = ttk.Checkbutton(MoveFlagFrame, text = "Bypass Ability", variable = A, command = lambda: SetMoveFlag(A, 0))
SetSelfFlag = ttk.Checkbutton(MoveFlagFrame, text = "Self Effect", variable = B, command = lambda: SetMoveFlag(B, 1))
SetKingsRockFlag = ttk.Checkbutton(MoveFlagFrame, text = "King's Rock", variable = C, command = lambda: SetMoveFlag(C, 2))
SetMirrorMoveFlag = ttk.Checkbutton(MoveFlagFrame, text = "Mirror Move", variable = D, command = lambda: SetMoveFlag(D, 3))
SetSnatchFlag = ttk.Checkbutton(MoveFlagFrame, text = "Snatch", variable = E, command = lambda: SetMoveFlag(E, 4))
SetMagicCoatFlag = ttk.Checkbutton(MoveFlagFrame, text = "Magic Coat", variable = F, command = lambda: SetMoveFlag(F, 5))
SetProtectFlag = ttk.Checkbutton(MoveFlagFrame, text = "Protect", variable = G, command = lambda: SetMoveFlag(G, 6))
SetDirectContactFlag = ttk.Checkbutton(MoveFlagFrame, text = "Direct Contact", variable = H, command = lambda: SetMoveFlag(H, 7))

FlagHelp = IntVar()
FlagHelp.set(0)

def MoveFlagHelp():
    FlagHelp.set(0)
    MakeInfoBox("Help", "Move Flags",
                ["When these are set, the Move has different effects.",
                 "Bypass Ability: The Move will ignore Ignorable Abilities",
                 "Self Effect: The additional effects will always apply to the user",
                 "King's Rock: The Move will be affected by the King's Rock Item",
                 "Mirror Move: The Move can be copied by Mirror Move",
                 "Snatch: The Move can be stolen by Snatch",
                 "Magic Coat: The Move can be reflected by Magic Coat",
                 "Protect: The Move will be blocked by Protect",
                 "Direct Contact: The Move will make Direct Contact"])

MoveFlagHelpButton = ttk.Checkbutton(MoveFlagLabelFrame, text = "?", variable = FlagHelp, command = MoveFlagHelp)

MoveFlagLabelFrame.grid(row = 4, column = 0, padx = 15, pady = (5,0), sticky = W)
MoveFlagHelpButton.pack(side = tk.LEFT)
MoveFlagLabel.pack(side = tk.LEFT)

MoveFlagFrame.grid(row = 5, column = 0, padx = 15, pady = 5, sticky = W)
SetAbilityFlag.grid(row = 0, column = 0, sticky = W)
SetSelfFlag.grid(row = 0, column = 1, sticky = W)
SetKingsRockFlag.grid(row = 1, column = 0, sticky = W)
SetMirrorMoveFlag.grid(row = 1, column = 1, sticky = W)
SetSnatchFlag.grid(row = 2, column = 0, sticky = W)
SetMagicCoatFlag.grid(row = 2, column = 1, sticky = W)
SetProtectFlag.grid(row = 3, column = 0, sticky = W)
SetDirectContactFlag.grid(row = 3, column = 1, sticky = W)

#------------------------------------------------------------
# Edit Damage Formula
#------------------------------------------------------------

DamageFormulaFrame = tk.Frame(EditorFrame, bg = "Black")

def EditDamageFormula(self):
    global Table
    i = CurrentMoveNumber.get()

    Table[i][DamageFormulaIndex] = DamageFormula.get()

    Refresh()
    
DamageFormulaLabel = ttk.Label(DamageFormulaFrame, text = "Damage Formula:")
DamageFormulaEntry = ttk.Combobox(DamageFormulaFrame, textvariable = DamageFormula, width = 2, values = HexBytes, font = ("Courier", SmallSize))
DamageFormulaEntry.bind("<<ComboboxSelected>>", EditDamageFormula)

FormulaHelp = IntVar()
FormulaHelp.set(0)

def DamageFormulaHelp():
    FormulaHelp.set(0)

    MakeInfoBoxWithMenu("Help", "Damage Formula",
                        ["The damage formula is used to determine the Base Power",
                         "the of the Move.",
                         "If this is set to anything other than zero, then the",
                         "game will run an additional routine to find the true",
                         "Base Power, which may use the Base Power given here."],
                        {"Test":["Test Test Test"]})

DamageFormulaHelpButton = ttk.Checkbutton(DamageFormulaFrame, text = "?", variable = FormulaHelp, command = DamageFormulaHelp)

DamageFormulaFrame.grid(row = 3, column = 0, padx = 15, pady = 5, sticky = W)
DamageFormulaHelpButton.pack(side = tk.LEFT)
DamageFormulaLabel.pack(side = tk.LEFT, padx = (0,5))
DamageFormulaEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Move Kind
#------------------------------------------------------------

MoveKindFrame = tk.Frame(EditorFrame, bg = "Black")

Kinds = ["Physical", "Special", "Status"]

def EditMoveKind(self):
    global Table
    i = CurrentMoveNumber.get()

    Table[i][MoveKindIndex] = MoveKind.get()

    Refresh()
    
MoveKindLabel = ttk.Label(MoveKindFrame, text = "Move Kind:")
MoveKindEntry = ttk.Combobox(MoveKindFrame, textvariable = MoveKind, width = 10, values = Kinds, font = ("Courier", SmallSize))
MoveKindEntry.bind("<<ComboboxSelected>>", EditMoveKind)

KindHelp = IntVar()
KindHelp.set(0)

def MoveKindHelp():
    KindHelp.set(0)
    MakeInfoBox("Help", "Move Kind",
                ["The Move Kind determines whether the Move is Physical, Special or Status.",
                 "Physical: Uses Attack/Defence when calculating Damage",
                 "Special: Uses Sp. Attack/Sp. Defence when calculating Damage",
                 "Status: Does not deal direct damage."])

MoveKindHelpButton = ttk.Checkbutton(MoveKindFrame, text = "?", variable = KindHelp, command = MoveKindHelp)

MoveKindFrame.grid(row = 3, column = 1, padx = 15, pady = 5, sticky = W)
MoveKindHelpButton.pack(side = tk.LEFT)
MoveKindLabel.pack(side = tk.LEFT, padx = (0,5))
MoveKindEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Edit Script Argument
#------------------------------------------------------------

ScriptArgFrame = tk.Frame(EditorFrame, bg = "Black")

def EditScriptArg(Argument):
    if ScriptArgEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()

        try:
            Argument = int(Argument)
        except:
            Argument = 0

        if Argument > 255:
            Argument = 255

        if Argument < 0:
            Argument = 0

        Table[i][ScriptArgIndex] = Argument

        Refresh()
    
ScriptArgLabel = ttk.Label(ScriptArgFrame, text = "Script Argument:")
ScriptArgEntry = tk.Text(ScriptArgFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
ScriptArgEntry.bind("<KeyRelease>", (lambda event: EditScriptArg(ScriptArgEntry.get(1.0, "end-1c"))))

ArgHelp = IntVar()
ArgHelp.set(0)

def ScriptArgHelp():
    ArgHelp.set(0)

    Text = ""
    for Line in MoveScriptArgText["Script {}".format(MoveScript.get())]:
        Text += Line + "\n"
    
    MakeInfoBox("Help", "Script Argument",
                ["The Script Argument is used by ACE to customise a Move Script.",
                 "This value can range from 0 to 255.",
                 "The specifics of what this does depends on the Move Script.",
                 "\n",
                 "Script {}".format(MoveScript.get()),
                 "{}".format(Text)])

ScriptArgHelpButton = ttk.Checkbutton(ScriptArgFrame, text = "?", variable = ArgHelp, command = ScriptArgHelp)

ScriptArgFrame.grid(row = 3, column = 2, padx = 15, pady = 5, sticky = W)
ScriptArgHelpButton.pack(side = tk.LEFT)
ScriptArgLabel.pack(side = tk.LEFT, padx = (0, 5))
ScriptArgEntry.pack(side = tk.LEFT)

#------------------------------------------------------------
# Table Entry hex Viewer
#------------------------------------------------------------

TableHexFrame = tk.Frame(EditorFrame, bg = "Black")
TableHexLabel = ttk.Label(TableHexFrame, text = "Hex Viewer")

HexByteSize = 20
HexByteHSpace = 5
HexByteVSpace = 5

HexViewFrame = tk.Frame(EditorFrame, bg = "Black")
MoveScriptByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
BasePowerByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
TypeByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
AccuracyByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
PowerPointByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
EffectChanceByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
RangeByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
PriorityByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
MoveFlagsByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
DamageFormulaByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
MoveKindByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))
ScriptArgByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexByteSize))

HexHelp = IntVar()
HexHelp.set(0)

def HexViewerHelp():
    HexHelp.set(0)
    MakeInfoBox("Help", "Hex Viewer",
                ["This area shows what the compiled entry looks like in hexadecimal."])

HexHelpButton = ttk.Checkbutton(TableHexFrame, text = "?", variable = HexHelp, command = HexViewerHelp)

TableHexFrame.grid(row = 4, column = 1, padx = 15, pady = 5, sticky = W)
HexHelpButton.pack(side = tk.LEFT)
TableHexLabel.pack(side = tk.LEFT)

HexViewFrame.grid(row = 5, column = 1, padx = 15, pady = 5, sticky = W)
MoveScriptByte.grid(row = 0, column = 0, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
BasePowerByte.grid(row = 0, column = 1, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
TypeByte.grid(row = 0, column = 2, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
AccuracyByte.grid(row = 0, column = 3, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
PowerPointByte.grid(row = 0, column = 4, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
EffectChanceByte.grid(row = 0, column = 5, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
RangeByte.grid(row = 1, column = 0, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
PriorityByte.grid(row = 1, column = 1, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
MoveFlagsByte.grid(row = 1, column = 2, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
DamageFormulaByte.grid(row = 1, column = 3, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
MoveKindByte.grid(row = 1, column = 4, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)
ScriptArgByte.grid(row = 1, column = 5, padx = HexByteHSpace, pady = HexByteVSpace, sticky = W)

#------------------------------------------------------------
# Move Description Editor
#------------------------------------------------------------

DescriptionLabelFrame = tk.Frame(EditorFrame, bg = "Black")
DescriptionLabel = ttk.Label(DescriptionLabelFrame, text = "Move Description")

# I want to have it so that each line is truncated at 19 characters
# If you enter in more than 19 characters on lines 1-3, the extra characters are
# moved to the next line
# If you enter in move than 19 characters on the 4th line, it truncates
# If you enter a newline in line 4, it truncates

def ProcessText(Text):
    if DescriptionBox.cget('state') == "normal":
        global Table
        
        Lines = Text.split("\n")

        while len(Lines) < 4:
            Lines.append("")
        
        Line1 = Lines[0]
        Line2 = Lines[1]
        Line3 = Lines[2]
        Line4 = Lines[3]

        if len(Line1) > 19: # bleeds into the next line        
            Line2 = Line1[19:] + Line2
            Line1 = Line1[0:19]

        if len(Line2) > 19:
            Line3 = Line2[19:] + Line3
            Line2 = Line2[0:19]

        if len(Line3) > 19:
            Line4 = Line3[19:] + Line4
            Line3 = Line3[0:19]

        if len(Line4) > 19:
            Line4 = Line4[0:19]
            Lines.append(Line4[19:])

        Lines[0] = Line1
        Lines[1] = Line2
        Lines[2] = Line3
        Lines[3] = Line4

        if len(Lines) > 4:
            Lines = Lines[0:4]
            DescriptionBox.delete(1.0, "end-1c")
            DescriptionBox.insert(1.0, Line4)
            DescriptionBox.insert(1.0, "\n")
            DescriptionBox.insert(1.0, Line3)
            DescriptionBox.insert(1.0, "\n")
            DescriptionBox.insert(1.0, Line2)
            DescriptionBox.insert(1.0, "\n")
            DescriptionBox.insert(1.0, Line1)

        NewText = "{}\n{}\n{}\n{}".format(Line1, Line2, Line3, Line4)
                     
        Table[CurrentMoveNumber.get()][DescriptionIndex] = NewText
        Refresh()

TextBoxFrame = tk.Frame(EditorFrame, bg = "Black")
DescriptionBox = tk.Text(TextBoxFrame, width = 19, height = 4, bg = "White", fg = "Black", font = ("Courier", SmallSize))
DescriptionBox.bind("<KeyRelease>", (lambda event: ProcessText(DescriptionBox.get(1.0, "end-1c"))))

DHelp = IntVar()
DHelp.set(0)

def DescriptionHelp():
    DHelp.set(0)
    MakeInfoBox("Help", "Move Description",
                ["This is the description of the Move seen in the Move Viewer in game.",
                 "This can be up to four lines long, with 19 characters per line.",
                 "The Move Description is compiled into a separate table."])

DescriptionHelpButton = ttk.Checkbutton(DescriptionLabelFrame, text = "?", variable = DHelp, command = DescriptionHelp)

DescriptionLabelFrame.grid(row = 4, column = 2, padx = 15, pady = 5, sticky = W)
DescriptionHelpButton.pack(side = tk.LEFT)
DescriptionLabel.pack(side = tk.LEFT)

TextBoxFrame.grid(row = 5, column = 2, padx = 15, pady = 5, sticky = W)
DescriptionBox.pack()

#------------------------------------------------------------
# Make the display function
#------------------------------------------------------------
def CompileToHexViewer():   
    MoveScriptByte.configure(text = MoveScript.get())
    BasePowerByte.configure(text = ConvertToHex(BasePower.get()))
    TypeByte.configure(text = TypeConversion[Type.get()])
    AccuracyByte.configure(text = ConvertToHex(Accuracy.get()))
    PowerPointByte.configure(text = ConvertToHex(PowerPoints.get()))
    EffectChanceByte.configure(text = ConvertToHex(EffectChance.get()))
    RangeByte.configure(text = RangeConversion[Range.get()])

    if Priority.get() != 0:
        if Parity.get() == 1:
            P = 256 - Priority.get()
        else:
            P = Priority.get()
    else:
        P = 0

    PriorityByte.configure(text = ConvertToHex(P))

    MoveFlags = [A.get(), B.get(), C.get(), D.get(), E.get(), F.get(), G.get(), H.get()]

    FlagLine = 0
    for i, Flag in enumerate(MoveFlags):
        FlagLine += (128 // 2**i) * Flag
        
    MoveFlagsByte.configure(text = ConvertToHex(FlagLine))
    
    DamageFormulaByte.configure(text = DamageFormula.get())
    MoveKindByte.configure(text = KindConversion[MoveKind.get()])
    ScriptArgByte.configure(text = ConvertToHex(ScriptArgument.get()))

def SetVariables():
    L = Table[CurrentMoveNumber.get()]

    MoveName.set(L[MoveNameIndex])
    MoveScript.set(L[MoveScriptIndex])
    BasePower.set(L[BasePowerIndex])
    Type.set(L[TypeIndex])
    Accuracy.set(L[AccuracyIndex])
    PowerPoints.set(L[PowerPointIndex])
    EffectChance.set(L[EffectChanceIndex])
    Range.set(L[RangeIndex])

    if L[PriorityIndex] < 0:
        Priority.set(abs(L[PriorityIndex]))
        Parity.set(1)
        ParityButton.configure(text = "-")
    else:
        Priority.set(L[PriorityIndex])
        Parity.set(0)
        ParityButton.configure(text = "+")

    A.set(L[MoveFlagIndex][0])
    B.set(L[MoveFlagIndex][1])
    C.set(L[MoveFlagIndex][2])
    D.set(L[MoveFlagIndex][3])
    E.set(L[MoveFlagIndex][4])
    F.set(L[MoveFlagIndex][5])
    G.set(L[MoveFlagIndex][6])
    H.set(L[MoveFlagIndex][7])
    
    DamageFormula.set(L[DamageFormulaIndex])
    MoveKind.set(L[MoveKindIndex])
    ScriptArgument.set(L[ScriptArgIndex])
    
def Refresh():
    global MoveNameList
     
    SetVariables()
    
    MoveNameEntry.delete(1.0, "end")
    MoveNameEntry.insert(1.0, MoveName.get())

    BasePowerEntry.delete(1.0, "end")
    BasePowerEntry.insert(1.0, BasePower.get())

    AccuracyEntry.delete(1.0, "end")
    AccuracyEntry.insert(1.0, Accuracy.get())

    PowerPointEntry.delete(1.0, "end")
    PowerPointEntry.insert(1.0, PowerPoints.get())

    PriorityEntry.delete(1.0, "end")
    PriorityEntry.insert(1.0, Priority.get())

    EffectChanceEntry.delete(1.0, "end")
    EffectChanceEntry.insert(1.0, EffectChance.get())

    ScriptArgEntry.delete(1.0, "end")
    ScriptArgEntry.insert(1.0, ScriptArgument.get())

    MoveNumberLabel.configure(text = "Move {} of {}".format(CurrentMoveNumber.get() + 1, len(Table)))

    MoveNameList = []
    for i, Entry in enumerate(Table):
        N = i + 1
        if N < 10:
            N = "00{}".format(N)
        elif N < 100:
            N = "0{}".format(N)
        else:
            N = str(N)
            
        MoveNameList.append("{} - {}".format(N, Entry[MoveNameIndex]))

    ScriptArgEntry.delete(1.0, "end")
    ScriptArgEntry.insert(1.0, ScriptArgument.get())

    CompileToHexViewer()

    MoveFinder.configure(values = MoveNameList)
    CurrentMove.set(MoveNameList[CurrentMoveNumber.get()])

#------------------------------------------------------------
# Make the buttons in the top row
#------------------------------------------------------------

# Make a new table
def CreateNewFile():
    global Table

    Sure = BooleanVar()
    MakeYesNoBox("Warning", "Create a New Table File?", Sure,
                ["Are you sure you want to make a new table?",
                 "This will overwrite the current one.",
                 "Make sure you have saved it if you would like to keep it."])

    if not Sure.get():
        return
    
    NewFile = fd.asksaveasfile(initialdir = os.getcwd(), initialfile = "New Table", defaultextension = ".txt")

    if NewFile is not None:
        global CurrentOpenFile
        CurrentOpenFile = os.path.realpath(NewFile.name)
        CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(NewFile.name)))
        NewFile.close()
        
        Length = ""

        TestLength = IntVar()
        while type(Length) != int:
            TestLength.set(0)
            MakeEntryBox("Enter A Number", "Number of Moves", TestLength, 1,
                         ["Enter the number of Moves to add to the table."])

            if TestLength.get() < 0:
                MakeInfoBox("Error!", "Invalid input!",
                            ["This input is invalid!",
                             "The number of Moves must be a positive number."])
                Length = ""

            elif TestLength.get() == 0:
                MakeInfoBox("Error!", "Invalid input!",
                            ["This input is invalid!",
                             "The number of Moves cannot be zero."])
                Length = ""

            else:
                Length = TestLength.get()

        if Length > 999:
            Length = 999

        OpenNames = BooleanVar()
        MakeYesNoBox("Open File", "Open Name File?", OpenNames,
                     ["Would you like to load the names",
                      "of the Moves in the table from a file?"])
                     
        NamesList = ("Move Name\n"*Length).split("\n")[0:-1]

        Table = [[]] * Length
        for i in range(len(Table)):
            Table[i] = ["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]
        
        if OpenNames.get():
            NamesFile = fd.askopenfilename(title = "Open Table", initialdir = os.getcwd(), filetypes = FileTypes)
            NamesFile = open(NamesFile, "r")
            
            for i, Name in enumerate(NamesFile.read().splitlines()):
                if i >= len(Table):
                    NamesList.append("Move Name")
                
                NamesList[i] = Name

        for i, Name in enumerate(Table):
            Table[i][MoveNameIndex] = NamesList[i]
            
        if len(NamesList) != Length:
            MakeInfoBox("Warning!", "Warning!",
                        ["The length of the name list is different than the length of the table.",
                         "The current number of Moves is {}.".format(len(Table))])

        MakeInfoBox("Success!", "The table was created!",
                ["The table was created successfully.",
                 "It has {} Moves in total.".format(len(Table))])

        CurrentMoveNumber.set(0)
        EnableEverything()
        Refresh()  

NewFileButton = ttk.Button(ButtonFrame, text = "New Table", command = CreateNewFile)

# Format description when opening file
def FormatDescription(RawText):
    Line1 = RawText[0:19].strip()
    Line2 = RawText[19:38].strip()
    Line3 = RawText[38:57].strip()
    Line4 = RawText[57:76].strip()

    NewText = "{}\n{}\n{}\n{}".format(Line1, Line2, Line3, Line4)
    return NewText

# Open a table from a text file
def OpenFile():
    NewFile = fd.askopenfilename(title = "Open Table", initialdir = os.getcwd(), filetypes = FileTypes)

    TableChars = "0123456798ABCDEF \n"
    Compiled = True

    if NewFile is not None:
        global CurrentOpenFile
        FileName = NewFile
        
        NewFile = open(FileName, "r")

        for Line in NewFile:
            for Char in Line:
                if Char not in TableChars:
                    Compiled = False
                    break

            if not Compiled:
                break

        NewFile.close()
        NewFile = open(FileName, "r")

        if Compiled: # Make new file
            FileName = "Opened " + os.path.basename(FileName)
            
        CurrentOpenFile = os.path.realpath(FileName)
        CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(FileName)))
        
        global Table
        Table = []

        if Compiled: # Load from bytes, this is easier
            for Line in NewFile:
                TableLine = []
                Line = Line.strip()

                Entry = Line.split()

                TableLine.append("Move Name")   # Get Move Name from Move Table
                TableLine.append(Entry[0])  # Move Script
                TableLine.append(int(Entry[1], 16)) # Base Power
                TableLine.append(list(TypeConversion.keys())[list(TypeConversion.values()).index(Entry[2])])
                TableLine.append(int(Entry[3], 16)) # Accuracy
                TableLine.append(int(Entry[4], 16)) # Power Points
                TableLine.append(int(Entry[5], 16)) # Effect Chance
                TableLine.append(list(RangeConversion.keys())[list(RangeConversion.values()).index(Entry[6])])

                P = int(Entry[7], 16)
                if P > 127:
                    P = 256 - P
                    P = -P
                    
                TableLine.append(P) # Priority

                MoveFlags = [0,0,0,0,0,0,0,0]
                F = int(Entry[8], 16)

                for i in range(8):
                    if F & 128 // 2**i != 0: # Flag is set
                        MoveFlags[i] = 1

                TableLine.append(MoveFlags)
                
                TableLine.append(Entry[9]) # Damage Formula
                TableLine.append(list(KindConversion.keys())[list(KindConversion.values()).index(Entry[10])])
                TableLine.append(int(Entry[11], 16))

                TableLine.append('')
                Table.append(TableLine)

        else: # Parse from text, this is harder
            FileStuff = NewFile.read().split("\n\n")
            
            for Entry in FileStuff:
                TableLine = []
                Entry = Entry.split("\n")

                for i, Line in enumerate(Entry):
                    if i == MoveNameIndex:
                        TableLine.append(Line.split("-")[0].strip())

                    elif i == MoveScriptIndex:
                        TableLine.append(Line.split(")")[1].replace(",", "").strip()[2:])

                    elif i == BasePowerIndex:
                        TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))

                    elif i == TypeIndex:
                        TableLine.append(Line.split(")")[1].replace(",", "").strip())

                    elif i == AccuracyIndex:
                        TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))

                    elif i == PowerPointIndex:
                        TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))

                    elif i == EffectChanceIndex:
                        TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))
                        
                    elif i == RangeIndex:
                        Range = Line.split(")")[1].replace(",", "").strip()

                        C = {"MySide":"My Side", "FoeSide":"Foe Side",
                             "AllButUser":"All But User", "UserOrPartner":"User Or Partner",
                             "TargetOrPartner":"Target Or Partner", "LastHitMe":"Last Attacker"}

                        for Key in C:
                            if Range == Key:
                                Range = C[Key]
                                break
                        
                        TableLine.append(Range)

                    elif i == PriorityIndex:
                        P = int(Line.split(")")[1].replace(",", "").strip())

                        if P > 127:
                            P = 256 - P
                            P = -P

                        TableLine.append(P)

                    elif i == MoveFlagIndex:
                        F = Line.split(")")[1].replace(",", "").strip()
                        MoveFlags = [0,0,0,0,0,0,0,0]

                        for i, Flag in enumerate(F.split("+")):
                            Flag = Flag.strip()[2:]

                            if int(Flag, 16) & 128 // 2**i:
                                MoveFlags[i] = 1

                        TableLine.append(MoveFlags)

                    elif i == DamageFormulaIndex:
                        TableLine.append(Line.split(")")[1].replace(",", "").strip()[2:])

                    elif i == MoveKindIndex:
                        TableLine.append(Line.split(")")[1].replace(",", "").strip())

                    elif i == ScriptArgIndex:
                        TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))

                    elif i == DescriptionIndex: # Includes a Move Description Line
                        TableLine.append(FormatDescription(Line.split(")")[1].replace(",","").strip()))

                while len(TableLine) < 14:
                    TableLine.append('')
                    
                Table.append(TableLine)

    for i, Entry in enumerate(Table): # Get rid of blank line entries
        if Entry == ['', '', '', '', '', '', '', '', '', '', '', '', '', '']:
            Table.pop(i) 

    MakeInfoBox("Success!", "The table was created!",
                ["The table was created successfully.",
                 "It has {} Moves in total.".format(len(Table))])
    
    CurrentMoveNumber.set(0)
    EnableEverything()
    Refresh() 
    EnableEverything()

OpenFileButton = ttk.Button(ButtonFrame, text = "Open", command = OpenFile)

# Write current table to the currently opened file
def SaveFile():
    TableText = ""

    for Entry in Table:
        for i, Item in enumerate(Entry):
            if i == MoveNameIndex:
                TableText += "{}\n".format(Item)
                continue

            if i == MoveScriptIndex:
                TableText += "(Move Script) 0x{}\n".format(Item)
                continue
                        
            if i == BasePowerIndex:
                TableText += "(Base Power) {}\n".format(Item)
                continue
            
            if i == TypeIndex:
                TableText += "(Type) {}\n".format(Item)
                continue
                        
            if i == AccuracyIndex:
                TableText += "(Accuracy) {}\n".format(Item)
                continue
                        
            if i == PowerPointIndex:
                TableText += "(Power Points) {}\n".format(Item)
                continue
                        
            if i == EffectChanceIndex:
                TableText += "(Effect Chance) {}\n".format(Item)
                continue
                        
            if i == RangeIndex:
                TableText += "(Range) {}\n".format(Item)
                continue
                        
            if i == PriorityIndex:
                if int(Item) < 0: # Negative value, subtract from 256 first
                    Item = 256 + int(Item)
                            
                TableText += "(Priority) {}\n".format(Item)
                continue
                        
            if i == MoveFlagIndex:
                FlagValue = ""
                        
                for i, Flag in enumerate(Item):
                    FlagValue += " {} +".format(hex(128 // 2**i * Flag))

                FlagValue = FlagValue[:-1]
                            
                TableText += "(Move Flags) {}\n".format(FlagValue)
                continue
                        
            if i == DamageFormulaIndex:
                TableText += "(Damage Formula) 0x{}\n".format(Item)
                continue
                        
            if i == MoveKindIndex:
                TableText += "(Kind) {}\n".format(Item)
                continue
                        
            if i == ScriptArgIndex:
                TableText += "(Script Arg) {}\n".format(Item)
                continue

            if i == DescriptionIndex:
                TableText += "(Description) {}\n\n".format(Item.strip())

    NewFile = open(CurrentOpenFile, "w")
    NewFile.write(TableText.strip())
    NewFile.close()

    MakeInfoBox("Complete", "Table Saved!",
                ["The current table was successfully saved!"])

SaveButton = ttk.Button(ButtonFrame, text = "Save Table", command = SaveFile)

# Save the current table to a new file
def SaveFileAs():
    Edit = BooleanVar()
    MakeYesNoBox("New File", "Save A Copy", Edit,
                ["Would you like to switch to editing the new file",
                 "after you save a copy of this one?"])
    
    NewFile = fd.asksaveasfile(initialfile = "New Table", defaultextension = ".txt")

    if NewFile is not None:
        global CurrentOpenFile
        
        if not Edit.get():
            TempFile = CurrentOpenFile
            CurrentOpenFile = os.path.realpath(NewFile.name)
            CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(NewFile.name)))
            NewFile.close()
            CurrentOpenFile = TempFile
            SaveFile()
        else:
            CurrentOpenFile = os.path.realpath(NewFile.name)
            CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(NewFile.name)))
            NewFile.close()
            SaveFile()

SaveAsButton = ttk.Button(ButtonFrame, text = "Save Table As", command = SaveFileAs)

# Compile to bytes
def CompileTable():
    Option = StringVar()
    Option.set("None")

    MenuText = {"Attack Data Table": ["This is the main Attack Data Table.",
                                      "This can be completely compiled without needing an address."],
                "Move Name Table": ["This is the table of pointers for Move Names",
                                    "This requires an address beforehand."],
                "Move Description Table": ["This is the table of pointers for Move Names",
                                    "This requires an address beforehand."]}
    
    MakeMultiChoiceBox("Pick A Choice", "Which table should be compiled?", Option,
                       ["There are three possible tables which could be compiled."
                        "Please select one."], MenuText)

    if Option.get() == "Attack Data Table":
        NewFile = fd.asksaveasfile(initialfile = "Compiled ADT", defaultextension = ".bin")

        if NewFile is not None:
            FileName = os.path.realpath(NewFile.name)
            NewFile.close()

            NewFile = open(FileName, "wb")

            ByteList = []
            for Entry in Table:
                ByteList.append(int(Entry[MoveScriptIndex], 16))
                ByteList.append(Entry[BasePowerIndex])
                ByteList.append(int(TypeConversion[Entry[TypeIndex]], 16))
                ByteList.append(Entry[AccuracyIndex])
                ByteList.append(Entry[PowerPointIndex])
                ByteList.append(Entry[EffectChanceIndex])
                ByteList.append(int(RangeConversion[Entry[RangeIndex]]))

                if Entry[PriorityIndex] < 0:
                    P = 256 + Entry[PriorityIndex]
                else:
                    P = Entry[PriorityIndex]
                    
                ByteList.append(P)

                FlagLine = 0
                for i, Flag in enumerate(Entry[MoveFlagIndex]):
                    FlagLine += (128 // 2**i) * Flag

                ByteList.append(FlagLine)
                ByteList.append(int(Entry[DamageFormulaIndex]))
                ByteList.append(int(KindConversion[Entry[MoveKindIndex]]))
                ByteList.append(Entry[ScriptArgIndex])

            NewFile.write(bytes(ByteList))
            NewFile.close()
            MakeInfoBox("Success", "Compilation complete!",
                        ["The table was compiled to a file successfully!"])

    elif Option.get() == "Move Name Table":
        NewFile = fd.asksaveasfile(initialfile = "Compiled Names", defaultextension = ".bin")

        Address = StringVar()
        MakeAddressEntryBox("Enter Address", "Enter the starting address", Address,
                            ["Enter the starting address for the table in the following form:",
                             "08AABBCC",
                             "Where AABBCC is a placeholder for the offset of your table.",
                             "Use placeholder 0's (i.e. 0x12345 -> 08012345)"])

        Extend = BooleanVar()
        MakeYesNoBox("Question", "Future-proof the table?", Extend,
                     ["Would you like to future proof the table?",
                      "This makes each string of text the maximum length",
                      "it can be, with extra bytes being written as 00.",
                      "This takes up more space now, but will let you avoid",
                      "repointing the table later if you change string lengths."])

        if NewFile is not None:
            FileName = os.path.realpath(NewFile.name)
            NewFile.close()

            NewFile = open(FileName, "wb")

            NameByteList = []
            PointerByteList = []

            FirstPointerAddress = int(Address.get(), 16) + 4 * len(Table)
            P = FirstPointerAddress
            
            for N, Entry in enumerate(Table):
                MoveName = Entry[MoveNameIndex]
                
                if Extend.get():
                    Name = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    NameLength = 13
                else:
                    Name = [0] * (len(MoveName) + 1)
                    NameLength = len(MoveName) + 1

                if len(MoveName) == 0:
                    MoveName = "A"
                    Name = [0, 0]
                    NameLength = 2

                for i, Letter in enumerate(MoveName):
                    Name[i] = int(TextToBytes[Letter], 16)

                Name[i+1] = 255

                for Byte in Name:
                    NameByteList.append(Byte)
               
                PointerByteList.append((P & 4278190080) >> 24)
                PointerByteList.append((P & 16711680) >> 16)
                PointerByteList.append((P & 65280) >> 8)
                PointerByteList.append(P & 255)

                P = P + NameLength
                    
            NewFile.write(bytes(PointerByteList))
            NewFile.write(bytes(NameByteList))
            NewFile.close()
            MakeInfoBox("Success", "Compilation complete!",
                        ["The table was compiled to a file successfully!"])
            
    else: # Move Description
        NewFile = fd.asksaveasfile(initialfile = "Compiled Descriptions", defaultextension = ".bin")

        Address = StringVar()
        MakeAddressEntryBox("Enter Address", "Enter the starting address", Address,
                            ["Enter the starting address for the table in the following form:",
                             "08AABBCC",
                             "Where AABBCC is a placeholder for the offset of your table.",
                             "Use placeholder 0's (i.e. 0x12345 -> 08012345)"])

        Extend = BooleanVar()
        MakeYesNoBox("Question", "Future-proof the table?", Extend,
                     ["Would you like to future proof the table?",
                      "This makes each string of text the maximum length",
                      "it can be, with extra bytes being written as 00.",
                      "This takes up more space now, but will let you avoid",
                      "repointing the table later if you change string lengths."])

        if NewFile is not None:
            FileName = os.path.realpath(NewFile.name)
            NewFile.close()

            NewFile = open(FileName, "wb")

            NameByteList = []
            PointerByteList = []

            FirstPointerAddress = int(Address.get(), 16) + 4 * len(Table)
            P = FirstPointerAddress
            
            for N, Entry in enumerate(Table):
                MoveDesc = Entry[DescriptionIndex]
                
                if Extend.get():
                    Desc = [0] * 77
                    DescLength = 77
                else:
                    Desc = [0] * (len(MoveDesc) + 1)
                    DescLength = len(MoveDesc) + 1

                if len(MoveDesc) == 0:
                    MoveDesc = "A"
                    Desc = [0, 0]
                    DescLength = 2

                for i, Letter in enumerate(MoveDesc):
                    Desc[i] = int(TextToBytes[Letter], 16)

                Desc[i+1] = 255

                for Byte in Desc:
                    NameByteList.append(Byte)
               
                PointerByteList.append((P & 4278190080) >> 24)
                PointerByteList.append((P & 16711680) >> 16)
                PointerByteList.append((P & 65280) >> 8)
                PointerByteList.append(P & 255)

                P = P + DescLength
                    
            NewFile.write(bytes(PointerByteList))
            NewFile.write(bytes(NameByteList))
            NewFile.close()
            MakeInfoBox("Success", "Compilation complete!",
                        ["The table was compiled to a file successfully!"])

CompileButton = ttk.Button(ButtonFrame, text = "Compile Table", command = CompileTable)

ButtonHSpacing = 30
ButtonVSpacing = 5

NewFileButton.grid(row = 0, column = 0, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = W)
OpenFileButton.grid(row = 0, column = 1, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = W)
SaveButton.grid(row = 0, column = 2, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = W)
SaveAsButton.grid(row = 0, column = 3, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = W)
CompileButton.grid(row = 0, column = 4, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = W)

#------------------------------------------------------------
# Make the second layer of buttons
#------------------------------------------------------------

# Back move
def GoBackward():
    i = CurrentMoveNumber.get()

    i -= 1

    if i <= 0: # First Move, cannot go backwards anymore
        i = 0
        BackButton.configure(state = "disabled")

    ForwardButton.configure(state = "normal")
    CurrentMoveNumber.set(i)
    Refresh()

BackButton = ttk.Button(ButtonFrame, text = "Back", command = GoBackward)

# Forward Move
def GoForward():
    i = CurrentMoveNumber.get()

    i += 1

    if i >= len(Table) - 1: # Last Move, cannot go forwards anymore
        i = len(Table) - 1
        ForwardButton.configure(state = "disabled")

    BackButton.configure(state = "normal")
    CurrentMoveNumber.set(i)
    Refresh()

ForwardButton = ttk.Button(ButtonFrame, text = "Forward", command = GoForward)

# Add a move
def AddMove():
    global Table
    Table.append(["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""])
    CurrentMoveNumber.set(len(Table) - 1)

def AddMoves():
    Length = ""

    TestLength = IntVar()
    while type(Length) != int:
        TestLength.set(0)
        MakeEntryBox("Enter A Number", "Number of Moves", TestLength, 1,
                     ["Enter the number of Moves to add to the table."])

        if TestLength.get() < 0:
            MakeInfoBox("Error!", "Invalid input!",
                        ["This input is invalid!",
                         "The number of Moves must be a positive number."])
            Length = ""

        elif TestLength.get() == 0:
            MakeInfoBox("Error!", "Invalid input!",
                        ["This input is invalid!",
                         "The number of Moves cannot be zero."])
            Length = ""

        else:
            Length = TestLength.get()

    for i in range(Length):
        AddMove()

    if CurrentMoveNumber.get() > 0:
        BackButton.configure(state = "normal")

    ForwardButton.configure(state = "disabled")

    MakeInfoBox("Success!", "A new Move was added!",
                ["The table was modified successfully.",
                 "There are now {} Moves in total.".format(len(Table))])

    Refresh()     

AddMoveButton = ttk.Button(ButtonFrame, text = "Add Moves", command = AddMoves)

# Delete a Move
def DeleteMove():
    global Table

    Sure = BooleanVar()
    Sure.set(False)
    MakeYesNoBox("Warning!", "Warning!", Sure,
                 ["You are about to remove the current Move from the table.",
                  "This action cannot be undone.",
                  "Would you still like to proceed?"])

    if Sure.get():
        if len(Table) == 1: # Only one Move left
            MakeInfoBox("Error", "Warning!",
                        ["This is the only Move left in the table!",
                         "It cannot be fully deleted.",
                         "It will instead be replace with an empty Move."])

            Table = [["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]]
            Refresh()
            
        else:
            i = CurrentMoveNumber.get()
            Table.pop(i)

            if i > len(Table) - 1:
                CurrentMoveNumber.set(len(Table) - 1)

            Refresh()

DeleteMoveButton = ttk.Button(ButtonFrame, text = "Delete Move", command = DeleteMove)

MoveNumberLabel = ttk.Label(ButtonFrame, text = "Move {} of {}".format(CurrentMoveNumber.get() + 1, len(Table)))

AddMoveButton.grid(row = 1, column = 0, padx = ButtonHSpacing, sticky = W)
BackButton.grid(row = 1, column = 1, padx = ButtonHSpacing, sticky = W)
MoveNumberLabel.grid(row = 1, column = 2, padx = ButtonHSpacing, sticky = W)
ForwardButton.grid(row = 1, column = 3, padx = ButtonHSpacing, sticky = W)
DeleteMoveButton.grid(row = 1, column = 4, padx = ButtonHSpacing, sticky = W)

#------------------------------------------------------------
# Disable/Enable
#------------------------------------------------------------

def DisableEverything():
    MoveNameEntry.configure(state = "disabled")
    MoveScriptEntry.configure(state = "disabled")
    BasePowerEntry.configure(state = "disabled")
    TypeEntry.configure(state = "disabled")
    AccuracyEntry.configure(state = "disabled")
    PowerPointEntry.configure(state = "disabled")
    EffectChanceEntry.configure(state = "disabled")
    RangeEntry.configure(state = "disabled")
    PriorityEntry.configure(state = "disabled")

    SetAbilityFlag.configure(state = "disabled")
    SetSelfFlag.configure(state = "disabled")
    SetKingsRockFlag.configure(state = "disabled")
    SetMirrorMoveFlag.configure(state = "disabled")
    SetSnatchFlag.configure(state = "disabled")
    SetMagicCoatFlag.configure(state = "disabled")
    SetProtectFlag.configure(state = "disabled")
    SetDirectContactFlag.configure(state = "disabled")
        
    DamageFormulaEntry.configure(state = "disabled")
    MoveKindEntry.configure(state = "disabled")
    ScriptArgEntry.configure(state = "disabled")

    DescriptionBox.configure(state = "disabled")

    MoveNameHelpButton.configure(state = "disabled")
    MoveScriptHelpButton.configure(state = "disabled")
    BasePowerHelpButton.configure(state = "disabled")
    TypeHelpButton.configure(state = "disabled")
    AccuracyHelpButton.configure(state = "disabled")
    PowerPointHelpButton.configure(state = "disabled")
    EffectChanceHelpButton.configure(state = "disabled")
    RangeHelpButton.configure(state = "disabled")
    PriorityHelpButton.configure(state = "disabled")
    MoveFlagHelpButton.configure(state = "disabled")
    DamageFormulaHelpButton.configure(state = "disabled")
    MoveKindHelpButton.configure(state = "disabled")
    ScriptArgHelpButton.configure(state = "disabled")
    HexHelpButton.configure(state = "disabled")
    DescriptionHelpButton.configure(state = "disabled")
    
    SaveButton.configure(state = "disabled")
    SaveAsButton.configure(state = "disabled")
    CompileButton.configure(state = "disabled")

    BackButton.configure(state = "disabled")
    ForwardButton.configure(state = "disabled")
    AddMoveButton.configure(state = "disabled")
    DeleteMoveButton.configure(state = "disabled")

    MoveFinder.configure(state = "disabled")
    ParityButton.configure(state = "disabled")

def EnableEverything():
    MoveNameEntry.configure(state = "normal")
    MoveScriptEntry.configure(state = "normal")
    BasePowerEntry.configure(state = "normal")
    TypeEntry.configure(state = "normal")
    AccuracyEntry.configure(state = "normal")
    PowerPointEntry.configure(state = "normal")
    EffectChanceEntry.configure(state = "normal")
    RangeEntry.configure(state = "normal")
    PriorityEntry.configure(state = "normal")

    SetAbilityFlag.configure(state = "normal")
    SetSelfFlag.configure(state = "normal")
    SetKingsRockFlag.configure(state = "normal")
    SetMirrorMoveFlag.configure(state = "normal")
    SetSnatchFlag.configure(state = "normal")
    SetMagicCoatFlag.configure(state = "normal")
    SetProtectFlag.configure(state = "normal")
    SetDirectContactFlag.configure(state = "normal")
    
    DamageFormulaEntry.configure(state = "normal")
    MoveKindEntry.configure(state = "normal")
    ScriptArgEntry.configure(state = "normal")

    DescriptionBox.configure(state = "normal")

    MoveNameHelpButton.configure(state = "normal")
    MoveScriptHelpButton.configure(state = "normal")
    BasePowerHelpButton.configure(state = "normal")
    TypeHelpButton.configure(state = "normal")
    AccuracyHelpButton.configure(state = "normal")
    PowerPointHelpButton.configure(state = "normal")
    EffectChanceHelpButton.configure(state = "normal")
    RangeHelpButton.configure(state = "normal")
    PriorityHelpButton.configure(state = "normal")
    MoveFlagHelpButton.configure(state = "normal")
    DamageFormulaHelpButton.configure(state = "normal")
    MoveKindHelpButton.configure(state = "normal")
    ScriptArgHelpButton.configure(state = "normal")
    HexHelpButton.configure(state = "normal")
    DescriptionHelpButton.configure(state = "normal")
    
    SaveButton.configure(state = "normal")
    SaveAsButton.configure(state = "normal")
    CompileButton.configure(state = "normal")
    AddMoveButton.configure(state = "normal")
    DeleteMoveButton.configure(state = "normal")

    MoveFinder.configure(state = "normal")
    ParityButton.configure(state = "normal")

    if len(Table) > 1:
        ForwardButton.configure(state = "normal")

#------------------------------------------------------------
# Make Shortcuts
#------------------------------------------------------------

if OnAMac:
    ShortcutNew = "<Command-n>"
    ShortcutQuit = "<Command-q>"
    ShortcutSave = "<Command-s>"
    ShortcutSaveAs = "<Command-e>"
    ShortcutOpen = "<Command-o>"
    ShortcutDebug = "<Command-d>"
    ShortcutForward = "<Command-0>"
    ShortcutBackward = "<Command-9>"
    ShortcutHelp = "<Command-h>"
else:
    ShortcutNew = "<Control-n>"
    ShortcutQuit = "<Control-q>"
    ShortcutSave = "<Control-s>"
    ShortcutSaveAs = "<Control-e>"
    ShortcutOpen = "<Control-o>"
    ShortcutDebug = "<Control-d>"
    ShortcutForward = "<Control-0>"
    ShortcutBackward = "<Control-9>"
    ShortcutHelp = "<Control-h>"

def CallNew(self):
    CreateNewFile()

def CallQuit(self):
    Root.destroy()

def CallSave(self):
    SaveFile()

def CallSaveAs(self):
    SaveFileAs()

def CallDebug(self):
    OpenFileDirectory()

def CallForwardButton(self):
    GoForward()

def CallBackwardButton(self):
    GoBackward()

def CallHelpMenu(self):
    ShowHelpMenu()

def CallOpen(self):
    OpenFile()

Root.bind(ShortcutNew, CallNew)
Root.bind(ShortcutQuit, CallQuit)
Root.bind(ShortcutSave, CallSave)
Root.bind(ShortcutSaveAs, CallSaveAs)
Root.bind(ShortcutDebug, CallDebug)
Root.bind(ShortcutForward, CallForwardButton)
Root.bind(ShortcutBackward, CallBackwardButton)
Root.bind(ShortcutHelp, CallHelpMenu)
Root.bind(ShortcutOpen, CallOpen)

#------------------------------------------------------------
# Main Loop
#------------------------------------------------------------
DisableEverything()
DebugMakeTable()
Root.mainloop()
