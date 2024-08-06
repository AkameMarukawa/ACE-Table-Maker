import tkinter as tk
from tkinter import ttk

SmallSize = 16

#------------------------------------------------------------
# None
#------------------------------------------------------------
"""
-------------------------------------------------------------
This just displays the label which states that there are no
arguments for the current Move Script
-------------------------------------------------------------
"""
def NoArguments(WidgetFrame):
    ttk.Label(WidgetFrame, text = "This formula has no arguments.", font = ("Courier", SmallSize)).pack()

#------------------------------------------------------------
# Target Only
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper function is for set damage equal to the given
quantity on the given Target ID.
-------------------------------------------------------------
"""
def TargetSetDamage(WidgetFrame, Args, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")

    Quantity = Args[0]
    Targets = ["User", "Target", "User's Partner", "Target's Partner"]

    Target = tk.StringVar()
    Target.set("User")

    TextNormal = "The damage will be set equal to the {}'s {}.".format(Target.get(), Quantity)
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SetTarget():
        match Target.get():
            case "User":
                FinalValue.set(0)
            case "Target":
                FinalValue.set(1)
            case "User's Partner":
                FinalValue.set(2)
            case "Target's Partner":
                FinalValue.set(3)
                
        T = "The damage will be set equal to the {}'s {}.".format(Target.get(), Quantity)
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    TargetLabel = ttk.Label(FrameB, text = "Target:", font = ("Courier", SmallSize))
    TargetPicker = ttk.Combobox(FrameB, textvariable = Target, width = 16, values = Targets, font = ("Courier", SmallSize))
    TargetPicker.bind("<<ComboboxSelected>>", lambda e: SetTarget())
    
    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack(pady = 10)
    FrameB.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack()
    TargetLabel.pack(side = "left", padx = 5)
    TargetPicker.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Direct Or Inverse
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper function is for a Damage Formula which uses the
targets and a relationship as arguments.

The first two bits are the Target ID value. That is one of
the four possible Pokemon on the field.

The third bit is the Inverse Flag. If this is set, then the
Base Power and the given Quantity will have an inverse
relationship.

The fourth bit is the Compare Flag. If this is set, then the
Base Power formula will compare the user's Quantity with the
given Target ID's quantity and the Base Power will be set
based on that.
-------------------------------------------------------------
"""
def RelationshipArgument(WidgetFrame, Args, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    Quantity = Args[0]
    Targets = ["User", "Target", "User's Partner", "Target's Partner"]
    Relations = ["higher", "lower"]

    Target = tk.StringVar()
    Target.set("User")
    
    Relation = tk.IntVar()
    Relation.set(0)
    
    Compare = tk.IntVar()
    Compare.set(0)

    TextNormal = "The Base Power will be {} if the\n{}'s {} is higher.".format(Relations[Relation.get()], Target.get(), Quantity)
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SwitchText():
        if Compare.get() == 1: # Compare thing with target
            T = "The Base Power will be {} if the User's\n{} is higher than the {}'s.".format(Relations[Relation.get()], Quantity, Target.get())
        else:
            T = "The Base Power will be {} if the\n{}'s {} is higher.".format(Relations[Relation.get()], Target.get(), Quantity)

        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetTarget():
        TopHalf = FinalValue.get() & 12 # Top two bits

        match Target.get():
            case "User":
                FinalValue.set(TopHalf | 0)
            case "Target":
                FinalValue.set(TopHalf | 1)
            case "User's Partner":
                FinalValue.set(TopHalf | 2)
            case "Target's Partner":
                FinalValue.set(TopHalf | 3)
        
        SwitchText()        

    def SetRelation():
        FinalValue.set(FinalValue.get() | 4) # Set the inverse Flag
        
        if Relation.get() == 0:
            FinalValue.set(FinalValue.get() ^ 4) # Reset the inverse Flag

        SwitchText()

    def SetComparison():
        FinalValue.set(FinalValue.get() | 8) # Set the compare Flag
        
        if Compare.get() == 0:
            FinalValue.set(FinalValue.get() ^ 8) # Reset the compare Flag

        SwitchText()    

    TargetLabel = ttk.Label(FrameB, text = "Target:", font = ("Courier", SmallSize))
    TargetPicker = ttk.Combobox(FrameB, textvariable = Target, width = 16, values = Targets, font = ("Courier", SmallSize))
    TargetPicker.bind("<<ComboboxSelected>>", lambda e: SetTarget())

    RelationPicker = ttk.Checkbutton(FrameC, text = "Inverse?", variable = Relation, command = SetRelation)
    ComparisonPicker = ttk.Checkbutton(FrameC, text = "Compare With Target?", variable = Compare, command = SetComparison)

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack(pady = 10)
    FrameB.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack()
    TargetLabel.pack(side = "left", padx = 5)
    TargetPicker.pack(side = "left", padx = 5)

    FrameC.pack(pady = 5)
    RelationPicker.pack(pady = 5)
    ComparisonPicker.pack(pady = 5)

#------------------------------------------------------------
# Set Damage Multiple
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper function is for set damage equal to 10 times the
given multiple.
-------------------------------------------------------------
"""
def SetDamageMultiple(WidgetFrame, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")

    Multiple = tk.IntVar()
    Multiple.set(1)

    TextNormal = "The damage will be set equal to {}.".format(Multiple.get() * 10)
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SetMultiple():
        FinalValue.set(Multiple.get())                
        T = "The damage will be set equal to {}.".format(Multiple.get() * 10)
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    MultipleLabel = ttk.Label(FrameB, text = "Multiplier:", font = ("Courier", SmallSize))
    MultipleSlider = ttk.Scale(FrameB, variable = Multiple, length = 450, from_ = 1, to = 15, command = lambda e: SetMultiple(), orient = "horizontal")
    
    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack(pady = 10)
    FrameB.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack()
    MultipleLabel.pack(side = "left", padx = 5)
    MultipleSlider.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Set Custom Base Power
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper function is to pick the custom formula which
goes with a specific Move or kind of Move.
-------------------------------------------------------------
"""
def SetCustomFormula(WidgetFrame, Args, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")

    Options = Args[0]

    Option = tk.StringVar()
    Option.set(Options[0])

    TextNormal = "The Base Power will be calculated using\n{}'s Damage Formula.".format(Option.get())
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SetOption():
        for i, Name in enumerate(Options):
            if Option.get() == Name:
                FinalValue.set(i)
                break
                      
        T = "The Base Power will be calculated using\n{}'s Damage Formula.".format(Option.get())
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    OptionLabel = ttk.Label(FrameB, text = "Target:", font = ("Courier", SmallSize))
    OptionPicker = ttk.Combobox(FrameB, textvariable = Option, width = 16, values = Options, font = ("Courier", SmallSize))
    OptionPicker.bind("<<ComboboxSelected>>", lambda e: SetOption())
    
    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack(pady = 10)
    FrameB.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack()
    OptionLabel.pack(side = "left", padx = 5)
    OptionPicker.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Direct Or Inverse (Stat Stages)
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper function is for a Damage Formula which uses the
targets and a relationship as arguments.

The first two bits are the Target ID value. That is one of
the four possible Pokemon on the field.

The third bit is the Positive Flag. If this is set, then the
formula will use Stat Stages above zero. If not, it will use
only the Stat Stages which are below zero

The fourth bit is the Inverse Flag. If this is set, then the
Base Power and the given Quantity will have an inverse
relationship.
-------------------------------------------------------------
"""
def RelationshipStatStages(WidgetFrame, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    Targets = ["User", "Target", "User's Partner", "Target's Partner"]
    Relations = ["higher", "lower"]
    Parities = ["above", "below"]

    Target = tk.StringVar()
    Target.set("User")
    
    Relation = tk.IntVar()
    Relation.set(0)
    
    Parity = tk.IntVar()
    Parity.set(0)

    TextNormal = "The Base Power will be {} if the\n{} has more Stat Stages {} zero.".format(Relations[Relation.get()], Target.get(), Parities[Parity.get()])
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SwitchText():
        T = "The Base Power will be {} if the\n{} has more Stat Stages {} zero.".format(Relations[Relation.get()], Target.get(), Parities[Parity.get()])
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetTarget():
        TopHalf = FinalValue.get() & 12 # Top two bits

        match Target.get():
            case "User":
                FinalValue.set(TopHalf | 0)
            case "Target":
                FinalValue.set(TopHalf | 1)
            case "User's Partner":
                FinalValue.set(TopHalf | 2)
            case "Target's Partner":
                FinalValue.set(TopHalf | 3)
        
        SwitchText()        

    def SetRelation():
        FinalValue.set(FinalValue.get() | 8) # Set the inverse Flag
        
        if Relation.get() == 0:
            FinalValue.set(FinalValue.get() ^ 8) # Reset the inverse Flag

        SwitchText()

    def SetParity():
        FinalValue.set(FinalValue.get() | 4) # Set the compare Flag
        
        if Parity.get() == 0:
            FinalValue.set(FinalValue.get() ^ 4) # Reset the compare Flag

        SwitchText()   

    TargetLabel = ttk.Label(FrameB, text = "Target:", font = ("Courier", SmallSize))
    TargetPicker = ttk.Combobox(FrameB, textvariable = Target, width = 16, values = Targets, font = ("Courier", SmallSize))
    TargetPicker.bind("<<ComboboxSelected>>", lambda e: SetTarget())

    RelationPicker = ttk.Checkbutton(FrameC, text = "Inverse?", variable = Relation, command = SetRelation)
    ParityPicker = ttk.Checkbutton(FrameC, text = "Positive?", variable = Parity, command = SetParity)

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack(pady = 10)
    FrameB.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack()
    TargetLabel.pack(side = "left", padx = 5)
    TargetPicker.pack(side = "left", padx = 5)

    FrameC.pack(pady = 5)
    RelationPicker.pack(pady = 5)
    ParityPicker.pack(pady = 5)

#------------------------------------------------------------
# Percent Set Damage Helpers
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper sets the Damage according to the target and the
given fixed percentage of their stat.
-------------------------------------------------------------
"""
def SetDamagePercent(WidgetFrame, Args, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    Targets = ["User", "Target", "User's Partner", "Target's Partner"]
    Percents = ["25%", "50%", "75%", "100%"]
    Quantity = Args[0]

    Target = tk.StringVar()
    Target.set("User")

    Percent = tk.StringVar()
    Percent.set("25%")

    TextNormal = "The Damage will be set to {}\nof the {}'s {}.".format(Percent.get(), Target.get(), Quantity)
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SwitchText():
        T = "The Damage will be set to {}\nof the {}'s {}.".format(Percent.get(), Target.get(), Quantity)
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetTarget():
        TopHalf = FinalValue.get() & 12 # Top two bits

        match Target.get():
            case "User":
                FinalValue.set(TopHalf | 0)
            case "Target":
                FinalValue.set(TopHalf | 1)
            case "User's Partner":
                FinalValue.set(TopHalf | 2)
            case "Target's Partner":
                FinalValue.set(TopHalf | 3)
        
        SwitchText()

    def SetPercent():
        BottomHalf = FinalValue.get() & 3 # Bottom two bits

        match Percent.get():
            case "25%":
                FinalValue.set(BottomHalf | 0 << 2)
            case "50%":
                FinalValue.set(BottomHalf | 1 << 2)
            case "75%":
                FinalValue.set(BottomHalf | 2 << 2)
            case "100%":
                FinalValue.set(BottomHalf | 3 << 2)
        
        SwitchText()

    TargetLabel = ttk.Label(FrameB, text = "Target:", font = ("Courier", SmallSize))
    TargetPicker = ttk.Combobox(FrameB, textvariable = Target, width = 16, values = Targets, font = ("Courier", SmallSize))
    TargetPicker.bind("<<ComboboxSelected>>", lambda e: SetTarget())

    PercentLabel = ttk.Label(FrameC, text = "Percent:", font = ("Courier", SmallSize))
    PercentPicker = ttk.Combobox(FrameC, textvariable = Percent, width = 4, values = Percents, font = ("Courier", SmallSize))
    PercentPicker.bind("<<ComboboxSelected>>", lambda e: SetPercent())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack(pady = 10)
    FrameB.pack(pady = 10)
    FrameC.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack()
    TargetLabel.pack(side = "left", padx = 5)
    TargetPicker.pack(side = "left", padx = 5)
    PercentLabel.pack(side = "left", padx = 5)
    PercentPicker.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Held Item Damage Formula
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper sets the Base Power formula based on the type of
Item the given Pokemon is holding.
-------------------------------------------------------------
"""
def HeldItem(WidgetFrame, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    Targets = ["User", "Target", "User's Partner", "Target's Partner"]
    Options = ["Held Item", "Held Berry"]

    Target = tk.StringVar()
    Target.set("User")

    Option = tk.StringVar()
    Option.set("Held Item")

    TextNormal = "The Base Power will be set according to\nthe {}'s {}.".format(Target.get(), Option.get())
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SwitchText():
        T = "The Base Power will be set according to\nthe {}'s {}.".format(Target.get(), Option.get())
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetTarget():
        TopHalf = FinalValue.get() & 12 # Top two bits

        match Target.get():
            case "User":
                FinalValue.set(TopHalf | 0)
            case "Target":
                FinalValue.set(TopHalf | 1)
            case "User's Partner":
                FinalValue.set(TopHalf | 2)
            case "Target's Partner":
                FinalValue.set(TopHalf | 3)
        
        SwitchText()

    def SetOption():
        BottomHalf = FinalValue.get() & 3 # Bottom two bits

        match Option.get():
            case "Held Item":
                FinalValue.set(BottomHalf | 0 << 2)
            case "Held Berry":
                FinalValue.set(BottomHalf | 1 << 2)
        
        SwitchText()

    TargetLabel = ttk.Label(FrameB, text = "Target:", font = ("Courier", SmallSize))
    TargetPicker = ttk.Combobox(FrameB, textvariable = Target, width = 16, values = Targets, font = ("Courier", SmallSize))
    TargetPicker.bind("<<ComboboxSelected>>", lambda e: SetTarget())

    OptionLabel = ttk.Label(FrameC, text = "Percent:", font = ("Courier", SmallSize))
    OptionPicker = ttk.Combobox(FrameC, textvariable = Option, width = 10, values = Options, font = ("Courier", SmallSize))
    OptionPicker.bind("<<ComboboxSelected>>", lambda e: SetOption())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack(pady = 10)
    FrameB.pack(pady = 10)
    FrameC.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack()
    TargetLabel.pack(side = "left", padx = 5)
    TargetPicker.pack(side = "left", padx = 5)
    OptionLabel.pack(side = "left", padx = 5)
    OptionPicker.pack(side = "left", padx = 5)

#------------------------------------------------------------
# Counter Helper
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper sets the amount of Damage based on the kind of
Damage the given Pokemon has taken.
-------------------------------------------------------------
"""
def DamageKind(WidgetFrame, FinalValue, Changed):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    Targets = ["User", "Target", "User's Partner", "Target's Partner"]
    Options = {"Counter":[2, "Physical"], "Mirror Coat":[2, "Physical"], "Metal Burst":[1.5, "Total"], "Bide":[2, "Total"]}
    

    Target = tk.StringVar()
    Target.set("User")

    Option = tk.StringVar()
    Option.set("Counter")

    TextNormal = "The amount of Damage will be set to {}x the amount of\n{} Damage that the {}\ntook since using the Move.".format(Options[Option.get()][0], Options[Option.get()][1], Target.get())
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SwitchText():
        T = "The amount of Damage will be set to {}x the amount of\n{} Damage that the {}\ntook since using the Move.".format(Options[Option.get()][0], Options[Option.get()][1], Target.get())
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetTarget():
        TopHalf = FinalValue.get() & 12 # Top two bits

        match Target.get():
            case "User":
                FinalValue.set(TopHalf | 0)
            case "Target":
                FinalValue.set(TopHalf | 1)
            case "User's Partner":
                FinalValue.set(TopHalf | 2)
            case "Target's Partner":
                FinalValue.set(TopHalf | 3)
        
        SwitchText()

    def SetOption():
        BottomHalf = FinalValue.get() & 3 # Bottom two bits

        match Option.get():
            case "Counter":
                FinalValue.set(BottomHalf | 0 << 2)
            case "Mirror Coat":
                FinalValue.set(BottomHalf | 1 << 2)
            case "Metal Burst":
                FinalValue.set(BottomHalf | 2 << 2)
            case "Bide":
                FinalValue.set(BottomHalf | 3 << 2)
        
        SwitchText()

    TargetLabel = ttk.Label(FrameB, text = "Target:", font = ("Courier", SmallSize))
    TargetPicker = ttk.Combobox(FrameB, textvariable = Target, width = 16, values = Targets, font = ("Courier", SmallSize))
    TargetPicker.bind("<<ComboboxSelected>>", lambda e: SetTarget())

    OptionLabel = ttk.Label(FrameC, text = "Percent:", font = ("Courier", SmallSize))
    OptionPicker = ttk.Combobox(FrameC, textvariable = Option, width = 12, values = list(Options.keys()), font = ("Courier", SmallSize))
    OptionPicker.bind("<<ComboboxSelected>>", lambda e: SetOption())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack(pady = 10)
    FrameB.pack(pady = 10)
    FrameC.pack(pady = 10)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack()
    TargetLabel.pack(side = "left", padx = 5)
    TargetPicker.pack(side = "left", padx = 5)
    OptionLabel.pack(side = "left", padx = 5)
    OptionPicker.pack(side = "left", padx = 5)
    
#------------------------------------------------------------
# Make Formula Arg Helper Box
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function creates a normal Info Box, but it loads a
custom helper function depending on what the current Damage
Formula Argument value is.

These helper functions make it easier to choose the correct
Formula Argument.
-------------------------------------------------------------
"""
def MakeFormulaArgHelperBox(Root, Title, Header, Text, Option = None, Args = None, Var = None):
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
            case "SetTarget":
                TargetSetDamage(WidgetFrame, Args, FinalValue, Changed)
                
            case "Relation":
                RelationshipArgument(WidgetFrame, Args, FinalValue, Changed)

            case "Multiple":
                SetDamageMultiple(WidgetFrame, FinalValue, Changed)

            case "Custom":
                SetCustomFormula(WidgetFrame, Args, FinalValue, Changed)

            case "StatStages":
                RelationshipStatStages(WidgetFrame, FinalValue, Changed)

            case "Percent":
                SetDamagePercent(WidgetFrame, Args, FinalValue, Changed)

            case "Item":
                HeldItem(WidgetFrame, FinalValue, Changed)

            case "Counter":
                DamageKind(WidgetFrame, FinalValue, Changed)
                
            case _:
                NoArguments(WidgetFrame)

    def SetNewValue(Event = None):
        if Changed.get():
            if Var is not None:
                Var.set(hex(FinalValue.get())[2:].upper())
            
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = SetNewValue)
    OkayButton.pack()

    Top.bind("<Return>", SetNewValue)
    Top.wait_window()
