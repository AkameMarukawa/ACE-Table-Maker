# ACE-Table-Maker
A tool for editing and compiling Attack Data, Move Name and Move Description Tables for Pokemon Gen III games. Meant for Akame's Custom Engine.

# Introduction
Akame's Custom Engine (which has not been released yet) is a project for Pokemon FireRed which aims to redesign the battle engine for easier customisability. In the process of doing this, the Move Scripts were revamped and the Attack Data Table was slightly reformatted. The purpose of this tool is to make editing those tables a little easier. They can still be edited with other tools, but descriptions of Move Scripts or what bytes do may be incorrect.

# What Can You Do?
When you open the program, you will have the option to make a new table or open an old one. Tables are saved as human-readable text files before they are compiled. When editing, you will be editing the human-readable version. The text table is saved in the following format:

```
Move Name
(Move Script) 0x00
(Base Power) 0
(Type) Normal
(Accuracy) 0
(Power Points) 0
(Effect Chance) 0
(Range) Target
(Priority) 0
(Move Flags)  0x0 + 0x0 + 0x0 + 0x0 + 0x0 + 0x0 + 0x0 + 0x0 
(Damage Formula) 0x00
(Kind) Status
(Script Arg) 0
(Description) This is the Move Description
```
Once a table is open, you can edit and save the human-readable version. When you are done, you can compile it into a hex binary file, which can then be copied to your ROM.

# Creating Files
When you hit "New Table", you will be able to create a new human-readable table saved as a text file. This will overwrite any table already present in the editor. In addition, you may give it a list of Move Names saved as a text file to use when creating the table. This file should have each Move Name on a separate line. Move Names can be up to 12 characters long.

If the table you create is shorter than the list of Moves you chose, then the program will stop reading the Move List early. If the table you create is longer, then the extra Moves will be given a default name. If you choose not to load a Move Names file, then all entries will have a default Move Name.

Tables may consist of up to 999 Moves. This should be enough for most people.

# Opening Files
You can open a human-readable table in the format above, saved as a plain text file. In addition, you may also open a compiled table which was saved as a .bin file. However, Move Names and Descriptions will not be loaded as they are not part of the Attack Data Table (see **Compiling**).

# Saving
When you hit the "Save Table" button, all changes that you've made in the editor will be committed to the open file. **Your changes will not be written until you do this!** The "Save Table As" button will allow you to save the current table as a new file. You can then choose to continue editing this new file, or stay editing the old one.

# Compiling
There are three options when compiling a table. Tables compile to a .bin file which can be opened in a Hex Editor and pasted into the ROM.

The Attack Data Table consists of one entry per Move and contains all of the information in the editor except for the Move Name and Move Description. Each entry is a fixed length and contains no pointers, so you do not need to provide an address ahead of time. You will only need to repoint the table if you add new Moves to it, otherwise the compiled table can be copied over the old one in a Hex Editor.

The Move Name and Move Description Tables are tables of pointers which point to strings of text. You will need to provide the tool with a starting address for your table if you are compiling either of these. When inserting the table, it needs to be inserted at the same address that you gave, so make sure to write it down. Failure to do so will result in crashes due to the wrong data being read.

You will be given, with the Move Name and Description Tables, the option to "future-proof" it. What this means is that each entry will be a fixed length (13 bytes for the Move Name table and 77 bytes for the Move Description table). Not all of the bytes in that entry will necessarily be filled out when compiling, so it uses up more space. However, if you decide to change the length of a Move Name or Description later, you will not need to repoint the table since the space will already have been allocated when you compiled it the first time. If you future-proof the table the first time you compile it, you will need to select this option each time you compile it afterwards for it to be the same length. Adding additional Moves will still require repointing as usual.

Future-proofing the table is recommended unless you are seriously low on free space, since it makes making changes later on less of a hassle. Likely you will need to repoint the table once, though, since the default tables will be shorter than the future-proofed table. After this, unless Moves are added, no further repointing is needed.

# Converting
You can convert a table that is in the old FireRed format to the new ACE format. This entails changing the Move Scripts to their ACE equivalents and setting the Script Arguments accordingly, changing the Move Ranges to the correct values, and adding in Damage Formulae and their arguments properly.

This process will be a perfect conversion if the input table is an unedited Fire Red table. However, if edits were made, the conversion may not be completely perfect. Still, it should save a good amount of time over having to do the whole entire thing yourself.
