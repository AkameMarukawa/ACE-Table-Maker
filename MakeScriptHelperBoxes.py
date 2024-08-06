import tkinter as tk
import MakeBoxes as mb
import TableFunctions as tf
import Dictionaries as d
from tkinter import ttk

SmallSize = 16

#------------------------------------------------------------
# Amount Entry Helper
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers where the user needs to enter in
a numeric value between two limiting values
-------------------------------------------------------------
"""
def AmountEntry(WidgetFrame, String, LabelText, Low, High, Width, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")

    Amount = tk.IntVar()
    Amount.set(0)

    TextNormal = String.format(Amount.get())
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    ttk.Label(FrameA, text = "Valid values range between {} and {}".format(Low, High), font = ("Courier", SmallSize, "underline")).pack(pady = (0,10))

    def SetAmount(Input):
        try:
            X = int(Input)
            if X < Low:
                X = Low
                
            elif X > High:
                X = High

            Amount.set(X)
            TextLabel.configure(text = String.format(Amount.get()))
            FinalValue.set(X)
            FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
            Changed.set(True)

            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Amount.get())

        except Exception as e:
            print(e)
            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Input[:-1])
            
    AmountLabel = ttk.Label(FrameB, text = LabelText, font = ("Courier", SmallSize)) 
    AmountEntry = tk.Text(FrameB, width = Width, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize)) 
    AmountEntry.bind("<KeyRelease>", lambda _: SetAmount(AmountEntry.get(1.0, "end-1c")))
    AmountEntry.bind(mb.Paste, lambda _: "break")

    AmountEntry.delete(1.0, "end-1c")
    AmountEntry.insert(1.0, Amount.get())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack()
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    AmountLabel.pack(side = "left", padx = 5)
    AmountEntry.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Single Combo Box Helper
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers where the user needs to select
only one value from a predetermined list.
-------------------------------------------------------------
"""
def SingleComboBox(WidgetFrame, String, LabelText, List, FinalValue, Changed, StringList = None, Width = 13):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")

    Var = tk.StringVar()
    Var.set(List[0])

    if StringList is None:
        TextNormal = String.format(Var.get())
    else:
        TextNormal = String + "\n" + StringList[0]
        
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SetVariable():       
        for i, Name in enumerate(List):
            if Var.get() == Name:
                if StringList is None:
                    TextLabel.configure(text = String.format(Var.get()))
                else:
                    TextLabel.configure(text = String + "\n" + StringList[i])
            
                FinalValue.set(i)
                break
            
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    VarLabel = ttk.Label(FrameB, text = LabelText, font = ("Courier", SmallSize)) 
    VarPicker = ttk.Combobox(FrameB, textvariable = Var, width = Width, values = List, font = ("Courier", SmallSize))
    VarPicker.bind("<<ComboboxSelected>>", lambda _: SetVariable())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack()
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    VarLabel.pack(side = "left", padx = 5)
    VarPicker.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Two Combo Boxes
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which use two combo boxes.
-------------------------------------------------------------
"""
def TwoComboBoxes(WidgetFrame, String, LabelTextA, LabelTextB, ListA, ListB, FinalValue, Changed, StringList = None, Width = 13, FlagBits = [240, 15, 4]):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    VarA = tk.StringVar()
    VarA.set(ListA[0])

    VarB = tk.StringVar()
    VarB.set(ListB[0])

    FlagBitA = FlagBits[0] # Combo Box A = Bottom Part of Value
    FlagBitB = FlagBits[1] # Combo Box B = Top Part of Value
    FlagShift = FlagBits[2]

    if StringList is None:
        TextNormal = String.format(VarA.get(), VarB.get())
    else:
        TextNormal = String + "\n" + StringList[0]
        
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SwitchText(Var, List):
        for i, Name in enumerate(List):
            if Var.get() == Name:
                if StringList is None:
                    TextLabel.configure(text = String.format(VarA.get(), VarB.get()))
                else:
                    TextLabel.configure(text = String + "\n" + StringList[i])

                break

        return i

    def SetVariableA():
        i = SwitchText(VarA, ListA)
        TopHalf = FinalValue.get() & FlagBitA
        FinalValue.set(TopHalf | i)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetVariableB():
        i = SwitchText(VarB, ListB)
        BottomHalf = FinalValue.get() & FlagBitB
        FinalValue.set((i << FlagShift) | BottomHalf)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    VarLabelA = ttk.Label(FrameB, text = LabelTextA, font = ("Courier", SmallSize))
    VarPickerA = ttk.Combobox(FrameB, textvariable = VarA, width = Width, values = ListA, font = ("Courier", SmallSize))
    VarPickerA.bind("<<ComboboxSelected>>", lambda _: SetVariableA())

    VarLabelB = ttk.Label(FrameC, text = LabelTextB, font = ("Courier", SmallSize))
    VarPickerB = ttk.Combobox(FrameC, textvariable = VarB, width = Width, values = ListB, font = ("Courier", SmallSize))
    VarPickerB.bind("<<ComboboxSelected>>", lambda _: SetVariableB())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack(pady = 5)
    FrameC.pack(pady = 5)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    VarLabelA.pack(side = "left", padx = 5)
    VarPickerA.pack(side = "left", padx = 5)
    VarLabelB.pack(side = "left", padx = 5)
    VarPickerB.pack(side = "left", padx = 5)  

#------------------------------------------------------------
# Combo Box + Search Bar
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers with a single combo box with a
lot of entries, so a search bar is included to find a
specific entry more easily.
-------------------------------------------------------------
"""
def SingleComboBoxWithSearch(WidgetFrame, String, LabelText, List, FinalValue, Changed, StringList = None, Width = 13):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")
    FrameD = tk.Frame(WidgetFrame, bg = "Black")

    Var = tk.StringVar()
    Var.set(List[0])

    if StringList is None:
        TextNormal = String.format(Var.get())
    else:
        TextNormal = String + "\n" + StringList[0]
        
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    ResultsLabel = ttk.Label(FrameC, text = "", font = ("Courier", SmallSize))

    def ProcessEntry(Text):
        Values = []
        for Name in List:
            if Text.lower() in Name.lower():
                Values.append(Name)       

        VarPicker.configure(values = Values)

        if Text == "":
            ResultsLabel.configure(text = "")
        else:
            ResultsLabel.configure(text = "Found {} results".format(len(Values)))
        
        if len(Values) > 0:
            Var.set(Values[0])
        else:
            Var.set("None")
    
    SearchBar = tk.Text(FrameB, width = 20, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    SearchBar.bind("<KeyRelease>", (lambda event: ProcessEntry(SearchBar.get(1.0, "end-1c"))))

    Cleared = tk.IntVar()
    Cleared.set(0)
    def ClearSearch():
        Cleared.set(0)
        SearchBar.delete(1.0, "end-1c")

        Values = []
        for Key in List:
            Values.append(Key)

        VarPicker.configure(values = Values)
        ResultsLabel.configure(text = "")
        Var.set(Values[0])
    
    SearchClear = ttk.Checkbutton(FrameB, text = "X", variable = Cleared, command = ClearSearch)  

    def SetVariable():       
        for i, Name in enumerate(List):
            if Var.get() == Name:
                if StringList is None:
                    TextLabel.configure(text = String.format(Var.get()))
                else:
                    TextLabel.configure(text = String + "\n" + StringList[i])
            
                FinalValue.set(i)
                break
            
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    VarLabel = ttk.Label(FrameD, text = LabelText, font = ("Courier", SmallSize)) 
    VarPicker = ttk.Combobox(FrameD, textvariable = Var, width = Width, values = List, font = ("Courier", SmallSize))
    VarPicker.bind("<<ComboboxSelected>>", lambda _: SetVariable())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack()
    FrameC.pack()
    FrameD.pack()
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    SearchClear.pack(side = "left", padx = 5)
    SearchBar.pack(side = "left")
    ResultsLabel.pack()
    VarLabel.pack(side = "left", padx = 5)
    VarPicker.pack(side = "left", padx = 5)    

#------------------------------------------------------------
# Entry + One Combo Box
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which have an entry box and one
combobox.
-------------------------------------------------------------
"""
def AmountEntryOneComboBox(WidgetFrame, List, StringA, StringB, LabelTextA, LabelTextB, StringFlags, Low, High, WidthA, WidthB, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    Amount = tk.IntVar()
    Amount.set(0)

    StringFlag = tk.IntVar()
    StringFlag.set(0)

    Var = tk.StringVar()
    Var.set(List[0])

    TextNormal = StringA.format(Amount.get(), Var.get())
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    ttk.Label(FrameA, text = "Valid values range between {} and {}".format(Low, High), font = ("Courier", SmallSize, "underline")).pack(pady = (0,10))

    def SwitchText():
        if StringFlag.get() not in StringFlags:
            T = StringA.format(Amount.get(), Var.get())
        else:
            T = StringB.format(Low, Amount.get(), Var.get())
            
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetAmount(Input):
        try:
            X = int(Input)
            if X < Low:
                X = Low
                
            elif X > High:
                X = High

            Amount.set(X)
            TopHalf = FinalValue.get() & 240 # Get top half of byte
            FinalValue.set(TopHalf | X)
            
            SwitchText()

            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Amount.get())

            VarPicker.configure(state = "normal")

        except Exception as e:
            print(e)
            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Input[:-1])

    def SetVariable():        
        for i, Name in enumerate(List):
            if Var.get() == Name:
                BottomHalf = FinalValue.get() & 15 # Get bottom half of byte
                TopHalf = i << 4
                StringFlag.set(i)
                FinalValue.set(TopHalf | BottomHalf)
                break

        SwitchText()

    VarLabel = ttk.Label(FrameC, text = LabelTextA, font = ("Courier", SmallSize)) 
    VarPicker = ttk.Combobox(FrameC, textvariable = Var, width = WidthA, values = List, state = "disabled", font = ("Courier", SmallSize))
    VarPicker.bind("<<ComboboxSelected>>", lambda _: SetVariable())

    AmountLabel = ttk.Label(FrameB, text = LabelTextB, font = ("Courier", SmallSize)) 
    AmountEntry = tk.Text(FrameB, width = WidthB, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize)) 
    AmountEntry.bind("<KeyRelease>", lambda _: SetAmount(AmountEntry.get(1.0, "end-1c")))
    AmountEntry.bind(mb.Paste, lambda _: "break")

    AmountEntry.delete(1.0, "end-1c")
    AmountEntry.insert(1.0, Amount.get())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack()
    FrameC.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    AmountLabel.pack(side = "left", padx = 5)
    AmountEntry.pack(side = "left", padx = 5)
    VarLabel.pack(side = "left", padx = 5)
    VarPicker.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Entry + One Flag
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which have an entry box and one
Flag.
-------------------------------------------------------------
"""
def AmountEntryOneFlag(WidgetFrame, StringA, StringB, FlagBit, LabelText, ButtonText, Low, High, Width, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")

    Amount = tk.IntVar()
    Amount.set(0)

    Flag = tk.IntVar()
    Flag.set(0)

    TextNormal = StringA.format(Amount.get())
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    ttk.Label(FrameA, text = "Valid values range between {} and {}".format(Low, High), font = ("Courier", SmallSize, "underline")).pack(pady = (0,10))

    def SwitchText():
        if Flag.get() == 1:
            T = StringA.format(Amount.get())
        else:
            T = StringB.format(Amount.get())
            
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetAmount(Input):
        try:
            X = int(Input)
            if X < Low:
                X = Low
                
            elif X > High:
                X = High

            Amount.set(X)

            FinalValue.set((Flag.get() << FlagBit) | Amount.get())

            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Amount.get())

            FlagButton.configure(state = "normal")

            SwitchText()

        except Exception as e:
            print(e)
            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Input[:-1])

    def SetFlag():
        FinalValue.set(FinalValue.get() | (1 << FlagBit)) # Set the flag

        if Flag.get() == 0: # Reset the Flag
            FinalValue.set(FinalValue.get() ^ (1 << FlagBit)) # Reset the flag now that it's set

        SwitchText()
            
    AmountLabel = ttk.Label(FrameB, text = LabelText, font = ("Courier", SmallSize)) 
    AmountEntry = tk.Text(FrameB, width = Width, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize)) 
    AmountEntry.bind("<KeyRelease>", lambda _: SetAmount(AmountEntry.get(1.0, "end-1c")))
    AmountEntry.bind(mb.Paste, lambda _: "break")

    AmountEntry.delete(1.0, "end-1c")
    AmountEntry.insert(1.0, Amount.get())

    FlagButton = ttk.Checkbutton(FrameB, text = ButtonText, variable = Flag, state = "disabled", command = SetFlag)
    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack()
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    FlagButton.pack(side = "left", padx = 5)
    AmountLabel.pack(side = "left", padx = 5)
    AmountEntry.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Entry + Two Flags
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which have an entry box and two
Flags.
-------------------------------------------------------------
"""
def AmountEntryTwoFlags(WidgetFrame, StringList, LabelText, FinalValue, Changed, FlagList, FlagBits, Low, High, Width, All = False, AllValue = 0):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    Amount = tk.IntVar()
    Amount.set(0)

    FlagA = tk.IntVar()
    FlagA.set(0)

    FlagB = tk.IntVar()
    FlagB.set(0)

    StringA = StringList[0]
    StringB = StringList[1]
    StringC = StringList[2]
    StringD = StringList[3]

    FlagTextA = FlagList[0]
    FlagTextB = FlagList[1]

    FlagBitA = FlagBits[0]
    FlagBitB = FlagBits[1]

    TextNormal = StringA.format(Amount.get())
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    ttk.Label(FrameA, text = "Valid values range between {} and {}".format(Low, High), font = ("Courier", SmallSize, "underline")).pack(pady = (0,10))

    def SwitchText():
        match FlagA.get(), FlagB.get():
            case 0, 0:
                T = StringA.format(Amount.get())
            case 0, 1:
                T = StringC.format(Amount.get())
            case 1, 0:
                T = StringB.format(Amount.get())
            case 1, 1:
                T = StringD.format(Amount.get())
            
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetAmount(Input):
        if AmountEntry.cget('state') == "normal":
            try:
                X = int(Input)
                if X < Low:
                    X = Low
                    
                elif X > High:
                    X = High
                    
                Amount.set(X)

                FinalValue.set((FlagA.get() << FlagBitA) | (FlagB.get() << FlagBitB) | Amount.get())

                AmountEntry.delete(1.0, "end-1c")
                AmountEntry.insert(1.0, Amount.get())

                FlagButtonA.configure(state = "normal")
                FlagButtonB.configure(state = "normal")

                SwitchText()

            except Exception as e:
                print(e)
                AmountEntry.delete(1.0, "end-1c")
                AmountEntry.insert(1.0, Input[:-1])

    def SetFlag(FlagBit, Flag):
        FinalValue.set(FinalValue.get() | (1 << FlagBit)) # Set the flag

        if Flag.get() == 0: # Reset the Flag
            FinalValue.set(FinalValue.get() ^ (1 << FlagBit)) # Reset the flag now that it's set

        SwitchText()

    def AllFlag(FlagBit, Flag):
        if All:
            if Flag.get() == 1:
                FinalValue.set((FlagB.get() << FlagBitB) | AllValue)
                SwitchText()
                AmountEntry.configure(state = "disabled")
            else:
                FinalValue.set((FlagB.get() << FlagBitB) | Amount.get())
                SwitchText()
                AmountEntry.configure(state = "normal")

        else:
            SetFlag(FlagBit, Flag)
    
    AmountLabel = ttk.Label(FrameB, text = LabelText, font = ("Courier", SmallSize)) 
    AmountEntry = tk.Text(FrameB, width = Width, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize)) 
    AmountEntry.bind("<KeyRelease>", lambda _: SetAmount(AmountEntry.get(1.0, "end-1c")))
    AmountEntry.bind(mb.Paste, lambda _: "break")

    AmountEntry.delete(1.0, "end-1c")
    AmountEntry.insert(1.0, Amount.get())

    FlagButtonA = ttk.Checkbutton(FrameC, text = FlagTextA, variable = FlagA, state = "disabled", command = lambda: AllFlag(FlagBitA, FlagA))
    FlagButtonB = ttk.Checkbutton(FrameC, text = FlagTextB, variable = FlagB, state = "disabled", command = lambda: SetFlag(FlagBitB, FlagB))

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack()
    FrameC.pack()
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    AmountLabel.pack(side = "left", padx = 5)
    AmountEntry.pack(side = "left", padx = 5)
    FlagButtonA.pack(side = "left", padx = 5)
    FlagButtonB.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Multi-Flag List
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which have multiple Flags that
the user can select any number of.
-------------------------------------------------------------
"""
def MultiFlagList(WidgetFrame, String, FlagList, LabelText, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    FrameA.pack()
    FrameB.pack(pady = (10,0))
    FrameC.pack()

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))
    FinalValueLabel.pack(side = "top")

    FlagVars = [tk.IntVar(value = 0) for i in range(len(FlagList))]

    TextNormal = String
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))
    TextLabel.pack()

    FlagLabel = ttk.Label(FrameB, text = LabelText, font = ("Courier", SmallSize))
    FlagLabel.pack()

    def SetFlag(N, Var):
        FinalValue.set(FinalValue.get() | (1 << N))

        if Var.get() == 0:
            FinalValue.set(FinalValue.get() ^ (1 << N))

        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    for i, Var in enumerate(FlagVars):
        if i < 4:
            R = 0
        else:
            R = 1
            
        C = i % 4
        ttk.Checkbutton(FrameC, text = FlagList[i], variable = FlagVars[i], command = lambda i = i: SetFlag(i, FlagVars[i])).grid(row = R, column = C, padx = 10, pady = 5, sticky = "w")

#------------------------------------------------------------
# One Flag Switch Text
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which have one Flag (0 or 1)
which switches what the text says entirely
-------------------------------------------------------------
"""
def OneFlagSwitchText(WidgetFrame, StringA, StringB, FlagName, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")

    Flag = tk.IntVar()
    Flag.set(0)

    TextNormal = StringA
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SetFlag():
        if Flag.get() == 1:
            TextLabel.configure(text = StringB)
        else:
            TextLabel.configure(text = StringA)
        
        FinalValue.set(Flag.get())
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    FlagLabel = ttk.Label(FrameB, text = "Option:", font = ("Courier", SmallSize))
    FlagButton = ttk.Checkbutton(FrameB, text = FlagName, variable = Flag, command = SetFlag)

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack()
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    FlagLabel.pack()
    FlagButton.pack()

#------------------------------------------------------------
# None
#------------------------------------------------------------
def NoArguments(WidgetFrame):
    ttk.Label(WidgetFrame, text = "This script has no arguments.", font = ("Courier", SmallSize)).pack()

#------------------------------------------------------------
# Turns
#------------------------------------------------------------
def TurnsFunction(WidgetFrame, Args, FinalValue, Changed):
    StringA = "The Flag will be set for anywhere between {} and {}\nturns, including this one.".format(Args[0], "{}")
    StringB = "The Flag will be set for {} turns, including this one."
    AmountEntryOneFlag(WidgetFrame, StringA, StringB, 4, "Turns:", "Random?", Args[0], Args[1], 3, FinalValue, Changed)

#------------------------------------------------------------
# Percentage Helper
#------------------------------------------------------------
def PercentValue(WidgetFrame, Args, FinalValue, Changed):
    Text = "The {} will {}\n{}% of {} as {}.".format(Args[0], Args[1], {}, Args[2], Args[3])
    AmountEntry(WidgetFrame, Text, "Percent:", 1, 100, 3, FinalValue, Changed)

#------------------------------------------------------------
# Type Helper
#------------------------------------------------------------
def TypeArgument(WidgetFrame, Args, FinalValue, Changed):
    Types = list(tf.TypeConversion.keys())
    Type = tk.StringVar()
    SingleComboBox(WidgetFrame, Args[0], "Type:", Types, Type, FinalValue, Changed)

#------------------------------------------------------------
# Stat Stage Amount Helper
#------------------------------------------------------------
def StatStageAmount(WidgetFrame, Args, FinalValue, Changed):
    Text = "The Target's {} will {}\nby {} Stat Stages.".format(Args[0], Args[1], "{}")
    AmountEntry(WidgetFrame, Text, "Amount:", 1, 6, 3, FinalValue, Changed)

#------------------------------------------------------------
# Major Status Flags Helper
#------------------------------------------------------------
def MajorStatusArgument(WidgetFrame, Args, FinalValue, Changed):
    String = Args[0]
    Statuses = ["Sleep", "Poison", "Burn", "Freeze", "Paralysis", "Bad Poison", "Confusion", "Infatuation"]
    Status = tk.StringVar()

    if Args[1] == 0: # Use Flags
        MultiFlagList(WidgetFrame, String, Statuses, "Options:", FinalValue, Changed)
        
    if Args[1] == 1: # Use Single Combo box
        SingleComboBox(WidgetFrame, String, "Status:", Statuses, Status, FinalValue, Changed)

#------------------------------------------------------------
# Multiple Stat Stages Helper
#------------------------------------------------------------
def StatStageFlags(WidgetFrame, Args, FinalValue, Changed):
    String = Args[0]
    Stats = ["Attack", "Defence", "Speed", "Sp. Attack", "Sp. Defence", "Accuracy", "Evasion"]
    MultiFlagList(WidgetFrame, String, Stats, "Options:", FinalValue, Changed)

#------------------------------------------------------------
# Weather Helper
#------------------------------------------------------------
def WeatherArgument(WidgetFrame, Args, FinalValue, Changed):
    String = Args[0]

    if Args[1] == 0: # Use Flags
        Weathers = ["Rain", "Sandstorm", "Sunshine", "Hail", "Fog", "Snow"]
        MultiFlagList(WidgetFrame, String, Weathers, "Options:", FinalValue, Changed)
        
    if Args[1] == 1: # Use Single Combo box
        Weathers = ["Clear", "Rain", "Sandstorm", "Sunshine", "Hail", "Fog", "Snow"]
        Weather = tk.StringVar()
        SingleComboBox(WidgetFrame, String, "Weather:", Weathers, Weather, FinalValue, Changed)

#------------------------------------------------------------
# Multi-Hit Move Helper
#------------------------------------------------------------
def MultiHitMove(WidgetFrame, FinalValue, Changed):
    StringA = "The Move will hit {} times with\nthe {} distribution."
    StringB = "The Move will hit {}-{} times with\nthe {} distribution."
    Distributions = ["Normal", "Bullet Seed", "Tail Slap", "Population Bomb"]
    StringFlags = [1, 2, 3]
    AmountEntryOneComboBox(WidgetFrame, Distributions, StringA, StringB, "Distribution:", "Times:", StringFlags, 2, 15, 15, 3, FinalValue, Changed)

#------------------------------------------------------------
# Custom Script Argument Helper
#------------------------------------------------------------
def CustomHelper(WidgetFrame, Args, FinalValue, Changed):
    match Args[0]:
        case 0: # Pay Day
            String = "The Player will earn money\naccording to the {} formula."
            Formulae = ["Pay Day", "Happy Hour"]
            SingleComboBox(WidgetFrame, String, "Weather:", Formulae, FinalValue, Changed)

        case 1: # Terrain Flags
            String = "The selected Terrain Flags will be set."
            Terrain = ["Grassy", "Electric", "Misty", "Psychic"]
            MultiFlagList(WidgetFrame, String, Terrain, "Options:", FinalValue, Changed)

        case 2: # Autotomise
            String = "The Target's Speed will rise by two Stat Stages\nand their weight will decrease by {} kilogrammes."
            AmountEntry(WidgetFrame, String, "Amount:", 1, 255, 3, FinalValue, Changed)

        case 3: # Whirlwind
            StringA = "The Target will switch out to another Pokemon."
            StringB = "The Target will switch out and pass along various effects."
            OneFlagSwitchText(WidgetFrame, StringA, StringB, "Baton Pass?", FinalValue, Changed)

        case 4: # Bug Bite
            StringA = "The Target's Berry will be removed and the User will eat it."
            StringB = "The Target's Berry will be removed and the User won't eat it."
            OneFlagSwitchText(WidgetFrame, StringA, StringB, "Don't Eat Berry", FinalValue, Changed)

        case 5: # Thief
            StringA = "The Target's Held Item will be removed and given to the User."
            StringB = "The User's Held Item will be removed and given to the Target."
            OneFlagSwitchText(WidgetFrame, StringA, StringB, "Bestow", FinalValue, Changed)

        case 6: # Flame Wheel
            StringA = "The User will thaw out if they were Frozen."
            StringB = "The User and the Target will thaw out if they were Frozen."
            OneFlagSwitchText(WidgetFrame, StringA, StringB, "Thaw Both", FinalValue, Changed)

        case 7: # Custom String
            String = "The following text will be displayed, and that's it."
            Strings = ["Celebrate", "Happy Hour", "Splash"]
            StringList = ["Congratulations, [PLAYER]!",
                          "[USER] and [PARTNER] are holding hands!",
                          "But nothing happened!"]
            SingleComboBox(WidgetFrame, String, "String:", Strings, FinalValue, Changed, StringList)

        case 8: # Entry Hazards
            String = "The {} Entry Hazard will be set."
            Hazards = ["Spikes", "Toxic Spikes", "Stealth Rock", "Sticky Web", "Steelsurge"]
            SingleComboBox(WidgetFrame, String, "Entry Hazard:", Hazards, FinalValue, Changed)

        case 9: # Heal HP Formula
            String = "The Target will heal HP according to the following formula:"
            Strings = ["Heal 50%", "Sunshine", "Rain", "Sandstorm", "Hail", "Swallow", "Grassy", "Heal 25%"]
            StringList = ["Always heals 50% of the maximum HP",
                          "Heals 2/3 in Sunshine, 1/2 when Clear, 1/4 in other Weather",
                          "Heals 2/3 in Rain, 1/2 when Clear, 1/4 in other Weather",
                          "Heals 2/3 in Sandstorm, 1/2 when Clear, 1/4 in other Weather",
                          "Heals 2/3 in Hail, 1/2 when Clear, 1/4 in other Weather",
                          "Heals HP depending on number of Stockpile layers",
                          "Heals 2/3 in Grassy Terrain, 1/2 otherwise",
                          "Always heals 25% of the maximum HP"]
            SingleComboBox(WidgetFrame, String, "String:", Strings, FinalValue, Changed, StringList)

        case 10: # Switch + Heal
            String = "The User will faint and Pokemon replacing\nthem will have {} healed."
            Options = ["HP", "HP + PP", "HP + PP + Major Statuses"]
            SingleComboBox(WidgetFrame, String, "Options:", Options, FinalValue, Changed, None, 25)

        case 11: # Target Redirect Flag
            String = "The {} Flag will be set on the Target."
            Flags = ["Follow Me", "Spotlight", "Rage Powder"]
            SingleComboBox(WidgetFrame, String, "Flags:", Flags, FinalValue, Changed)

        case 12: # Role Play
            String = "The {} will have their Ability\nreplaced with the Target's."
            Options = ["User", "User + Partner"]
            SingleComboBox(WidgetFrame, String, "Options:", Options, FinalValue, Changed)

        case 13: # Ability Replace'
            String = "The Target's Ability will be replaced with {}."
            SingleComboBoxWithSearch(WidgetFrame, String, "Ability:", list(d.AbilityList.keys()), FinalValue, Changed)

        case 14: # Revival
            String = "{} Pokemon on the User's Party will be Revived."
            Options = ["A Random", "A Chosen", "All"]
            SingleComboBox(WidgetFrame, String, "Options:", Options, FinalValue, Changed)

#------------------------------------------------------------
# Power Points Helper
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper is for Scripts which use the Alter Power Points
SetEffect routine.
-------------------------------------------------------------
"""
def AlterPowerPoints(WidgetFrame, FinalValue, Changed):
    StringList = ["The Target will have {} Power Points removed\nfrom their last-used Move.",
                  "The Target will have all Power Points removed\nfrom their last-used Move.",
                  "The Target will have between 1-{} Power Points\nremoved from their last-used Move.",
                  "The Target will have between 1 to all of the Power\nPoints removed from their last-used Move."]
    FlagList = ["All?", "Random?"]
    FlagBits = [0, 7]
    AmountEntryTwoFlags(WidgetFrame, StringList, "Power Points:", FinalValue, Changed, FlagList, FlagBits, 1, 126, 3, True, 127)

#------------------------------------------------------------
# Two Stats Helper
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper is for Move Scripts which take two Stats at once
as an argument.
-------------------------------------------------------------
"""
def TwoStatsAtOnce(WidgetFrame, Args, FinalValue, Changed):
    String = Args[0]
    Stats = ["HP", "Attack", "Defence", "Sp. Attack", "Sp. Defence", "Speed"]
    TwoComboBoxes(WidgetFrame, String, "Stat 1:", "Stat 2:", Stats, Stats, FinalValue, Changed)

#------------------------------------------------------------
# Stats + Type
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper is for Move Scripts which take a Type and a Stat
as an argument.
-------------------------------------------------------------
"""
def StatAndType(WidgetFrame, Args, FinalValue, Changed):
    String = Args[0]
    Types = list(tf.TypeConversion.keys())
    Stats = ["Attack", "Defence", "Speed", "Sp. Attack", "Sp. Defence", "Accuracy", "Evasion"]
    TwoComboBoxes(WidgetFrame, String, "Type:", "Stat:", Types, Stats, FinalValue, Changed, StringList = None, Width = 13, FlagBits = [224, 31, 5])

#------------------------------------------------------------
# Stats + Type
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper is for Move Scripts which take a Type and a Stat
as an argument.
-------------------------------------------------------------
"""
def StatAndStatus(WidgetFrame, Args, FinalValue, Changed):
    String = Args[0]
    Statuses = ["Sleep", "Poison", "Burn", "Freeze", "Paralysis", "Bad Poison", "Confusion", "Infatuation"]
    Stats = ["Attack", "Defence", "Speed", "Sp. Attack", "Sp. Defence", "Accuracy", "Evasion"]
    TwoComboBoxes(WidgetFrame, String, "Status:", "Stat:", Statuses, Stats, FinalValue, Changed)
    
#------------------------------------------------------------
# Make Script Arg Helper Box
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function creates a normal Info Box, but it loads a
custom helper function depending on what the current Move
Script value is.

These helper functions make it easier to choose the correct
Script Argument.
-------------------------------------------------------------
"""
def MakeScriptArgHelperBox(Root, Title, Header, Text, Option = None, Args = None, Var = None):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")

    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)

    MenuTextFrame = tk.Frame(Top, bg = "Black")
    MenuTextFrame.pack(fill = "x", pady = 10)

    WidgetFrame = tk.Frame(Top, bg = "Black")
    WidgetFrame.pack(fill = "both", pady = 10)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 10)

    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()

    N = 0
    for i, Line in enumerate(Text):
        N = i+1
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).grid(row = N, column = 0, padx = 5, pady = 1, sticky = "w")

    DoLine = ttk.Label(MenuTextFrame, text = "-----", font = ("Courier", SmallSize))
    DoLine.pack()

    for Widget in WidgetFrame.winfo_children():
        Widget.destroy()

    Changed = tk.BooleanVar()
    Changed.set(False)
    
    FinalValue = tk.IntVar()
    
    if Option is not None:
        match Option:
            case "Turns": # Create Script Turn Helper
                TurnsFunction(WidgetFrame, Args, FinalValue, Changed)

            case "Percent": # Create Script Percentage Helper
                PercentValue(WidgetFrame, Args, FinalValue, Changed)

            case "Type":
                TypeArgument(WidgetFrame, Args, FinalValue, Changed)

            case "StageAmount":
                StatStageAmount(WidgetFrame, Args, FinalValue, Changed)

            case "MajorStatus":
                MajorStatusArgument(WidgetFrame, Args, FinalValue, Changed)

            case "StatFlags":
                StatStageFlags(WidgetFrame, Args, FinalValue, Changed)

            case "Weather":
                WeatherArgument(WidgetFrame, Args, FinalValue, Changed)

            case "MultiHit":
                MultiHitMove(WidgetFrame, FinalValue, Changed)

            case "Custom":
                CustomHelper(WidgetFrame, Args, FinalValue, Changed)

            case "PowerPoints":
                AlterPowerPoints(WidgetFrame, FinalValue, Changed)

            case "TwoStats":
                TwoStatsAtOnce(WidgetFrame, Args, FinalValue, Changed)

            case "StatType":
                StatAndType(WidgetFrame, Args, FinalValue, Changed)

            case "StatStatus":
                StatAndStatus(WidgetFrame, Args, FinalValue, Changed)

            case _:
                NoArguments(WidgetFrame)

    def SetNewValue(Event = None):
        if Changed.get():
            if Var is not None:
                Var.set(str(FinalValue.get()))
            
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = SetNewValue)
    OkayButton.pack()

    Top.bind("<Return>", SetNewValue)
    Top.wait_window()
