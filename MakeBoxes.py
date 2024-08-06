import platform
import tkinter as tk
from tkinter import ttk

SmallSize = 16

if(platform.system() == 'Darwin'): # This is a Mac
    Paste = "<Command-v>"
else:
    Paste = "<Control-v>"

#------------------------------------------------------------
# Make Info Box
#------------------------------------------------------------
def MakeInfoBox(Root, Title, Header, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = "w")

    def QuitBox(Event = None):
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = QuitBox)
    OkayButton.pack()

    Top.bind("<Return>", QuitBox)
    Top.wait_window()

#------------------------------------------------------------
# Make Yes/No Box
#------------------------------------------------------------
def MakeYesNoBox(Root, Title, Header, Var, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Arial", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Arial", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = "w")

    def SetYes(Event = None):
        Var.set(True)
        Top.destroy()

    def SetNo():
        Var.set(False)
        Top.destroy()

    YesButton = ttk.Button(OkayFrame, text = "Yes", command = SetYes)
    YesButton.pack()

    NoButton = ttk.Button(OkayFrame, text = "No", command = SetNo)
    NoButton.pack()

    Top.bind("<Return>", SetYes)
    Top.wait_window()

#------------------------------------------------------------
# Make Entry Box
#------------------------------------------------------------
def MakeEntryBox(Root, Title, Header, Var, Type, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)

    PromptFrame = tk.Frame(Top, bg = "Black")
    PromptFrame.pack(fill = "x", pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Arial", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Arial", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = "w")
    
    def ProcessEntry(Text):
        try:
            N = type(Type)(Text)
            OkayButton.configure(state = "normal")
            
        except Exception as e:
            print(e)
            PromptEntry.delete(1.0, "end-1c")
            PromptEntry.insert(1.0, Text[:-1])           
    
    PromptEntry = tk.Text(PromptFrame, width = 20, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    PromptEntry.bind("<KeyRelease>", (lambda event: ProcessEntry(PromptEntry.get(1.0, "end-1c"))))
    PromptEntry.bind(Paste, lambda _: "break")
    PromptEntry.pack()

    def SetValue(Event = None):
        PromptNumber = PromptEntry.get(1.0, "end-1c")
        Var.set(PromptNumber)
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = SetValue)
    OkayButton.configure(state = "disabled")
    OkayButton.pack()

    Top.bind("<Return>", SetValue)
    Top.wait_window()
    
#------------------------------------------------------------
# Make Address Entry Box
#------------------------------------------------------------
def MakeAddressEntryBox(Root, Title, Header, Var, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)

    PromptFrame = tk.Frame(Top, bg = "Black")
    PromptFrame.pack(fill = "x", pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Arial", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Arial", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = "w")

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

    def SetValue(Event = None):
        PromptNumber = PromptEntry.get(1.0, "end-1c")
        Var.set(PromptNumber)
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = SetValue)
    OkayButton.configure(state = "disabled")
    OkayButton.pack()

    Top.bind("<Return>", SetValue)
    Top.wait_window()
    
#------------------------------------------------------------
# Make Info Box With Menu
#------------------------------------------------------------
def MakeInfoBoxWithMenu(Root, Title, Header, Text, MenuText, Var = None, Initial = None):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)

    MenuTextFrame = tk.Frame(Top, bg = "Black")
    MenuTextFrame.pack(fill = "x", pady = 10)

    MenuFrame = tk.Frame(Top, bg = "Black")
    MenuFrame.pack(fill = "x", pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = "w")

    DoLine = ttk.Label(MenuTextFrame, text = "-----", font = ("Courier", SmallSize))
    DoLine.pack()

    Values = []
    for Key in MenuText:
        Values.append(Key)

    Option = tk.StringVar()

    if Initial is None:
        Option.set("-")
    else:
        Option.set(Initial)
    
    def ChangeText():
        List = MenuText[Option.get()]

        for Widget in MenuTextFrame.winfo_children():
            Widget.destroy()

        ttk.Label(MenuTextFrame, text = "-----\n", font = ("Courier", SmallSize)).pack()

        for Line in List:
            ttk.Label(MenuTextFrame, text = Line, font = ("Courier", SmallSize)).pack()

    MenuDropDown = ttk.Combobox(MenuFrame, textvariable = Option, width = 20, values = Values, font = ("Courier", SmallSize))      
    MenuDropDown.bind("<<ComboboxSelected>>", lambda _: ChangeText())
    MenuDropDown.pack()
    ChangeText()

    def QuitBox(Event = None):
        if Var is not None:
            Var.set(Option.get())
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Done", command = QuitBox)
    OkayButton.pack()

    Top.bind("<Return>", QuitBox)
    Top.wait_window()
    
#------------------------------------------------------------
# Make Info Box With Menu And Search Bar
#------------------------------------------------------------
def MakeInfoBoxMenuSearch(Root, Title, Header, Text, MenuText, Var = None, Initial = None):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)

    MenuTextFrame = tk.Frame(Top, bg = "Black")
    MenuTextFrame.pack(fill = "x", pady = 10)

    SearchFrame = tk.Frame(Top, bg = "Black")
    SearchFrame.pack(pady = 10)

    MenuFrame = tk.Frame(Top, bg = "Black")
    MenuFrame.pack(fill = "x", pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = "w")

    DoLine = ttk.Label(MenuTextFrame, text = "-----", font = ("Courier", SmallSize))
    DoLine.pack()

    Values = []
    for Key in MenuText:
        Values.append(Key)

    Option = tk.StringVar()

    if Initial is None:
        Option.set("Script 00")
    else:
        Option.set(Initial)

    for i in range(4):
        ttk.Label(MenuTextFrame, text = "", font = ("Courier", SmallSize)).pack()

    def ChangeText():
        List = MenuText[Option.get()]

        for Widget in MenuTextFrame.winfo_children():
            Widget.destroy()

        ttk.Label(MenuTextFrame, text = "-----\n", font = ("Courier", SmallSize)).pack()

        for Line in List:
            ttk.Label(MenuTextFrame, text = Line, font = ("Courier", SmallSize)).pack()

    MenuDropDown = ttk.Combobox(MenuFrame, textvariable = Option, width = 20, values = Values, font = ("Courier", SmallSize))      
    MenuDropDown.bind("<<ComboboxSelected>>", lambda e: ChangeText())
    MenuDropDown.pack()
    ChangeText()

    def ProcessEntry(Text):
        Values = []
        for Key in MenuText:
            if Text.lower() in " ".join(MenuText[Key]).lower():
                Values.append(Key)

        MenuDropDown.configure(values = Values)

        if Text == "":
            ResultsLabel.configure(text = "")
        else:
            ResultsLabel.configure(text = "Found {} results".format(len(Values)))
        
        if len(Values) > 0:
            Option.set(Values[0])
        else:
            Option.set("Script 00")
            
        ChangeText()

    Cleared = tk.IntVar()
    Cleared.set(0)
    def ClearSearch():
        Cleared.set(0)
        SearchBar.delete(1.0, "end-1c")

        Values = []
        for Key in MenuText:
            Values.append(Key)

        MenuDropDown.configure(values = Values)
        ResultsLabel.configure(text = "")
        Option.set(Values[0])

    ResultsLabel = ttk.Label(SearchFrame, text = "", font = ("Courier", SmallSize))
    ResultsLabel.pack()

    BarFrame = tk.Frame(SearchFrame, bg = "Black")
    BarFrame.pack(pady = 5)
    
    SearchBar = tk.Text(BarFrame, width = 20, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    SearchBar.bind("<KeyRelease>", (lambda event: ProcessEntry(SearchBar.get(1.0, "end-1c"))))
    SearchClear = ttk.Checkbutton(BarFrame, text = "X", variable = Cleared, command = ClearSearch)
    SearchClear.pack(side = "left", padx = 5)
    SearchBar.pack(side = "left")
    
    def QuitBox(Event = None):
        if Var is not None:
            Var.set(Option.get())
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Done", command = QuitBox)
    OkayButton.pack()

    Top.bind("<Return>", QuitBox)
    Top.wait_window()

#------------------------------------------------------------
# Make Multi-Choice Box
#------------------------------------------------------------
def MakeMultiChoiceBox(Root, Title, Header, Var, Text, MenuText, InitialOption = "-"):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)

    MenuTextFrame = tk.Frame(Top, bg = "Black")
    MenuTextFrame.pack(fill = "x", pady = 10)

    MenuFrame = tk.Frame(Top, bg = "Black")
    MenuFrame.pack(fill = "x", pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = "w")

    DoLine = ttk.Label(MenuTextFrame, text = "-----", font = ("Courier", SmallSize))
    DoLine.pack()

    Values = []
    for Key in MenuText:
        Values.append(Key)

    Option = tk.StringVar()
    
    def ChangeText():
        List = MenuText[Option.get()]

        for Widget in MenuTextFrame.winfo_children():
            Widget.destroy()

        ttk.Label(MenuTextFrame, text = "-----\n", font = ("Courier", SmallSize)).pack()

        for Line in List:
            ttk.Label(MenuTextFrame, text = Line, font = ("Courier", SmallSize)).pack()

        Var.set(Option.get())

    if InitialOption in MenuText:
        Option.set(InitialOption)
        ChangeText()

    MenuDropDown = ttk.Combobox(MenuFrame, textvariable = Option, width = 20, values = Values, font = ("Courier", SmallSize))      
    MenuDropDown.bind("<<ComboboxSelected>>", lambda e: ChangeText())
    MenuDropDown.pack()

    def QuitBox(Event = None):
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = QuitBox)
    OkayButton.pack()

    Top.bind("<Return>", QuitBox)
    Top.wait_window()
