import MakeBoxes as mb

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

HexHalfBytes = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F"]

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

RangeConversion = {"User":"11", "Target":"1E", "User Or Partner":"13",
                   "Target Or Partner":"1C", "My Side":"23",
                   "Foe Side":"2C", "All But User":"2E", "Everyone":"2F",
                   "Random":"80", "Last Attacker":"40"}

KindConversion = {"Physical":"00", "Special":"01", "Status":"02"}

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

#------------------------------------------------------------
# Format Description
#------------------------------------------------------------
def FormatDescription(RawText):
    RawText = RawText.replace("|", "\n")

    try:
        Line1 = RawText.split("\n")[0].strip()
    except Exception as e:
        print(e)
        Line1 = ""

    try:
        Line2 = RawText.split("\n")[1].strip()
    except Exception as e:
        print(e)
        Line2 = ""

    try:
        Line3 = RawText.split("\n")[2].strip()
    except Exception as e:
        print(e)
        Line3 = ""

    try:
        Line4 = RawText.split("\n")[3].strip()
    except Exception as e:
        print(e)
        Line4 = ""

    NewText = "{}\n{}\n{}\n{}".format(Line1, Line2, Line3, Line4)
    return NewText

#------------------------------------------------------------
# Get Strings From Compiled Tables of Pointers
#------------------------------------------------------------
def GrabStringsFromTable(File):
    File = open(File, "rb")

    ByteList = []
    Byte = File.read(1)
    while Byte != b"":
        Value = int(bin(ord(Byte)), 2)
        Byte = hex(Value).upper()[2:]

        if Value < 16:
            Byte = "0" + Byte

        ByteList.append(Byte)
        Byte = File.read(1)

    FileBytes = ""
    for i, Byte in enumerate(ByteList):
        if (i+1) % 4 == 0:
            FileBytes += Byte + "\n"
        else:
            FileBytes += Byte + " "

    Strings = []
    String = ""
    for Line in FileBytes.strip().split("\n"):
        if not Line.startswith("08"): # Strings in AGB never have 08 in them
            for Byte in Line.split():
                if Byte == "FF": # Terminator
                    Strings.append(String.strip())
                    String = ""
                else:
                    String += Byte + " "

    return Strings

#------------------------------------------------------------
# Parse Pointer Table Function
#------------------------------------------------------------
def ParsePointerTable(FileName, Table, Type):
    try:
        Strings = GrabStringsFromTable(FileName)

        Error = ""
        if Type == "Name":
            Index = MoveNameIndex
        else:
            Index = DescriptionIndex
                    
        for i, String in enumerate(Strings):
            Text = ""

            try:
                for Byte in String.split():
                    Keys = list(TextToBytes.keys())
                    Values = list(TextToBytes.values())
                    
                    Text += Keys[Values.index(Byte)]
                    
            except:
                if Type == "Name":
                    Text = "Move Name"
                else:
                    Text = ""

                Error += "0"

            Table[i][Index] = Text.strip()

        if Error != "":
            mb.MakeInfoBox(Root, "Error!", "There was a problem!",
                        ["There was an error loading {} {}s.".format(Error.count("0"), Type.lower()),
                         "They were replaced with a default value."])
    
        return Table

    except Exception as e:
        print(e)
        mb.MakeInfoBox(Root, "Error!", "There was a problem!",
                    ["The Move {} Table given was invalid.".format(Type),
                     "No {}s were loaded.".format(Type.lower())])

        return Table

#------------------------------------------------------------
# Make Table Array from Compiled Table
#------------------------------------------------------------
def MakeTableFromCompiled(FileBytes, Error):
    Table = []
    for Line in FileBytes.strip().split("\n"):
        TableLine = []
        Line = Line.strip()

        Entry = Line.split()

        TableLine.append("Move Name")

        try:
            TableLine.append(Entry[0])  # Move Script
        except Exception as e:
            print(e)
            TableLine.append("00")
            Error += "0"

        try:
            TableLine.append(int(Entry[1], 16)) # Base Power
        except Exception as e:
            print(e)
            TableLine.append(0)
            Error += "1"

        try:
            TableLine.append(list(TypeConversion.keys())[list(TypeConversion.values()).index(Entry[2])])
        except Exception as e:
            print(e)
            TableLine.append("Normal")
            Error += "2"

        try:
            A = int(Entry[3], 16)
            if A > 100:
                A = 100
            TableLine.append(A) # Accuracy
        except Exception as e:
            print(e)
            TableLine.append(0)
            Error += "3"

        try:
            A = int(Entry[4], 16)
            if A > 99:
                A = 99
            TableLine.append(A) # Power Points
        except Exception as e:
            print(e)
            TableLine.append(0)
            Error += "4"

        try:
            A = int(Entry[5], 16)
            if A > 100:
                A = 100
            TableLine.append(A) # Effect Chance
        except:
            TableLine.append(0)
            Error += "5"

        try:
            TableLine.append(list(RangeConversion.keys())[list(RangeConversion.values()).index(Entry[6])])
        except Exception as e:
            print(e)
            TableLine.append("Target")
            Error += "6"

        try:
            P = int(Entry[7], 16)
            if P > 127:
                P = 256 - P
                P = -P
                
            TableLine.append(P) # Priority
        except Exception as e:
            print(e)
            TableLine.append(0)
            Error += "7"

        try:
            MoveFlags = [0,0,0,0,0,0,0,0]
            F = int(Entry[8], 16)

            for i in range(8):
                if F & 128 // 2**i != 0: # Flag is set
                    MoveFlags[i] = 1

            TableLine.append(MoveFlags)
        except Exception as e:
            print(e)
            TableLine.append([0,0,0,0,0,0,0,0])
            Error += "8"

        try:
            TableLine.append(Entry[9]) # Damage Formula
        except Exception as e:
            print(e)
            TableLine.append("00")
            Error += "9"

        try:
            TableLine.append(list(KindConversion.keys())[list(KindConversion.values()).index(Entry[10])])
        except Exception as e:
            print(e)
            TableLine.append("Status")
            Error += "A"

        try:
            TableLine.append(int(Entry[11], 16))
        except Exception as e:
            print(e)
            TableLine.append(0)
            Error += "B"

        # Blank Move Description
        TableLine.append('')
            
        Table.append(TableLine)

    return Table, Error

#------------------------------------------------------------
# Make Table Array from Human-Readable Table
#------------------------------------------------------------
def MakeTableFromText(FileStuff, Error):
    Table = []
    for Entry in FileStuff:
        TableLine = []
        Entry = Entry.split("\n")

        for i, Line in enumerate(Entry):
            if i == MoveNameIndex:
                try:
                    TableLine.append(Line.split("-")[0].strip()[0:12]) # Truncate at 12
                except Exception as e:
                    print(e)
                    TableLine.append("Move Name")
                    Error += "X"

            elif i == MoveScriptIndex:
                try:
                    TableLine.append(Line.split(")")[1].replace(",", "").strip()[2:])
                except Exception as e:
                    print(e)
                    TableLine.append("00")
                    Error += "0"

            elif i == BasePowerIndex:
                try:
                    TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    print(e)
                    TableLine.append(0)
                    Error += "1"

            elif i == TypeIndex:
                try:
                    TableLine.append(Line.split(")")[1].replace(",", "").strip())
                except Exception as e:
                    print(e)
                    TableLine.append("Normal")
                    Error += "2"

            elif i == AccuracyIndex:
                try:
                    TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    print(e)
                    TableLine.append(0)
                    Error += "3"

            elif i == PowerPointIndex:
                try:
                    TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    print(e)
                    TableLine.append(0)
                    Error += "4"

            elif i == EffectChanceIndex:
                try:
                    TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    print(e)
                    TableLine.append(0)
                    Error += "5"
                
            elif i == RangeIndex:
                try:
                    Range = Line.split(")")[1].replace(",", "").strip()

                    C = {"MySide":"My Side", "FoeSide":"Foe Side",
                         "AllButUser":"All But User", "UserOrPartner":"User Or Partner",
                         "TargetOrPartner":"Target Or Partner", "LastHitMe":"Last Attacker"}

                    for Key in C:
                        if Range == Key:
                            Range = C[Key]
                            break
                    
                    TableLine.append(Range)
                except Exception as e:
                    print(e)
                    TableLine.append("Target")
                    Error += "6"

            elif i == PriorityIndex:
                try:
                    P = int(Line.split(")")[1].replace(",", "").strip())

                    if P > 127:
                        P = 256 - P
                        P = -P

                    TableLine.append(P)
                except Exception as e:
                    print(e)
                    TableLine.append(0)
                    Error += "7"

            elif i == MoveFlagIndex:
                try:
                    F = Line.split(")")[1].replace(",", "").strip()
                    MoveFlags = [0,0,0,0,0,0,0,0]

                    for i, Flag in enumerate(F.split("+")):
                        Flag = Flag.strip()[2:]

                        if int(Flag, 16) & 128 // 2**i:
                            MoveFlags[i] = 1

                    TableLine.append(MoveFlags)
                except Exception as e:
                    print(e)
                    TableLine.append([0,0,0,0,0,0,0,0])
                    Error += "8"

            elif i == DamageFormulaIndex:
                try:
                    TableLine.append(Line.split(")")[1].replace(",", "").strip()[2:])
                except Exception as e:
                    print(e)
                    TableLine.append("00")
                    Error += "9"

            elif i == MoveKindIndex:
                try:
                    TableLine.append(Line.split(")")[1].replace(",", "").strip())
                except Exception as e:
                    print(e)
                    TableLine.append("Status")
                    Error += "A"

            elif i == ScriptArgIndex:
                try:
                    TableLine.append(int(Line.split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    print(e)
                    TableLine.append(0)
                    Error += "B"

            elif i == DescriptionIndex: # Includes a Move Description Line
                try:
                    Text = Line.split(")")[1].replace(",","").strip()
                    if Text != "":
                        TableLine.append(FormatDescription(Text))
                    else:
                        TableLine.append('')
                except Exception as e:
                    print(e)
                    TableLine.append('')
                    Error += "C"

        if len(TableLine) < 14:
            TableLine = ["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]
            Error += "D"
            
        Table.append(TableLine)

    return Table, Error

#------------------------------------------------------------
# Display Errors in Table
#------------------------------------------------------------
def LoadTableErrors(Root, Table, Error):
    if Error == "":
        mb.MakeInfoBox(Root, "Success!", "The table was created!",
                    ["The table was created successfully.",
                     "It has {} Moves in total.".format(len(Table))])
    else:
        ErrorLines = ["There was a problem loading the table!",
                      "Default values were provided for bad data.",
                      "The table has {} Moves in total.".format(len(Table)),
                      "\n",
                      "The following errors occurred."]
        
        if "0" in Error:
            ErrorLines.append("Error loading {} Move Script values".format(Error.count("0")))

        if "1" in Error:
            ErrorLines.append("Error loading {} Base Power values".format(Error.count("1")))

        if "2" in Error:
            ErrorLines.append("Error loading {} Type values".format(Error.count("2")))

        if "3" in Error:
            ErrorLines.append("Error loading {} Accuracy values".format(Error.count("3")))

        if "4" in Error:
            ErrorLines.append("Error loading {} Power Point values".format(Error.count("4")))

        if "5" in Error:
            ErrorLines.append("Error loading {} Effect Chance values".format(Error.count("5")))

        if "6" in Error:
            ErrorLines.append("Error loading {} Range values".format(Error.count("6")))

        if "7" in Error:
            ErrorLines.append("Error loading {} Priority values".format(Error.count("7")))

        if "8" in Error:
            ErrorLines.append("Error loading {} Move Flag values".format(Error.count("8")))

        if "9" in Error:
            ErrorLines.append("Error loading {} Damage Formula values".format(Error.count("9")))

        if "A" in Error:
            ErrorLines.append("Error loading {} Move Kind values".format(Error.count("A")))

        if "B" in Error:
            ErrorLines.append("Error loading {} Script Argument values".format(Error.count("B")))

        if "C" in Error:
            ErrorLines.append("Error loading {} Move Description values".format(Error.count("C")))

        if "X" in Error:
            ErrorLines.append("Error loading {} Move Name values".format(Error.count("X")))

        if "D" in Error:
            ErrorLines.append("{} lines could not be loaded and were set to default values.".format(Error.count("D")))

        mb.MakeInfoBox(Root, "Error!", "There was a problem.", ErrorLines)

#------------------------------------------------------------
# Process Table To Remove Mistakes
#------------------------------------------------------------
def ProcessTable(Root, Table):
    Error = ""
    for i, Entry in enumerate(Table): # Get rid of blank line entries
        if Entry == ['', '', '', '', '', '', '', '', '', '', '', '', '', '']:
            Table.pop(i)

        for j, Line in enumerate(Entry): # Correct type mismatches
            if j > 13: # Extra bits
                Entry.pop(j)
                
            match j:
                case 0:
                    if type(Line) != str or Line == "":
                        Table[i][j] = "Move Name"
                        Error += "X"
                        
                case 1: # Move Script
                    if Line.upper() not in HexBytes:
                        Table[i][j] = "00"
                        Error += "0"
                    else:
                        Table[i][j] = Line.upper()

                case 2: # Base Power
                    if type(Line) != int:
                        Table[i][j] = 0
                        Error += "1"

                case 3: # Type
                    if Line not in TypeConversion:
                        Table[i][j] = "Normal"
                        Error += "2"

                case 4: # Accuracy
                    if type(Line) != int:
                        Table[i][j] = 0
                        Error += "3"

                case 5: # Power Point
                    if type(Line) != int:
                        Table[i][j] = 0
                        Error += "4"

                case 6: # Effect Chance
                    if type(Line) != int:
                        Table[i][j] = 0
                        Error += "5"

                case 7: # Move Range
                    if Line not in RangeConversion:
                        Table[i][j] = "Target"
                        Error += "6"

                case 8: # Priority
                    if type(Line) != int:
                        Table[i][j] = 0
                        Error += "7"

                case 9: # Move Flags
                    if len(Line) != 8:
                        Table[i][j] = [0,0,0,0,0,0,0,0]
                        Error += "8"
                        
                    else:
                        if not all(y in (0,1) for y in Line): 
                            Table[i][j] = Line
                            Error += "8"

                case 10: # Damage Formula
                    if Line.upper() not in HexBytes:
                        Table[i][j] = "00"
                        Error += "9"
                    else:
                        Table[i][j] = Line.upper()

                case 11: # Move Kind
                    if Line != "Physical" and Line != "Special" and Line != "Status":
                        Table[i][j] = "Status"
                        Error += "A"

                case 12: # Move Script
                    if type(Line) != int:
                        Table[i][j] = 0
                        Error += "B"

                case 13: # Move Description
                    if type(Line) != str:
                        Table[i][j] = ""
                        Error += "C"                    

    if Error != "":
        mb.MakeInfoBox(Root, "Error!", "Table has errors",
                    ["One or more entries of the table has an error.",
                     "Invalid entries were replaced with default values."])

    if len(Table) == 0:
        Table = [["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]]

        mb.MakeInfoBox(Root, "Error!", "There was a problem.",
                    ["There was a problem loading the table.",
                     "A blank one was provided instead.",
                     "It has {} Moves in total.".format(len(Table))])
        
    return Table
