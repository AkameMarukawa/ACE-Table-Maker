import os
import sys
import platform
import shutil
import MakeBoxes as mb
import Dictionaries as d
import TableFunctions as tf
import MakeScriptHelperBoxes as mshb
import MakeFormulaHelperBoxes as mfhb
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from subprocess import call, Popen

try:
    # ------------------------------------------------------------
    # Set Platform Variable
    # ------------------------------------------------------------
    if(platform.system() == 'Darwin'): # This is a Mac
        OnAMac = True
    else:
        OnAMac = False

    if OnAMac:
        Desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
        Paste = "<Command-v>"
        CompiledDir = "Resources"
    else:
        Desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        Paste = "<Control-v>"
        CompiledDir = "ACEW"

    if os.path.basename(os.getcwd()) == CompiledDir:
        InitialFolder = Desktop
    else:
        InitialFolder = os.getcwd()

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

    # Create File Bytes for reading Binary File
    def CreateFileBytes(BinFile, N):
        ByteList = []
        Byte = BinFile.read(1)
        while Byte:
            Value = int(bin(ord(Byte)), 2)
            Byte = hex(Value).upper()[2:]

            if Value < 16:
                Byte = "0" + Byte

            ByteList.append(Byte)
            Byte = BinFile.read(1)

        FileBytes = ""
        for i, Byte in enumerate(ByteList):
            if (i+1) % N == 0:
                FileBytes += Byte + "\n"
            else:
                FileBytes += Byte + " "

        return FileBytes

    #------------------------------------------------------------
    # Global stuff
    #------------------------------------------------------------
    Table = []
    MoveNameList = []

    CurrentOpenFile = ""

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
    Root.title("Akame's Custom Engine")
    Root.resizable(False, False)
    Root.configure(bg = "Black")

    s = ttk.Style()
    s.theme_use('alt')

    SmallSize = 16

    if not OnAMac:
        Root.iconbitmap('ACE.ico')

    # This is what the widgets look like when not disabled
    s.configure("TRadiobutton", background = "black", foreground = "white", indicatorcolor = "grey")
    s.configure("TCombobox", background = "white", foreground = "black")
    s.configure("TMenuButton", background = "white", foreground = "black")
    s.configure("TCheckbutton", background = "black", foreground = "white", indicatorcolor = "white")
    s.configure("TLabel", background = "black", foreground = "white", font = ('Courier', SmallSize, 'bold'))
    s.configure("TFrame", background = "black", foreground = "white")
    s.configure("TScale", background = "black", foreground = "white")
    s.configure("TButton", background = "black", foreground = "white")

    # This is what the widgets look like when disabled or hovered over (active)
    s.map("TRadiobutton", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")], indicatorcolor = [("selected", "yellow")])
    s.map("TCombobox", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")])
    s.map("TMenuButton", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")])
    s.map("TCheckbutton", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")], indicatorcolor = [("selected", "blue")])
    s.map("TScale", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")])
    s.map("TButton", background = [("active", "white"), ("disabled", "black")], foreground = [("active", "black"), ("disabled", "grey")])

    # -------------------------------------------------------
    # Make Frames
    # -------------------------------------------------------    
    TopLayerFrame = tk.Frame(Root, bg = "Black")
    TopLayerFrame.pack(side = "top", padx = 10, pady = 10)

    ButtonFrame = tk.Frame(Root, bg = "Black")
    ButtonFrame.pack(fill = "x", padx = 10, pady = 0)

    EditorFrame = tk.Frame(Root, bg = "Black")
    EditorFrame.pack(side = "left", padx = 10, pady = 10)

    #------------------------------------------------------------
    # Set Index and Tkinter Variables
    #------------------------------------------------------------
    MoveName = tk.StringVar()
    MoveScript = tk.StringVar()
    BasePower = tk.IntVar()
    Type = tk.StringVar()
    Accuracy = tk.IntVar()
    PowerPoints = tk.IntVar()
    EffectChance = tk.IntVar()
    Range = tk.StringVar()
    Priority = tk.IntVar()

    Parity = tk.IntVar()
    Parity.set(0)

    A = tk.IntVar()    # Ability Bypass
    B = tk.IntVar()    # Self Effect
    C = tk.IntVar()    # King's Rock
    D = tk.IntVar()    # Mirror Move
    E = tk.IntVar()    # Snatch
    F = tk.IntVar()    # Magic Coat
    G = tk.IntVar()    # Protect
    H = tk.IntVar()    # Direct Contact 

    DamageFormula = tk.StringVar()
    DamageArgument = tk.StringVar()
    MoveKind = tk.StringVar()
    ScriptArgument = tk.IntVar()
    Description = tk.StringVar()

    CurrentMoveNumber = tk.IntVar()
    CurrentMoveNumber.set(0)

    CurrentMove = tk.StringVar()

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
    # Top of the screen stuff
    #------------------------------------------------------------
    BulbasaurFrame = tk.Frame(TopLayerFrame, bg = "Black")
    IconFrame = tk.Frame(TopLayerFrame, bg = "Black")
    TablePicFrame = tk.Frame(TopLayerFrame, bg = "Black")

    BulbasaurPic = tk.PhotoImage(file = "Bulbasaur.png")
    BulbasaurPic = BulbasaurPic.zoom(6)
    BulbasaurPic = BulbasaurPic.subsample(5)
    BulbasaurLabel = ttk.Label(BulbasaurFrame, image = BulbasaurPic)
    BulbasaurLabel.image = BulbasaurPic

    TablePic = tk.PhotoImage(file = "Table.png")
    TablePic = TablePic.subsample(2)
    TableLabel = ttk.Label(TablePicFrame, image = TablePic)
    TableLabel.image = TablePic
    
    LabelFrame = tk.Frame(IconFrame, bg = "Black")
    MenuFrame = tk.Frame(IconFrame, bg = "Black")
    MoveFinderFrame = tk.Frame(MenuFrame, bg = "Black")

    MainLabel = ttk.Label(LabelFrame, text = "ACE Move Table Maker", font = ("Arial", int(1.5 * SmallSize), "bold"))
    CurrentLabel = ttk.Label(MenuFrame, text = "{}".format(CurrentOpenFile))
    CopyrightLabel = ttk.Label(LabelFrame, text = "Program by AkameTheBulbasaur, v2.0.0", font = ("Arial", SmallSize - 2))

    # Move Label
    MoveNumberLabel = ttk.Label(MenuFrame, text = "Move {} of {}".format(CurrentMoveNumber.get() + 1, len(Table)))

    # Make Help Menu
    def ShowHelpMenu():
        mb.MakeInfoBox(Root, "Help", "Shortcuts",
                    ["Cmd/Ctrl N: Make new table file",
                     "Cmd/Ctrl O: Open saved table file",
                     "Cmd/Ctrl S: Save current table file",
                     "Cmd/Ctrl E: Save current table as new file",
                     "Cmd/Ctrl 0: Show next Move in table",
                     "Cmd/Ctrl 9: Show previous Move in table",
                     "Cmd/Ctrl H: Open shortcut menu",
                     "Cmd/Ctrl Q: Quit program"])

    ShowHelp = tk.IntVar()
    ShowHelp.set(0)

    def DisplayHelp():
        ShowHelp.set(0)
        ShowHelpMenu()

    ShowHelpButton = ttk.Checkbutton(MoveFinderFrame, text = "?", variable = ShowHelp, command = DisplayHelp)

    # Jump to Move
    def JumpToMove(self):
        # Gets the Move Number
        MoveNumber = int(CurrentMove.get().split("-")[0].strip()) - 1

        CurrentMoveNumber.set(MoveNumber)
        Refresh()

    MoveFinder = ttk.Combobox(MoveFinderFrame, textvariable = CurrentMove, width = 18, values = MoveNameList, font = ("Courier", SmallSize))
    MoveFinder.bind("<<ComboboxSelected>>", JumpToMove)

    #------------------------------------------------------------
    # Edit Move Name
    #------------------------------------------------------------
    MoveNameFrame = tk.Frame(EditorFrame, bg = "Black")

    def EditName(Name):
        if MoveNameEntry.cget('state') == "normal":
            global Table
            i = CurrentMoveNumber.get()
            
            Name = Name[0:12]
            Table[i][tf.MoveNameIndex] = Name
            
            Refresh()

    MoveNameLabel = ttk.Label(MoveNameFrame, text = "Move Name:")
    MoveNameEntry = tk.Text(MoveNameFrame, width = 12, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    MoveNameEntry.bind("<KeyRelease>", (lambda event: EditName(MoveNameEntry.get(1.0, "end-1c"))))

    NameHelp = tk.IntVar()
    NameHelp.set(0)

    def MoveNameHelp():
        NameHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Move Name", \
                    ["This is the name of the Move.",
                     "This does not appear in the compiled Attack Data Table.",
                     "Instead, Move Names are compiled to a separate Move Name Table."])

    MoveNameHelpButton = ttk.Checkbutton(MoveNameFrame, text = "?", variable = NameHelp, command = MoveNameHelp)

    #------------------------------------------------------------
    # Edit Move Script
    #------------------------------------------------------------
    MoveScriptFrame = tk.Frame(EditorFrame, bg = "Black")

    def EditMoveScript():
        global Table
        i = CurrentMoveNumber.get()

        Table[i][tf.MoveScriptIndex] = MoveScript.get()

        Refresh()

    def ProcessMoveScript():
        Input = MoveScript.get().upper()
        Hex = "0123456789ABCDEF"
        
        for Letter in Hex:
            if Input == Letter:
                MoveScript.set("0" + Letter)
                EditMoveScript()

        if Input in tf.HexBytes:
            MoveScript.set(Input)
            EditMoveScript()

    MoveScriptLabel = ttk.Label(MoveScriptFrame, text = "Move Script:")
    MoveScriptEntry = ttk.Combobox(MoveScriptFrame, textvariable = MoveScript, width = 2, values = tf.HexBytes, font = ("Courier", SmallSize))
    MoveScriptEntry.bind("<<ComboboxSelected>>", lambda e: EditMoveScript())
    MoveScriptEntry.bind("<Return>", lambda e: ProcessMoveScript())

    ScriptHelp = tk.IntVar()
    ScriptHelp.set(0)

    def MoveScriptHelp():
        ScriptHelp.set(0)

        NewValue = tk.StringVar()
        NewValue.set("None")
        mb.MakeInfoBoxMenuSearch(Root, "Help", "Move Scripts",
                            ["The Move Script is a Battle Script that is specifically",
                             "executed by a Move when it is selected in battle.",
                             "Select a script from the dropdown menu to see what it does.",
                             "Note: these are the defaults for ACE, your scripts may vary."],
                            d.MoveScriptText, NewValue, "Script {}".format(MoveScript.get()))

        if NewValue.get() != "None":
            MoveScript.set(NewValue.get().replace("Script", "").strip())
            EditMoveScript()

    MoveScriptHelpButton = ttk.Checkbutton(MoveScriptFrame, text = "?", variable = ScriptHelp, command = MoveScriptHelp)

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
            except Exception as e:
                print(e)
                Power = 0

            if Power > 255:
                Power = 255

            if Power < 0:
                Power = 0

            Table[i][tf.BasePowerIndex] = Power
            
            Refresh()

    BasePowerLabel = ttk.Label(BasePowerFrame, text = "Base Power:")
    BasePowerEntry = tk.Text(BasePowerFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    BasePowerEntry.bind("<KeyRelease>", (lambda event: EditBasePower(BasePowerEntry.get(1.0, "end-1c"))))

    PowerHelp = tk.IntVar()
    PowerHelp.set(0)

    def BasePowerHelp():
        PowerHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Base Power",
                    ["The Base Power of a Move generally indicates its strength.",
                     "This value can range from 0 to 255.",
                     "Setting this value to zero means the Move is Non-Damaging."])

    BasePowerHelpButton = ttk.Checkbutton(BasePowerFrame, text = "?", variable = PowerHelp, command = BasePowerHelp)

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

        Table[i][tf.TypeIndex] = Type.get()

        Refresh()
        
    TypeLabel = ttk.Label(TypeFrame, text = "Type:")
    TypeEntry = ttk.Combobox(TypeFrame, textvariable = Type, width = 8, values = Types, font = ("Courier", SmallSize))
    TypeEntry.bind("<<ComboboxSelected>>", EditType)

    TypeHelp = tk.IntVar()
    TypeHelp.set(0)

    def MoveTypeHelp():
        TypeHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Move Type",
                    ["This is the base Type of the Move."
                     "The actual Type when used in Battle may be different,"
                     "but will, by default, be the one given here."])

    TypeHelpButton = ttk.Checkbutton(TypeFrame, text = "?", variable = TypeHelp, command = MoveTypeHelp)

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
            except Exception as e:
                print(e)
                Accuracy = 0

            if Accuracy > 100:
                Accuracy = 100

            if Accuracy < 0:
                Accuracy = 0

            Table[i][tf.AccuracyIndex] = Accuracy
            
            Refresh()
        
    AccuracyLabel = ttk.Label(AccuracyFrame, text = "Accuracy:")
    AccuracyEntry = tk.Text(AccuracyFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    AccuracyEntry.bind("<KeyRelease>", (lambda event: EditAccuracy(AccuracyEntry.get(1.0, "end-1c"))))

    AccHelp = tk.IntVar()
    AccHelp.set(0)

    def AccuracyHelp():
        AccHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Accuracy",
                    ["This is the base Accuracy of the Move.",
                     "This value can range from 0 to 100.",
                     "A higher Accuracy means the Move will hit more often.",
                     "An Accuracy of 0 means the Move bypasses Accuracy checks."])

    AccuracyHelpButton = ttk.Checkbutton(AccuracyFrame, text = "?", variable = AccHelp, command = AccuracyHelp)

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
            except Exception as e:
                print(e)
                PowerPoints = 0

            if PowerPoints > 99:
                PowerPoints = 99

            if PowerPoints < 0:
                PowerPoints = 0

            Table[i][tf.PowerPointIndex] = PowerPoints
            
            Refresh()
        
    PowerPointLabel = ttk.Label(PowerPointFrame, text = "Power Points:")
    PowerPointEntry = tk.Text(PowerPointFrame, width = 2, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    PowerPointEntry.bind("<KeyRelease>", (lambda event: EditPowerPoints(PowerPointEntry.get(1.0, "end-1c"))))

    PPHelp = tk.IntVar()
    PPHelp.set(0)

    def PowerPointHelp():
        PPHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Power Points",
                    ["This is the default amount of Power Points that the Move can have.",
                     "This value can range from 0 to 99.",
                     "More Power Points means the Move can be used more.",
                     "This does not include the amount added by using Items such as PPUp or PPMax."])

    PowerPointHelpButton = ttk.Checkbutton(PowerPointFrame, text = "?", variable = PPHelp, command = PowerPointHelp)

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
            except Exception as e:
                print(e)
                Chance = 0

            if Chance > 100:
                Chance = 100

            if Chance < 0:
                Chance = 0

            Table[i][tf.EffectChanceIndex] = Chance
            
            Refresh()
        
    EffectChanceLabel = ttk.Label(EffectChanceFrame, text = "Effect Chance:")
    EffectChanceEntry = tk.Text(EffectChanceFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    EffectChanceEntry.bind("<KeyRelease>", (lambda event: EditEffectChance(EffectChanceEntry.get(1.0, "end-1c"))))

    ChanceHelp = tk.IntVar()
    ChanceHelp.set(0)

    def EffectChanceHelp():
        ChanceHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Effect Chance",
                    ["This is the chance of the Move Script's effect activating (if it has one).",
                     "This values ranges from 0 to 100.",
                     "A higher value means the effect will occur more often.",
                     "Setting this to zero makes the effect always activate."])

    EffectChanceHelpButton = ttk.Checkbutton(EffectChanceFrame, text = "?", variable = ChanceHelp, command = EffectChanceHelp)

    #------------------------------------------------------------
    # Edit Attack Range
    #------------------------------------------------------------
    RangeList = ["Target", "User", "Foe Side", "My Side", "All But User", "Everyone", "Random", "Last Attacker", "User Or Partner", "Target Or Partner"]

    RangeFrame = tk.Frame(EditorFrame, bg = "Black")

    def EditRange(self):
        global Table
        i = CurrentMoveNumber.get()

        Table[i][tf.RangeIndex] = Range.get()

        Refresh()
        
    RangeLabel = ttk.Label(RangeFrame, text = "Range:")
    RangeEntry = ttk.Combobox(RangeFrame, textvariable = Range, width = 13, values = RangeList, font = ("Courier", SmallSize))
    RangeEntry.bind("<<ComboboxSelected>>", EditRange)

    RHelp = tk.IntVar()
    RHelp.set(0)

    def RangeHelp():
        RHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Range",
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
            except Exception as e:
                print(e)
                Priority = 0

            if Priority > 127:
                Priority = 127

            if Priority < 0:
                Priority = 0

            if Parity.get() == 1: # Negative Priority
                Priority = -Priority

            Table[i][tf.PriorityIndex] = Priority
            
            Refresh()
        
    PriorityLabel = ttk.Label(PriorityFrame, text = "Priority:")
    PriorityEntry = tk.Text(PriorityFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    PriorityEntry.bind("<KeyRelease>", (lambda event: EditPriority(PriorityEntry.get(1.0, "end-1c"))))

    PriHelp = tk.IntVar()
    PriHelp.set(0)

    def PriorityHelp():
        PriHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Priority",
                    ["Moves with higher Priority will go before those which have a lower Priority.",
                     "This values ranges from -127 to 127.",
                     "The default is zero, with higher values moving first and negative values moving later."])

    PriorityHelpButton = ttk.Checkbutton(PriorityFrame, text = "?", variable = PriHelp, command = PriorityHelp)

    X = tk.IntVar()
    X.set(0)

    def EditParity():
        global Table
        i = CurrentMoveNumber.get()
        X.set(0)

        if Parity.get() == 0: # +
            ParityButton.configure(text = "-")
            Parity.set(1)
            Table[i][tf.PriorityIndex] = -Table[i][tf.PriorityIndex]
            
        else:
            ParityButton.configure(text = "+")
            Parity.set(0)
            Table[i][tf.PriorityIndex] = -Table[i][tf.PriorityIndex]

        Refresh()

    ParityButton = ttk.Checkbutton(PriorityFrame, text = "+", variable = X, command = EditParity)

    #------------------------------------------------------------
    # Edit Move Flags
    #------------------------------------------------------------
    MoveFlagLabelFrame = tk.Frame(EditorFrame, bg = "Black")
    MoveFlagFrame = tk.Frame(EditorFrame, bg = "Black")

    MoveFlagLabel = ttk.Label(MoveFlagLabelFrame, text = "Move Flags")

    def SetMoveFlag(CheckVar, X):
        global Table
        i = CurrentMoveNumber.get()

        Table[i][tf.MoveFlagIndex][X] = CheckVar.get()

        Refresh()

    SetAbilityFlag = ttk.Checkbutton(MoveFlagFrame, text = "Bypass Ability", variable = A, command = lambda: SetMoveFlag(A, 0))
    SetSelfFlag = ttk.Checkbutton(MoveFlagFrame, text = "Self Effect", variable = B, command = lambda: SetMoveFlag(B, 1))
    SetKingsRockFlag = ttk.Checkbutton(MoveFlagFrame, text = "King's Rock", variable = C, command = lambda: SetMoveFlag(C, 2))
    SetMirrorMoveFlag = ttk.Checkbutton(MoveFlagFrame, text = "Mirror Move", variable = D, command = lambda: SetMoveFlag(D, 3))
    SetSnatchFlag = ttk.Checkbutton(MoveFlagFrame, text = "Snatch", variable = E, command = lambda: SetMoveFlag(E, 4))
    SetMagicCoatFlag = ttk.Checkbutton(MoveFlagFrame, text = "Magic Coat", variable = F, command = lambda: SetMoveFlag(F, 5))
    SetProtectFlag = ttk.Checkbutton(MoveFlagFrame, text = "Protect", variable = G, command = lambda: SetMoveFlag(G, 6))
    SetDirectContactFlag = ttk.Checkbutton(MoveFlagFrame, text = "Direct Contact", variable = H, command = lambda: SetMoveFlag(H, 7))

    FlagHelp = tk.IntVar()
    FlagHelp.set(0)

    def MoveFlagHelp():
        FlagHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Move Flags",
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

    #------------------------------------------------------------
    # Edit Damage Formula + Argument
    #------------------------------------------------------------
    DamageFormulaFrame = tk.Frame(EditorFrame, bg = "Black")
    DamageArgumentFrame = tk.Frame(EditorFrame, bg = "Black")

    def EditDamageFormula():
        global Table
        i = CurrentMoveNumber.get()

        if DamageArgument.get() == "":
            DamageArgument.set("00")

        if DamageFormula.get() == "":
            DamageFormula.set("00")

        DamageValue = hex((int(DamageArgument.get(), 16) << 4) + (int(DamageFormula.get(), 16) & 15)).upper()[2:]

        if int(DamageValue, 16) < 16:
            DamageValue = "0" + DamageValue

        Table[i][tf.DamageFormulaIndex] = DamageValue

        Refresh()

    def ProcessDamageFormula():
        Input = DamageFormula.get().upper()
        Hex = "0123456789ABCDEF"
        
        for Letter in Hex:
            if Input == Letter:
                DamageFormula.set("0" + Letter)
                EditDamageFormula()

        if Input in tf.HexBytes:
            DamageFormula.set(Input)
            EditDamageFormula()

    def ProcessDamageArgument():
        Input = DamageArgument.get().upper()
        Hex = "0123456789ABCDEF"
        
        for Letter in Hex:
            if Input == Letter:
                DamageArgument.set("0" + Letter)
                EditDamageFormula()

        if Input in tf.HexBytes:
            DamageArgument.set(Input)
            EditDamageFormula()
        
    DamageFormulaLabel = ttk.Label(DamageFormulaFrame, text = "Damage Formula:")
    DamageFormulaEntry = ttk.Combobox(DamageFormulaFrame, textvariable = DamageFormula, width = 2, values = tf.HexHalfBytes, font = ("Courier", SmallSize))
    DamageFormulaEntry.bind("<<ComboboxSelected>>", lambda e: EditDamageFormula())
    DamageFormulaEntry.bind("<Return>", lambda e: ProcessDamageFormula())

    DamageArgumentLabel = ttk.Label(DamageArgumentFrame, text = "Formula Argument:")
    DamageArgumentEntry = ttk.Combobox(DamageArgumentFrame, textvariable = DamageArgument, width = 2, values = tf.HexHalfBytes, font = ("Courier", SmallSize))
    DamageArgumentEntry.bind("<<ComboboxSelected>>", lambda e: EditDamageFormula())
    DamageArgumentEntry.bind("<Return>", lambda e: ProcessDamageArgument())

    FormulaHelp = tk.IntVar()
    FormulaHelp.set(0)

    def DamageFormulaHelp():
        FormulaHelp.set(0)

        NewValue = tk.StringVar()
        NewValue.set("-")
        mb.MakeInfoBoxWithMenu(Root, "Help", "Damage Formula",
                            ["The damage formula is used to determine the Base Power",
                             "the of the Move.",
                             "If this is set to anything other than zero, then the",
                             "game will run an additional routine to find the true",
                             "Base Power, which may use the Base Power given here."],
                            d.DamageFormulaText, NewValue, "Formula {}".format(DamageFormula.get()))
        
        if NewValue.get() != "-":
            DamageFormula.set(NewValue.get().replace("Formula", "").strip())
            EditDamageFormula()

    DamageFormulaHelpButton = ttk.Checkbutton(DamageFormulaFrame, text = "?", variable = FormulaHelp, command = DamageFormulaHelp)

    FormulaArgHelp = tk.IntVar()
    FormulaArgHelp.set(0)

    def DamageFormulaArgHelp():
        FormulaArgHelp.set(0)

        Text = ""
        FormulaOption = d.FormulaArgumentHelpers[DamageFormula.get()][0]
        FormulaOptionArgs = d.FormulaArgumentHelpers[DamageFormula.get()][1]

        NewValue = tk.StringVar()
        NewValue.set("None")
        mfhb.MakeFormulaArgHelperBox(Root, "Help", "Damage Formula Argument",
                              ["The Damage Formula Argument is used for customising Damage Formulae.",
                               "This value can range from 0 to 255.",
                               "The helper below is for the currently selected Damage Formula."],
                              FormulaOption,
                              FormulaOptionArgs,
                              NewValue)

        if NewValue.get() != "None":
            DamageArgument.set(NewValue.get())
            EditDamageFormula()
        
    DamageArgumentHelpButton = ttk.Checkbutton(DamageArgumentFrame, text = "?", variable = FormulaArgHelp, command = DamageFormulaArgHelp)

    #------------------------------------------------------------
    # Edit Move Kind
    #------------------------------------------------------------
    MoveKindFrame = tk.Frame(EditorFrame, bg = "Black")

    Kinds = ["Physical", "Special", "Status"]

    def EditMoveKind(self):
        global Table
        i = CurrentMoveNumber.get()

        Table[i][tf.MoveKindIndex] = MoveKind.get()

        Refresh()
        
    MoveKindLabel = ttk.Label(MoveKindFrame, text = "Move Kind:")
    MoveKindEntry = ttk.Combobox(MoveKindFrame, textvariable = MoveKind, width = 10, values = Kinds, font = ("Courier", SmallSize))
    MoveKindEntry.bind("<<ComboboxSelected>>", EditMoveKind)

    KindHelp = tk.IntVar()
    KindHelp.set(0)

    def MoveKindHelp():
        KindHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Move Kind",
                    ["The Move Kind determines whether the Move is Physical, Special or Status.",
                     "Physical: Uses Attack/Defence when calculating Damage",
                     "Special: Uses Sp. Attack/Sp. Defence when calculating Damage",
                     "Status: Does not deal direct damage."])

    MoveKindHelpButton = ttk.Checkbutton(MoveKindFrame, text = "?", variable = KindHelp, command = MoveKindHelp)

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
            except Exception as e:
                print(e)
                Argument = 0

            if Argument > 255:
                Argument = 255

            if Argument < 0:
                Argument = 0

            Table[i][tf.ScriptArgIndex] = Argument

            Refresh()
        
    ScriptArgLabel = ttk.Label(ScriptArgFrame, text = "Script Argument:")
    ScriptArgEntry = tk.Text(ScriptArgFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    ScriptArgEntry.bind("<KeyRelease>", lambda e: EditScriptArg(ScriptArgEntry.get(1.0, "end-1c")))

    ArgHelp = tk.IntVar()
    ArgHelp.set(0)

    def ScriptArgHelp():
        ArgHelp.set(0)

        Text = ""
        ScriptOption = d.ScriptArgumentHelpers[MoveScript.get()][0]
        ScriptOptionArgs = d.ScriptArgumentHelpers[MoveScript.get()][1]

        NewValue = tk.StringVar()
        NewValue.set("None")
        mshb.MakeScriptArgHelperBox(Root, "Help", "Script Argument",
                              ["The Script Argument is used for customising Move Scripts.",
                               "This value can range from 0 to 255.",
                               "The helper below is for the currently selected Move Script."],
                              ScriptOption,
                              ScriptOptionArgs,
                              NewValue)

        if NewValue.get() != "None":
            EditScriptArg(NewValue.get())

    ScriptArgHelpButton = ttk.Checkbutton(ScriptArgFrame, text = "?", variable = ArgHelp, command = ScriptArgHelp)

    #------------------------------------------------------------
    # Table Entry hex Viewer
    #------------------------------------------------------------
    TableHexFrame = tk.Frame(EditorFrame, bg = "Black")
    TableHexLabel = ttk.Label(TableHexFrame, text = "Hex Viewer")

    tf.HexBytesize = 20
    HexByteHSpace = 5
    HexByteVSpace = 5

    HexViewFrame = tk.Frame(EditorFrame, bg = "Black")
    MoveScriptByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    BasePowerByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    TypeByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    AccuracyByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    PowerPointByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    EffectChanceByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    RangeByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    PriorityByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    MoveFlagsByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    DamageFormulaByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    MoveKindByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))
    ScriptArgByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", tf.HexBytesize))

    HexHelp = tk.IntVar()
    HexHelp.set(0)

    def HexViewerHelp():
        HexHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Hex Viewer",
                    ["This area shows what the compiled entry looks like in hexadecimal.",
                     "If a byte cannot be properly loaded/compiled, it will show up red."])

    HexHelpButton = ttk.Checkbutton(TableHexFrame, text = "?", variable = HexHelp, command = HexViewerHelp)

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
                         
            Table[CurrentMoveNumber.get()][tf.DescriptionIndex] = NewText
            Refresh()

    TextBoxFrame = tk.Frame(EditorFrame, bg = "Black")
    DescriptionBox = tk.Text(TextBoxFrame, width = 19, height = 4, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    DescriptionBox.bind("<KeyRelease>", (lambda event: ProcessText(DescriptionBox.get(1.0, "end-1c"))))

    DHelp = tk.IntVar()
    DHelp.set(0)

    def DescriptionHelp():
        DHelp.set(0)
        mb.MakeInfoBox(Root, "Help", "Move Description",
                    ["This is the description of the Move seen in the Move Viewer in game.",
                     "This can be up to four lines long, with 19 characters per line.",
                     "The Move Description is compiled into a separate table."])

    DescriptionHelpButton = ttk.Checkbutton(DescriptionLabelFrame, text = "?", variable = DHelp, command = DescriptionHelp)

    #------------------------------------------------------------
    # Make the display update function
    #------------------------------------------------------------
    def CompileToHexViewer():
        try:
            MoveScriptByte.configure(text = MoveScript.get(), foreground = "White")
        except Exception as e:
            print(e)
            MoveScriptByte.configure(text = "00", foreground = "Red")

        try:
            BasePowerByte.configure(text = ConvertToHex(BasePower.get()), foreground = "White")
        except Exception as e:
            print(e)
            BasePowerByte.configure(text = "00", foreground = "Red")

        try:
            TypeByte.configure(text = tf.TypeConversion[Type.get()], foreground = "White")
        except Exception as e:
            print(e)
            TypeByte.configure(text = "00", foreground = "Red")

        try:
            AccuracyByte.configure(text = ConvertToHex(Accuracy.get()), foreground = "White")
        except Exception as e:
            print(e)
            AccuracyByte.configure(text = "00", foreground = "Red")

        try:
            PowerPointByte.configure(text = ConvertToHex(PowerPoints.get()), foreground = "White")
        except Exception as e:
            print(e)
            PowerPointByte.configure(text = "00", foreground = "Red")

        try:
            EffectChanceByte.configure(text = ConvertToHex(EffectChance.get()), foreground = "White")
        except Exception as e:
            print(e)
            EffectChanceByte.configure(text = "00", foreground = "Red")

        try:
            RangeByte.configure(text = tf.RangeConversion[Range.get()], foreground = "White")
        except Exception as e:
            print(e)
            RangeByte.configure(text = "00", foreground = "Red")
            
        try:
            if Priority.get() != 0:
                if Parity.get() == 1:
                    P = 256 - Priority.get()
                else:
                    P = Priority.get()
            else:
                P = 0

            PriorityByte.configure(text = ConvertToHex(P), foreground = "White")
        except Exception as e:
            print(e)
            PriorityByte.configure(text = "00", foreground = "Red")

        try:
            MoveFlags = [A.get(), B.get(), C.get(), D.get(), E.get(), F.get(), G.get(), H.get()]

            FlagLine = 0
            for i, Flag in enumerate(MoveFlags):
                FlagLine += (128 // 2**i) * Flag
            
            MoveFlagsByte.configure(text = ConvertToHex(FlagLine), foreground = "White")
        except Exception as e:
            print(e)
            MoveFlagsByte.configure(text = "00", foreground = "Red")
            
        try:
            DamageValue = DamageArgument.get()[1] + DamageFormula.get()[1]
            DamageFormulaByte.configure(text = DamageValue, foreground = "White")
        except Exception as e:
            print(e)
            DamageFormulaByte.configure(text = "00", foreground = "Red")
            
        try:
            MoveKindByte.configure(text = tf.KindConversion[MoveKind.get()], foreground = "White")
        except Exception as e:
            print(e)
            MoveKindByte.configure(text = "00", foreground = "Red")
            
        try:
            ScriptArgByte.configure(text = ConvertToHex(ScriptArgument.get()), foreground = "White")
        except Exception as e:
            print(e)
            ScriptArgByte.configure(text = "00", foreground = "Red")

    def SetVariables():
        L = Table[CurrentMoveNumber.get()]

        MoveName.set(L[tf.MoveNameIndex])
        MoveScript.set(L[tf.MoveScriptIndex])
        BasePower.set(L[tf.BasePowerIndex])
        Type.set(L[tf.TypeIndex])
        Accuracy.set(L[tf.AccuracyIndex])
        PowerPoints.set(L[tf.PowerPointIndex])
        EffectChance.set(L[tf.EffectChanceIndex])
        Range.set(L[tf.RangeIndex])
        
        if L[tf.PriorityIndex] < 0:
            Priority.set(abs(L[tf.PriorityIndex]))
            Parity.set(1)
            ParityButton.configure(text = "-")
        else:
            Priority.set(L[tf.PriorityIndex])
            Parity.set(0)
            ParityButton.configure(text = "+")

        A.set(L[tf.MoveFlagIndex][0])
        B.set(L[tf.MoveFlagIndex][1])
        C.set(L[tf.MoveFlagIndex][2])
        D.set(L[tf.MoveFlagIndex][3])
        E.set(L[tf.MoveFlagIndex][4])
        F.set(L[tf.MoveFlagIndex][5])
        G.set(L[tf.MoveFlagIndex][6])
        H.set(L[tf.MoveFlagIndex][7])

        DamageValue = L[tf.DamageFormulaIndex]
        Formula = int(DamageValue, 16) & 15
        Argument = (int(DamageValue, 16) & 240) >> 4

        if Formula < 16:
            DamageFormula.set("0" + hex(Formula).upper()[2:])
        else:
            DamageFormula.set(hex(Formula).upper()[2:])

        if Argument < 16:
            DamageArgument.set("0" + hex(Argument).upper()[2:])
        else:
            DamageArgument.set(hex(Argument).upper()[2:])
        
        MoveKind.set(L[tf.MoveKindIndex])
        ScriptArgument.set(L[tf.ScriptArgIndex])

        Description.set(L[tf.DescriptionIndex])
        
    def Refresh(Desc = False):
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
                
            MoveNameList.append("{} - {}".format(N, Entry[tf.MoveNameIndex]))

        ScriptArgEntry.delete(1.0, "end")
        ScriptArgEntry.insert(1.0, ScriptArgument.get())

        CompileToHexViewer()

        if Desc:
            DescriptionBox.delete(1.0, "end")
            DescriptionBox.insert(1.0, Description.get())

        MoveFinder.configure(values = MoveNameList)
        CurrentMove.set(MoveNameList[CurrentMoveNumber.get()])

    #------------------------------------------------------------
    # Make the buttons in the top row
    #------------------------------------------------------------
    # Make a new table
    def CreateNewFile():
        global Table, InitialFolder

        Sure = tk.BooleanVar()
        mb.MakeYesNoBox(Root, "Warning", "Create a New Table File?", Sure,
                    ["Are you sure you want to make a new table?",
                     "This will overwrite the current one.",
                     "Make sure you have saved it if you would like to keep it."])

        if not Sure.get():
            return
        
        NewFile = fd.asksaveasfile(initialdir = InitialFolder, initialfile = "New Table", defaultextension = ".txt")

        if NewFile is not None:
            global CurrentOpenFile
            CurrentOpenFile = os.path.realpath(NewFile.name)
            InitialFolder = os.path.dirname(CurrentOpenFile)
            CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(NewFile.name)))
            NewFile.close()
            
            Length = ""

            TestLength = tk.IntVar()
            while type(Length) != int:
                TestLength.set(0)
                mb.MakeEntryBox(Root, "Enter A Number", "Number of Moves", TestLength, 1,
                             ["Enter the number of Moves to add to the table."])

                if TestLength.get() < 0:
                    mb.MakeInfoBox(Root, "Error!", "Invalid input!",
                                ["This input is invalid!",
                                 "The number of Moves must be a positive number."])
                    Length = ""

                elif TestLength.get() == 0:
                    mb.MakeInfoBox(Root, "Error!", "Invalid input!",
                                ["This input is invalid!",
                                 "The number of Moves cannot be zero."])
                    Length = ""

                else:
                    Length = TestLength.get()

            if Length > 999:
                Length = 999

            OpenNames = tk.BooleanVar()
            mb.MakeYesNoBox(Root, "Open File", "Open Name File?", OpenNames,
                         ["Would you like to load the names",
                          "of the Moves in the table from a file?"])
                         
            NamesList = ("Move Name\n"*Length).split("\n")[0:-1]

            Table = [[]] * Length
            for i in range(len(Table)):
                Table[i] = ["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]
            
            if OpenNames.get():
                NamesFile = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = [("text files", "*.txt")])
                NamesFile = open(NamesFile, "r")

                InitialFolder = os.path.dirname(os.path.realpath(NamesFile.name))
                
                for i, Name in enumerate(NamesFile.read().splitlines()):
                    if i >= len(Table):
                        NamesList.append("Move Name")
                    
                    NamesList[i] = Name[0:12] # Names can only be 12 characters, so we should truncate

            for i, Name in enumerate(Table):
                Table[i][tf.MoveNameIndex] = NamesList[i]
                
            if len(NamesList) != Length:
                mb.MakeInfoBox(Root, "Warning!", "Warning!",
                            ["The length of the name list is different than the length of the table.",
                             "The current number of Moves is {}.".format(len(Table))])

            mb.MakeInfoBox(Root, "Success!", "The table was created!",
                    ["The table was created successfully.",
                     "It has {} Moves in total.".format(len(Table))])

            CurrentMoveNumber.set(0)
            EnableEverything()
            Refresh(True)

    NewFileButton = ttk.Button(ButtonFrame, text = "New Table", command = CreateNewFile)
    
    # Open a table from a text file
    def OpenFile():
        global CurrentOpenFile, InitialFolder
        MenuText = {"Human-Readable": ["This type of table is a plain text file."],
                    "Compiled":["This type of table is a hex binary file."]}

        Option = tk.StringVar()
        Option.set("Human-Readable")
        mb.MakeMultiChoiceBox(Root, "Pick A Choice", "Which type of table?", Option,
                           ["You may open a human-readable or a compiled table."
                            "Please select one."], MenuText, "Human-Readable")

        if Option.get() == "Compiled":
            FileType = [("binary hex file", "*.bin")]
        elif Option.get() == "Human-Readable":
            FileType = [("text files", "*.txt")]
        else:
            return

        NewFile = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = FileType)
        
        if NewFile != "":
            if Option.get() == "Compiled": # Make new file
                FileName = NewFile.replace(".bin", " Opened.txt")
                open(FileName, "w").close()
                NewFile = open(NewFile, "rb")
                
            else:
                FileName = NewFile
                NewFile = open(FileName, "r")
                
            CurrentOpenFile = os.path.realpath(FileName)
            InitialFolder = os.path.dirname(CurrentOpenFile)
            CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(FileName)))
            
            global Table
            Table = []

            Error = ""

            if Option.get() == "Compiled": # Load from bytes, this is easier
                FileBytes = CreateFileBytes(NewFile, 12)

                Table, Error = tf.MakeTableFromCompiled(FileBytes, Error)

                Sure = tk.BooleanVar()
                mb.MakeYesNoBox(Root, "Open Table", "Open compiled Move Name Table?", Sure,
                             ["Would you like to load the Move Names from",
                              "a COMPILED Move Name Table?"])

                if Sure.get(): # Load Move Name Table
                    NameFile = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = [("binary hex file", "*.bin")])

                    if NameFile is not None:
                        InitialFolder = os.path.dirname(os.path.realpath(NameFile))
                        Table = tf.ParsePointerTable(NameFile, Table, "Name")

                Sure = tk.BooleanVar()
                mb.MakeYesNoBox(Root, "Open Table", "Open compiled Move Description Table?", Sure,
                             ["Would you like to load the Move Description from",
                              "a COMPILED Move Description Table?"])

                if Sure.get(): # Load Move Name Table
                    DescFile = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = [("binary hex file", "*.bin")])

                    if DescFile is not None:
                        InitialFolder = os.path.dirname(os.path.realpath(DescFile))
                        Table = tf.ParsePointerTable(DescFile, Table, "Description")

            else: # Parse from text, only needs one file
                FileStuff = NewFile.read().split("\n\n")
                Table, Error = tf.MakeTableFromText(FileStuff, Error)

            # Post-process the table and load any error messages encountered
            Table = tf.ProcessTable(Root, Table)
            tf.LoadTableErrors(Root, Table, Error)

            # Refresh the screen
            CurrentMoveNumber.set(0)
            EnableEverything()
            Refresh(True) 
            EnableEverything()
            
        else:
            return

    OpenFileButton = ttk.Button(ButtonFrame, text = "Open Table", command = OpenFile)

    # Write current table to the currently opened file
    def SaveFile(Table, FileName, Silent = False):
        TableText = ""

        for Entry in Table:
            for i, Item in enumerate(Entry):
                if i == tf.MoveNameIndex:
                    TableText += "{}\n".format(Item)
                    continue

                if i == tf.MoveScriptIndex:
                    TableText += "(Move Script) 0x{}\n".format(Item)
                    continue
                            
                if i == tf.BasePowerIndex:
                    TableText += "(Base Power) {}\n".format(Item)
                    continue
                
                if i == tf.TypeIndex:
                    TableText += "(Type) {}\n".format(Item)
                    continue
                            
                if i == tf.AccuracyIndex:
                    TableText += "(Accuracy) {}\n".format(Item)
                    continue
                            
                if i == tf.PowerPointIndex:
                    TableText += "(Power Points) {}\n".format(Item)
                    continue
                            
                if i == tf.EffectChanceIndex:
                    TableText += "(Effect Chance) {}\n".format(Item)
                    continue
                            
                if i == tf.RangeIndex:
                    TableText += "(Range) {}\n".format(Item)
                    continue
                            
                if i == tf.PriorityIndex:
                    if int(Item) < 0: # Negative value, subtract from 256 first
                        Item = 256 + int(Item)
                                
                    TableText += "(Priority) {}\n".format(Item)
                    continue
                            
                if i == tf.MoveFlagIndex:
                    FlagValue = ""
                            
                    for i, Flag in enumerate(Item):
                        FlagValue += " {} +".format(hex(128 // 2**i * Flag))

                    FlagValue = FlagValue[:-1]
                                
                    TableText += "(Move Flags) {}\n".format(FlagValue)
                    continue
                            
                if i == tf.DamageFormulaIndex:
                    TableText += "(Damage Formula) 0x{}\n".format(Item)
                    continue
                            
                if i == tf.MoveKindIndex:
                    TableText += "(Kind) {}\n".format(Item)
                    continue
                            
                if i == tf.ScriptArgIndex:
                    TableText += "(Script Arg) {}\n".format(Item)
                    continue

                if i == tf.DescriptionIndex:
                    Item = Item.strip().replace("\n", " | ")
                    TableText += "(Description) {}\n\n".format(Item.strip())

        NewFile = open(FileName, "w")
        NewFile.write(TableText.strip())
        NewFile.close()

        if not Silent:
            mb.MakeInfoBox(Root, "Complete", "Table Saved!",
                        ["The current table was successfully saved!"])

    SaveButton = ttk.Button(ButtonFrame, text = "Save Table", command = lambda: SaveFile(Table, CurrentOpenFile))

    # Save the current table to a new file
    def SaveFileAs():
        global CurrentOpenFile, InitialFolder
        Edit = tk.BooleanVar()
        mb.MakeYesNoBox(Root, "New File", "Save A Copy", Edit,
                    ["Would you like to switch to editing the new file",
                     "after you save a copy of this one?"])
        
        NewFile = fd.asksaveasfile(initialdir = InitialFolder, initialfile = "New Table", defaultextension = ".txt")

        if NewFile is not None:        
            if not Edit.get():
                TempFile = CurrentOpenFile
                CurrentOpenFile = os.path.realpath(NewFile.name)
                InitialFolder = os.path.dirname(CurrentOpenFile)
                SaveFile()
                NewFile.close()
                CurrentOpenFile = TempFile
                CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(CurrentOpenFile)))
            else:
                CurrentOpenFile = os.path.realpath(NewFile.name)
                InitialFolder = os.path.dirname(CurrentOpenFile)
                CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(NewFile.name)))
                NewFile.close()
                SaveFile()

    SaveAsButton = ttk.Button(ButtonFrame, text = "Save Table As", command = SaveFileAs)

    # Compile to bytes
    def CompileTable(Table):
        global InitialFolder
        Option = tk.StringVar()

        MenuText = {"Attack Data Table": ["This is the main Attack Data Table.",
                                          "This can be completely compiled without needing an address."],
                    "Move Name Table": ["This is the table of pointers for Move Names",
                                        "This requires an address beforehand."],
                    "Move Description Table": ["This is the table of pointers for Move Descriptions",
                                        "This requires an address beforehand."]}

        mb.MakeMultiChoiceBox(Root, "Pick A Choice", "Which table should be compiled?", Option,
                           ["There are three possible tables which could be compiled."
                            "Please select one."], MenuText)

        if Option.get() == "Attack Data Table":
            NewFile = fd.asksaveasfile(initialdir = InitialFolder, initialfile = "Compiled ADT", defaultextension = ".bin")

            if NewFile is not None:
                FileName = os.path.realpath(NewFile.name)
                InitialFolder = os.path.dirname(FileName)
                NewFile.close()

                NewFile = open(FileName, "wb")

                ByteList = []
                for Entry in Table:
                    ByteList.append(int(Entry[tf.MoveScriptIndex], 16))
                    ByteList.append(Entry[tf.BasePowerIndex])
                    ByteList.append(int(tf.TypeConversion[Entry[tf.TypeIndex]], 16))
                    ByteList.append(Entry[tf.AccuracyIndex])
                    ByteList.append(Entry[tf.PowerPointIndex])
                    ByteList.append(Entry[tf.EffectChanceIndex])
                    ByteList.append(int(tf.RangeConversion[Entry[tf.RangeIndex]], 16))

                    if Entry[tf.PriorityIndex] < 0:
                        P = 256 + Entry[tf.PriorityIndex]
                    else:
                        P = Entry[tf.PriorityIndex]
                        
                    ByteList.append(P)

                    FlagLine = 0
                    for i, Flag in enumerate(Entry[tf.MoveFlagIndex]):
                        FlagLine += (128 // 2**i) * Flag

                    ByteList.append(FlagLine)
                    ByteList.append(int(Entry[tf.DamageFormulaIndex], 16))
                    ByteList.append(int(tf.KindConversion[Entry[tf.MoveKindIndex]], 16))
                    ByteList.append(Entry[tf.ScriptArgIndex])

                NewFile.write(bytes(ByteList))
                NewFile.close()
                mb.MakeInfoBox(Root, "Success", "Compilation complete!",
                            ["The table was compiled to a file successfully!"])

        else:
            if Option.get() == "Move Name Table":
                SplitPoint = 13
                FileName = "Compiled Names"
            else:
                SplitPoint = 77
                FileName = "Compiled Descriptions"

            NewFile = fd.asksaveasfile(initialdir = InitialFolder, initialfile = FileName, defaultextension = ".bin")

            if NewFile is not None:
                Address = tk.StringVar()
                mb.MakeAddressEntryBox(Root, "Enter Address", "Enter the starting address", Address,
                                    ["Enter the starting address for the table in the following form:",
                                     "08AABBCC",
                                     "Where AABBCC is a placeholder for the offset of your table.",
                                     "Use placeholder 0's (i.e. 0x12345 -> 08012345)"])

                Extend = tk.BooleanVar()
                mb.MakeYesNoBox(Root, "Question", "Future-proof the table?", Extend,
                             ["Would you like to future proof the table?",
                              "This makes each string of text the maximum length",
                              "it can be, with extra bytes being written as 00.",
                              "This takes up more space now, but will let you avoid",
                              "repointing the table later if you change string lengths."])

            if NewFile is not None:
                FileName = NewFile.name
                InitialFolder = os.path.dirname(FileName)
                NewFile.close()

                NewFile = open(FileName, "wb")

                TextByteList = []
                PointerByteList = []

                FirstPointerAddress = int(Address.get(), 16) + 4 * len(Table)
                P = FirstPointerAddress
                
                for N, Entry in enumerate(Table):
                    if Option.get() == "Move Name Table":
                        Text = Entry[tf.MoveNameIndex]
                    else:
                        Text = Entry[tf.DescriptionIndex]

                    if Extend.get():
                        Array = [0] * SplitPoint
                        ArrayLength = SplitPoint
                    else:
                        Array = [0] * (len(Text) + 1)
                        ArrayLength = len(Text) + 1

                    if len(Text) == 0:
                            Text = "A"
                            Array = [0, 0]
                            ArrayLength = 2

                    for i, Letter in enumerate(Text):
                        try:
                            Array[i] = int(tf.TextToBytes[Letter], 16)
                        except:
                            pass

                    Array[i+1] = 255

                    for Byte in Array:
                        TextByteList.append(Byte)
                       
                    PointerByteList.append((P & 4278190080) >> 24)
                    PointerByteList.append((P & 16711680) >> 16)
                    PointerByteList.append((P & 65280) >> 8)
                    PointerByteList.append(P & 255)

                    P = P + ArrayLength
                            
                NewFile.write(bytes(PointerByteList))
                NewFile.write(bytes(TextByteList))
                NewFile.close()
                mb.MakeInfoBox(Root, "Success", "Compilation complete!",
                            ["The table was compiled to a file successfully!"])

    CompileButton = ttk.Button(ButtonFrame, text = "Compile Table", command = lambda: CompileTable(Table))

    ButtonHSpacing = 30
    ButtonVSpacing = 5

    # Convert an old form table to a new form table
    def ConvertTable():
        global InitialFolder
        Sure = tk.BooleanVar()
        mb.MakeYesNoBox(Root,  "Convert Table?", "Convert an old table?", Sure,
                    ["Convert a compiled gen 3 table to the ACE format?",
                     "This changes Move Scripts and Move Ranges and attempts",
                     "to assign the correct Damage Formula and Script Argument",
                     "values to what they should be by default in the ACE engine.",
                     "This assumes that scripts are unedited from the default.",
                     "Results may not be entirely correct or incomplete."])

        if not Sure.get():
            return
        else:
            OldTable = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = [("binary hex file", "*.bin")])
            if OldTable == "": # Cancelled opening file
                return

            OldFile = open(OldTable, "rb")
            InitialFolder = os.path.dirname(os.path.realpath(OldFile.name))

            FileName = os.path.basename(OldFile.name.replace(".bin", "")) # Base name of the file w/o extension
            DirName = os.path.dirname(OldFile.name) # Path of the directory the file is in

            CurrentFolderName = os.path.basename(os.path.dirname(os.path.realpath(OldFile.name))) # Base name of the directory file is in
            NewFolderName = "Converted - {}".format(FileName) # Base name of directory to create

            if CurrentFolderName != NewFolderName: # The correct folder is not the current one
                NewFolder = os.path.join(DirName, NewFolderName) # Path of new subfolder to use

                if not os.path.exists(NewFolder): # if the folder doesn't exist, create it
                    os.makedirs(NewFolder)

                MovedFile = os.path.join(NewFolder, os.path.basename(OldTable)) # path of the new location of the file
                shutil.move(OldTable, OldCompiled)

                mb.MakeInfoBox(Root, "Announcement!", "Old Table Moved",
                               ["The old table file that you just opened was",
                                "moved to the same folder as the new table.",
                                "{}".format(NewFolder)])

                CurrentFolder = NewFolder

            else:
                CurrentFolder = InitialFolder

            NewCompiled = os.path.join(CurrentFolder, "Converted {}.bin".format(FileName))
            NewText = os.path.join(CurrentFolder, "Converted {}.txt".format(FileName))

            # Convert Compiled Old to Compiled New
            FileBytes = CreateFileBytes(OldFile, 12)

            NewTableString = ""
            for Line in FileBytes.split("\n"):
                Entry = Line.split()
                Script = ""
                
                for i, Byte in enumerate(Entry):
                    Byte = Byte.strip()

                    match i:
                        case 0: # Move Script
                            if Byte in d.OldToNewScripts:
                                NewTableString += d.OldToNewScripts[Byte] + " "
                            else:
                                NewTableString += Byte + " "

                            Script = Byte
                        
                        case 6: # Move Range
                            if Byte in d.OldToNewRanges:
                                NewTableString += d.OldToNewRanges[Byte] + " "
                            else:
                                NewTableString += Byte + " "
                        
                        case 8: # Move Flags
                            if Script in d.SelfEffectFlagList:
                                NewTableString += hex(int(Byte, 16) + 64).upper()[2:] + " "
                            else:
                                NewTableString += Byte + " "

                        case 9: # Damage Formula
                            if Script in d.OldToNewDamageFormula:
                                NewTableString += d.OldToNewDamageFormula[Script] + " "
                            else:
                                NewTableString += Byte + " "

                        case 11: # Script Argument
                            if Script in d.OldToNewArguments:
                                NewTableString += d.OldToNewArguments[Script] + " "
                            else:
                                NewTableString += Byte + " "

                        case _:
                            NewTableString += Byte + " "

            NewTableString = NewTableString.strip()

            NewFile = open(NewCompiled, "wb")
            BytesToWrite = [int(i, 16) for i in NewTableString.split(" ")]
            NewFile.write(bytes(BytesToWrite))
            NewFile.close()

            # Save the human-readable version
            CompiledFile = open(NewCompiled, "rb")
            FileBytes = CreateFileBytes(CompiledFile, 12)
            
            Error = ""
            NewTable, Error = tf.MakeTableFromCompiled(FileBytes, Error)

            Names = tk.BooleanVar()
            mb.MakeYesNoBox(Root, "Open Name File?", "Conversion Success!", Names,
                            ["The table was converted successfully!",
                             "Would you like to open a HUMAN-READABLE name file",
                             "for the new table?"])

            if Names.get():
                Length = len(NewTable)
                         
                NamesList = ("Move Name\n"*Length).split("\n")[0:-1]
                NamesFile = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = [("text files", "*.txt")])
                NamesFile = open(NamesFile, "r")

                InitialFolder = os.path.dirname(os.path.realpath(NamesFile.name))
                
                for i, Name in enumerate(NamesFile.read().splitlines()):
                    if i >= len(NewTable):
                        NamesList.append("Move Name")
                    
                    NamesList[i] = Name[0:12] # Names can only be 12 characters, so we should truncate

                for i, Name in enumerate(NewTable):
                    NewTable[i][tf.MoveNameIndex] = NamesList[i]
                    
                if len(NamesList) != Length:
                    mb.MakeInfoBox(Root, "Warning!", "Warning!",
                                ["The length of the name list is different than the length of the table.",
                                 "The current number of Moves is {}.".format(len(NewTable))])

            SaveFile(NewTable, NewText, True)

            OpenNew = tk.BooleanVar()
            mb.MakeYesNoBox(Root, "Open File", "Open newly converted table?", OpenNew,
                            ["Conversion success!",
                             "Would you like to open the newly converted table",
                             "in the editor?"])

            if OpenNew.get():
                global Table, CurrentOpenFile
                NewFile = open(NewText, "r")
                CurrentOpenFile = os.path.realpath(NewText)
                InitialFolder = os.path.dirname(CurrentOpenFile)
                CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(NewText)))

                Table = []
                Error = ""
                FileStuff = NewFile.read().split("\n\n")
                Table, Error = tf.MakeTableFromText(FileStuff, Error)
                
                Table = tf.ProcessTable(Root, Table)
                tf.LoadTableErrors(Root, Table, Error)
                
                CurrentMoveNumber.set(0)
                EnableEverything()
                Refresh(True) 
                EnableEverything()
              
    ConvertButton = ttk.Button(ButtonFrame, text = "Convert Table", command = ConvertTable)

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
        Refresh(True)

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
        Refresh(True)

    ForwardButton = ttk.Button(ButtonFrame, text = "Forward", command = GoForward)

    # Add a move
    def AddMove():
        global Table
        Table.append(["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""])
        CurrentMoveNumber.set(len(Table) - 1)

    def AddMoves():
        Length = ""

        TestLength = tk.IntVar()
        while type(Length) != int:
            TestLength.set(0)
            mb.MakeEntryBox(Root, "Enter A Number", "Number of Moves", TestLength, 1,
                         ["Enter the number of Moves to add to the table."])

            if TestLength.get() < 0:
                mb.MakeInfoBox(Root, "Error!", "Invalid input!",
                            ["This input is invalid!",
                             "The number of Moves must be a positive number."])
                Length = ""

            else:
                Length = TestLength.get()

        for i in range(Length):
            AddMove()

        if CurrentMoveNumber.get() > 0:
            BackButton.configure(state = "normal")

        ForwardButton.configure(state = "disabled")

        if Length != 0:
            mb.MakeInfoBox(Root, "Success!", "A new Move was added!",
                        ["The table was modified successfully.",
                         "There are now {} Moves in total.".format(len(Table))])

            Refresh(True)     

    AddMoveButton = ttk.Button(ButtonFrame, text = "Add Moves", command = AddMoves)

    # Delete a Move
    def DeleteMove():
        global Table

        Sure = tk.BooleanVar()
        Sure.set(False)
        mb.MakeYesNoBox(Root, "Warning!", "Warning!", Sure,
                     ["You are about to remove the current Move from the table.",
                      "This action cannot be undone.",
                      "Would you still like to proceed?"])

        if Sure.get():
            if len(Table) == 1: # Only one Move left
                mb.MakeInfoBox(Root, "Error", "Warning!",
                            ["This is the only Move left in the table!",
                             "It cannot be fully deleted.",
                             "It will instead be replaced with an empty Move."])

                Table = [["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]]
                Refresh()
                
            else:
                i = CurrentMoveNumber.get()
                Table.pop(i)

                if i > len(Table) - 1:
                    CurrentMoveNumber.set(len(Table) - 1)

                Refresh(True)

    DeleteMoveButton = ttk.Button(ButtonFrame, text = "Delete Move", command = DeleteMove)

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
        DamageArgumentEntry.configure(state = "disabled")
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
        DamageArgumentHelpButton.configure(state = "disabled")
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
        DamageArgumentEntry.configure(state = "normal")
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
        DamageArgumentHelpButton.configure(state = "normal")
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
    # Place everything
    #------------------------------------------------------------
    # Icon Frame
    BulbasaurFrame.pack(side = "left", padx = 50)
    BulbasaurLabel.pack()
    
    IconFrame.pack(side = "left", padx = 10)
    LabelFrame.pack(pady = 10)
    MainLabel.pack()
    CopyrightLabel.pack()

    TablePicFrame.pack(side = "left", padx = 30)
    TableLabel.pack()

    MenuFrame.pack()
    CurrentLabel.pack(pady = 5)
    MoveFinderFrame.pack()
    ShowHelpButton.pack(side = "left", pady = 5)
    MoveFinder.pack(side = "left", pady = 5)
    MoveNumberLabel.pack(pady = 5)

    # Button Frame
    NewFileButton.grid(row = 0, column = 0, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = "w")
    OpenFileButton.grid(row = 0, column = 1, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = "w")
    ConvertButton.grid(row = 0, column = 2, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = "w")
    SaveButton.grid(row = 0, column = 3, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = "w")
    SaveAsButton.grid(row = 0, column = 4, padx = ButtonHSpacing, pady = ButtonVSpacing, sticky = "w")

    AddMoveButton.grid(row = 1, column = 0, padx = ButtonHSpacing, sticky = "w")
    BackButton.grid(row = 1, column = 1, padx = ButtonHSpacing, sticky = "w")
    CompileButton.grid(row = 1, column = 2, padx = ButtonHSpacing, sticky = "w")
    ForwardButton.grid(row = 1, column = 3, padx = ButtonHSpacing, sticky = "w")
    DeleteMoveButton.grid(row = 1, column = 4, padx = ButtonHSpacing, sticky = "w")

    # Editor Frame
    MoveNameFrame.grid(row = 0, column = 1, padx = 15, pady = 5, sticky = "w")
    MoveNameHelpButton.pack(side = "left")
    MoveNameLabel.pack(side = "left", padx = (0,5))
    MoveNameEntry.pack(side = "left")

    MoveScriptFrame.grid(row = 1, column = 0, padx = 15, pady = 5, sticky = "w")
    MoveScriptHelpButton.pack(side = "left")
    MoveScriptLabel.pack(side = "left", padx = (0,5))
    MoveScriptEntry.pack(side = "left")

    BasePowerFrame.grid(row = 1, column = 1, padx = 15, pady = 5, sticky = "w")
    BasePowerHelpButton.pack(side = "left")
    BasePowerLabel.pack(side = "left", padx = (0,5))
    BasePowerEntry.pack(side = "left")

    TypeFrame.grid(row = 1, column = 2, padx = 15, pady = 5, sticky = "w")
    TypeHelpButton.pack(side = "left")
    TypeLabel.pack(side = "left", padx = (0,5))
    TypeEntry.pack(side = "left")

    AccuracyFrame.grid(row = 2, column = 0, padx = 15, pady = 5, sticky = "w")
    AccuracyHelpButton.pack(side = "left")
    AccuracyLabel.pack(side = "left", padx = (0,5))
    AccuracyEntry.pack(side = "left")

    PowerPointFrame.grid(row = 2, column = 1, padx = 15, pady = 5, sticky = "w")
    PowerPointHelpButton.pack(side = "left")
    PowerPointLabel.pack(side = "left", padx = (0,5))
    PowerPointEntry.pack(side = "left")

    EffectChanceFrame.grid(row = 2, column = 2, padx = 15, pady = 5, sticky = "w")
    EffectChanceHelpButton.pack(side = "left")
    EffectChanceLabel.pack(side = "left", padx = (0,5))
    EffectChanceEntry.pack(side = "left")

    RangeFrame.grid(row = 3, column = 0, padx = 15, pady = 5, sticky = "w")
    RangeHelpButton.pack(side = "left")
    RangeLabel.pack(side = "left", padx = (0,5))
    RangeEntry.pack(side = "left")

    PriorityFrame.grid(row = 3, column = 2, padx = 15, pady = 5, sticky = "w")
    PriorityHelpButton.pack(side = "left")
    PriorityLabel.pack(side = "left", padx = (0,5))
    ParityButton.pack(side = "left")
    PriorityEntry.pack(side = "left")

    MoveKindFrame.grid(row = 3, column = 1, padx = 15, pady = 5, sticky = "w")
    MoveKindHelpButton.pack(side = "left")
    MoveKindLabel.pack(side = "left", padx = (0,5))
    MoveKindEntry.pack(side = "left")

    DamageFormulaFrame.grid(row = 4, column = 0, padx = 15, pady = 5, sticky = "w")
    DamageFormulaHelpButton.pack(side = "left")
    DamageFormulaLabel.pack(side = "left", padx = (0,5))
    DamageFormulaEntry.pack(side = "left")

    DamageArgumentFrame.grid(row = 4, column = 1, padx = 15, pady = 5, sticky = "w")
    DamageArgumentHelpButton.pack(side = "left")
    DamageArgumentLabel.pack(side = "left", padx = (0,5))
    DamageArgumentEntry.pack(side = "left")

    ScriptArgFrame.grid(row = 4, column = 2, padx = 15, pady = 5, sticky = "w")
    ScriptArgHelpButton.pack(side = "left")
    ScriptArgLabel.pack(side = "left", padx = (0, 5))
    ScriptArgEntry.pack(side = "left")

    MoveFlagLabelFrame.grid(row = 5, column = 0, padx = 15, pady = (5,0), sticky = "w")
    MoveFlagHelpButton.pack(side = "left")
    MoveFlagLabel.pack(side = "left")

    MoveFlagFrame.grid(row = 6, column = 0, padx = 15, pady = 5, sticky = "w")
    SetAbilityFlag.grid(row = 0, column = 0, sticky = "w")
    SetSelfFlag.grid(row = 0, column = 1, sticky = "w")
    SetKingsRockFlag.grid(row = 1, column = 0, sticky = "w")
    SetMirrorMoveFlag.grid(row = 1, column = 1, sticky = "w")
    SetSnatchFlag.grid(row = 2, column = 0, sticky = "w")
    SetMagicCoatFlag.grid(row = 2, column = 1, sticky = "w")
    SetProtectFlag.grid(row = 3, column = 0, sticky = "w")
    SetDirectContactFlag.grid(row = 3, column = 1, sticky = "w")

    TableHexFrame.grid(row = 5, column = 1, padx = 15, pady = 5, sticky = "w")
    HexHelpButton.pack(side = "left")
    TableHexLabel.pack(side = "left")

    HexViewFrame.grid(row = 6, column = 1, padx = 15, pady = 5, sticky = "w")
    MoveScriptByte.grid(row = 0, column = 0, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    BasePowerByte.grid(row = 0, column = 1, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    TypeByte.grid(row = 0, column = 2, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    AccuracyByte.grid(row = 0, column = 3, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    PowerPointByte.grid(row = 0, column = 4, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    EffectChanceByte.grid(row = 0, column = 5, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    
    RangeByte.grid(row = 1, column = 0, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    PriorityByte.grid(row = 1, column = 1, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    MoveFlagsByte.grid(row = 1, column = 2, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    DamageFormulaByte.grid(row = 1, column = 3, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    MoveKindByte.grid(row = 1, column = 4, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")
    ScriptArgByte.grid(row = 1, column = 5, padx = HexByteHSpace, pady = HexByteVSpace, sticky = "w")

    DescriptionLabelFrame.grid(row = 5, column = 2, padx = 15, pady = 5, sticky = "w")
    DescriptionHelpButton.pack(side = "left")
    DescriptionLabel.pack(side = "left")

    TextBoxFrame.grid(row = 6, column = 2, padx = 15, pady = 5, sticky = "w")
    DescriptionBox.pack()

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
        SaveFile(Table, CurrentOpenFile)

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

except Exception as e:
    print("Crash alert!")
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
