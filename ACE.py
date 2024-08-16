import os
import sys
import platform
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as stxt
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from subprocess import call, Popen
from random import randint
from math import modf

# Set the Version Number
VerNum = "2.1.0"
AutoSave = True

def PrintError(Error):
    print(Error)

# ------------------------------------------------------------
# Set Platform Variable
# ------------------------------------------------------------
if(platform.system() == 'Darwin'): # This is a Mac
    OnAMac = True
else:
    OnAMac = False

if OnAMac:
    Paste = "<Command-v>"
    if os.path.basename(os.getcwd()) == "Resources":
        InitialFolder = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
    else:
        InitialFolder = os.getcwd()
else:
    Paste = "<Control-v>"
    if hasattr(sys, "_MEIPASS"):
        InitialFolder = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    else:
        InitialFolder = os.getcwd()

SmallSize = 16

"""
================================================================================================
DICTIONARIES - Create the Lists and Dictionaries used by many other functions
================================================================================================
"""

# ------------------------------------------------------------
# Preset Move List Dictionary
# ---------------------------------------------------------
PresetMoveList = {
        "None": ["None", "00", 0, "Normal", 0, 0, 0, 
                "Target", 0, [0, 1, 1, 1, 1, 1, 1, 1], "00", "Status", 0, 
                ""],

        "Pound": ["Pound", "00", 40, "Normal", 100, 35, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A physical attack\ndelivered with a\nlong tail or a\nforeleg, etc."],

        "Karate Chop": ["Karate Chop", "00", 50, "Fighting", 100, 25, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is attacked\nwith a sharp chop.\nIt has a high\ncritical-hit ratio."],

        "Double-Slap": ["Double-Slap", "1D", 15, "Normal", 85, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 21, 
                "The foe is slapped\nrepeatedly, back\nand forth, two to\nfive times."],

        "Comet Punch": ["Comet Punch", "1D", 18, "Normal", 85, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 21, 
                "The foe is hit with\na flurry of punches\nthat strike two to\nfive times."],

        "Mega Punch": ["Mega Punch", "00", 80, "Normal", 85, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is slugged\nby a punch thrown\nwith muscle-packed\npower."],

        "Pay Day": ["Pay Day", "22", 40, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 1, 
                "Numerous coins are\nhurled at the foe.\nMoney is earned\nafter battle."],

        "Fire Punch": ["Fire Punch", "04", 75, "Fire", 100, 15, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is punched\nwith a fiery fist.\nIt may leave the\nfoe with a burn."],

        "Ice Punch": ["Ice Punch", "05", 75, "Ice", 100, 15, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is punched\nwith an icy fist.\nIt may leave the\nfoe frozen."],

        "Thunderpunch": ["Thunderpunch", "06", 75, "Electric", 100, 15, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is punched\nwith an electrified\nfist. It may leave\nthe foe paralyzed."],

        "Scratch": ["Scratch", "00", 40, "Normal", 100, 35, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "Hard, pointed, and\nsharp claws rake\nthe foe."],

        "Vise Grip": ["Vise Grip", "00", 55, "Normal", 100, 30, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "Huge, impressive\npincers grip and\nsqueeze the foe."],

        "Guillotine": ["Guillotine", "00", 0, "Normal", 30, 5, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 1], "D9", "Physical", 0, 
                "A vicious tearing\nattack with\npincers. The foe\nfaints if it hits."],

        "Razor Wind": ["Razor Wind", "00", 80, "Normal", 100, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "Blades of wind hit\nthe foe on the 2nd\nturn. It has a high\ncritical-hit ratio."],

        "Swords Dance": ["Swords Dance", "0A", 0, "Normal", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                "A frenetic dance of\nfighting. It\nsharply raises the\nAttack Stat."],

        "Cut": ["Cut", "00", 50, "Normal", 95, 30, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A basic attack.\nIt can be used to\ncut down thin trees\nand grass."],

        "Gust": ["Gust", "00", 40, "Flying", 100, 35, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "Strikes the foe\nwith a gust of wind\nwhipped up by\nwings."],

        "Wing Attack": ["Wing Attack", "00", 60, "Flying", 100, 35, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is struck\nwith large,\nimposing wings\nspread wide."],

        "Whirlwind": ["Whirlwind", "1C", 0, "Normal", 0, 20, 0, 
                "Target", 250, [0, 0, 0, 1, 0, 1, 0, 0], "00", "Status", 0, 
                "The foe is made to\nswitch out with an\nally. In the wild,\nthe battle ends."],

        "Fly": ["Fly", "00", 90, "Flying", 95, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A 2-turn move that\nhits on the 2nd\nturn. Use it to fly\nto any known town."],

        "Bind": ["Bind", "2A", 15, "Normal", 85, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A long body or\ntentacles are used\nto bind the foe for\ntwo to five turns."],

        "Slam": ["Slam", "00", 80, "Normal", 75, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is struck\nwith a long tail,\nvines, etc."],

        "Vine Whip": ["Vine Whip", "00", 45, "Grass", 100, 25, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is struck\nwith slender,\nwhiplike vines."],

        "Stomp": ["Stomp", "00", 65, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is stomped\nwith a big foot.\nIt may make the\nfoe flinch."],

        "Double Kick": ["Double Kick", "1D", 30, "Fighting", 100, 30, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                "Two legs are used\nto quickly kick the\nfoe twice in one\nturn."],

        "Mega Kick": ["Mega Kick", "00", 120, "Normal", 75, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is attacked\nby a kick fired\nwith muscle-packed\npower."],

        "Jump Kick": ["Jump Kick", "00", 100, "Fighting", 95, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user jumps up\nhigh, then kicks.\nIf it misses, the\nuser hurts itself."],

        "Rolling Kick": ["Rolling Kick", "1F", 60, "Fighting", 85, 15, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A quick kick from a\nrolling spin.\nIt may make the\nfoe flinch."],

        "Sand-Attack": ["Sand-Attack", "17", 0, "Ground", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "A lot of sand is\nhurled in the foe's\nface, reducing its\naccuracy."],

        "Headbutt": ["Headbutt", "1F", 70, "Normal", 100, 15, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user sticks its\nhead out and rams.\nIt may make the\nfoe flinch."],

        "Horn Attack": ["Horn Attack", "00", 65, "Normal", 100, 25, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is jabbed\nwith a sharply\npointed horn to\ninflict damage."],

        "Fury Attack": ["Fury Attack", "1D", 15, "Normal", 85, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 21, 
                "The foe is jabbed\nrepeatedly with a\nhorn or beak two to\nfive times."],

        "Horn Drill": ["Horn Drill", "00", 0, "Normal", 30, 5, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 1], "D9", "Physical", 0, 
                "The horn is rotated\nlike a drill to\nram. The foe will\nfaint if it hits."],

        "Tackle": ["Tackle", "00", 40, "Normal", 100, 35, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A physical attack\nin which the user\ncharges, full body,\ninto the foe."],

        "Body Slam": ["Body Slam", "06", 85, "Normal", 100, 15, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user drops its\nfull body on the\nfoe. It may leave\nthe foe paralyzed."],

        "Wrap": ["Wrap", "2A", 15, "Normal", 90, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A long body or\nvines are used to\nwrap the foe for\ntwo to five turns."],

        "Take Down": ["Take Down", "30", 90, "Normal", 85, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 25, 
                "A reckless, full-\nbody charge attack\nthat also hurts the\nuser a little."],

        "Thrash": ["Thrash", "1B", 120, "Normal", 100, 10, 0, 
                "Random", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 3, 
                "The user rampages\nabout for two to\nthree turns, then\nbecomes confused."],

        "Double-Edge": ["Double-Edge", "30", 120, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 33, 
                "A reckless, life-\nrisking tackle\nthat also hurts the\nuser a little."],

        "Tail Whip": ["Tail Whip", "13", 0, "Normal", 100, 30, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "The user wags its\ntail cutely, making\nthe foe lower its\nDefense stat."],

        "Poison Sting": ["Poison Sting", "02", 15, "Poison", 100, 35, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "The foe is stabbed\nwith a toxic barb,\netc. It may poison\nthe foe."],

        "Twineedle": ["Twineedle", "1D", 25, "Bug", 100, 20, 20, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Physical", 2, 
                "The foe is stabbed\ntwice with foreleg\nstingers. It may\npoison the foe."],

        "Pin Missile": ["Pin Missile", "1D", 25, "Bug", 95, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 21, 
                "Sharp pins are shot\nat the foe and hit\ntwo to five times\nat once."],

        "Leer": ["Leer", "13", 0, "Normal", 100, 30, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "The foe is given an\nintimidating look\nthat lowers its\nDefense stat."],

        "Bite": ["Bite", "1F", 60, "Dark", 100, 25, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user bites with\nvicious fangs.\nIt may make the\nfoe flinch."],

        "Growl": ["Growl", "12", 0, "Normal", 100, 40, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "The user growls in\na cute way, making\nthe foe lower its\nAttack stat."],

        "Roar": ["Roar", "1C", 0, "Normal", 0, 20, 0, 
                "Target", 250, [0, 0, 0, 1, 0, 1, 0, 0], "00", "Status", 0, 
                "The foe is made to\nswitch out with an\nally. In the wild,\nthe battle ends."],

        "Sing": ["Sing", "01", 0, "Normal", 55, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "A soothing song\nin a calming voice\nlulls the foe into\na deep slumber."],

        "Supersonic": ["Supersonic", "31", 0, "Normal", 55, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "The user generates\nodd sound waves.\nIt may confuse the\nfoe."],

        "Sonic Boom": ["Sonic Boom", "00", 0, "Normal", 90, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "24", "Special", 0, 
                ""],

        "Disable": ["Disable", "56", 0, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "For a few turns,\nit prevents the foe\nfrom using the move\nit last used."],

        "Acid": ["Acid", "13", 40, "Poison", 100, 30, 33, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Ember": ["Ember", "04", 40, "Fire", 100, 25, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is attacked\nwith small flames.\nThe foe may suffer\na burn."],

        "Flamethrower": ["Flamethrower", "04", 90, "Fire", 100, 15, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is scorched\nwith intense flames.\nThe foe may suffer\na burn."],

        "Mist": ["Mist", "2E", 0, "Ice", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "The ally party is\nprotected by a\nmist that prevents\nstat reductions."],

        "Water Gun": ["Water Gun", "00", 40, "Water", 100, 25, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is struck\nwith a lot of water\nexpelled forcibly\nfrom the mouth."],

        "Hydro Pump": ["Hydro Pump", "00", 110, "Water", 80, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "A high volume of\nwater is blasted at\nthe foe under great\npressure."],

        "Surf": ["Surf", "00", 90, "Water", 100, 15, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "A big wave crashes\ndown on the foe.\nCan also be used\nfor crossing water."],

        "Ice Beam": ["Ice Beam", "05", 90, "Ice", 100, 10, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is struck\nwith an icy beam.\nIt may freeze the\nfoe solid."],

        "Blizzard": ["Blizzard", "05", 110, "Ice", 70, 5, 10, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is blasted\nwith a blizzard.\nIt may freeze the\nfoe solid."],

        "Psybeam": ["Psybeam", "31", 65, "Psychic", 100, 20, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "A peculiar ray is\nshot at the foe.\nIt may leave the\nfoe confused."],

        "Bubblebeam": ["Bubblebeam", "14", 65, "Water", 100, 20, 33, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "A spray of bubbles\nstrikes the foe.\nIt may lower the\nfoe's SPEED stat."],

        "Aurora Beam": ["Aurora Beam", "12", 65, "Ice", 100, 20, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Hyper Beam": ["Hyper Beam", "50", 150, "Normal", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "A severely damaging\nattack that makes\nthe user rest on\nthe next turn."],

        "Peck": ["Peck", "00", 35, "Flying", 100, 35, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is jabbed\nwith a sharply\npointed beak or\nhorn."],

        "Drill Peck": ["Drill Peck", "00", 80, "Flying", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A corkscrewing\nattack with the\nsharp beak acting\nas a drill."],

        "Submission": ["Submission", "30", 80, "Fighting", 80, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 25, 
                ""],

        "Low Kick": ["Low Kick", "00", 0, "Fighting", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "15", "Physical", 0, 
                "A low, tripping kick\nthat inflicts more\ndamage on heavier\nfoes."],

        "Counter": ["Counter", "00", 0, "Fighting", 100, 20, 0, 
                "LastHitMe", 251, [0, 0, 0, 0, 0, 0, 1, 1], "00B", "Physical", 0, 
                "A retaliation move\nthat counters any\nphysical hit with\ndouble the damage."],

        "Seismic Toss": ["Seismic Toss", "00", 0, "Fighting", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "01", "Physical", 0, 
                ""],

        "Strength": ["Strength", "00", 80, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is slugged\nat maximum power.\nCan also be used\nto move boulders."],

        "Absorb": ["Absorb", "03", 20, "Grass", 100, 25, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 50, 
                "An attack that\nabsorbs half the\ndamage it inflicted\nto restore HP."],

        "Mega Drain": ["Mega Drain", "03", 40, "Grass", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 50, 
                "A tough attack that\ndrains half the\ndamage it inflicted\nto restore HP."],

        "Leech Seed": ["Leech Seed", "54", 0, "Grass", 90, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "A seed is planted\non the foe to steal\nsome HP for the\nuser on every turn."],

        "Growth": ["Growth", "CF", 0, "Normal", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 4, 
                "The user's body is\nforced to grow,\nraising the SP.\nATK stat."],

        "Razor Leaf": ["Razor Leaf", "00", 55, "Grass", 95, 25, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Solarbeam": ["Solarbeam", "00", 120, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Poisonpowder": ["Poisonpowder", "02", 0, "Poison", 75, 35, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "A cloud of toxic\ndust is scattered.\nIt may poison the\nfoe."],

        "Stun Spore": ["Stun Spore", "06", 0, "Grass", 75, 30, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "Paralyzing dust is\nscattered wildly.\nIt may paralyze\nthe foe."],

        "Sleep Powder": ["Sleep Powder", "01", 0, "Grass", 75, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Petal Dance": ["Petal Dance", "1B", 120, "Grass", 100, 10, 0, 
                "Random", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Special", 3, 
                "The user attacks\nwith petals for two\nto three turns,\nthen gets confused."],

        "String Shot": ["String Shot", "14", 0, "Bug", 95, 40, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "The foe is bound\nwith strings shot\nfrom the mouth to\nreduce its SPEED."],

        "Dragon Rage": ["Dragon Rage", "00", 0, "Dragon", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "44", "Special", 0, 
                ""],

        "Fire Spin": ["Fire Spin", "2A", 35, "Fire", 85, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is trapped\nin an intense spiral\nof fire that rages\ntwo to five turns."],

        "Thundershock": ["Thundershock", "06", 40, "Electric", 100, 30, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "An electric shock\nattack that may\nalso leave the foe\nparalyzed."],

        "Thunderbolt": ["Thunderbolt", "06", 90, "Electric", 100, 15, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "A strong electrical\nattack that may\nalso leave the foe\nparalyzed."],

        "Thunder Wave": ["Thunder Wave", "06", 0, "Electric", 90, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "A weak electric\nshock that is sure\nto cause paralysis\nif it hits."],

        "Thunder": ["Thunder", "06", 110, "Electric", 70, 10, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "A brutal lightning\nattack that may\nalso leave the foe\nparalyzed."],

        "Rock Throw": ["Rock Throw", "00", 50, "Rock", 90, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "The foe is attacked\nwith a shower of\nsmall, easily\nthrown rocks."],

        "Earthquake": ["Earthquake", "00", 100, "Ground", 100, 10, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Fissure": ["Fissure", "00", 0, "Ground", 30, 5, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "D9", "Physical", 0, 
                "The foe is dropped\ninto a fissure.\nThe foe faints if it\nhits."],

        "Dig": ["Dig", "00", 80, "Ground", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack that hits\non the 2nd turn.\nCan also be used\nto exit dungeons."],

        "Toxic": ["Toxic", "21", 0, "Poison", 90, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "A move that badly\npoisons the foe.\nIts poison damage\nworsens every turn."],

        "Confusion": ["Confusion", "31", 50, "Psychic", 100, 25, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "A weak telekinetic\nattack that may\nalso leave the foe\nconfused."],

        "Psychic": ["Psychic", "16", 90, "Psychic", 100, 10, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "A strong telekinetic\nattack. It may also\nlower the foe's\nSP. DEF stat."],

        "Hypnosis": ["Hypnosis", "01", 0, "Psychic", 60, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "Hypnotic suggestion\nis used to make the\nfoe fall into a\ndeep sleep."],

        "Meditate": ["Meditate", "0A", 0, "Psychic", 0, 40, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "The user meditates\nto awaken its power\nand raise its\nATTACK stat."],

        "Agility": ["Agility", "0C", 0, "Psychic", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                "The user relaxes\nand lightens its\nbody to sharply\nboost its SPEED."],

        "Quick Attack": ["Quick Attack", "00", 40, "Normal", 100, 30, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An almost invisibly\nfast attack that\nis certain to strike\nfirst."],

        "Rage": ["Rage", "51", 20, "Normal", 100, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack that\nbecomes stronger\neach time the user\nis hit in battle."],

        "Teleport": ["Teleport", "29", 0, "Psychic", 0, 20, 0, 
                "User", 250, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Night Shade": ["Night Shade", "00", 0, "Ghost", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "01", "Special", 0, 
                "An attack with a\nmirage that inflicts\ndamage matching\nthe user's level."],

        "Mimic": ["Mimic", "52", 0, "Normal", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Status", 0, 
                "The user copies the\nmove last used by\nthe foe for the\nrest of the battle."],

        "Screech": ["Screech", "13", 0, "Normal", 85, 40, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                ""],

        "Double Team": ["Double Team", "10", 0, "Normal", 0, 15, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "The user creates\nillusory copies of\nitself to raise its\nevasiveness."],

        "Recover": ["Recover", "9D", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Harden": ["Harden", "0B", 0, "Normal", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "The user stiffens\nall the muscles in\nits body to raise\nits DEFENSE stat."],

        "Minimize": ["Minimize", "6C", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "The user compresses\nall the cells in its\nbody to raise its\nevasiveness."],

        "Smokescreen": ["Smokescreen", "17", 0, "Normal", 0, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "An obscuring cloud\nof smoke or ink\nreduces the foe's\naccuracy."],

        "Confuse Ray": ["Confuse Ray", "31", 0, "Ghost", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "The foe is exposed\nto a sinister ray\nthat triggers\nconfusion."],

        "Withdraw": ["Withdraw", "0B", 0, "Water", 0, 40, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "The user withdraws\nits body in its hard\nshell, raising its\nDEFENSE stat."],

        "Defense Curl": ["Defense Curl", "9C", 0, "Normal", 0, 40, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "The user curls up\nto conceal weak\nspots and raise its\nDEFENSE stat."],

        "Barrier": ["Barrier", "0B", 0, "Psychic", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                "The user creates a\nsturdy wall that\nsharply raises its\nDEFENSE stat."],

        "Light Screen": ["Light Screen", "23", 0, "Psychic", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "A wall of light\ncuts damage from\nSP. ATK attacks\nfor five turns."],

        "Haze": ["Haze", "19", 0, "Ice", 0, 30, 0, 
                "Everyone", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Reflect": ["Reflect", "41", 0, "Psychic", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "A wall of light\ncuts damage from\nphysical attacks\nfor five turns."],

        "Focus Energy": ["Focus Energy", "2F", 0, "Normal", 0, 0, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Bide": ["Bide", "1A", 0, "Normal", 0, 10, 0, 
                "User", 1, [0, 0, 1, 0, 0, 0, 1, 1], "CB", "Physical", 3, 
                "The user endures\nattacks for two\nturns, then strikes\nback double."],

        "Metronome": ["Metronome", "53", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "Waggles a finger\nand stimulates the\nbrain into using any\nmove at random."],

        "Mirror Move": ["Mirror Move", "09", 0, "Flying", 0, 20, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "The user counters\nthe move last used\nby the foe with the\nsame move."],

        "Self-Destruct": ["Self-Destruct", "07", 200, "Normal", 100, 5, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "The user blows up\nto inflict severe\ndamage, even\nmaking itself faint."],

        "Egg Bomb": ["Egg Bomb", "00", 100, "Normal", 75, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "A large egg is\nhurled with great\nforce at the foe to\ninflict damage."],

        "Lick": ["Lick", "06", 30, "Ghost", 100, 30, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is licked\nand hit with a long\ntongue. It may\nalso paralyze."],

        "Smog": ["Smog", "02", 30, "Poison", 70, 20, 40, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is attacked\nwith exhaust gases.\nIt may also poison\nthe foe."],

        "Sludge": ["Sludge", "02", 65, "Poison", 100, 20, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "Toxic sludge is\nhurled at the foe.\nIt may poison the\ntarget."],

        "Bone Club": ["Bone Club", "1F", 65, "Ground", 85, 20, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "The foe is clubbed\nwith a bone held in\nhand. It may make\nthe foe flinch."],

        "Fire Blast": ["Fire Blast", "04", 110, "Fire", 85, 5, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is hit with\nan intense flame.\nIt may leave the\ntarget with a burn."],

        "Waterfall": ["Waterfall", "1F", 80, "Water", 100, 15, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A powerful charge\nattack. It can also\nbe used to climb\na waterfall."],

        "Clamp": ["Clamp", "2A", 35, "Water", 85, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is clamped\nand squeezed by\nthe user's shell for\ntwo to five turns."],

        "Swift": ["Swift", "00", 60, "Normal", 0, 20, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Skull Bash": ["Skull Bash", "00", 130, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user raises its\nDEFENSE in the 1st\nturn, then attacks\nin the 2nd turn."],

        "Spike Cannon": ["Spike Cannon", "1D", 20, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 21, 
                "Sharp spikes are\nfired at the foe to\nstrike two to five\ntimes."],

        "Constrict": ["Constrict", "14", 10, "Normal", 100, 35, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                "The foe is attacked\nwith long tentacles\nor vines. It may\nlower SPEED."],

        "Amnesia": ["Amnesia", "0E", 0, "Psychic", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                "Forgets about\nsomething and\nsharply raises\nSP. DEF."],

        "Kinesis": ["Kinesis", "17", 0, "Psychic", 80, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "The user distracts\nthe foe by bending\na spoon. It may\nlower accuracy."],

        "Softboiled": ["Softboiled", "9D", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "Heals the user by\nup to half its full\nHP. It can be used\nto heal an ally."],

        "Hi Jump Kick": ["Hi Jump Kick", "00", 130, "Fighting", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A strong jumping\nknee kick. If it\nmisses, the user is\nhurt."],

        "Glare": ["Glare", "06", 0, "Normal", 100, 30, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "The user intimidates\nthe foe with the\ndesign on its belly\nto cause paralysis."],

        "Dream Eater": ["Dream Eater", "03", 100, "Psychic", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 50, 
                "Absorbs half the\ndamage it inflicted\non a sleeping foe\nto restore HP."],

        "Poison Gas": ["Poison Gas", "02", 0, "Poison", 90, 40, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "The foe is sprayed\nwith a cloud of\ntoxic gas that may\npoison the foe."],

        "Barrage": ["Barrage", "1D", 15, "Normal", 85, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 21, 
                "Round objects are\nhurled at the foe\nto strike two to\nfive times."],

        "Leech Life": ["Leech Life", "03", 80, "Bug", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 50, 
                "An attack that\nabsorbs half the\ndamage it inflicted\nto restore HP."],

        "Lovely Kiss": ["Lovely Kiss", "01", 0, "Normal", 75, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "The user forces a\nkiss on the foe\nwith a scary face\nthat induces sleep."],

        "Sky Attack": ["Sky Attack", "1F", 140, "Flying", 90, 5, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Transform": ["Transform", "39", 0, "Normal", 0, 10, 0, 
                "Target", 0, [0, 1, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "The user transforms\ninto a copy of the\nfoe with even the\nsame move set."],

        "Bubble": ["Bubble", "14", 40, "Water", 100, 30, 10, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "A spray of bubbles\nhits the foe.\nIt may lower the\nfoe's SPEED stat."],

        "Dizzy Punch": ["Dizzy Punch", "31", 70, "Normal", 100, 10, 20, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is hit with\na rhythmic punch\nthat may leave it\nconfused."],

        "Spore": ["Spore", "01", 0, "Grass", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "The user scatters\nbursts of fine\nspores that induce\nsleep."],

        "Flash": ["Flash", "17", 0, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "A blast of light\nthat cuts the foe's\naccuracy. It also\nilluminates caves."],

        "Psywave": ["Psywave", "000", 0, "Psychic", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "007", "Special", 0, 
                "The foe is attacked\nwith an odd, hot\nenergy wave that\nvaries in intensity."],

        "Splash": ["Splash", "8B", 0, "Normal", 0, 40, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "The user just flops\nand splashes around\nwithout having any\neffect."],

        "Acid Armor": ["Acid Armor", "0B", 0, "Poison", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                "The user alters its\ncells to liquefy\nitself and sharply\nraise DEFENSE."],

        "Crabhammer": ["Crabhammer", "00", 100, "Water", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Explosion": ["Explosion", "07", 250, "Normal", 100, 5, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "The user explodes\nto inflict terrible\ndamage even while\nfainting itself."],

        "Fury Swipes": ["Fury Swipes", "1D", 18, "Normal", 80, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 21, 
                "The foe is raked\nwith sharp claws or\nscythes two to five\ntimes."],

        "Bonemerang": ["Bonemerang", "1D", 50, "Ground", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 2, 
                "The user throws a\nbone that hits the\nfoe once, then once\nagain on return."],

        "Rest": ["Rest", "25", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                "The user sleeps for\ntwo turns to fully\nrestore HP and heal\nany status problem."],

        "Rock Slide": ["Rock Slide", "1F", 75, "Rock", 90, 10, 30, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "Large boulders are\nhurled at the foe.\nIt may make the\nfoe flinch."],

        "Hyper Fang": ["Hyper Fang", "1F", 80, "Normal", 90, 15, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is attacked\nwith sharp fangs.\nIt may make the\nfoe flinch."],

        "Sharpen": ["Sharpen", "0A", 0, "Normal", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "The user reduces\nits polygon count\nto sharpen edges\nand raise ATTACK."],

        "Conversion": ["Conversion", "1E", 0, "Normal", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "The user changes\nits type to match\nthe type of one of\nits moves."],

        "Tri-Attack": ["Tri-Attack", "24", 80, "Normal", 100, 10, 20, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 112, 
                ""],

        "Super Fang": ["Super Fang", "00", 0, "Normal", 90, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "59", "Physical", 0, 
                "The user attacks\nwith sharp fangs\nand halves the\nfoe's HP."],

        "Slash": ["Slash", "00", 70, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Substitute": ["Substitute", "4F", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Struggle": ["Struggle", "30", 50, "Normal", 0, 1, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 1], "00", "Physical", 25, 
                "An attack that is\nused only if there\nis no PP. It also\nhurts the user."],

        "Sketch": ["Sketch", "5F", 0, "Normal", 0, 1, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "This move copies\nthe move last used\nby the foe, then\ndisappears."],

        "Triple Kick": ["Triple Kick", "00", 10, "Fighting", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "1B", "Physical", 0, 
                ""],

        "Thief": ["Thief", "69", 60, "Dark", 100, 25, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack that may\ntake the foe's held\nitem if the user\nisn't holding one."],

        "Spider Web": ["Spider Web", "6A", 0, "Bug", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 0, 0], "00", "Status", 0, 
                "Ensnares the foe\nwith sticky string\nso it doesn't flee\nor switch out."],

        "Mind Reader": ["Mind Reader", "5E", 0, "Normal", 0, 5, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                "The user predicts\nthe foe's action to\nensure its next\nattack hits."],

        "Nightmare": ["Nightmare", "6B", 0, "Ghost", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                "A sleeping foe is\nshown a nightmare\nthat inflicts some\ndamage every turn."],

        "FlameWheel": ["FlameWheel", "7D", 60, "Fire", 100, 25, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user makes a\nfiery charge at the\nfoe. It may cause\na burn."],

        "Snore": ["Snore", "1F", 50, "Normal", 100, 15, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "An attack that can\nbe used only while\nasleep. It may\ncause flinching."],

        "Curse": ["Curse", "6D", 0, "Ghost", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Flail": ["Flail", "00", 0, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "43", "Physical", 0, 
                "A desperate attack\nthat becomes more\npowerful the less\nHP the user has."],

        "Conversion 2": ["Conversion 2", "5D", 0, "Normal", 0, 30, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "The user changes\ntype to make itself\nresistant to the\nlast attack it took."],

        "Aeroblast": ["Aeroblast", "00", 100, "Flying", 95, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Cotton Spore": ["Cotton Spore", "14", 0, "Grass", 100, 40, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                ""],

        "Reversal": ["Reversal", "00", 0, "Fighting", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "43", "Physical", 0, 
                ""],

        "Spite": ["Spite", "64", 0, "Ghost", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 4, 
                "A move that cuts\n2 to 5 PP from the\nmove last used by\nthe foe."],

        "Powder Snow": ["Powder Snow", "05", 40, "Ice", 100, 25, 10, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "Blasts the foe with\na snowy gust.\nIt may cause\nfreezing."],

        "Protect": ["Protect", "6F", 0, "Normal", 0, 10, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "Enables the user to\nevade all attacks.\nIt may fail if used\nin succession."],

        "Mach Punch": ["Mach Punch", "00", 40, "Fighting", 100, 30, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A punch thrown at\nblinding speed.\nIt is certain to\nstrike first."],

        "Scary Face": ["Scary Face", "14", 0, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                "Frightens the foe\nwith a scary face\nto sharply reduce\nits SPEED."],

        "Feint Attack": ["Feint Attack", "00", 60, "Dark", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user draws up\nclose to the foe\ndisarmingly, then\nhits without fail."],

        "Sweet Kiss": ["Sweet Kiss", "31", 0, "Fairy", 75, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "The user kisses\nthe foe with sweet\ncuteness that\ncauses confusion."],

        "Belly Drum": ["Belly Drum", "8E", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "The user maximizes\nits ATTACK stat at\nthe cost of half\nits full HP."],

        "Sludge Bomb": ["Sludge Bomb", "02", 90, "Poison", 100, 10, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "Filthy sludge is\nhurled at the foe.\nIt may poison the\ntarget."],

        "Mud-Slap": ["Mud-Slap", "17", 20, "Ground", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "Mud is hurled in\nthe foe's face to\ninflict damage and\nlower its accuracy."],

        "Octazooka": ["Octazooka", "17", 65, "Water", 85, 10, 50, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "Ink is blasted in\nthe foe's face or\neyes to damage and\nlower accuracy."],

        "Spikes": ["Spikes", "70", 0, "Ground", 0, 20, 0, 
                "FoeSide", 0, [0, 0, 0, 0, 0, 1, 0, 0], "00", "Status", 0, 
                "A trap of spikes is\nlaid around the\nfoe's party to hurt\nfoes switching in."],

        "Zap Cannon": ["Zap Cannon", "06", 120, "Electric", 50, 5, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "An electric blast is\nfired like a cannon\nto inflict damage\nand paralyze."],

        "Foresight": ["Foresight", "71", 0, "Normal", 0, 40, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "Completely negates\nthe foe's efforts to\nheighten its ability\nto evade."],

        "Destiny Bond": ["Destiny Bond", "62", 0, "Ghost", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "If the user faints,\nthe foe delivering\nthe final hit also\nfaints."],

        "Perish Song": ["Perish Song", "72", 0, "Normal", 0, 5, 0, 
                "Everyone", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "Any battler that\nhears this faints\nin three turns\nunless it switches."],

        "Icy Wind": ["Icy Wind", "14", 55, "Ice", 95, 15, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "A chilling wind is\nused to attack.\nIt also lowers the\nSPEED stat."],

        "Detect": ["Detect", "6F", 0, "Fighting", 0, 5, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "Enables the user to\nevade all attacks.\nIt may fail if used\nin succession."],

        "Bone Rush": ["Bone Rush", "1D", 25, "Ground", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 21, 
                "The user strikes\nthe foe with a bone\nin hand two to five\ntimes."],

        "Lock-On": ["Lock-On", "5E", 0, "Normal", 0, 5, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                "The user locks on\nto the foe, making\nthe next move sure\nto hit."],

        "Outrage": ["Outrage", "1B", 120, "Dragon", 100, 10, 0, 
                "Random", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 3, 
                "The user thrashes\nabout for two to\nthree turns, then\nbecomes confused."],

        "Sandstorm": ["Sandstorm", "73", 0, "Rock", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Giga Drain": ["Giga Drain", "03", 75, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 50, 
                "A harsh attack that\nabsorbs half the\ndamage it inflicted\nto restore HP."],

        "Endure": ["Endure", "74", 0, "Normal", 0, 10, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "The user endures\nany hit with 1 HP\nleft. It may fail if\nused in succession."],

        "Charm": ["Charm", "12", 0, "Fairy", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                "The foe is charmed\nby the user's cute\nappeals, sharply\ncutting its ATTACK."],

        "Rollout": ["Rollout", "75", 30, "Rock", 90, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "37", "Physical", 0, 
                ""],

        "False Swipe": ["False Swipe", "00", 40, "Normal", 100, 40, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A restrained attack\nthat always leaves\nthe foe with at\nleast 1 HP."],

        "Swagger": ["Swagger", "76", 0, "Normal", 85, 0, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                "A move that makes\nthe foe confused,\nbut also sharply\nraises its ATTACK."],

        "Milk Drink": ["Milk Drink", "9D", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "Heals the user by\nup to half its full\nHP. It can be used\nto heal an ally."],

        "Spark": ["Spark", "06", 65, "Electric", 100, 20, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An electrically\ncharged tackle that\nmay also paralyze\nthe foe."],

        "Fury Cutter": ["Fury Cutter", "77", 40, "Bug", 95, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "47", "Physical", 0, 
                "An attack that\ngrows stronger on\neach successive\nhit."],

        "Steel Wing": ["Steel Wing", "0B", 70, "Steel", 90, 25, 10, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                "The foe is hit with\nwings of steel.\nIt may also raise\nthe user's DEFENSE."],

        "Mean Look": ["Mean Look", "6A", 0, "Normal", 0, 5, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 0, 0], "00", "Status", 0, 
                "The foe is fixed\nwith a mean look\nthat prevents it\nfrom escaping."],

        "Attract": ["Attract", "78", 0, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "If it is the other\ngender, the foe is\nmade infatuated and\nunlikely to attack."],

        "Sleep Talk": ["Sleep Talk", "61", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "While asleep, the\nuser randomly uses\none of the moves it\nknows."],

        "Heal Bell": ["Heal Bell", "66", 0, "Normal", 0, 5, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "A soothing bell\nchimes to heal the\nstatus problems of\nall allies."],

        "Return": ["Return", "00", 0, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "02", "Physical", 0, 
                "This attack move\ngrows more powerful\nthe more the user\nlikes its TRAINER."],

        "Present": ["Present", "00", 0, "Normal", 90, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "57", "Physical", 0, 
                ""],

        "Frustration": ["Frustration", "00", 0, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "42", "Physical", 0, 
                "This attack move\ngrows more powerful\nthe less the user\nlikes its TRAINER."],

        "Safeguard": ["Safeguard", "7C", 0, "Normal", 0, 25, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "It protects the\nuser's party from\nall status problems\nfor five turns."],

        "Pain Split": ["Pain Split", "57", 0, "Normal", 0, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                "The user adds its\nHP to the foe's HP,\nthen equally shares\nthe total HP."],

        "Sacred Fire": ["Sacred Fire", "04", 100, "Fire", 95, 5, 50, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "A mystical and\npowerful fire\nattack that may\ninflict a burn."],

        "Magnitude": ["Magnitude", "00", 0, "Ground", 100, 30, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "17", "Physical", 0, 
                ""],

        "Dynamicpunch": ["Dynamicpunch", "31", 100, "Fighting", 50, 5, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is punched\nwith the user's full\npower. It confuses\nthe foe if it hits."],

        "Megahorn": ["Megahorn", "00", 120, "Bug", 85, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A brutal ramming\nattack delivered\nwith a tough and\nimpressive horn."],

        "Dragonbreath": ["Dragonbreath", "06", 60, "Dragon", 100, 20, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is hit with\nan incredible blast\nof breath that may\nalso paralyze."],

        "Baton Pass": ["Baton Pass", "1C", 0, "Normal", 0, 40, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 1, 
                "The user switches\nout, passing along\nany stat changes\nto the new battler."],

        "Encore": ["Encore", "5A", 0, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "Makes the foe use\nthe move it last\nused repeatedly for\ntwo to six turns."],

        "Pursuit": ["Pursuit", "00", 40, "Dark", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack move that\nworks especially\nwell on a foe that\nis switching out."],

        "Rapid Spin": ["Rapid Spin", "81", 50, "Normal", 100, 40, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack that\nfrees the user from\nBIND, WRAP, LEECH\nSEED, and SPIKES."],

        "Sweet Scent": ["Sweet Scent", "18", 0, "Normal", 100, 20, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                ""],

        "Iron Tail": ["Iron Tail", "13", 100, "Steel", 75, 15, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Metal Claw": ["Metal Claw", "0A", 50, "Steel", 95, 35, 10, 
                "Target", 0, [0, 1, 0, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                "The foe is attacked\nwith steel claws.\nIt may also raise\nthe user's ATTACK."],

        "Vital Throw": ["Vital Throw", "00", 70, "Fighting", 0, 10, 0, 
                "Target", 255, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "Makes the user\nattack after the\nfoe. In return,\nit will not miss."],

        "Morning Sun": ["Morning Sun", "9D", 0, "Normal", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "Restores the user's\nHP. The amount of\nHP regained varies\nwith the weather."],

        "Synthesis": ["Synthesis", "9D", 0, "Grass", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "Restores the user's\nHP. The amount of\nHP regained varies\nwith the weather."],

        "Moonlight": ["Moonlight", "9D", 0, "Fairy", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "Restores the user's\nHP. The amount of\nHP regained varies\nwith the weather."],

        "Hidden Power": ["Hidden Power", "00", 60, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "An attack that\nvaries in type and\nintensity depending\non the user."],

        "Cross Chop": ["Cross Chop", "00", 100, "Fighting", 80, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Twister": ["Twister", "1F", 40, "Dragon", 100, 20, 20, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "A vicious twister\nattacks the foe.\nIt may make the\nfoe flinch."],

        "Rain Dance": ["Rain Dance", "73", 0, "Water", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 1, 
                ""],

        "Sunny Day": ["Sunny Day", "73", 0, "Fire", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 4, 
                ""],

        "Crunch": ["Crunch", "16", 80, "Dark", 100, 15, 20, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                "The foe is crunched\nwith sharp fangs.\nIt may lower the\nfoe's SP. DEF."],

        "Mirror Coat": ["Mirror Coat", "00", 0, "Psychic", 100, 20, 0, 
                "LastHitMe", 251, [0, 0, 0, 0, 0, 0, 1, 0], "4B", "Special", 0, 
                "A retaliation move\nthat pays back the\nfoe's special attack\ndouble."],

        "Psych Up": ["Psych Up", "8F", 0, "Normal", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "The user hypnotizes\nitself into copying\nany stat change\nmade by the foe."],

        "Extremespeed": ["Extremespeed", "00", 80, "Normal", 100, 5, 0, 
                "Target", 2, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A blindingly speedy\ncharge attack that\nalways goes before\nany other."],

        "Ancientpower": ["Ancientpower", "8C", 60, "Rock", 100, 5, 10, 
                "Target", 0, [0, 1, 0, 1, 0, 0, 1, 0], "00", "Special", 31, 
                "An ancient power is\nused to attack. It\nmay also raise all\nthe user's stats."],

        "Shadow Ball": ["Shadow Ball", "16", 80, "Ghost", 100, 15, 20, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "A shadowy blob is\nhurled at the foe.\nMay also lower the\nfoe's SP. DEF."],

        "Future Sight": ["Future Sight", "32", 120, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Special", 2, 
                "Two turns after\nthis move is used,\nthe foe is attacked\npsychically."],

        "Rock Smash": ["Rock Smash", "13", 40, "Fighting", 100, 15, 50, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                "An attack that may\nalso cut DEFENSE.\nIt can also smash\ncracked boulders."],

        "Whirlpool": ["Whirlpool", "2A", 35, "Water", 85, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is trapped\nin a fast, vicious\nwhirlpool for two\nto five turns."],

        "Beat Up": ["Beat Up", "9A", 0, "Dark", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "67", "Physical", 0, 
                ""],

        "Fake Out": ["Fake Out", "1F", 40, "Normal", 100, 10, 0, 
                "Target", 3, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack that hits\nfirst and causes\nflinching. Usable\nonly on 1st turn."],

        "Uproar": ["Uproar", "9F", 90, "Normal", 100, 10, 0, 
                "Random", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The user attacks in\nan uproar that\nprevents sleep for\ntwo to five turns."],

        "Stockpile": ["Stockpile", "A0", 0, "Normal", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "The user charges\nup power for use\nlater. It can be\nused three times."],

        "Spit Up": ["Spit Up", "00", 0, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 0], "77", "Special", 0, 
                "The power built\nusing STOCKPILE is\nreleased at once\nfor attack."],

        "Swallow": ["Swallow", "9D", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 5, 
                "The energy it built\nusing STOCKPILE is\nabsorbed to restore\nHP."],

        "Heat Wave": ["Heat Wave", "04", 95, "Fire", 90, 10, 10, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The user exhales a\nheated breath to\nattack. It may also\ninflict a burn."],

        "Hail": ["Hail", "73", 0, "Ice", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 8, 
                ""],

        "Torment": ["Torment", "A5", 0, "Dark", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "It enrages the foe,\nmaking it incapable\nof using the same\nmove successively."],

        "Flatter": ["Flatter", "76", 0, "Dark", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 8, 
                "Flattery is used to\nconfuse the foe,\nbut its SP. ATK\nalso rises."],

        "Will-O-Wisp": ["Will-O-Wisp", "04", 0, "Fire", 85, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "A sinister, bluish\nwhite flame is shot\nat the foe to\ninflict a burn."],

        "Memento": ["Memento", "A8", 0, "Dark", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                "The user faints,\nbut sharply lowers\nthe foe's ATTACK\nand SP. ATK."],

        "Facade": ["Facade", "00", 70, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack that is\nboosted if user is\nburned, poisoned,\nor paralyzed."],

        "Focus Punch": ["Focus Punch", "00", 150, "Fighting", 100, 20, 0, 
                "Target", 253, [0, 0, 0, 0, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack that is\nexecuted last.\nThe user flinches\nif hit beforehand."],

        "Smellingsalt": ["Smellingsalt", "AB", 70, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 64, 
                "Doubly effective on\na paralyzed foe,\nbut it also cures\nthe foe's paralysis."],

        "Follow Me": ["Follow Me", "AC", 0, "Normal", 0, 20, 0, 
                "User", 2, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "The user draws\nattention to itself,\nmaking foes attack\nonly the user."],

        "Nature Power": ["Nature Power", "AD", 0, "Normal", 0, 20, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "An attack that\nchanges type\ndepending on the\nuser's location."],

        "Charge": ["Charge", "AE", 0, "Electric", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "The user charges\npower to boost the\nELECTRIC move it\nuses next."],

        "Taunt": ["Taunt", "AF", 0, "Dark", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "The foe is taunted\ninto a rage that\nallows it to use\nonly attack moves."],

        "Helping Hand": ["Helping Hand", "B0", 0, "Normal", 0, 20, 0, 
                "User", 5, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "A move that boosts\nthe power of the\nally's attack in a\nbattle."],

        "Trick": ["Trick", "B1", 0, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                "A move that tricks\nthe foe into\ntrading held items\nwith the user."],

        "Role Play": ["Role Play", "B2", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "The user mimics the\nfoe completely and\ncopies the foe's\nability."],

        "Wish": ["Wish", "B3", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Assist": ["Assist", "B4", 0, "Normal", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Ingrain": ["Ingrain", "B5", 0, "Grass", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "The user lays roots\nthat restore HP on\nevery turn.\nIt can't switch out."],

        "Superpower": ["Superpower", "8D", 120, "Fighting", 100, 5, 0, 
                "Target", 0, [0, 1, 0, 1, 0, 0, 1, 1], "00", "Physical", 3, 
                "A powerful attack,\nbut it also lowers\nthe user's ATTACK\nand DEFENSE stats."],

        "Magic Coat": ["Magic Coat", "B7", 0, "Psychic", 0, 15, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Recycle": ["Recycle", "B8", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "A move that\nrecycles a used\nitem for use once\nmore."],

        "Revenge": ["Revenge", "00", 60, "Fighting", 100, 10, 0, 
                "Target", 252, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack move that\ngains in intensity if\nthe target has hurt\nthe user."],

        "Brick Break": ["Brick Break", "BA", 75, "Fighting", 100, 15, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack that also\nbreaks any barrier\nlike LIGHT SCREEN\nand REFLECT."],

        "Yawn": ["Yawn", "BB", 0, "Normal", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "A huge yawn lulls\nthe foe into falling\nasleep on the next\nturn."],

        "Knock Off": ["Knock Off", "BC", 65, "Dark", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "Knocks down the\nfoe's held item to\nprevent its use\nduring the battle."],

        "Endeavor": ["Endeavor", "00", 0, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "87", "Physical", 0, 
                "Gains power the\nfewer HP the user\nhas compared with\nthe foe."],

        "Eruption": ["Eruption", "00", 150, "Fire", 100, 5, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "03", "Special", 0, 
                "The higher the\nuser's HP, the more\npowerful this\nattack becomes."],

        "Skill Swap": ["Skill Swap", "BF", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                "The user employs\nits psychic power\nto swap abilities\nwith the foe."],

        "Imprison": ["Imprison", "C0", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "Prevents foes from\nusing any move\nthat is also known\nby the user."],

        "Refresh": ["Refresh", "AB", 0, "Normal", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 88, 
                ""],

        "Grudge": ["Grudge", "C2", 0, "Ghost", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                "If the user faints,\nthis move deletes\nthe PP of the move\nthat finished it."],

        "Snatch": ["Snatch", "C3", 0, "Dark", 0, 10, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Secret Power": ["Secret Power", "C5", 70, "Normal", 100, 20, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "An attack that may\nhave an additional\neffect that varies\nwith the terrain."],

        "Dive": ["Dive", "00", 80, "Water", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user dives\nunderwater on the\nfirst turn and\nstrikes next turn."],

        "Arm Thrust": ["Arm Thrust", "1D", 15, "Fighting", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 21, 
                ""],

        "Camouflage": ["Camouflage", "D5", 0, "Normal", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "Alters the user's\ntype depending on\nthe location's\nterrain."],

        "Tail Glow": ["Tail Glow", "0D", 0, "Bug", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 3, 
                "The user flashes a\nlight that sharply\nraises its SP. ATK\nstat."],

        "Luster Purge": ["Luster Purge", "16", 70, "Psychic", 100, 5, 50, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "A burst of light\ninjures the foe. It\nmay also lower the\nfoe's SP. DEF."],

        "Mist Ball": ["Mist Ball", "15", 70, "Psychic", 100, 5, 50, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "A flurry of down\nhits the foe. It\nmay also lower the\nfoe's SP. ATK."],

        "Featherdance": ["Featherdance", "12", 0, "Flying", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                "The foe is covered\nwith a mass of down\nthat sharply cuts\nthe ATTACK stat."],

        "Teeter Dance": ["Teeter Dance", "31", 0, "Normal", 100, 20, 0, 
                "AllButUser", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                ""],

        "Blaze Kick": ["Blaze Kick", "04", 85, "Fire", 90, 10, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Mud Sport": ["Mud Sport", "C9", 0, "Ground", 0, 15, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Ice Ball": ["Ice Ball", "75", 30, "Ice", 90, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "37", "Physical", 0, 
                ""],

        "Needle Arm": ["Needle Arm", "1F", 60, "Grass", 100, 15, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack using\nthorny arms.\nIt may make the\nfoe flinch."],

        "Slack Off": ["Slack Off", "9D", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "The user slacks off\nand restores its HP\nby half its full\nHP."],

        "Hyper Voice": ["Hyper Voice", "00", 90, "Normal", 100, 10, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The user lets loose\na horribly loud\nshout with the\npower to damage."],

        "Poison Fang": ["Poison Fang", "21", 50, "Poison", 100, 15, 50, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The foe is bitten\nwith toxic fangs.\nIt may also badly\npoison the foe."],

        "Crush Claw": ["Crush Claw", "13", 75, "Normal", 95, 10, 50, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                "The foe is attacked\nwith sharp claws.\nIt may also lower\nthe foe's DEFENSE."],

        "Blast Burn": ["Blast Burn", "50", 150, "Fire", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is hit with\na huge explosion.\nThe user can't move\non the next turn."],

        "Hydro Cannon": ["Hydro Cannon", "50", 150, "Water", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is hit with\na watery cannon.\nThe user can't move\non the next turn."],

        "Meteor Mash": ["Meteor Mash", "0A", 90, "Steel", 90, 10, 20, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                "The foe is hit with\na hard, fast punch.\nIt may also raise\nthe user's ATTACK."],

        "Astonish": ["Astonish", "1F", 30, "Ghost", 100, 15, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An attack using a\nstartling shout.\nIt also may make\nthe foe flinch."],

        "Weather Ball": ["Weather Ball", "00", 50, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "An attack that\nvaries in power and\ntype depending on\nthe weather."],

        "Aromatherapy": ["Aromatherapy", "66", 0, "Grass", 0, 5, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                "A soothing scent is\nreleased to heal\nall status problems\nin the user's party."],

        "Fake Tears": ["Fake Tears", "16", 0, "Dark", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                "The user feigns\ncrying to sharply\nlower the foe's\nSP. DEF stat."],

        "Air Cutter": ["Air Cutter", "00", 60, "Flying", 95, 25, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Overheat": ["Overheat", "15", 130, "Fire", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                "An intense attack\nthat also sharply\nreduces the user's\nSP. ATK stat."],

        "Odor Sleuth": ["Odor Sleuth", "71", 0, "Normal", 0, 40, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "Completely negates\nthe foe's efforts to\nheighten its ability\nto evade."],

        "Rock Tomb": ["Rock Tomb", "14", 60, "Rock", 95, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Physical", 1, 
                "Boulders are hurled\nat the foe. It also\nlowers the foe's\nSPEED if it hits."],

        "Silver Wind": ["Silver Wind", "8C", 60, "Bug", 100, 5, 10, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 31, 
                "The foe is attacked\nwith a silver dust.\nIt may raise all\nthe user's stats."],

        "Metal Sound": ["Metal Sound", "16", 0, "Steel", 85, 40, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                "A horrible metallic\nscreech is used to\nsharply lower the\nfoe's SP. DEF."],

        "Grasswhistle": ["Grasswhistle", "01", 0, "Grass", 55, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                "A pleasant melody\nis played to lull\nthe foe into a deep\nsleep."],

        "Tickle": ["Tickle", "8D", 0, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 3, 
                "The foe is made to\nlaugh, reducing its\nATTACK and DEFENSE\nstats."],

        "Cosmic Power": ["Cosmic Power", "8C", 0, "Psychic", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 18, 
                "The user absorbs a\nmystic power to\nraise its DEFENSE\nand SP. DEF."],

        "Water Spout": ["Water Spout", "00", 150, "Water", 100, 5, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "03", "Special", 0, 
                "The higher the\nuser's HP, the more\npowerful this\nattack becomes."],

        "Signal Beam": ["Signal Beam", "31", 75, "Bug", 100, 15, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is hit with\na flashing beam\nthat may also\ncause confusion."],

        "Shadow Punch": ["Shadow Punch", "00", 60, "Ghost", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user throws a\npunch from the\nshadows. It cannot\nbe evaded."],

        "Extrasensory": ["Extrasensory", "1F", 80, "Psychic", 100, 20, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The user attacks\nwith an odd power\nthat may make the\nfoe flinch."],

        "Sky Uppercut": ["Sky Uppercut", "00", 85, "Fighting", 90, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user attacks\nwith an uppercut\nthrown skywards\nwith force."],

        "Sand Tomb": ["Sand Tomb", "2A", 35, "Ground", 85, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                "The foe is trapped\ninside a painful\nsandstorm for two\nto five turns."],

        "Sheer Cold": ["Sheer Cold", "00", 0, "Ice", 30, 5, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "D9", "Special", 0, 
                "The foe is attacked\nwith ultimate cold\nthat causes fainting\nif it hits."],

        "Muddy Water": ["Muddy Water", "17", 90, "Water", 85, 10, 30, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "The user attacks\nwith muddy water.\nIt may also lower\nthe foe's accuracy."],

        "Bullet Seed": ["Bullet Seed", "1D", 25, "Grass", 100, 30, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 21, 
                "The user shoots\nseeds at the foe.\nTwo to five seeds\nare shot at once."],

        "Aerial Ace": ["Aerial Ace", "00", 60, "Flying", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "An extremely fast\nattack against one\ntarget. It can't be\nevaded."],

        "Icicle Spear": ["Icicle Spear", "1D", 25, "Ice", 100, 30, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 21, 
                "Sharp icicles are\nfired at the foe.\nIt strikes two to\nfive times."],

        "Iron Defense": ["Iron Defense", "0B", 0, "Steel", 0, 15, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                "The user hardens\nits body's surface\nto sharply raise its\nDEFENSE stat."],

        "Block": ["Block", "6A", 0, "Normal", 0, 5, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 0, 0], "00", "Status", 0, 
                "The user blocks the\nfoe's way with arms\nspread wide to\nprevent escape."],

        "Howl": ["Howl", "0A", 0, "Normal", 0, 40, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 1, 
                "The user howls to\nraise its spirit and\nboost its ATTACK\nstat."],

        "Dragon Claw": ["Dragon Claw", "00", 80, "Dragon", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "Sharp, huge claws\nhook and slash the\nfoe quickly and\nwith great power."],

        "Frenzy Plant": ["Frenzy Plant", "50", 150, "Grass", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is hit with\nan enormous branch.\nThe user can't move\non the next turn."],

        "Bulk Up": ["Bulk Up", "8C", 0, "Fighting", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 3, 
                "The user bulks up\nits body to boost\nboth its ATTACK and\nDEFENSE stats."],

        "Bounce": ["Bounce", "06", 85, "Flying", 85, 5, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "The user bounces\non the foe on the\n2nd turn. It may\nparalyze the foe."],

        "Mud Shot": ["Mud Shot", "14", 55, "Ground", 95, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                "The user attacks by\nhurling mud.\nIt also reduces the\nfoe's SPEED."],

        "Poison Tail": ["Poison Tail", "02", 50, "Poison", 100, 25, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Covet": ["Covet", "69", 60, "Normal", 100, 25, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                "A cutely executed\nattack that also\nsteals the foe's\nhold item."],

        "Volt Tackle": ["Volt Tackle", "33", 120, "Electric", 100, 15, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 64, 
                "The user throws an\nelectrified tackle.\nIt hurts the user\na little."],

        "Magical Leaf": ["Magical Leaf", "00", 60, "Grass", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "The foe is attacked\nwith a strange leaf\nthat cannot be\nevaded."],

        "Water Sport": ["Water Sport", "D2", 0, "Water", 0, 15, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Calm Mind": ["Calm Mind", "8C", 0, "Psychic", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 24, 
                "The user focuses\nits mind to raise\nthe SP. ATK and\nSP. DEF stats."],

        "Leaf Blade": ["Leaf Blade", "00", 90, "Grass", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Dragon Dance": ["Dragon Dance", "8C", 0, "Dragon", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 5, 
                "A mystic, powerful\ndance that boosts\nthe user's ATTACK\nand SPEED stats."],

        "Rock Blast": ["Rock Blast", "1D", 25, "Rock", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 21, 
                "The user hurls two\nto five hard rocks\nat the foe to\nattack."],

        "Shock Wave": ["Shock Wave", "00", 60, "Electric", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "A rapid jolt of\nelectricity strikes\nthe foe. It can't\nbe evaded."],

        "Water Pulse": ["Water Pulse", "31", 60, "Water", 100, 20, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                "An attack with a\npulsing blast of\nwater. It may also\nconfuse the foe."],

        "Doom Desire": ["Doom Desire", "32", 140, "Steel", 100, 5, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Special", 2, 
                "A move that attacks\nthe foe with a\nblast of light two\nturns after use."],

        "Psycho Boost": ["Psycho Boost", "15", 140, "Psychic", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                "An intense attack\nthat also sharply\nreduces the user's\nSP. ATK stat."],

        "Roost": ["Roost", "3E", 0, "Flying", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Gravity": ["Gravity", "11", 0, "Psychic", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Miracle Eye": ["Miracle Eye", "3F", 0, "Psychic", 0, 40, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Wake-Up Slap": ["Wake-Up Slap", "AB", 70, "Fighting", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 4, 
                ""],

        "Hammer Arm": ["Hammer Arm", "14", 100, "Fighting", 90, 10, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Gyro Ball": ["Gyro Ball", "00", 0, "Steel", 10, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "C6", "Physical", 0, 
                ""],

        "Healing Wish": ["Healing Wish", "A7", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Brine": ["Brine", "00", 65, "Water", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Natural Gift": ["Natural Gift", "00", 0, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "4A", "Physical", 0, 
                ""],

        "Feint": ["Feint", "40", 30, "Normal", 100, 10, 0, 
                "Target", 2, [0, 0, 0, 1, 0, 0, 0, 0], "00", "Physical", 0, 
                ""],

        "Pluck": ["Pluck", "42", 60, "Flying", 100, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Tailwind": ["Tailwind", "35", 0, "Flying", 0, 15, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Acupressure": ["Acupressure", "43", 0, "Normal", 0, 30, 0, 
                "UserAndPartner", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Metal Burst": ["Metal Burst", "00", 0, "Steel", 100, 10, 0, 
                "LastHitMe", 0, [0, 0, 0, 1, 0, 0, 1, 0], "8B", "Physical", 0, 
                ""],

        "U-Turn": ["U-Turn", "1C", 70, "Bug", 100, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Close Combat": ["Close Combat", "8D", 120, "Fighting", 100, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 18, 
                ""],

        "Assurance": ["Assurance", "00", 60, "Dark", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Embargo": ["Embargo", "3C", 0, "Dark", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Fling": ["Fling", "00", 0, "Dark", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "0A", "Physical", 0, 
                ""],

        "Psycho Shift": ["Psycho Shift", "44", 0, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                ""],

        "Trump Card": ["Trump Card", "00", 0, "Normal", 0, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "97", "Special", 0, 
                ""],

        "Heal Block": ["Heal Block", "3D", 0, "Psychic", 100, 15, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Wring Out": ["Wring Out", "00", 120, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "13", "Special", 0, 
                ""],

        "Power Trick": ["Power Trick", "45", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 16, 
                ""],

        "Gastro Acid": ["Gastro Acid", "46", 0, "Poison", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Lucky Chant": ["Lucky Chant", "3A", 0, "Normal", 0, 30, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Me First": ["Me First", "47", 0, "Normal", 0, 20, 0, 
                "TargetOrPartner", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Status", 0, 
                ""],

        "Copycat": ["Copycat", "48", 0, "Normal", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Power Swap": ["Power Swap", "49", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 9, 
                ""],

        "Guard Swap": ["Guard Swap", "49", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 18, 
                ""],

        "Punishment": ["Punishment", "00", 0, "Dark", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "08", "Physical", 0, 
                ""],

        "Last Resort": ["Last Resort", "00", 140, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Worry Seed": ["Worry Seed", "4A", 0, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 15, 
                ""],

        "Sucker Punch": ["Sucker Punch", "00", 70, "Dark", 100, 5, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Toxic Spikes": ["Toxic Spikes", "70", 0, "Poison", 0, 20, 0, 
                "FoeSide", 0, [0, 0, 0, 0, 0, 1, 0, 0], "00", "Status", 1, 
                ""],

        "Heart Swap": ["Heart Swap", "49", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 127, 
                ""],

        "Aqua Ring": ["Aqua Ring", "B6", 0, "Water", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Magnet Rise": ["Magnet Rise", "4B", 0, "Electric", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Flare Blitz": ["Flare Blitz", "33", 120, "Fire", 100, 15, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 16, 
                ""],

        "Force Palm": ["Force Palm", "06", 60, "Fighting", 100, 10, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Aura Sphere": ["Aura Sphere", "00", 80, "Fighting", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Rock Polish": ["Rock Polish", "0C", 0, "Rock", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Poison Jab": ["Poison Jab", "02", 80, "Poison", 100, 20, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Dark Pulse": ["Dark Pulse", "1F", 80, "Dark", 100, 15, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Night Slash": ["Night Slash", "00", 70, "Dark", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Aqua Tail": ["Aqua Tail", "00", 90, "Water", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Seed Bomb": ["Seed Bomb", "00", 80, "Grass", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Air Slash": ["Air Slash", "1F", 75, "Flying", 95, 15, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "X-Scissor": ["X-Scissor", "00", 80, "Bug", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Bug Buzz": ["Bug Buzz", "16", 90, "Bug", 100, 10, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Dragon Pulse": ["Dragon Pulse", "00", 85, "Dragon", 100, 85, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Dragon Rush": ["Dragon Rush", "1F", 100, "Dragon", 75, 10, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Power Gem": ["Power Gem", "00", 80, "Rock", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Drain Punch": ["Drain Punch", "03", 75, "Fighting", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 50, 
                ""],

        "Vacuum Wave": ["Vacuum Wave", "00", 40, "Fighting", 100, 30, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Focus Blast": ["Focus Blast", "16", 120, "Fighting", 70, 5, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Energy Ball": ["Energy Ball", "16", 80, "Grass", 100, 10, 10, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Brave Bird": ["Brave Bird", "30", 120, "Flying", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 33, 
                ""],

        "Earth Power": ["Earth Power", "16", 90, "Ground", 100, 10, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Switcheroo": ["Switcheroo", "B1", 0, "Dark", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                ""],

        "Giga Impact": ["Giga Impact", "50", 150, "Normal", 90, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Nasty Plot": ["Nasty Plot", "0D", 0, "Dark", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Bullet Punch": ["Bullet Punch", "00", 40, "Steel", 100, 30, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Avalanche": ["Avalanche", "00", 60, "Ice", 100, 10, 0, 
                "Target", 252, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Ice Shard": ["Ice Shard", "00", 40, "Ice", 100, 30, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Shadow Claw": ["Shadow Claw", "00", 70, "Ghost", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Ice Fang": ["Ice Fang", "4C", 65, "Ice", 95, 15, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 32, 
                ""],

        "Fire Fang": ["Fire Fang", "4C", 65, "Fire", 95, 15, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 16, 
                ""],

        "Shadow Sneak": ["Shadow Sneak", "00", 40, "Ghost", 100, 30, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Mud Bomb": ["Mud Bomb", "17", 65, "Ground", 85, 15, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Psycho Cut": ["Psycho Cut", "00", 70, "Psychic", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Zen Headbutt": ["Zen Headbutt", "1F", 80, "Psychic", 90, 15, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Mirror Shot": ["Mirror Shot", "17", 65, "Steel", 85, 10, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Flash Cannon": ["Flash Cannon", "16", 80, "Steel", 100, 10, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Rock Climb": ["Rock Climb", "31", 90, "Normal", 85, 20, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Defog": ["Defog", "82", 0, "Flying", 0, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Trick Room": ["Trick Room", "4D", 0, "Psychic", 0, 5, 0, 
                "User", 249, [0, 0, 0, 1, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Draco Meteor": ["Draco Meteor", "15", 130, "Dragon", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                ""],

        "Discharge": ["Discharge", "06", 80, "Electric", 100, 15, 30, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Lava Plume": ["Lava Plume", "04", 80, "Fire", 100, 15, 30, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Leaf Storm": ["Leaf Storm", "15", 130, "Grass", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                ""],

        "Power Whip": ["Power Whip", "00", 120, "Grass", 85, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Rock Wrecker": ["Rock Wrecker", "50", 150, "Rock", 90, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Cross Poison": ["Cross Poison", "02", 70, "Poison", 100, 20, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Gunk Shot": ["Gunk Shot", "02", 120, "Poison", 80, 5, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Iron Head": ["Iron Head", "1F", 80, "Steel", 100, 15, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Magnet Bomb": ["Magnet Bomb", "00", 60, "Steel", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Stone Edge": ["Stone Edge", "00", 100, "Rock", 80, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Captivate": ["Captivate", "15", 0, "Normal", 100, 20, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                ""],

        "Stealth Rock": ["Stealth Rock", "70", 0, "Rock", 0, 20, 0, 
                "FoeSide", 0, [0, 0, 0, 0, 0, 1, 0, 0], "00", "Status", 2, 
                ""],

        "Grass Knot": ["Grass Knot", "00", 0, "Grass", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "15", "Special", 0, 
                ""],

        "Chatter": ["Chatter", "31", 65, "Flying", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Judgment": ["Judgment", "00", 100, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Bug Bite": ["Bug Bite", "42", 60, "Bug", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Charge Beam": ["Charge Beam", "0D", 50, "Electric", 90, 10, 70, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Wood Hammer": ["Wood Hammer", "30", 120, "Grass", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 33, 
                ""],

        "Aqua Jet": ["Aqua Jet", "00", 40, "Water", 100, 20, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Attack Order": ["Attack Order", "00", 90, "Bug", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Defend Order": ["Defend Order", "8C", 0, "Bug", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 18, 
                ""],

        "Heal Order": ["Heal Order", "9D", 0, "Bug", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Head Smash": ["Head Smash", "30", 150, "Rock", 80, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 33, 
                ""],

        "Double Hit": ["Double Hit", "1D", 35, "Normal", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                ""],

        "Roar of Time": ["Roar of Time", "50", 150, "Dragon", 90, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Spacial Rend": ["Spacial Rend", "00", 100, "Dragon", 95, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Lunar Dance": ["Lunar Dance", "A7", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Crush Grip": ["Crush Grip", "00", 120, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "13", "Physical", 0, 
                ""],

        "Magma Storm": ["Magma Storm", "2A", 100, "Fire", 75, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Dark Void": ["Dark Void", "01", 0, "Dark", 90, 10, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Seed Flare": ["Seed Flare", "16", 120, "Grass", 85, 5, 40, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                ""],

        "Ominous Wind": ["Ominous Wind", "8C", 60, "Ghost", 100, 15, 10, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 31, 
                ""],

        "Shadow Force": ["Shadow Force", "00", 120, "Ghost", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 0, 1], "00", "Physical", 0, 
                ""],

        "Hone Claws": ["Hone Claws", "8C", 0, "Dark", 0, 15, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 33, 
                ""],

        "Wide Guard": ["Wide Guard", "37", 0, "Rock", 0, 10, 0, 
                "MySide", 3, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Guard Split": ["Guard Split", "57", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Status", 19, 
                ""],

        "Power Split": ["Power Split", "57", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Status", 2, 
                ""],

        "Wonder Room": ["Wonder Room", "58", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 1, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Psyshock": ["Psyshock", "00", 80, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Venoshock": ["Venoshock", "00", 65, "Poison", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Autotomize": ["Autotomize", "2D", 0, "Steel", 0, 15, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 100, 
                ""],

        "Rage Powder": ["Rage Powder", "AC", 0, "Bug", 0, 20, 0, 
                "User", 2, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Telekinesis": ["Telekinesis", "59", 0, "Psychic", 0, 15, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Magic Room": ["Magic Room", "5C", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 1, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Smack Down": ["Smack Down", "60", 50, "Rock", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Storm Throw": ["Storm Throw", "00", 60, "Fighting", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Flame Burst": ["Flame Burst", "63", 70, "Fire", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 6, 
                ""],

        "Sludge Wave": ["Sludge Wave", "02", 95, "Poison", 100, 10, 10, 
                "AllButUser", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Quiver Dance": ["Quiver Dance", "8C", 0, "Bug", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 28, 
                ""],

        "Heavy Slam": ["Heavy Slam", "000", 0, "Steel", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "95", "Physical", 0, 
                ""],

        "Synchronoise": ["Synchronoise", "00", 120, "Psychic", 100, 10, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Electro Ball": ["Electro Ball", "00", 0, "Electric", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "C6", "Special", 0, 
                ""],

        "Soak": ["Soak", "65", 0, "Water", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 11, 
                ""],

        "Flame Charge": ["Flame Charge", "0C", 50, "Fire", 100, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Coil": ["Coil", "8C", 0, "Poison", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 35, 
                ""],

        "Low Sweep": ["Low Sweep", "14", 65, "Fighting", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Acid Spray": ["Acid Spray", "16", 40, "Poison", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                ""],

        "Foul Play": ["Foul Play", "00", 95, "Dark", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Simple Beam": ["Simple Beam", "4A", 0, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 87, 
                ""],

        "Entrainment": ["Entrainment", "4A", 0, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 255, 
                ""],

        "After You": ["After You", "67", 0, "Normal", 0, 15, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Round": ["Round", "68", 60, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "A7", "Special", 0, 
                ""],

        "Echoed Voice": ["Echoed Voice", "6E", 40, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "B7", "Special", 0, 
                ""],

        "Chip Away": ["Chip Away", "00", 70, "Normal", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Clear Smog": ["Clear Smog", "19", 50, "Poison", 0, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Stored Power": ["Stored Power", "00", 20, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "14", "Special", 0, 
                ""],

        "Quick Guard": ["Quick Guard", "36", 0, "Fighting", 0, 15, 0, 
                "MySide", 3, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Ally Switch": ["Ally Switch", "79", 0, "Psychic", 0, 15, 0, 
                "User", 2, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Scald": ["Scald", "7D", 80, "Water", 100, 15, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Shell Smash": ["Shell Smash", "7A", 0, "Normal", 0, 15, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Heal Pulse": ["Heal Pulse", "9D", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Hex": ["Hex", "00", 65, "Ghost", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Sky Drop": ["Sky Drop", "00", 60, "Flying", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Shift Gear": ["Shift Gear", "26", 0, "Steel", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Circle Throw": ["Circle Throw", "1C", 60, "Fighting", 90, 10, 0, 
                "Target", 250, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Incinerate": ["Incinerate", "42", 60, "Fire", 100, 15, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Quash": ["Quash", "7B", 0, "Dark", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                ""],

        "Acrobatics": ["Acrobatics", "00", 55, "Flying", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Reflect Type": ["Reflect Type", "7E", 0, "Normal", 0, 15, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Status", 0, 
                ""],

        "Retaliate": ["Retaliate", "00", 70, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Final Gambit": ["Final Gambit", "30", 0, "Fighting", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 0], "C9", "Special", 100, 
                ""],

        "Bestow": ["Bestow", "69", 0, "Normal", 0, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 0, 0], "00", "Status", 1, 
                ""],

        "Inferno": ["Inferno", "04", 100, "Fire", 50, 5, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Water Pledge": ["Water Pledge", "00", 80, "Water", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Fire Pledge": ["Fire Pledge", "00", 80, "Fire", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Grass Pledge": ["Grass Pledge", "00", 80, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Volt Switch": ["Volt Switch", "1C", 70, "Electric", 100, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Struggle Bug": ["Struggle Bug", "15", 50, "Bug", 100, 20, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Bulldoze": ["Bulldoze", "14", 60, "Ground", 100, 20, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 1, 
                ""],

        "Frost Breath": ["Frost Breath", "00", 60, "Ice", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Dragon Tail": ["Dragon Tail", "1C", 60, "Dragon", 90, 10, 0, 
                "Target", 250, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Work Up": ["Work Up", "8C", 0, "Normal", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 9, 
                ""],

        "Electroweb": ["Electroweb", "14", 55, "Electric", 95, 15, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Wild Charge": ["Wild Charge", "30", 90, "Electric", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 25, 
                ""],

        "Drill Run": ["Drill Run", "00", 80, "Ground", 95, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Dual Chop": ["Dual Chop", "1D", 40, "Dragon", 90, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                ""],

        "Heart Stamp": ["Heart Stamp", "1F", 60, "Psychic", 100, 25, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Horn Leech": ["Horn Leech", "03", 75, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 50, 
                ""],

        "Sacred Sword": ["Sacred Sword", "00", 90, "Fighting", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Razor Shell": ["Razor Shell", "13", 75, "Water", 95, 10, 50, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Heat Crash": ["Heat Crash", "000", 1, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "95", "Status", 0, 
                ""],

        "Leaf Tornado": ["Leaf Tornado", "17", 65, "Grass", 90, 10, 50, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Steamroller": ["Steamroller", "1F", 65, "Bug", 100, 20, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Cotton Guard": ["Cotton Guard", "0B", 0, "Grass", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 3, 
                ""],

        "Night Daze": ["Night Daze", "17", 85, "Dark", 95, 10, 40, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Psystrike": ["Psystrike", "00", 100, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Tail Slap": ["Tail Slap", "1D", 25, "Normal", 85, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 37, 
                ""],

        "Hurricane": ["Hurricane", "31", 110, "Flying", 70, 10, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Head Charge": ["Head Charge", "30", 120, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 25, 
                ""],

        "Gear Grind": ["Gear Grind", "1D", 50, "Steel", 85, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                ""],

        "Searing Shot": ["Searing Shot", "04", 100, "Fire", 100, 5, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Techno Blast": ["Techno Blast", "00", 120, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Relic Song": ["Relic Song", "01", 75, "Normal", 100, 10, 10, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Secret Sword": ["Secret Sword", "00", 85, "Fighting", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Glaciate": ["Glaciate", "14", 65, "Ice", 95, 10, 0, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Bolt Strike": ["Bolt Strike", "06", 130, "Electric", 85, 5, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Blue Flare": ["Blue Flare", "04", 130, "Fire", 85, 5, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Fiery Dance": ["Fiery Dance", "0D", 80, "Fire", 100, 10, 50, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Freeze Shock": ["Freeze Shock", "06", 140, "Ice", 90, 5, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Ice Burn": ["Ice Burn", "04", 140, "Ice", 90, 5, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Snarl": ["Snarl", "15", 55, "Dark", 95, 15, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Icicle Crash": ["Icicle Crash", "1F", 85, "Ice", 90, 10, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "V-Create": ["V-Create", "8D", 180, "Fire", 95, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 22, 
                ""],

        "Fusion Flare": ["Fusion Flare", "00", 100, "Fire", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Fusion Bolt": ["Fusion Bolt", "00", 100, "Electric", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Flying Press": ["Flying Press", "00", 100, "Fighting", 95, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Mat Block": ["Mat Block", "38", 0, "Fighting", 0, 10, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Belch": ["Belch", "00", 120, "Poison", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Rototiller": ["Rototiller", "7F", 0, "Ground", 0, 10, 0, 
                "Everyone", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Sticky Web": ["Sticky Web", "70", 0, "Bug", 0, 20, 0, 
                "FoeSide", 0, [0, 0, 0, 0, 0, 1, 0, 0], "00", "Status", 3, 
                ""],

        "Fell Stinger": ["Fell Stinger", "55", 50, "Bug", 100, 25, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Phantom Force": ["Phantom Force", "00", 90, "Ghost", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 0, 1], "00", "Physical", 0, 
                ""],

        "Trick Or Treat": ["Trick Or Treat", "3B", 0, "Ghost", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 7, 
                ""],

        "Noble Roar": ["Noble Roar", "8D", 0, "Normal", 100, 30, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 9, 
                ""],

        "Ion Deluge": ["Ion Deluge", "2B", 0, "Electric", 0, 25, 0, 
                "User", 1, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "CurvedCharge": ["CurvedCharge", "03", 65, "Electric", 100, 20, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 50, 
                ""],

        "ForestsCurse": ["ForestsCurse", "3B", 0, "Grass", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 12, 
                ""],

        "Petal Storm": ["Petal Storm", "00", 90, "Grass", 100, 15, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Freeze-Dry": ["Freeze-Dry", "05", 70, "Ice", 100, 20, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Disarm Voice": ["Disarm Voice", "00", 40, "Fairy", 0, 15, 0, 
                "FoeSide", 0, [0, 0, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Parting Shot": ["Parting Shot", "80", 0, "Dark", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 9, 
                ""],

        "Topsy-Turvy": ["Topsy-Turvy", "83", 0, "Dark", 0, 20, 0, 
                "Target", 0, [0, 1, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Draining Kiss": ["Draining Kiss", "03", 50, "Fairy", 100, 10, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Special", 75, 
                ""],

        "Crafty Shield": ["Crafty Shield", "84", 0, "Fairy", 0, 10, 0, 
                "MySide", 3, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Flower Shield": ["Flower Shield", "85", 0, "Fairy", 0, 10, 0, 
                "Everyone", 0, [0, 1, 0, 0, 0, 0, 0, 0], "00", "Status", 2, 
                ""],

        "GrassTerrain": ["GrassTerrain", "2C", 0, "Grass", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 1, 
                ""],

        "Misty Terrain": ["Misty Terrain", "2C", 0, "Fairy", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 4, 
                ""],

        "Electrify": ["Electrify", "27", 0, "Electric", 0, 20, 0, 
                "Target", 0, [0, 1, 0, 1, 0, 0, 1, 0], "00", "Status", 13, 
                ""],

        "Play Rough": ["Play Rough", "12", 90, "Fairy", 90, 10, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Fairy Wind": ["Fairy Wind", "00", 40, "Fairy", 100, 30, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Moonblast": ["Moonblast", "15", 95, "Fairy", 100, 15, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Boomburst": ["Boomburst", "00", 140, "Normal", 100, 10, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Fairy Lock": ["Fairy Lock", "86", 0, "Fairy", 0, 10, 0, 
                "User", 0, [0, 0, 0, 1, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "King's Shield": ["King's Shield", "87", 0, "Steel", 0, 10, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Play Nice": ["Play Nice", "12", 0, "Normal", 0, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 0, 0], "00", "Status", 1, 
                ""],

        "Confide": ["Confide", "15", 0, "Normal", 0, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 0, 0], "00", "Status", 1, 
                ""],

        "Diamond Storm": ["Diamond Storm", "0B", 100, "Rock", 95, 5, 50, 
                "FoeSide", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Physical", 2, 
                ""],

        "AquaEruption": ["AquaEruption", "7D", 110, "Water", 95, 5, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "HyperHole": ["HyperHole", "40", 80, "Psychic", 0, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 0, 0], "00", "Special", 0, 
                ""],

        "AquaShuriken": ["AquaShuriken", "1D", 15, "Water", 100, 20, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 37, 
                ""],

        "Mystical Fire": ["Mystical Fire", "15", 75, "Fire", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Spiky Shield": ["Spiky Shield", "89", 0, "Grass", 0, 10, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Aromatic Mist": ["Aromatic Mist", "90", 0, "Fairy", 0, 20, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 16, 
                ""],

        "Eerie Impulse": ["Eerie Impulse", "15", 0, "Electric", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 2, 
                ""],

        "Venom Drench": ["Venom Drench", "28", 0, "Poison", 100, 20, 0, 
                "FoeSide", 0, [0, 0, 0, 0, 0, 1, 1, 0], "00", "Status", 13, 
                ""],

        "Powder": ["Powder", "91", 0, "Bug", 100, 20, 0, 
                "Target", 1, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                ""],

        "Geomancy": ["Geomancy", "92", 0, "Fairy", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 28, 
                ""],

        "Magnetic Flux": ["Magnetic Flux", "5B", 0, "Electric", 0, 20, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 18, 
                ""],

        "Happy Hour": ["Happy Hour", "22", 0, "Normal", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 1, 
                ""],

        "SparkTerrain": ["SparkTerrain", "2C", 0, "Electric", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Dazzle Gleam": ["Dazzle Gleam", "00", 80, "Fairy", 100, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Celebrate": ["Celebrate", "8B", 0, "Normal", 0, 40, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Hold Hands": ["Hold Hands", "8B", 0, "Normal", 0, 40, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 1, 
                ""],

        "Baby-Doll Eyes": ["Baby-Doll Eyes", "12", 0, "Fairy", 100, 30, 0, 
                "Target", 1, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                ""],

        "Nuzzle": ["Nuzzle", "06", 20, "Electric", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Hold Back": ["Hold Back", "00", 40, "Normal", 100, 40, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "1C", "Physical", 0, 
                ""],

        "Infestation": ["Infestation", "2A", 20, "Bug", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Special", 0, 
                ""],

        "Power-Up Punch": ["Power-Up Punch", "0A", 40, "Fighting", 100, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Oblivion Wing": ["Oblivion Wing", "03", 80, "Flying", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 75, 
                ""],

        "1,000 Arrows": ["1,000 Arrows", "60", 90, "Ground", 100, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "1,000 Waves": ["1,000 Waves", "6A", 90, "Ground", 100, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Land's Wrath": ["Land's Wrath", "00", 90, "Ground", 100, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Light Of Ruin": ["Light Of Ruin", "30", 140, "Fairy", 90, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 50, 
                ""],

        "Origin Pulse": ["Origin Pulse", "00", 110, "Water", 85, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "StoneyBlades": ["StoneyBlades", "00", 120, "Ground", 85, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Dragon Ascent": ["Dragon Ascent", "8D", 120, "Dragon", 100, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 18, 
                ""],

        "Hyper Fury": ["Hyper Fury", "8D", 100, "Dark", 0, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 0, 0], "00", "Physical", 2, 
                ""],

        "ZNormal": ["ZNormal", "00", 0, "Normal", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZFighting": ["ZFighting", "00", 0, "Fighting", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZFlying": ["ZFlying", "00", 0, "Flying", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZPoison": ["ZPoison", "00", 0, "Poison", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZGround": ["ZGround", "00", 0, "Ground", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZRock": ["ZRock", "00", 0, "Rock", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZBug": ["ZBug", "00", 0, "Bug", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZGhost": ["ZGhost", "00", 0, "Ghost", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZSteel": ["ZSteel", "00", 0, "Steel", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZFire": ["ZFire", "00", 0, "Fire", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZWater": ["ZWater", "00", 0, "Water", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZGrass": ["ZGrass", "00", 0, "Grass", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZElectric": ["ZElectric", "00", 0, "Electric", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZPsychic": ["ZPsychic", "00", 0, "Psychic", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZIce": ["ZIce", "00", 0, "Ice", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZDragon": ["ZDragon", "00", 0, "Dragon", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZDark": ["ZDark", "00", 0, "Dark", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZFairy": ["ZFairy", "00", 0, "Fairy", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 0, 
                ""],

        "ZPikachu": ["ZPikachu", "00", 210, "Electric", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 1], "00", "Physical", 0, 
                ""],

        "Shore Up": ["Shore Up", "9D", 0, "Ground", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 3, 
                ""],

        "FirstMeeting": ["FirstMeeting", "00", 90, "Bug", 100, 10, 0, 
                "Target", 2, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "PoisonBunker": ["PoisonBunker", "94", 0, "Poison", 0, 10, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "GhostShackle": ["GhostShackle", "6A", 80, "Ghost", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Dark Lariat": ["Dark Lariat", "00", 85, "Dark", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Sparkle Aria": ["Sparkle Aria", "AB", 90, "Water", 100, 10, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 16, 
                ""],

        "Ice Hammer": ["Ice Hammer", "14", 100, "Ice", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Floral Heal": ["Floral Heal", "9D", 0, "Fairy", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 1, 1, 0], "00", "Status", 6, 
                ""],

        "HiHorsepower": ["HiHorsepower", "00", 95, "Ground", 95, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Strength Sap": ["Strength Sap", "95", 0, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 1, 
                ""],

        "Solar Blade": ["Solar Blade", "00", 125, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Leafage": ["Leafage", "00", 40, "Grass", 100, 40, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Spotlight": ["Spotlight", "AC", 0, "Normal", 0, 15, 0, 
                "Target", 3, [0, 0, 0, 0, 0, 1, 1, 0], "00", "Status", 1, 
                ""],

        "Toxic Thread": ["Toxic Thread", "97", 0, "Poison", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 51, 
                ""],

        "Laser Focus": ["Laser Focus", "98", 0, "Normal", 0, 30, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Gear Up": ["Gear Up", "93", 0, "Steel", 0, 20, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 9, 
                ""],

        "Throat Chop": ["Throat Chop", "99", 80, "Dark", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                ""],

        "Pollen Puff": ["Pollen Puff", "00", 90, "Bug", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Anchor Shot": ["Anchor Shot", "6A", 80, "Steel", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "PsychTerrain": ["PsychTerrain", "2C", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 8, 
                ""],

        "Lunge": ["Lunge", "12", 80, "Bug", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Fire Lash": ["Fire Lash", "13", 80, "Fire", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Power Trip": ["Power Trip", "00", 20, "Dark", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "14", "Physical", 0, 
                ""],

        "Burn Up": ["Burn Up", "9B", 130, "Fire", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Speed Swap": ["Speed Swap", "45", 0, "Psychic", 0, 10, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 4, 
                ""],

        "Smart Strike": ["Smart Strike", "00", 70, "Steel", 0, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Purify": ["Purify", "A1", 0, "Poison", 0, 20, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Awaken Dance": ["Awaken Dance", "00", 90, "Normal", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Core Enforcer": ["Core Enforcer", "46", 100, "Dragon", 100, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Trop Kick": ["Trop Kick", "12", 70, "Grass", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Instruct": ["Instruct", "A3", 0, "Psychic", 0, 15, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Status", 0, 
                ""],

        "Beak Blast": ["Beak Blast", "A4", 100, "Flying", 100, 15, 0, 
                "Target", 253, [0, 1, 1, 0, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Scale Clang": ["Scale Clang", "13", 110, "Dragon", 100, 5, 0, 
                "FoeSide", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Dragon Hammer": ["Dragon Hammer", "00", 90, "Dragon", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Brutal Swing": ["Brutal Swing", "00", 60, "Dark", 100, 20, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Aurora Veil": ["Aurora Veil", "34", 0, "Ice", 0, 20, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "ZDecidueye": ["ZDecidueye", "00", 180, "Ghost", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "00", "Physical", 0, 
                ""],

        "ZIncineroar": ["ZIncineroar", "00", 180, "Dark", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "00", "Physical", 0, 
                ""],

        "ZPrimarina": ["ZPrimarina", "00", 195, "Water", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "00", "Special", 0, 
                ""],

        "ZGuardian": ["ZGuardian", "00", 0, "Fairy", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "99", "Special", 0, 
                ""],

        "ZMarshadow": ["ZMarshadow", "00", 195, "Ghost", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "00", "Physical", 0, 
                ""],

        "ZARaichu": ["ZARaichu", "06", 175, "Electric", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "00", "Special", 0, 
                ""],

        "ZSnorlax": ["ZSnorlax", "00", 210, "Normal", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 1], "00", "Physical", 0, 
                ""],

        "ZEevee": ["ZEevee", "92", 0, "Normal", 0, 0, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 31, 
                ""],

        "ZMew": ["ZMew", "2C", 185, "Psychic", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "00", "Special", 8, 
                ""],

        "Shell Trap": ["Shell Trap", "A6", 150, "Fire", 100, 5, 0, 
                "FoeSide", 253, [0, 0, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Fleur Cannon": ["Fleur Cannon", "15", 130, "Fairy", 90, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                ""],

        "Psychic Fangs": ["Psychic Fangs", "BA", 85, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "StompTantrum": ["StompTantrum", "00", 75, "Ground", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Shadow Bone": ["Shadow Bone", "13", 85, "Ghost", 100, 10, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 1, 
                ""],

        "Accelerock": ["Accelerock", "00", 40, "Rock", 100, 20, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Liquidation": ["Liquidation", "13", 85, "Water", 100, 10, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Prism Laser": ["Prism Laser", "50", 160, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "GhostlyThief": ["GhostlyThief", "A9", 90, "Ghost", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "SunsteelBash": ["SunsteelBash", "00", 100, "Steel", 100, 5, 0, 
                "Target", 0, [1, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Moongeist": ["Moongeist", "00", 100, "Ghost", 100, 5, 0, 
                "Target", 0, [1, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Tearful Look": ["Tearful Look", "8D", 0, "Normal", 0, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 0, 0], "00", "Status", 9, 
                ""],

        "Zing Zap": ["Zing Zap", "1F", 80, "Electric", 100, 10, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Nature Wrath": ["Nature Wrath", "00", 0, "Fairy", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "59", "Special", 0, 
                ""],

        "Multi-Attack": ["Multi-Attack", "00", 120, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "ZCapPikachu": ["ZCapPikachu", "00", 195, "Electric", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "00", "Special", 0, 
                ""],

        "Mind Blown": ["Mind Blown", "AA", 150, "Fire", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 50, 
                ""],

        "Plasma Fists": ["Plasma Fists", "B9", 100, "Electric", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Photon Geyser": ["Photon Geyser", "00", 100, "Psychic", 100, 5, 0, 
                "Target", 0, [1, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "ZUNecrozma": ["ZUNecrozma", "00", 200, "Psychic", 0, 0, 0, 
                "Target", 0, [1, 0, 1, 0, 0, 0, 0, 0], "00", "Special", 0, 
                ""],

        "ZSNecrozma": ["ZSNecrozma", "00", 200, "Steel", 0, 0, 0, 
                "Target", 0, [1, 0, 1, 0, 0, 0, 0, 1], "00", "Physical", 0, 
                ""],

        "ZLNecrozma": ["ZLNecrozma", "00", 200, "Ghost", 0, 0, 0, 
                "Target", 0, [1, 0, 1, 0, 0, 0, 0, 0], "00", "Special", 0, 
                ""],

        "ZMimikyu": ["ZMimikyu", "00", 190, "Fairy", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 1], "00", "Physical", 0, 
                ""],

        "ZLycanroc": ["ZLycanroc", "BD", 190, "Rock", 0, 0, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 0, 0], "00", "Physical", 0, 
                ""],

        "ZKommo-o": ["ZKommo-o", "8C", 185, "Dragon", 0, 0, 0, 
                "FoeSide", 0, [0, 1, 1, 0, 0, 0, 0, 0], "00", "Special", 31, 
                ""],

        "Zippy Zap": ["Zippy Zap", "00", 50, "Electric", 100, 15, 0, 
                "Target", 2, [0, 0, 0, 0, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "SplishSplash": ["SplishSplash", "06", 90, "Water", 100, 15, 30, 
                "FoeSide", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Floaty Fall": ["Floaty Fall", "1F", 90, "Flying", 95, 15, 30, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Pika Papow": ["Pika Papow", "00", 0, "Electric", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 0], "02", "Special", 0, 
                ""],

        "Bouncy Bubble": ["Bouncy Bubble", "03", 90, "Water", 100, 15, 0, 
                "FoeSide", 0, [0, 0, 1, 0, 0, 0, 1, 0], "00", "Special", 50, 
                ""],

        "Sizzly Slide": ["Sizzly Slide", "04", 90, "Fire", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Glitzy Glow": ["Glitzy Glow", "23", 90, "Psychic", 100, 15, 0, 
                "Target", 0, [0, 1, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Baddy Bad": ["Baddy Bad", "41", 90, "Dark", 100, 15, 0, 
                "Target", 0, [0, 1, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Sappy Seed": ["Sappy Seed", "54", 90, "Grass", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 1, 1, 0], "00", "Physical", 0, 
                ""],

        "Freezy Frost": ["Freezy Frost", "19", 90, "Ice", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Sparkly Swirl": ["Sparkly Swirl", "66", 90, "Fairy", 100, 15, 0, 
                "Target", 0, [0, 1, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Veevee Volley": ["Veevee Volley", "00", 0, "Normal", 0, 20, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 1], "02", "Physical", 0, 
                ""],

        "DoublePanzer": ["DoublePanzer", "1D", 60, "Steel", 100, 5, 30, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                ""],

        "Max Guard": ["Max Guard", "4E", 0, "Normal", 0, 0, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "DynamaxCanon": ["DynamaxCanon", "00", 100, "Dragon", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Snipe Shot": ["Snipe Shot", "00", 80, "Water", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Jaw Lock": ["Jaw Lock", "6A", 80, "Dark", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Stuff Cheeks": ["Stuff Cheeks", "C1", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                ""],

        "No Retreat": ["No Retreat", "C6", 0, "Fighting", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 31, 
                ""],

        "Tar Shot": ["Tar Shot", "C7", 0, "Rock", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Magic Powder": ["Magic Powder", "65", 0, "Psychic", 100, 20, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 14, 
                ""],

        "Dragon Darts": ["Dragon Darts", "00", 50, "Dragon", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Teatime": ["Teatime", "C8", 0, "Normal", 0, 10, 0, 
                "Everyone", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Octolock": ["Octolock", "CA", 0, "Fighting", 100, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Status", 0, 
                ""],

        "Bolt Beak": ["Bolt Beak", "00", 85, "Electric", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Fishious Rend": ["Fishious Rend", "00", 85, "Water", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Court Change": ["Court Change", "CB", 0, "Normal", 100, 10, 0, 
                "User", 0, [0, 0, 0, 1, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Max Flare": ["Max Flare", "73", 0, "Fire", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 4, 
                ""],

        "Max Lightning": ["Max Lightning", "2C", 0, "Electric", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 2, 
                ""],

        "Max Knuckle": ["Max Knuckle", "CD", 0, "Fighting", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 1, 1, 0, 0, 0, 0, 0], "0C", "Physical", 1, 
                ""],

        "Max Phantasm": ["Max Phantasm", "CC", 0, "Ghost", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 2, 
                ""],

        "Max Hailstorm": ["Max Hailstorm", "73", 0, "Ice", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 8, 
                ""],

        "Max Ooze": ["Max Ooze", "CD", 0, "Poison", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 1, 1, 0, 0, 0, 0, 0], "0C", "Physical", 8, 
                ""],

        "Max Geyser": ["Max Geyser", "73", 0, "Water", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 1, 
                ""],

        "Max Airstream": ["Max Airstream", "CD", 0, "Flying", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 1, 1, 0, 0, 0, 0, 0], "0C", "Physical", 4, 
                ""],

        "Max Starfall": ["Max Starfall", "2C", 0, "Fairy", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 4, 
                ""],

        "Max Wyrmwind": ["Max Wyrmwind", "CC", 0, "Dragon", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 1, 
                ""],

        "Max Mindstorm": ["Max Mindstorm", "2C", 0, "Psychic", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 8, 
                ""],

        "Max Rockfall": ["Max Rockfall", "73", 0, "Rock", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 2, 
                ""],

        "Max Quake": ["Max Quake", "CD", 0, "Ground", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 1, 1, 0, 0, 0, 0, 0], "0C", "Physical", 16, 
                ""],

        "Max Darkness": ["Max Darkness", "CC", 0, "Dark", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 16, 
                ""],

        "Max Overgrow": ["Max Overgrow", "2C", 0, "Grass", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 0, 1, 0, 0, 0, 0, 0], "0C", "Physical", 1, 
                ""],

        "MaxSteelspyk": ["MaxSteelspyk", "CD", 0, "Steel", 0, 0, 0, 
                "TargetOrPartner", 0, [0, 1, 1, 0, 0, 0, 0, 0], "0C", "Physical", 2, 
                ""],

        "Clanging Soul": ["Clanging Soul", "CE", 0, "Dragon", 0, 5, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 31, 
                ""],

        "Body Press": ["Body Press", "00", 80, "Fighting", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Decorate": ["Decorate", "92", 0, "Fairy", 0, 15, 0, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 9, 
                ""],

        "Drum Beating": ["Drum Beating", "14", 80, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 1, 
                ""],

        "Snap Trap": ["Snap Trap", "2A", 35, "Grass", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Pyro Ball": ["Pyro Ball", "7D", 120, "Fire", 90, 5, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "BehemothCut": ["BehemothCut", "00", 100, "Steel", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Behemoth Bash": ["Behemoth Bash", "00", 100, "Steel", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "AuraWheel": ["AuraWheel", "0C", 110, "Electric", 100, 10, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Physical", 1, 
                ""],

        "Break Swipe": ["Break Swipe", "12", 60, "Dragon", 100, 15, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Branch Poke": ["Branch Poke", "00", 40, "Grass", 100, 40, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Overdrive": ["Overdrive", "00", 80, "Electric", 100, 10, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Apple Acid": ["Apple Acid", "16", 80, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Grav Apple": ["Grav Apple", "16", 80, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 1, 
                ""],

        "Spirit Break": ["Spirit Break", "15", 75, "Fairy", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Strange Steam": ["Strange Steam", "31", 90, "Fairy", 95, 10, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Life Dew": ["Life Dew", "9D", 0, "Water", 0, 10, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 7, 
                ""],

        "Obstruct": ["Obstruct", "D0", 0, "Normal", 0, 0, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "FalseRetreat": ["FalseRetreat", "00", 80, "Dark", 0, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Star Assault": ["Star Assault", "50", 150, "Fighting", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Eternabeam": ["Eternabeam", "50", 160, "Dragon", 90, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Steel Beam": ["Steel Beam", "AA", 140, "Steel", 95, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 50, 
                ""],

        "Expand Force": ["Expand Force", "00", 80, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Steel Roller": ["Steel Roller", "BD", 130, "Steel", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Scale Shot": ["Scale Shot", "1D", 25, "Dragon", 90, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 21, 
                ""],

        "Meteor Beam": ["Meteor Beam", "00", 120, "Rock", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "ShellSideArm": ["ShellSideArm", "02", 90, "Poison", 100, 10, 20, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Misty Blast": ["Misty Blast", "07", 100, "Fairy", 100, 5, 0, 
                "AllButUser", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Grassy Glide": ["Grassy Glide", "00", 55, "Grass", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Voltage Rise": ["Voltage Rise", "00", 70, "Electric", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Terrain Pulse": ["Terrain Pulse", "00", 50, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Skitter Smack": ["Skitter Smack", "15", 70, "Bug", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Burning Envy": ["Burning Envy", "88", 70, "Fire", 100, 5, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 16, 
                ""],

        "Lash Out": ["Lash Out", "00", 75, "Dark", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Poltergeist": ["Poltergeist", "00", 110, "Ghost", 90, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Corrosive Gas": ["Corrosive Gas", "BC", 0, "Poison", 100, 40, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Coaching": ["Coaching", "90", 0, "Fighting", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 3, 
                ""],

        "Flip Turn": ["Flip Turn", "1C", 60, "Water", 100, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Triple Axel": ["Triple Axel", "00", 20, "Ice", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "1B", "Physical", 0, 
                ""],

        "Dual Wingbeat": ["Dual Wingbeat", "1D", 40, "Flying", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                ""],

        "BurningSands": ["BurningSands", "7D", 70, "Ground", 100, 10, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Jungle Heal": ["Jungle Heal", "D6", 0, "Grass", 0, 10, 0, 
                "MySide", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 7, 
                ""],

        "Wicked Blow": ["Wicked Blow", "00", 75, "Dark", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "SurgeStrikes": ["SurgeStrikes", "1D", 25, "Water", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 3, 
                ""],

        "Thunder Cage": ["Thunder Cage", "2A", 80, "Electric", 90, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Dragon Energy": ["Dragon Energy", "00", 150, "Dragon", 100, 5, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "03", "Special", 0, 
                ""],

        "Freeze Glare": ["Freeze Glare", "05", 90, "Psychic", 100, 10, 10, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Fiery Wrath": ["Fiery Wrath", "1F", 90, "Dark", 100, 10, 20, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Thunder Kick": ["Thunder Kick", "13", 90, "Fighting", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Glacial Lance": ["Glacial Lance", "00", 120, "Ice", 100, 5, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Astral Bit": ["Astral Bit", "00", 120, "Ghost", 100, 5, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Eerie Spell": ["Eerie Spell", "64", 80, "Psychic", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 3, 
                ""],

        "Dire Claw": ["Dire Claw", "24", 80, "Poison", 100, 15, 50, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 79, 
                ""],

        "Barrier Bash": ["Barrier Bash", "0B", 70, "Psychic", 90, 10, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Power Shift": ["Power Shift", "45", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 1, 0, 0, 0, 0], "00", "Status", 16, 
                ""],

        "Stone Axe": ["Stone Axe", "70", 65, "Rock", 90, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                ""],

        "Spring Storm": ["Spring Storm", "12", 100, "Fairy", 80, 10, 30, 
                "FoeSide", 0, [0, 0, 0, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Mystic Power": ["Mystic Power", "0D", 70, "Psychic", 90, 10, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Raging Fury": ["Raging Fury", "1B", 120, "Fire", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 3, 
                ""],

        "Wave Crash": ["Wave Crash", "30", 120, "Water", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 33, 
                ""],

        "Chloroblast": ["Chloroblast", "AA", 150, "Grass", 95, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 50, 
                ""],

        "Mountain Gale": ["Mountain Gale", "1F", 100, "Ice", 85, 10, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Victory Dance": ["Victory Dance", "8C", 0, "Fighting", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 7, 
                ""],

        "Headlong Rush": ["Headlong Rush", "8D", 120, "Ground", 100, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 18, 
                ""],

        "Barb Barrage": ["Barb Barrage", "02", 60, "Poison", 100, 10, 50, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Esper Wing": ["Esper Wing", "0C", 80, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 1, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Bitter Malice": ["Bitter Malice", "12", 75, "Ghost", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Shelter": ["Shelter", "0B", 0, "Steel", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 2, 
                ""],

        "Triple Arrows": ["Triple Arrows", "D7", 90, "Fighting", 100, 10, 50, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 2, 
                ""],

        "Fire Parade": ["Fire Parade", "04", 60, "Ghost", 100, 15, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Eternal Edge": ["Eternal Edge", "70", 65, "Dark", 90, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Chilly Winds": ["Chilly Winds", "14", 100, "Flying", 80, 10, 30, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "WildboltWind": ["WildboltWind", "06", 100, "Electric", 80, 10, 20, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "SandsearWind": ["SandsearWind", "04", 100, "Ground", 80, 10, 20, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "MoonBlessing": ["MoonBlessing", "D6", 0, "Psychic", 0, 5, 0, 
                "MySide", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 7, 
                ""],

        "Take Heart": ["Take Heart", "D8", 0, "Psychic", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 24, 
                ""],

        "Tera Blast": ["Tera Blast", "00", 80, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Silk Trap": ["Silk Trap", "D9", 0, "Bug", 0, 10, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Axe Kick": ["Axe Kick", "31", 120, "Fighting", 90, 10, 30, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Last Respects": ["Last Respects", "00", 50, "Ghost", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "C7", "Physical", 0, 
                ""],

        "Lumina Crash": ["Lumina Crash", "16", 80, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                ""],

        "Order Up": ["Order Up", "00", 80, "Dragon", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Jet Punch": ["Jet Punch", "00", 60, "Water", 100, 15, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Spicy Extract": ["Spicy Extract", "DA", 0, "Grass", 0, 15, 0, 
                "Target", 0, [0, 0, 0, 1, 0, 1, 1, 0], "00", "Status", 0, 
                ""],

        "Spin Out": ["Spin Out", "14", 100, "Steel", 100, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 2, 
                ""],

        "Proliferate": ["Proliferate", "1D", 20, "Normal", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 58, 
                ""],

        "Ice Spinner": ["Ice Spinner", "BD", 80, "Ice", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Glaive Rush": ["Glaive Rush", "DB", 120, "Dragon", 100, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Revival": ["Revival", "DC", 0, "Normal", 0, 1, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 1, 
                ""],

        "Salt Cure": ["Salt Cure", "DD", 40, "Rock", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Triple Dive": ["Triple Dive", "1D", 30, "Water", 95, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 3, 
                ""],

        "Mortal Spin": ["Mortal Spin", "DE", 30, "Poison", 100, 15, 0, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 8, 
                ""],

        "Doodle": ["Doodle", "B2", 0, "Normal", 100, 10, 0, 
                "TargetOrPartner", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 1, 
                ""],

        "Fillet Away": ["Fillet Away", "DF", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 1, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Kowtow Cleave": ["Kowtow Cleave", "00", 85, "Dark", 0, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Flower Trick": ["Flower Trick", "00", 70, "Grass", 0, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Torch Song": ["Torch Song", "0D", 80, "Fire", 100, 10, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Aqua Step": ["Aqua Step", "0C", 80, "Water", 100, 10, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Raging Bull": ["Raging Bull", "BA", 90, "Normal", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Make It Rain": ["Make It Rain", "C4", 120, "Steel", 100, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 8, 
                ""],

        "Psyblade": ["Psyblade", "00", 80, "Psychic", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Hydro Steam": ["Hydro Steam", "00", 80, "Water", 100, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Ruination": ["Ruination", "00", 0, "Dark", 90, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "59", "Special", 0, 
                ""],

        "Collision": ["Collision", "00", 100, "Fighting", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Electro Drift": ["Electro Drift", "00", 100, "Electric", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Special", 0, 
                ""],

        "Shed Tail": ["Shed Tail", "A2", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "ColdGreeting": ["ColdGreeting", "9E", 0, "Ice", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 8, 
                ""],

        "Tidy Up": ["Tidy Up", "D1", 0, "Normal", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Snowscape": ["Snowscape", "73", 0, "Ice", 0, 10, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 32, 
                ""],

        "Pounce": ["Pounce", "14", 50, "Bug", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Trailblaze": ["Trailblaze", "0C", 50, "Grass", 100, 20, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 1], "00", "Physical", 1, 
                ""],

        "Chilly Water": ["Chilly Water", "12", 50, "Water", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 1, 
                ""],

        "Hyper Drill": ["Hyper Drill", "00", 100, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 0, 1], "00", "Physical", 0, 
                ""],

        "Twin Beam": ["Twin Beam", "1D", 40, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                ""],

        "Rage Fist": ["Rage Fist", "00", 50, "Ghost", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "D7", "Physical", 0, 
                ""],

        "Armor Cannon": ["Armor Cannon", "8D", 120, "Fire", 100, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Special", 18, 
                ""],

        "Bitter Blade": ["Bitter Blade", "03", 90, "Fire", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 50, 
                ""],

        "Double Shock": ["Double Shock", "08", 120, "Electric", 100, 5, 0, 
                "Target", 0, [0, 1, 1, 1, 0, 0, 1, 0], "00", "Physical", 13, 
                ""],

        "Huge Hammer": ["Huge Hammer", "00", 160, "Steel", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Comeuppance": ["Comeuppance", "00", 0, "Dark", 100, 10, 0, 
                "LastHitMe", 0, [0, 0, 1, 1, 0, 0, 1, 0], "8B", "Physical", 0, 
                ""],

        "Aqua Cutter": ["Aqua Cutter", "00", 70, "Water", 100, 20, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "BlazeTorque": ["BlazeTorque", "04", 80, "Fire", 100, 10, 30, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Wicked Torque": ["Wicked Torque", "01", 80, "Dark", 100, 10, 10, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "PoisonTorque": ["PoisonTorque", "02", 100, "Poison", 100, 10, 30, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Combat Torque": ["Combat Torque", "06", 100, "Fighting", 100, 10, 30, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Magic Torque": ["Magic Torque", "31", 100, "Fairy", 100, 10, 30, 
                "Target", 0, [0, 0, 0, 0, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Blood Moon": ["Blood Moon", "00", 140, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "MatchaGotcha": ["MatchaGotcha", "20", 80, "Grass", 90, 15, 20, 
                "FoeSide", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Syrup Bomb": ["Syrup Bomb", "BE", 60, "Grass", 85, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 3, 
                ""],

        "Ivy Cudgel": ["Ivy Cudgel", "00", 100, "Grass", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Physical", 0, 
                ""],

        "Electro Shot": ["Electro Shot", "00", 130, "Electric", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "TeraStarbeam": ["TeraStarbeam", "00", 120, "Normal", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Fickle Beam": ["Fickle Beam", "00", 80, "Dragon", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "E7", "Special", 0, 
                ""],

        "Bulwark Burn": ["Bulwark Burn", "96", 0, "Fire", 0, 10, 0, 
                "User", 4, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Thunderclap": ["Thunderclap", "00", 70, "Electric", 100, 5, 0, 
                "Target", 1, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Mighty Cleave": ["Mighty Cleave", "00", 95, "Rock", 100, 5, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 0, 1], "00", "Physical", 0, 
                ""],

        "TachyonBlade": ["TachyonBlade", "1D", 50, "Steel", 0, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 2, 
                ""],

        "Hard Press": ["Hard Press", "00", 100, "Steel", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "13", "Physical", 0, 
                ""],

        "Dragon Cheer": ["Dragon Cheer", "8A", 0, "Dragon", 0, 15, 0, 
                "User", 0, [0, 0, 0, 0, 0, 0, 0, 0], "00", "Status", 0, 
                ""],

        "Allure Voice": ["Allure Voice", "88", 80, "Fairy", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Temper Flare": ["Temper Flare", "00", 75, "Fire", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "F7", "Physical", 0, 
                ""],

        "SupercelSlam": ["SupercelSlam", "00", 100, "Electric", 95, 15, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Psychic Noise": ["Psychic Noise", "3D", 75, "Psychic", 100, 10, 0, 
                "Target", 0, [0, 0, 1, 1, 0, 0, 1, 0], "00", "Special", 0, 
                ""],

        "Upper Hand": ["Upper Hand", "00", 65, "Fighting", 100, 15, 0, 
                "Target", 3, [0, 0, 1, 1, 0, 0, 1, 1], "00", "Physical", 0, 
                ""],

        "Evil Chain": ["Evil Chain", "21", 100, "Poison", 100, 5, 50, 
                "Target", 0, [0, 0, 1, 0, 0, 0, 1, 0], "00", "Special", 0, 
                ""]}

# ------------------------------------------------------------
# Create Auto Fill Dictionary
# ------------------------------------------------------------
AutoFillList = {}
Gen = 1
for Move in PresetMoveList:
    match Move:
        case "Sketch":
            Gen = 2
        case "Fake Out":
            Gen = 3
        case "Roost":
            Gen = 4
        case "Hone Claws":
            Gen = 5
        case "Flying Press":
            Gen = 6
        case "Breakneck Blitz":
            Gen = 7
        case "Max Guard":
            Gen = 8
        case "Tera Blast":
            Gen = 9
            
    AutoFillList[Move] = [Move, "Introduced in Generation {}".format(Gen)]
                  
# ------------------------------------------------------------
# Script Argument Helper Dictionary - {Number : [Kind:Args]}
# ------------------------------------------------------------
ScriptArgumentHelpers = {"00":["NoArgs", []],
                         "01":["Turns", [1,7]],
                         "02":["NoArgs", []],
                         "03":["Percent", ["User", "absorb", "the damage dealt", "HP"]],
                         "04":["NoArgs", []],
                         "05":["NoArgs", []],
                         "06":["NoArgs", []],
                         "07":["NoArgs", []],
                         "08":["Type", ["The Target will have their {} Type removed."]],
                         "09":["NoArgs", []],
                         "0A":["StageAmount", ["Attack", "increase"]],
                         "0B":["StageAmount", ["Defence", "increase"]],
                         "0C":["StageAmount", ["Speed", "increase"]],
                         "0D":["StageAmount", ["Sp. Attack", "increase"]],
                         "0E":["StageAmount", ["Sp. Defence", "increase"]],
                         "0F":["StageAmount", ["Accuracy", "increase"]],
                         "10":["StageAmount", ["Evasion", "increase"]],
                         "11":["NoArgs", []],
                         "12":["StageAmount", ["Attack", "decrease"]],
                         "13":["StageAmount", ["Defence", "decrease"]],
                         "14":["StageAmount", ["Speed", "decrease"]],
                         "15":["StageAmount", ["Sp. Attack", "decrease"]],
                         "16":["StageAmount", ["Sp. Defence", "decrease"]],
                         "17":["StageAmount", ["Accuracy", "decrease"]],
                         "18":["StageAmount", ["Evasion", "decrease"]],
                         "19":["NoArgs", []],
                         "1A":["Turns", [1,15]],
                         "1B":["Turns", [2,5]],
                         "1C":["Custom", [3]],
                         "1D":["MultiHit", []],
                         "1E":["NoArgs", []],
                         "1F":["NoArgs", []],
                         "20":["Percent", ["User", "absorb", "the damage dealt", "HP"]],
                         "21":["NoArgs", []],
                         "22":["Custom", [0]],
                         "23":["Turns", [1,15]],
                         "24":["MajorStatus", ["One of the selected Statuses will be chosen randomly.", 0]],
                         "25":["MajorStatus", ["The Target will heal fully, but will\nbe inflicted with the {} Status.", 1]],
                         "26":["NoArgs", []],
                         "27":["Type", ["The Target's next Move will become {} Type."]],
                         "28":["StatStatus2", ["The Target's given Stats will rise by one\nif they have the given Status."]],
                         "29":["NoArgs", []],
                         "2A":["Turns", [4,15]],
                         "2B":["Turns", [1,15]],
                         "2C":["Custom", [1]],
                         "2D":["Custom", [2]],
                         "2E":["Turns", [1,15]],
                         "2F":["NoArgs", []],
                         "30":["Percent", ["User", "take", "the damage dealt", "Recoil"]],
                         "31":["Turns", [1,15]],
                         "32":["Future", [1,15, "Future attack will happen"]],
                         "33":["PercentStatus", ["the damage dealt"]],
                         "34":["Turns", [1,15]],
                         "35":["Turns", [1,15]],
                         "36":["Turns", [1,15]],
                         "37":["Turns", [1,15]],
                         "38":["Turns", [1,15]],
                         "39":["NoArgs", []],
                         "3A":["Turns", [1,15]],
                         "3B":["Type", ["The Target will gain the {} Type."]],
                         "3C":["Turns", [1,15]],
                         "3D":["Turns", [1,15]],
                         "3E":["Type", ["The Target will heal 50% of their maximum HP\nand lose the {} Type."]],
                         "3F":["Turns", [1,15]],
                         "40":["NoArgs", []],
                         "41":["Turns", [1,15]],
                         "42":["Custom", [4]],
                         "43":["StageAmount", ["Random Stat", "increase"]],
                         "44":["NoArgs", []],
                         "45":["TwoStats", ["The {}'s raw {} and\n{} Stats will be swapped."]],
                         "46":["Custom", [15]],
                         "47":["NoArgs", []],
                         "48":["NoArgs", []],
                         "49":["StatFlags", ["The selected Stat Stages will be swapped\nbetween the User and the Target."]],
                         "4A":["Custom", [13]],
                         "4B":["Turns", [1,15]],
                         "4C":["MajorStatus", ["The Target will be inflicted with the {}\nStatus and will Flinch if they moved last.", 1]],
                         "4D":["Turns", [1,15]],
                         "4E":["NoArgs", []],
                         "4F":["NoArgs", []],
                         "50":["NoArgs", []],
                         "51":["NoArgs", []],
                         "52":["NoArgs", []],
                         "53":["NoArgs", []],
                         "54":["NoArgs", []],
                         "55":["StatFlags", ["The User's selected Stat Stages rise by two\nif the Target faints from this attack."]],
                         "56":["Turns", [1,15]],
                         "57":["TwoStats", ["The {}'s {} and {} will\nbe averaged and set to the result."]],
                         "58":["Turns", [1,15]],
                         "59":["Turns", [1,15]],
                         "5A":["Turns", [1,15]],
                         "5B":["StatFlags", ["The Target's selected Stat Stages will rise by\none if they have the Plus or Minus Ability."]],
                         "5C":["Turns", [1,15]],
                         "5D":["NoArgs", []],
                         "5E":["NoArgs", []],
                         "5F":["NoArgs", []],
                         "60":["NoArgs", []],
                         "61":["NoArgs", []],
                         "62":["Turns", [1,15]],
                         "63":["Percent", ["Target's Partner", "take", "their maximum HP", "Recoil"]],
                         "64":["PowerPoints", []],
                         "65":["Type", ["The Target will become a {} Type."]],
                         "66":["NoArgs", []],
                         "67":["NoArgs", []],
                         "68":["NoArgs", []],
                         "69":["Custom", [5]],
                         "6A":["TrapTarget", ["Trap"]],
                         "6B":["NoArgs", []],
                         "6C":["StageAmount", ["Evasion", "increase"]],
                         "6D":["NoArgs", []],
                         "6E":["NoArgs", []],
                         "6F":["NoArgs", []],
                         "70":["Custom", [8]],
                         "71":["NoArgs", []],
                         "72":["Turns", [1,15]],
                         "73":["Weather", ["The Weather will become {} for five turns.", 1]],
                         "74":["NoArgs", []],
                         "75":["NoArgs", []],
                         "76":["StatFlags", ["The Target will be Confused and the\nselected Stat Stages will rise by two."]],
                         "77":["NoArgs", []],
                         "78":["NoArgs", []],
                         "79":["NoArgs", []],
                         "7A":["NoArgs", []],
                         "7B":["NoArgs", []],
                         "7C":["Turns", [1,15]],
                         "7D":["Custom", [6]],
                         "7E":["NoArgs", []],
                         "7F":["Type", ["The Target's Attack and Sp. Attack will rise by\none Stat Stage if they are {} Type."]],
                         "80":["StatFlags", ["The Target's selected Stat Stages will drop\nby two and the User will switch out."]],
                         "81":["NoArgs", []],
                         "82":["NoArgs", []],
                         "83":["NoArgs", []],
                         "84":["NoArgs", []],
                         "85":["StatType", ["If the Target is {} Type, they will have\ntheir {} raised by one Stat Stage."]],
                         "86":["Turns", [1,15]],
                         "87":["NoArgs", []],
                         "88":["MajorStatus", ["The Target will be inflicted with {} but\nonly if their Stat Stages raised this turn.", 1]],
                         "89":["NoArgs", []],
                         "8A":["NoArgs", []],
                         "8B":["Custom", [7]],
                         "8C":["StatFlags", ["The Target's selected Stat Stages will rise by one."]],
                         "8D":["StatFlags", ["The Target's selected Stat Stages will drop by one."]],
                         "8E":["StatFlags", ["The Target's HP will by cut in half to maximise the selected Stat Stages."]],
                         "8F":["NoArgs", []],
                         "90":["StatFlags", ["The Target's Partner's selected Stat Stages will rise by one."]],
                         "91":["Turns", [1,15]],
                         "92":["StatFlags", ["The Target's selected Stat Stages will rise by two."]],
                         "93":["StatFlags", ["The Target's selected Stat Stages will drop by two."]],
                         "94":["NoArgs", []],
                         "95":["StatFlags", ["The Target's selected Stat Stages will drop by one\nand the User will heal HP based on those Stats."]],
                         "96":["NoArgs", []],
                         "97":["StatStatus", ["If the Target has the {} Status,\ntheir {} will drop by one Stat Stage."]],
                         "98":["Turns", [1,15]],
                         "99":["Turns", [1,15]],
                         "9A":["NoArgs", []],
                         "9B":["StatusType", ["If the Target is {} Type, they will be\ncured of {} and lose that Type."]],
                         "9C":["StageAmount", ["Defence", "increase"]],
                         "9D":["Custom", [9]],
                         "9E":["Weather", ["The Weather will become {} and\nthe Target will switch out.", 1]],
                         "9F":["Turns", [1,7]],
                         "A0":["NoArgs", []],
                         "A1":["NoArgs", []],
                         "A2":["NoArgs", []],
                         "A3":["NoArgs", []],
                         "A4":["NoArgs", []],
                         "A5":["NoArgs", []],
                         "A6":["NoArgs", []],
                         "A7":["Custom", [10]],
                         "A8":["StatFlags", ["The Target's given Stat Stages will drop\nby two and the User will faint."]],
                         "A9":["Custom", [16]],
                         "AA":["Percent", ["User", "take", "their maximum HP", "Recoil"]],
                         "AB":["MajorStatus", ["The Target will be cured of the selected Status Conditions.", 0]],
                         "AC":["Custom", [11]],
                         "AD":["NoArgs", []],
                         "AE":["Turns", [1,15]],
                         "AF":["Turns", [1,15]],
                         "B0":["Turns", [1,15]],
                         "B1":["NoArgs", []],
                         "B2":["Custom", [12]],
                         "B3":["Future", [1,15, "Wish will come true"]],
                         "B4":["NoArgs", []],
                         "B5":["NoArgs", []],
                         "B6":["NoArgs", []],
                         "B7":["Turns", [1,15]],
                         "B8":["NoArgs", []],
                         "B9":["Type", ["For the next turn, all Normal Type\nMoves become {} Type."]],
                         "BA":["NoArgs", []],
                         "BB":["NoArgs", []],
                         "BC":["NoArgs", []],
                         "BD":["NoArgs", []],
                         "BE":["Turns", [1,15]],
                         "BF":["NoArgs", []],
                         "C0":["Custom", [17]],
                         "C1":["StatFlags", ["The User eats their Held Berry and the selected Stat Stages rise by two."]],
                         "C2":["Turns", [1,15]],
                         "C3":["Turns", [1,15]],
                         "C4":["StatFlags", ["The Target's selected Stat Stages will drop by\none and the Player will earn money if they win."]],
                         "C5":["NoArgs", []],
                         "C6":["StatFlags", ["The Target's selected Stat Stages will rise by one and they will be Trapped."]],
                         "C7":["StatFlags", ["The Target's selected Stat Stages will drop by\none and the Tar Shot Flag will be set."]],
                         "C8":["NoArgs", []],
                         "C9":["Turns", [1,15]],
                         "CA":["TrapTarget", ["Octolock"]],
                         "CB":["NoArgs", []],
                         "CC":["StatFlags", ["The Target and their Partner's selected Stat Stages will rise by one."]],
                         "CD":["StatFlags", ["The Target and their Partner's selected Stat Stages will drop by one."]],
                         "CE":["StatFlags", ["The Target loses 1/3 of their maximum HP and\nthe selected Stat Stages will rise by one "]],
                         "CF":["Weather", ["The Target's Attack and Sp. Attack will rise by two in the selected Weather.", 0]],
                         "D0":["NoArgs", []],
                         "D1":["NoArgs", []],
                         "D2":["Turns", [1,15]],
                         "D3":["StatFlags", ["The Target's Partner's selected Stat Stages will rise by one."]],
                         "D4":["StatFlags", ["The Target's Partner's selected Stat Stages will drop by one."]],
                         "D5":["NoArgs", []],
                         "D6":["Custom", [9]],
                         "D7":["StatFlags", ["The Target's selected Stat Stages will drop by\none, with a 30% chance of Flinching too."]],
                         "D8":["StatFlags", ["The Target's selected Stat Stages will rise by\none and they will be cured of Major Statuses."]],
                         "D9":["NoArgs", []],
                         "DA":["NoArgs", []],
                         "DB":["NoArgs", []],
                         "DC":["Custom", [14]],
                         "DD":["NoArgs", []],
                         "DE":["MajorStatus", ["In addition to removing hazards from the User's side,\nthe Target will be given the {} Status.", 1]],
                         "DF":["StatFlags", ["The Target's HP will be cut in half and the selected Stat Stages will rise by two."]],
                         "E0":["NoArgs", []],
                         "E1":["NoArgs", []],
                         "E2":["NoArgs", []],
                         "E3":["NoArgs", []],
                         "E4":["NoArgs", []],
                         "E5":["NoArgs", []],
                         "E6":["NoArgs", []],
                         "E7":["NoArgs", []],
                         "E8":["NoArgs", []],
                         "E9":["NoArgs", []],
                         "EA":["NoArgs", []],
                         "EB":["NoArgs", []],
                         "EC":["NoArgs", []],
                         "ED":["NoArgs", []],
                         "EE":["NoArgs", []],
                         "EF":["NoArgs", []],
                         "F0":["NoArgs", []],
                         "F1":["NoArgs", []],
                         "F2":["NoArgs", []],
                         "F3":["NoArgs", []],
                         "F4":["NoArgs", []],
                         "F5":["NoArgs", []],
                         "F6":["NoArgs", []],
                         "F7":["NoArgs", []],
                         "F8":["NoArgs", []],
                         "F9":["NoArgs", []],
                         "FA":["NoArgs", []],
                         "FB":["NoArgs", []],
                         "FC":["NoArgs", []],
                         "FD":["NoArgs", []],
                         "FE":["NoArgs", []],
                         "FF":["NoArgs", []]}

# ------------------------------------------------------------
# Custom Damage Formula List - This is for Formula 07
# ------------------------------------------------------------
CustomList = ["Psywave",
              "Magnitude",
              "Triple Kick",
              "Momentum Move",
              "Fury Cutter",
              "Present",
              "Beat Up",
              "Spit Up", 
              "Endeavour",
              "Trump Card",
              "Round",
              "Echoed Voice",
              "Last Respects",
              "Rage Fist",
              "Fickle Beam",
              "Temper Flare"]

# ------------------------------------------------------------
# Formula Argument Dictionary - Same as the Script Argument
# ------------------------------------------------------------
FormulaArgumentHelpers = {"00":["Counter", []],
                          "01":["SetTarget", ["Level"]],
                          "02":["Relation", ["Friendship"]],
                          "03":["Relation", ["Current HP"]],
                          "04":["Multiple", []],
                          "05":["Relation", ["Weight"]],
                          "06":["Relation", ["Speed"]],
                          "07":["Custom", [CustomList]],
                          "08":["StatStages", []],
                          "09":["Percent", ["HP"]],
                          "0A":["Item", []],
                          "0B":["Counter", []],
                          "0C":["NoArgs", []],
                          "0D":["NoArgs", []],
                          "0E":["NoArgs", []],
                          "0F":["NoArgs", []]}

# ------------------------------------------------------------
# Ability Dictionary - This is the default for ACE, not all
# ------------------------------------------------------------
AbilityList = {"Stench":1,
               "Drizzle":2,
               "Speed Boost":3,
               "Battle Armour":4,
               "Sturdy":5,
               "Damp":6,
               "Limber":7,
               "Sand Veil":8,
               "Static":9,
               "Volt Absorb":10,
               "Water Absorb":11,
               "Oblivious":12,
               "Cloud Nine":13,
               "Compound Eyes":14,
               "Insomnia":15,
               "Color Change":16,
               "Immunity":17,
               "Flash Fire":18,
               "Shield Dust":19,
               "Own Tempo":20,
               "Suction Cups":21,
               "Intimidate":22,
               "Shadow Tag":23,
               "Rough Skin":24,
               "Wonder Guard":25,
               "Levitate":26,
               "Effect Spore":27,
               "Synchronise":28,
               "Clear Body":29,
               "Natural Cure":30,
               "Lightning Rod":31,
               "Serene Grace":32,
               "Swift Swim":33,
               "Chlorophyll":34,
               "Illuminate":35,
               "Trace":36,
               "Huge Power":37,
               "Poison Point":38,
               "Inner Focus":39,
               "Magma Armour":40,
               "Water Veil":41,
               "Magnet Pull":42,
               "Soundproof":43,
               "Rain Dish":44,
               "Sand Stream":45,
               "Pressure":46,
               "Thick Fat":47,
               "Early Bird":48,
               "Flame Body":49,
               "Run Away":50,
               "Keen Eye":51,
               "Hyper Cutter":52,
               "Pick Up":53,
               "Truant":54,
               "Hustle":55,
               "Cute Charm":56,
               "Plus":57,
               "Minus":58,
               "Forecast":59,
               "Sticky Hold":60,
               "Shed Skin":61,
               "Guts":62,
               "Marvel Scale":63,
               "Liquid Ooze":64,
               "Overgrow":65,
               "Blaze":66,
               "Torrent":67,
               "Swarm":68,
               "Rock Head":69,
               "Drought":70,
               "Arena Trap":71,
               "Vital Spirit":72,
               "White Smoke":73,
               "Pure Power":74,
               "Shell Armour":75,
               "Cacaphony":76,
               "Air Lock":77,
               "Tangled Feet":78,
               "Motor Drive":79,
               "Rivalry":80,
               "Steadfast":81,
               "Snow Cloak":82,
               "Gluttony":83,
               "Anger Point":84,
               "Unburden":85,
               "Heatproof":86,
               "Simple":87,
               "Dry Skin":88,
               "Download":89,
               "Iron Fist":90,
               "Poison Heal":91,
               "Adaptability":92,
               "Skill Link":93,
               "Hydration":94,
               "Solar Power":95,
               "Quick Feet":96,
               "Normalise":97,
               "Sniper":98,
               "Magic Guard":99,
               "No Guard":100,
               "Stall":101,
               "Technician":102,
               "Leaf Guard":103,
               "Klutz":104,
               "Mold Breaker":105,
               "Super Luck":106,
               "Aftermath":107,
               "Anticipation":108,
               "Forewarn":109,
               "Unaware":110,
               "Tinted Lens":111,
               "Filter":112,
               "Slow Start":113,
               "Scrappy":114,
               "Storm Drain":115,
               "Ice Body":116,
               "Solid Rock":117,
               "Snow Warning":118,
               "Honey Gather":119,
               "Frisk":120,
               "Reckless":121,
               "Multitype":122,
               "Flower Gift":123,
               "Bad Dreams":124,
               "Pickpocket":125,
               "Sheer Force":126,
               "Contrary":127,
               "Unnerve":128,
               "Defiant":129,
               "Defeatist":130,
               "Cursed Body":131,
               "Healer":132,
               "Friend Guard":133,
               "Weak Armour":134,
               "Heavy Metal":135,
               "Light Metal":136,
               "Multiscale":137,
               "Toxic Boost":138,
               "Flare Boost":139,
               "Harvest":140,
               "Telepathy":141,
               "Moody":142,
               "Overcoat":143,
               "Poison Touch":144,
               "Regenerator":145,
               "Big Pecks":146,
               "Sand Rush":147,
               "Wonder Skin":148,
               "Analytic":149,
               "Illusion":150,
               "Imposter":151,
               "Infiltrator":152,
               "Mummy":153,
               "Moxie":154,
               "Justified":155,
               "Rattled":156,
               "Magic Bounce":157,
               "Sap Sipper":158,
               "Prankster":159,
               "Sand Force":160,
               "Iron Barbs":161,
               "Zen Mode":162,
               "Victory Star":163,
               "Turboblaze":164,
               "Teravolt":165,
               "Aroma Veil":166,
               "Flower Veil":167,
               "Cheek Pouch":168,
               "Protean":169,
               "Fur Coat":170,
               "Magician":171,
               "Bulletproof":172,
               "Competitive":173,
               "Strong Jaw":174,
               "Refrigerate":175,
               "Sweet Veil":176,
               "Stance Change":177,
               "Gale Wings":178,
               "Mega Launcher":179,
               "Grass Pelt":180,
               "Symbiosis":181,
               "Tough Claws":182,
               "Pixilate":183,
               "Gooey":184,
               "Aerilate":185,
               "Parental Bond":186,
               "Dark Aura":187,
               "Fairy Aura":188,
               "Aura Break":189,
               "Ancient Sea":190,
               "Desolate Land":191,
               "Delta Stream":192,
               "Stamina":193,
               "Wimp Out":194,
               "Danger Dash":195,
               "Water Fort":196,
               "Merciless":197,
               "Shields Down":198,
               "Stakeout":199,
               "Water Bubble":200,
               "Steelworker":201,
               "Berserk":202,
               "Slush Rush":203,
               "Long Reach":204,
               "Liquid Voice":205,
               "Triage":206,
               "Galvanise":207,
               "Surge Surfer":208,
               "Schooling":209,
               "Disguise":210,
               "Battle Bond":211,
               "Swarm Change":212,
               "Corrosion":213,
               "Comatose":214,
               "Queen Majesty":215,
               "Innards Out":216,
               "Dancer":217,
               "Battery":218,
               "Fluffy":219,
               "Dazzling":220,
               "Soul":221,
               "Tangling Hair":222,
               "Receiver":223,
               "Alchemy Power":224,
               "Beast Boost":225,
               "R K S System":226,
               "Thunder Surge":227,
               "Psychic Surge":228,
               "Misty Surge":229,
               "Grassy Surge":230,
               "Full Metal":231,
               "Shadow Shield":232,
               "Prism Armour":233,
               "Neuroforce":234,
               "Daring Sword":235,
               "Daring Shield":236,
               "Libero":237,
               "Ball Fetch":238,
               "Cotton Down":239,
               "Propel Tail":240,
               "Mirror Armour":241,
               "Gulp Missile":242,
               "Stalwart":243,
               "Steam Engine":244,
               "Punk Rock":245,
               "Sand Spit":246,
               "Ice Scales":247,
               "Ripen":248,
               "Ice Face":249,
               "Power Spot":250,
               "Mimicry":251,
               "Screen Clean":252,
               "Steely Spirit":253,
               "Perish Body":254}

# ------------------------------------------------------------
# Move Script Text Dictionary - {Script N: [Text For Script N]
# ------------------------------------------------------------
MoveScriptText = {
    "Script 00":
    ["This script does not have any additional effects.",
    "If the Move is a Damaging Move, it will deal damage and",
    "nothing else.",
    "If the Move is a Status Move, it will do nothing at all."],

    "Script 01":
    ["This script has the effect of putting the Target to Sleep",
    "for the given number of turns.",
    "A Sleeping Pokemon will have their attacks Cancelled until",
    "they wake up."],

    "Script 02":
    ["This script has the effect of Poisoning the Target.",
    "A Poisoned Pokemon takes damage at the end of each turn."],

    "Script 03":
    ["This script has the effect of healing the User's HP by the",
    "given percentage of the damage this attack dealt.",
    "If this is not a Damaging Move, then no HP will be healed."],

    "Script 04":
    ["This script has the effect of Burning the Target.",
    "A Burned Pokemon has their Attack halved and takes damage at",
    "the end of the turn."],

    "Script 05":
    ["This script has the effect of Freezing the Target.",
    "A Frozen Pokemon has their attacks Cancelled until they thaw",
    "out, which has a 20% chance to occur each turn.",
    "In addition, all Fire Type Moves will thaw a Frozen Target."],

    "Script 06":
    ["This script has the effect of Paralysing the Target.",
    "A Paralysed Pokemon has their Speed quartered and has a 25%",
    "chance of having their attack Cancelled that turn."],

    "Script 07":
    ["This script has the effect of causing the User to faint",
    "after inflicting damage onto the Target.",
    "If the Move is nullified, the User will not faint."],

    "Script 08":
    ["This script has the effect of removing the given Type from",
    "the Target.",
    "If the Target does not have that Type, the Move fails."],

    "Script 09":
    ["This script is for the Move Mirror Move.",
    "Mirror Move copies the Move that was last executed and",
    "Targets the Pokemon who used it."],

    "Script 0A":
    ["This script has the effect of raising the User's Attack Stat",
    "Stages by the given amount."],

    "Script 0B":
    ["This script has the effect of raising the User's Defence",
    "Stat Stages by the given amount."],

    "Script 0C":
    ["This script has the effect of raising the User's Speed Stat",
    "Stages by the given amount."],

    "Script 0D":
    ["This script has the effect of raising the User's Sp. Attack",
    "Stat Stages by the given amount."],

    "Script 0E":
    ["This script has the effect of raising the User's Sp. Defence",
    "Stat Stages by the given amount."],

    "Script 0F":
    ["This script has the effect of raising the User's Accuracy",
    "Stat Stages by the given amount."],

    "Script 10":
    ["This script has the effect of raising the User's Evasion",
    "Stat Stages by the given amount."],

    "Script 11":
    ["This script has the effect of setting the Gravity Global",
    "Flag.",
    "The Gravity effect forces all Pokemon to be Grounded and",
    "forbids the selection of certain Moves."],

    "Script 12":
    ["This script has the effect of lowering the User's Attack",
    "Stat Stages by the given amount."],

    "Script 13":
    ["This script has the effect of lowering the User's Defence",
    "Stat Stages by the given amount."],

    "Script 14":
    ["This script has the effect of lowering the User's Speed",
    "Stat Stages by the given amount."],

    "Script 15":
    ["This script has the effect of lowering the User's Sp. Attack",
    "Stat Stages by the given amount."],

    "Script 16":
    ["This script has the effect of lowering the User's Sp.",
    "Defence Stat Stages by the given amount."],

    "Script 17":
    ["This script has the effect of lowering the User's Accuracy",
    "Stat Stages by the given amount."],

    "Script 18":
    ["This script has the effect of lowering the User's Evasion",
    "Stat Stages by the given amount."],

    "Script 19":
    ["The effect of this script is to reset all Pokemon's Stat",
    "Stages to zero."],

    "Script 1A":
    ["The effect of this script is to set the Bide Flag for the",
    "User.",
    "The Bide effect causes the Pokemon to skip their next two",
    "turns.",
    "At the end, they will deal damage to the last Pokemon to",
    "Target them."],

    "Script 1B":
    ["The effect of this script is to set the Thrash Flag for the",
    "User.",
    "The Thrash Flag locks the Pokemon into using the same Move",
    "for 2-3 turns.",
    "At the end, they will become Confused."],

    "Script 1C":
    ["This script forces the Target to switch out if they are able",
    "to.",
    "Stat Stages and other effects may be passed on.",
    "If the Self-effect Flag is set, the Target can choose who to",
    "switch to.",
    "If it is not, then it will be randomly chosen."],

    "Script 1D":
    ["This script has the effect of allowing the Move to hit the",
    "Target multiple times in a row.",
    "This could be a set amount of times or a random amount.",
    "Additional effects are tied to the Move itself via the",
    "SetMultiHiteffect command."],

    "Script 1E":
    ["This script is for the Move Conversion.",
    "This Move changes the User's Type to match one of their",
    "Moves.",
    "If they cannot change Types in this way, the Move fails."],

    "Script 1F":
    ["The effect of this script is to make the Target Flinch."],

    "Script 20":
    ["This script has the effect of healing the User's HP by the",
    "given percentage of the damage dealt.",
    "In addition, this script also has the effect of Burning the",
    "Target.",
    "If this is a Status Move, no HP will be healed but the Burn",
    "will still be inflicted."],

    "Script 21":
    ["The effect of this script is to Badly Poison the Target.",
    "A Badly Poisoned Pokemon will take damage at the end of the",
    "turn, with the damage increasing each time."],

    "Script 22":
    ["This script is for the Move Pay Day.",
    "The player will win extra money at the end of the battle, if",
    "they win, after using this Move."],

    "Script 23":
    ["This script has the effect of setting up Light Screen for",
    "the Target's side.",
    "The Light Screen effect boosts the Sp. Defence of the",
    "affected Pokemon."],

    "Script 24":
    ["This script has the effect of inflicting the Target with a",
    "random Major Status from the options given.",
    "Each has the same chance to occur.",
    "The effect chance is the probability that any of them will",
    "happen,",
    "i.e. Burn, Poison, Paralysis",
    "with effect chance = 30 means each has a 10 percent chance."],

    "Script 25":
    ["This script has the effect of fully healing the User's HP,",
    "but in return they are afflicted with the given Major",
    "Status."],

    "Script 26":
    ["This script has the effect of raising the User's Speed by",
    "two Stat Stages and the User's Attack by one Stat Stage."],

    "Script 27":
    ["This script has the effect of forcing the Target's next Move",
    "to become the given Type."],

    "Script 28":
    ["This script has the effect of lowering the Attack, Sp.",
    "Attack and Speed Stat Stages of the Target by one if they",
    "have the given Major Status condition."],

    "Script 29":
    ["This script is for the Move Teleport, which immediately",
    "causes the User to flee if they are able to."],

    "Script 2A":
    ["This script has the effect of setting the Wrap Flag for the",
    "Target for 4-5 turns.",
    "The Wrap Flag causes the Pokemon to take damage at the end",
    "of the turn and be unable to switch."],

    "Script 2B":
    ["This script has the effect of setting the Ion Deluge Global",
    "Flag for the given amount of turns.",
    "The Ion Deluge Flag causes all Normal Type Moves to become",
    "Electric Type while in effect."],

    "Script 2C":
    ["This script has the effect of setting the given Terrain",
    "Global Flag for five turns."],

    "Script 2D":
    ["This script is for the Move Autotomise.",
    "This raises the User's Speed by two Stat Stages and",
    "decreases their weight by 220 lbs/100 kg."],

    "Script 2E":
    ["This script has the effect of setting the Mist Flag for the",
    "Target's side for the given number of turns.",
    "The Mist effect prevents Stat Stages from being lowered by",
    "opponents (self-lowering is unaffected)."],

    "Script 2F":
    ["This script has the effect of setting the Focus Energy Flag",
    "for the Target.",
    "The Focus Energy effect raises the Pokemon's Critical Hit",
    "Ratio by two stages."],

    "Script 30":
    ["This script has the effect of inflicting the User with",
    "Recoil Damage equal to the given percentage of the damage",
    "this attack dealt.",
    "If this is a Status Move, no damage will be done to either",
    "party."],

    "Script 31":
    ["This script has the effect of Confusing the Target.",
    "A Confused Pokemon has a 33% chance to cancel their attack",
    "and hit themselves instead."],

    "Script 32":
    ["This script has the effect of causing an attack against the",
    "Pokemon in the Target's position to happen in the given",
    "number of turns."],

    "Script 33":
    ["This script has the effect of Paralysing the Target and",
    "causing recoil damage to the User equal to the given percent",
    "of the damage this attack dealt.",
    "If this is a Status Move, the Paralysis effect will occur,",
    "but not the recoil effect."],

    "Script 34":
    ["This script has the effect of setting the Aurora Veil Flag",
    "for the Target's side.",
    "The Aurora Veil effect boosts Defence and Sp. Defence, but",
    "can only be activated during Hail."],

    "Script 35":
    ["This script has the effect of setting the Tailwind Flag for",
    "the Target's side for the given number of turns.",
    "The Tailwind effect boosts the Speed of the Pokemon",
    "affected."],

    "Script 36":
    ["This script has the effect of setting the Quick Guard Flag",
    "for the Target's side.",
    "The Quick Guard effect blocks Priority Moves used against",
    "the affected Pokemon."],

    "Script 37":
    ["This script has the effect of setting the Wide Guard Flag",
    "for the Target's side.",
    "The Wide Guard effect blocks Moves which Target more than",
    "one Pokemon at a time.",
    "This effect still applies in Single Battles and is",
    "determined by the Range value of the Move."],

    "Script 38":
    ["This script has the effect of setting the Mat Block Flag for",
    "the Target's side.",
    "The Mat Block effect blocks Damaging Moves used against the",
    "affected Pokemon."],

    "Script 39":
    ["This script is for the Move Transform. Transforming into the",
    "Target copies their Moves, Stats (except HP) and Ability."],

    "Script 3A":
    ["This script has the effect of setting the Lucky Chant Flag",
    "for the Target's side for the given number of turns.",
    "The Lucky Chant effect prevents the Pokemon from taking",
    "Critical Hits."],

    "Script 3B":
    ["This script has the effect of giving the Target the given",
    "Type.",
    "If the Target has two Types already, they will be given a",
    "Third Type.",
    "If they have a Third Type already, it will be replaced with",
    "the new one."],

    "Script 3C":
    ["This script has the effect of setting the Embargo Global",
    "Flag for the given number of turns.",
    "The Embargo effect prevents the use of Items (held or from",
    "the Bag) while it is active."],

    "Script 3D":
    ["This script has the effect of setting the Heal Block Flag",
    "for the Target's side for the given number of turns.",
    "The Heal Block effect prevents the affected Pokemon from",
    "healing their HP."],

    "Script 3E":
    ["This script has the effect of healing the User's HP by 1/2",
    "of their maximum HP and to remove the given Type from them",
    "if they have it."],

    "Script 3F":
    ["This script has the effect of setting the Miracle Eye Flag",
    "on the Target for the given amount of turns.",
    "The Miracle Eye effect causes the Target's positive Evasion",
    "Stat Stages to be ignored and for Dark Types to lose their",
    "immunity to Psychic Type Moves."],

    "Script 40":
    ["This script has the effect of removing any and all",
    "Protection Flags from the Target.",
    "Protection Flags include Protect, King's Shield, Spiky",
    "Shield, Baneful Bunker, Max Guard, Obstruct, Silk Trap,",
    "Burning Bulwark, Mat Block, Quick Guard, Wide Guard, and",
    "Crafty Shield."],

    "Script 41":
    ["This script has the effect of setting the Reflect Flag on",
    "the Target's side for the given number of turns.",
    "The Reflect Flag boosts Defence for the affected Pokemon."],

    "Script 42":
    ["This script has the effect of removing the Target's Held",
    "Berry.",
    "The Berry may be eaten by the User or could be removed",
    "entirely without activating it."],

    "Script 43":
    ["This script has the effect of randomly raising one of the",
    "Target's Stat Stages by the given amount."],

    "Script 44":
    ["This script has the effect of transferring the User's Major",
    "Status to the Target.",
    "If the User does not have a Major Status, this script will",
    "fail."],

    "Script 45":
    ["This script has the effect of swapping the given raw Stats",
    "of the User."],

    "Script 46":
    ["This script has the effect of nullifying the Target's",
    "Ability."],

    "Script 47":
    ["This script is for the Move Me First.",
    "The Move Me First will use the Target's Move before they do",
    "with a slight damage boost."],

    "Script 48":
    ["This script is for the Move Copycat.",
    "The Move Copycat will cause the User to use the last Move to",
    "be used, Targeting a random Target."],

    "Script 49":
    ["This script has the effect of swapping the given Stat Stages",
    "between the User and the Target."],

    "Script 4A":
    ["This script has the effect of changing the Target's Ability",
    "to the one given.",
    "This will fail if the Target's Ability cannot be changed."],

    "Script 4B":
    ["This script has the effect of setting the Magnet Rise Flag",
    "on the Target for the given number of turns.",
    "The Magnet Rise effect makes the Target Ungrounded."],

    "Script 4C":
    ["This script has the effect of inflicting the given Status",
    "onto the Target and causing them to Flinch if the User moved",
    "first.",
     "The Status and Flinch effects both use the same Effect Chance",
     "value, but are activated independently of each other."],

    "Script 4D":
    ["This script has the effect of setting the Trick Room Global",
    "Flag for the given number of turns.",
    "The Trick Room effect makes it so that the slower Pokemon",
    "move before the faster ones."],

    "Script 4E":
    ["This script has the effect of setting the Max Guard Flag on",
    "the Target.",
    "The Max Guard effect blocks all Moves, including Max Moves."],

    "Script 4F":
    ["This script has the effect of setting the Substitute Flag on",
    "the Target.",
    "The Substitute Effect makes the Substitute take damage and",
    "blocks Status Moves until it fades."],

    "Script 50":
    ["This script has the effect of setting the Recharge Flag on",
    "the User.",
    "The Recharge effect makes the User skip their next turn",
    "after using the Move."],

    "Script 51":
    ["This script has the effect of setting the Rage Flag on the",
    "User.",
    "The Rage effect causes the User's Attack Stat Stages to rise",
    "by one every time they are hit when they use the Move",
    "multiple times in a row."],

    "Script 52":
    ["This script is for the Move Mimic.",
    "The Move Mimic temporarily copies the Move last used by the",
    "Target."],

    "Script 53":
    ["This script is for the Move Metronome.",
    "The Move Metronome calls a random other Move, which the User",
    "will use instead."],

    "Script 54":
    ["This script has the effect of setting the Leech Seed Flag on",
    "the Target.",
    "The Leech Seed effect causes the Seeded Target to lose HP",
    "and give it to the User."],

    "Script 55":
    ["This script has the effect of setting the Fell Stinger Flag",
    "on the User.",
    "The Fell Stinger Flag causes the given Stat Stage to rise by",
    "two, but only if the Move caused the Target to faint.",
    "If this is a Status Move, the Fell Stinger Flag will have no",
    "effect."],

    "Script 56":
    ["This script has the effect of setting the Disable Flag on",
    "the Target for the given number of turns.",
    "The Disable effect prevents the Target from selecting the",
    "last Move they used while the effect lasts."],

    "Script 57":
    ["This script has the effect of taking the average of the",
    "User's and the Target's given raw Stats and setting them all",
    "equal to the result."],

    "Script 58":
    ["This script has the effect of setting the Wonder Room Global",
    "Flag for the given number of turns.",
    "The Wonder Room effect swaps the raw Defence and Sp. Defence",
    "of all Pokemon on the field."],

    "Script 59":
    ["This script has the effect of setting the Telekinesis Flag",
    "on the Target for the given number of turns.",
    "The Telekinesis effect makes the Target Ungrounded and",
    "unable to evade Moves which Target them."],

    "Script 5A":
    ["This script has the effect of setting the Encore Flag on the",
    "Target for the given number of turns.",
    "The Encore effect makes the Target unable to select any",
    "Moves other than the one they last used."],

    "Script 5B":
    ["This script has the effect of raising the given Stat Stages",
    "by one for all Pokemon on the Target's side with either the",
    "Plus or Minus Ability."],

    "Script 5C":
    ["This script has the effect of setting the Magic Room Flag",
    "for the given number of turns.",
    "The Magic Room effect nullifies all Held Items for its",
    "duration."],

    "Script 5D":
    ["This script is for the Move Conversion 2.",
    "The Move Conversion 2 changes the User's Type to be",
    "resistant to the Move last used against them."],

    "Script 5E":
    ["This script has the effect of setting the Lock-On Flag on",
    "the given Target.",
    "The Lock-On effect makes any Moved used against the Target",
    "always hit."],

    "Script 5F":
    ["This script is for the Move Sketch.",
    "The Move Sketch permanently copies the last Move the Target",
    "used."],

    "Script 60":
    ["This script has the effect of making the Target Grounded."],

    "Script 61":
    ["This script is for the Move Sleep Talk.",
    "The Move Sleep Talk selects a random Move from the User's",
    "Move Set other than itself and uses it."],

    "Script 62":
    ["This script has the effect of setting the Destiny Bond Flag",
    "on the Target for the given number of turns.",
    "The Destiny Bond effect makes it so that if the Target",
    "faints, the Pokemon who knocked them out will faint after",
    "them."],

    "Script 63":
    ["This script has the effect of dealing recoil damage to the",
     "Target's Partner equal to the given percentage of their",
     "maximum HP, in addition to any damage dealt to the Target.",
     "If this is a Status Move, the damage to the Partner will",
     "still occur."],

    "Script 64":
    ["This script has the effect of lowering the Power Points of",
    "the last Move the Target used by the given amount."],

    "Script 65":
    ["This script has the effect of changing the Target's Type to",
    "the one given.",
    "This script will make the Target a Mono-Type if they were",
    "not already, however it will not affect Third Types."],

    "Script 66":
    ["This script has the effect of healing the User's entire",
    "party of all Major Statuses (and Confusion)."],

    "Script 67":
    ["This script is for the Move After You.",
    "The Move After You forces the Target to Move immediately",
    "after the User, ignoring the previous turn order or",
    "Priority."],

    "Script 68":
    ["This Script is for the Move Round.",
    "If multiple Pokemon have selected the Move Round, they will",
    "all use their Move one after the other, ignoring the",
    "previous turn order."],

    "Script 69":
    ["This script has the effect of either giving the Target the",
    "User's Held Item, if they have none, or taking the Target's",
    "Held Item and giving it to the User, if they have none."],

    "Script 6A":
    ["This script has the effect of setting the Trap Flag on the",
    "Target and any additional targets given.",
    "The Flag will disappear when any of the affected Pokemon",
    "switch out or faint."],

    "Script 6B":
    ["This script has the effect of setting the Nightmare Flag on",
    "the Target.",
    "The Nightmare effect, which only works if the Target is",
    "Asleep, deals damage at the end of the turn."],

    "Script 6C":
    ["This script has the effect of raising the Target's Evasion",
    "by the given amount and setting the Minimise Flag.",
    "The Minimise effect makes the Target more susceptible to",
    "certain Moves."],

    "Script 6D":
    ["This script does something different if the User is a Ghost",
    "Type.\n",
    "If the User is a Ghost Type, this script will set the Curse",
    "Flag on the opponent at the cost of 1/4 of the User's HP.",
    "The Curse effect makes the Target take damage at the end of",
    "the turn.\n",
    "If the User is not a Ghost Type, this script will raise",
    "their Attack and Defence by one Stat Stage each and lower",
    "their Speed by one Stat Stage."],

    "Script 6E":
    ["This script is for the Move Echoed Voice.",
    "The Move Echoed Voice does more damage when it is used by at",
    "least one Pokemon on the field per turn."],

    "Script 6F":
    ["This script has the effect of setting the Protect Flag on",
    "the Target.",
    "The Protect Flag blocks all Moves, except for those which",
    "can bypass Protect."],

    "Script 70":
    ["This script has the effect of setting the given Entry",
    "Hazard.",
    "An Entry Hazard affects a Pokemon when they first switch",
    "into the Battle Dimension."],

    "Script 71":
    ["This script has the effect of setting the Foresight Flag on",
    "the Target.",
    "The Foresight effect ignores the Target's positive Evasion",
    "Stat Stages and causes Ghost Types to lose their Type",
    "Immunities."],

    "Script 72":
    ["This script has the effect of setting the Perish Song Flag",
    "on the Target for the given number of turns.",
    "The Perish Song effect causes the Target to faint when the",
    "effect expires."],

    "Script 73":
    ["This script has the effect of setting the given Weather for",
    "five turns."],

    "Script 74":
    ["This script has the effect of setting the Endure Flag on the",
    "Target.",
    "The Endure effect causes a hit that would otherwise knock",
    "out the Target to leave them with one HP instead."],

    "Script 75":
    ["This script is for a Momentum Move.",
    "A Momentum Move is a Move which prevents the User from",
    "selecting another Move once it is used for five turns.",
    "Each turn that the Move hits, it will deal more damage."],

    "Script 76":
    ["This script has the effect of raising the Target's given",
    "Stat Stage by two, as well as Confusing them."],

    "Script 77":
    ["This script is for the Move Fury Cutter.",
    "The Move Fury Cutter increases its damage when it is used on",
    "consecutive turns."],

    "Script 78":
    ["This script has the effect of Infatuating the Target.",
    "An Infatuated Target has a 50% chance of having their attack",
    "Cancelled as long as the Pokemon they are in love with",
    "remains on the field."],

    "Script 79":
    ["This script has the effect of setting the Ally Switch Flag",
    "on the Target's side.",
    "The Ally Switch effect makes it so that attacks aimed at one",
    "Pokemon will hit their Partner instead."],

    "Script 7A":
    ["This script has the effect of raising the Target's Attack,",
    "Sp. Attack and Speed by two Stat Stages, while lowering",
    "their Defence and Sp. Defence by one Stat Stage."],

    "Script 7B":
    ["This script is for the Move Quash.",
    "The Move Quash forces the Target to move last during that",
    "turn, ignoring Priority."],

    "Script 7C":
    ["This script has the effect of setting the Safeguard Flag on",
    "the Target's side for the given number of turns.",
    "The Safeguard effect prevents the Target from being",
    "inflicted with Major Statuses or Confusion by opponents."],

    "Script 7D":
    ["This script has the effect of thawing out the User if they",
    "are Frozen before the Move is used.",
    "Optionally, this script may also have the effect of thawing",
    "out the Target if they are Frozen."],

    "Script 7E":
    ["This script has the effect of making the User have the same",
    "Types as the Target.",
    "This includes Third Types."],

    "Script 7F":
    ["This script has the effect of raising the Attack and Sp.",
     "Attack Stat Stages of the Target by one if they are the",
     "given Type (Third Types count) and Grounded."],

    "Script 80":
    ["This script has the effect of lowering the Target's given",
    "Stat Stages by one and then switching the User out if they",
    "are able to do so.",
    "The User will still switch out even if the Stat Stages are",
    "not successfully lowered."],

    "Script 81":
    ["This script has the effect of removing all Entry Hazards",
    "from the User's side of the field."],

    "Script 82":
    ["This script has the effect of removing all Entry Hazards",
    "from both sides of the field and lowering the Target's",
    "Evasion Stat Stages by one.",
    "Screen Moves, Mist and Safeguard are also removed from the",
    "Target's side only."],

    "Script 83":
    ["This script has the effect of inverting the Target's Stat",
    "Stages, so that positive changes are now negative and vice",
    "versa."],

    "Script 84":
    ["This script has the effect of setting the Crafty Shield Flag",
    "on the Target's side.",
    "The Crafty Shield effect blocks almost all Single-Target",
    "Status Moves used by opponents."],

    "Script 85":
    ["This script has the effect of raising the given Stat Stage",
    "by one for the Target if they are the given Type."],

    "Script 86":
    ["This script has the effect of setting the Fairy Lock Global",
    "Flag for the given number of turns.",
    "The Fairy Lock effect prevents Pokemon from switching out."],

    "Script 87":
    ["This script has the effect of setting the King's Shield Flag",
    "on the Target.",
    "The King's Shield effect blocks all Damaging Moves.",
    "If the Move blocked is a Direct-Contact Move, the attacker's",
    "Attack is lowered by one Stat Stage."],

    "Script 88":
    ["This script has the effect of giving the Target the given",
     "Major Status, but only if their Stat Stages were raised",
     "during the current turn."],

    "Script 89":
    ["This script has the effect of setting the Spiky Shield Flag",
    "on the Target.",
    "The Spiky Shield effect blocks all Moves.",
    "If the blocked Move makes Direct Contact, the attacker will",
    "take damage equal to 1/8th of their maximum HP."],

    "Script 8A":
    ["This script has the effect of setting the Dragon Cheer Flag",
    "on the Target.",
    "The Dragon Cheer effect raises the Target's Critical Hit",
    "ratio.",
    "This does not stack with Focus Energy."],

    "Script 8B":
    ["This script has the effect of displaying a string of text",
    "and nothing else."],

    "Script 8C":
    ["This script has the effect of raising all of the Target's",
    "given Stat Stages by one."],

    "Script 8D":
    ["This script has the effect of lowering all of the Target's",
    "given Stat Stages by one."],

    "Script 8E":
    ["This script has the effect of maximising the given Stat",
    "Stage for the Target, at the cost of 1/2 of their maximum",
    "HP."],

    "Script 8F":
    ["This script has the effect of copying the Target's current",
    "Stat Stages."],

    "Script 90":
    ["This script has the effect of raising the Target's Partner's",
    "given Stat Stage by one."],

    "Script 91":
    ["This script has the effect of setting the Powder Flag on the",
    "Target for the given number of turns.",
    "The Powder effect causes the Target to take damage when they",
    "attempt to use a Fire Type Move.",
    "The Move will not fully execute if this happens."],

    "Script 92":
    ["This script has the effect of raising the Target's given",
    "Stat Stages by two."],

    "Script 93":
    ["This script has the effect of lowering the Target's given",
    "Stat Stages by two."],

    "Script 94":
    ["This script has the effect of setting the Baneful Bunker",
    "Flag on the Target.",
    "The Baneful Bunker effect blocks all Moves.",
    "If the Blocked Move makes Direct Contact, the attacker will",
    "be Poisoned."],

    "Script 95":
    ["This script has the effect of lowering the Target's given",
    "Stat Stage by one, then healing the User's HP by an amount",
    "equal to the Target's effective given Stat (the raw Stat +",
    "Stat Stages)."],

    "Script 96":
    ["This script has the effect of setting the Burning Bulwark",
    "Flag on the Target.",
    "The Burning Bulwark effect blocks Damaging Moves.",
    "If the blocked Move would have made Direct Contact, the",
    "attacker becomes Burned."],

    "Script 97":
    ["This script has the effect of lowering the given Stat Stage",
    "by one if the Target has the given Status."],

    "Script 98":
    ["This script has the effect of setting the Laser Focus Flag",
    "on the Target for the given number of turns.",
    "The Laser Focus effect causes the Pokemon's Moves to always",
    "be Critical Hits."],

    "Script 99":
    ["This script has the effect of setting the Throat Chop Flag",
    "on the Target for the given number of turns."],

    "Script 9A":
    ["This script is for the Move Beat Up.",
    "The Move Beat Up is a Multi-Hit Move which hits once for",
    "each party member on the User's team."],

    "Script 9B":
    ["This script has the effect of curing the User of the given",
     "Major Status if they have the given Type, at the cost of",
     "removing that Type from them afterwards."],

    "Script 9C":
    ["This script has the effect of raising the Target's Defence",
    "by one Stat Stage and setting the Defence Curl Flag on the",
    "Target.",
    "The Defence Curl Flag causes Momentum Moves to deal more",
    "damage."],

    "Script 9D":
    ["This script has the effect of healing the Target's HP based",
    "on the given formula."],

    "Script 9E":
    ["This script has the effect of changing the Weather to the",
    "given one and switching out the Target."],

    "Script 9F":
    ["This script has the effect of setting the Uproar Global Flag",
    "for the given number of turns.",
    "The Uproar effect prevents Pokemon from falling Asleep."],

    "Script A0":
    ["This script has the effect of setting the Stockpile Flag for",
    "the Target.",
    "The Stockpile effect allows the User to use Swallow and Spit",
    "Up."],

    "Script A1":
    ["This script has the effect of healing all Major Statuses",
    "from the Target and healing up to 1/2 of their maximum HP."],

    "Script A2":
    ["This script has the effect of creating a Substitute for the",
    "Target and then switching them out, leaving the new Pokemon",
    "with the Substitute."],

    "Script A3":
    ["This script has the effect of making the User use the Move",
    "that the Target used most recently."],

    "Script A4":
    ["This script has the effect of setting the Beak Blast Flag.",
    "The Beak Blast effect causes all Pokemon who make Direct",
    "Contact with the User to become Burned."],

    "Script A5":
    ["This script has the effect of setting the Torment Flag on",
    "the Target.",
    "The Torment effect causes the Target to be unable to select",
    "the same Move twice in a row."],

    "Script A6":
    ["This script has the effect of setting a Shell Trap at the",
    "beginning of the turn.",
    "If another Pokemon hits the User, they will use their actual",
    "Move, otherwise they will do nothing."],

    "Script A7":
    ["This script has the effect of causing the User to faint in",
    "exchange for fully healing the Pokemon who replaces them."],

    "Script A8":
    ["This script has the effect of causing the User to faint in",
     "exchange for lowering the Target's given Stat Stages by two",
     "each."],

    "Script A9":
    ["This script has the effect of transferring either the",
    "positive or negative Stat Stages from either User to Target",
    "or Target to User.",
    "The donor Target's Stat Stages will then be reset.",
    "If this is a Damaging Move, this effect will happen before",
    "dealing Damage."],

    "Script AA":
    ["This script has the effect of dealing recoil damage to the",
    "User equal the given percentage of their maximum HP."],

    "Script AB":
    ["This script has the effect of curing the Target of the given",
    "Status."],

    "Script AC":
    ["This script has the effect of setting the given Target",
    "Redirection Flag on the Target."],

    "Script AD":
    ["This script is for the Move Nature Power.",
    "The Move Nature Power calls a different Move depending on",
    "the Terrain (not the Global Flag)."],

    "Script AE":
    ["This script has the effect of setting the Charge Flag on the",
    "Target for the given number of turns.",
    "The Charge effect powers up the User's Electric Type Moves."],

    "Script AF":
    ["This script has the effect of setting the Taunt Flag on the",
    "Target for the given number of turns.",
    "The Taunt effect causes the Target to be unable to select",
    "Status Moves."],

    "Script B0":
    ["This script has the effect of setting the Helping Hand Flag",
    "on the Target's Partner for the given number of turns.",
    "The Helping Hand effect increases the damage that the",
    "Target's Partner will do."],

    "Script B1":
    ["This script has the effect of swapping the User's and",
    "Target's Held Items.",
    "This will fail if either Pokemon's Held Items cannot be",
    "changed."],

    "Script B2":
    ["This script has the effect of copying the Target's Ability",
     "to the User or vice versa.",
     "There is also the option of copying the Ability to the",
     "recipient's Partner too."],

    "Script B3":
    ["This script has the effect of causing the Wish effect to",
     "happen in the given number of turns.",
    "The Move Wish heals the Target's HP at the end of the next",
    "turn."],

    "Script B4":
    ["This script has the effect of randomly using a Move that the",
    "one of the User's party members knows."],

    "Script B5":
    ["This script has the effect of setting the Ingrain Flag on",
    "the Target.",
    "The Ingrain effect heals a bit of HP at the end of the turn,",
    "but prevents the Target from switching out."],

    "Script B6":
    ["This script has the effect of setting the Aqua Ring Flag on",
    "the Target.",
    "The Aqua Ring effect heals a bit of HP at the end of the",
    "turn."],

    "Script B7":
    ["This script has the effect of setting the Magic Coat Flag on",
    "the Target for the given number of turns.",
    "The Magic Coat effect causes certain Moves used against the",
    "Pokemon to be reflected back at the attacker."],

    "Script B8":
    ["This script is for the Move Recycle.",
    "The Move Recycle restores a Consumable Held Item that the",
    "User has previously used."],

    "Script B9":
    ["This script has the effect of setting the Plasma Fists",
    "Global Flag with the given Type.",
    "The Plasma Flag turns all Normal Type Moves into the",
    "given Type Moves for the remainder of the turn."],

    "Script BA":
    ["This script has the effect of removing Screen effects (Light",
    "Screen, Reflect, Aurora Veil) from the Target's side of the",
    "field."],

    "Script BB":
    ["This script has the effect of making the Target Drowsy.",
    "A Drowsy Pokemon will fall Asleep at the end of the next",
    "turn."],

    "Script BC":
    ["This script has the effect of removing the Target's Held",
    "Item for the remainder of the battle."],

    "Script BD":
    ["This script has the effect of removing any and all Terrain",
    "Global Flags."],

    "Script BE":
    ["This script has the effect of setting the Syrup Bomb Flag on",
    "the Target for the given number of turns.",
    "The Syrup Bomb effect lowers the Target's Speed by one Stat",
    "Stage at the end of the turn."],

    "Script BF":
    ["This script has the effect of swapping the User's and the",
    "Target's Abilities.",
    "This will fail if either Pokemon's Ability cannot be",
    "changed."],

    "Script C0":
    ["This script has the effect of setting the Imprison Flag on",
    "the Target with the given Targets.",
    "The Imprison effect makes it so that other Pokemon cannot",
    "select Moves that the given Targets also know."],

    "Script C1":
    ["This script has the effect of raising the Target's given",
    "Stat Stage by two and removing their Held Berry, activating",
    "its effect."],

    "Script C2":
    ["This script has the effect of setting the Grudge Flag on the",
    "Target for the given number of turns.",
    "The Grudge effect makes it so that if the Target faints, the",
    "Pokemon who knocked them out will lose all the Power Points",
    "for the Move they used."],

    "Script C3":
    ["This script has the effect of setting the Snatch Flag on the",
    "Target.",
    "The Snatch Flag makes it so that if an opponent uses a Move",
    "with the Snatch Flag set, the Target will steal the Move for",
    "themselves."],

    "Script C4":
    ["This script has the effect of lowering the Target's given",
    "Stat Stage by one and awarding them a certain amount of",
    "money."],

    "Script C5":
    ["This script is for the Move Secret Power.",
    "The Move Secret Power has a different additional effect",
    "depending on the Terrain."],

    "Script C6":
    ["This script has the effect of raising the Target's given",
    "Stat Stages by one and setting the Trap Flag for the User."],

    "Script C7":
    ["This script has the effect of lowering the Target's given",
    "Stat by one Stat Stage and setting the Tar Shot Flag.",
    "The Tar Shot effect doubles the effectiveness of Moves used",
    "against the Target."],

    "Script C8":
    ["This script has the effect of causing all Targets to eat",
    "their Held Berry and activate its effect."],

    "Script C9":
    ["This script has the effect of setting the Mud Sport Global",
    "Flag for the given number of turns.",
    "The Mud Sport effect weakens Electric Types Moves."],

    "Script CA":
    ["This script has the effect of setting the Octolock Flag on",
    "the Target.",
    "The Octolock effect traps the Target and lowers their",
    "Defence and Sp. Defence by one Stat Stage at the end of the",
    "turn, until the Pokemon who set the Flag switches out."],

    "Script CB":
    ["This script has the effect of causing certain Flags to",
    "switch sides.",
    "Flags affected including Screens, Mist, Safeguard, Entry",
    "Hazards and Pledge Moves."],

    "Script CC":
    ["This script has the effect of lowering both the Target's and",
    "their Partner's given Stat Stage by one.",
    "If the Move is a Damaging Move, only the Target will be",
    "damaged, not their Partner."],

    "Script CD":
    ["This script has the effect of raising both the Target's and",
    "their Partner's given Stat Stage by one.",
    "If the Move is a Damaging Move, only the Target will be",
    "damaged, not their Partner."],

    "Script CE":
    ["This script has the effect of raising the Target's given",
    "Stat Stages by one at the cost of 1/3rd of the Target's",
    "maximum HP."],

    "Script CF":
    ["This script has the effect of raising the Target's Attack",
    "and Sp. Attack by one when the Weather is clear and by two",
    "in the given Weather."],

    "Script D0":
    ["This script has the effect of setting the Obstruct Flag on",
    "the given Target.",
    "The Obstruct effect blocks Damaging Moves.",
    "If the Move would have made Direct Contact, the attacker's",
    "Defence will decrease by two Stat Stages."],

    "Script D1":
    ["This script has the effect of raising the Target's given",
    "Stat Stages by one and removes Substitutes and Entry Hazards",
    "from all Pokemon (not just the Target)."],

    "Script D2":
    ["This script has the effect of setting the Water Sport Global",
    "Flag for the given number of turns.",
    "The Water Sport effect weakens Fire Type Moves."],

    "Script D3":
    ["This script has the effect of raising the Target's Partner's",
    "given Stat Stages by one.",
    "If the Move is a Damaging Move, only the Target will be",
    "damaged, not their Partner."],

    "Script D4":
    ["This script has the effect of lowering the Target's",
    "Partner's given Stat Stages by one.",
    "If the Move is a Damaging Move, only the Target will be",
    "damaged, not their Partner."],

    "Script D5":
    ["This script has the effect of turning the Target to a single",
    "Type, which depends on the current Terrain."],

    "Script D6":
    ["This script has the effect of healing the Target's HP based",
    "on the given formula, as well as curing any Major Statuses",
    "the Target has."],

    "Script D7":
    ["This script has the effect of lowering the Target's given",
    "Stat Stages by one.",
    "This script also has a fixed 30% chance of causing the",
    "Target to Flinch."],

    "Script D8":
    ["This script has the effect of raising the Target's given",
    "Stat Stages by one and healing any Major Status conditions",
    "they may have."],

    "Script D9":
    ["This script has the effect of setting the Silk Trap Flag on",
    "the Target.",
    "The Silk Trap effect blocks Damaging Moves.",
    "If the Move makes Direct Contact, then the attacker's Speed",
    "is lowered by one Stat Stage."],

    "Script DA":
    ["This script has the effect of raising the Target's Attack by",
    "two Stat Stages, but lowering their Defence by two Stat",
    "Stages."],

    "Script DB":
    ["This script has the effect of setting the Glaive Rush Flag",
    "on the Target.",
    "The Glaive Rush effect causes Moves directed at the Target",
    "to bypass Accuracy checks and to deal double damage."],

    "Script DC":
    ["This script has the effect of reviving a chosen Pokemon from",
    "the Target's party."],

    "Script DD":
    ["This script has the effect of setting the Salt Cure Flag on",
    "the Target.",
    "The Salt Cure effect deals damage to the Target at the end",
    "of the turn until they switch out.",
    "If the Target is a Water or Steel Type, the damage is",
    "higher."],

    "Script DE":
    ["This script has the effect of removing the Wrap Flag, Leech",
    "Seed and Entry Hazards from the User's side of the field, in",
    "addition to giving the Target the given Major Status."],

    "Script DF":
    ["This script has the effect of raising the Target's given",
    "Stat Stage by two at the cost of 1/2 of their maximum HP."],

    "Script E0":
    ["This script is unused by default in ACE."],

    "Script E1":
    ["This script is unused by default in ACE."],

    "Script E2":
    ["This script is unused by default in ACE."],

    "Script E3":
    ["This script is unused by default in ACE."],

    "Script E4":
    ["This script is unused by default in ACE."],

    "Script E5":
    ["This script is unused by default in ACE."],

    "Script E6":
    ["This script is unused by default in ACE."],

    "Script E7":
    ["This script is unused by default in ACE."],

    "Script E8":
    ["This script is unused by default in ACE."],

    "Script E9":
    ["This script is unused by default in ACE."],

    "Script EA":
    ["This script is unused by default in ACE."],

    "Script EB":
    ["This script is unused by default in ACE."],

    "Script EC":
    ["This script is unused by default in ACE."],

    "Script ED":
    ["This script is unused by default in ACE."],

    "Script EE":
    ["This script is unused by default in ACE."],

    "Script EF":
    ["This script is unused by default in ACE."],

    "Script F0":
    ["This script is unused by default in ACE."],

    "Script F1":
    ["This script is unused by default in ACE."],

    "Script F2":
    ["This script is unused by default in ACE."],

    "Script F3":
    ["This script is unused by default in ACE."],

    "Script F4":
    ["This script is unused by default in ACE."],

    "Script F5":
    ["This script is unused by default in ACE."],

    "Script F6":
    ["This script is unused by default in ACE."],

    "Script F7":
    ["This script is unused by default in ACE."],

    "Script F8":
    ["This script is unused by default in ACE."],

    "Script F9":
    ["This script is unused by default in ACE."],

    "Script FA":
    ["This script is unused by default in ACE."],

    "Script FB":
    ["This script is unused by default in ACE."],

    "Script FC":
    ["This script is unused by default in ACE."],

    "Script FD":
    ["This script is unused by default in ACE."],

    "Script FE":
    ["This script is unused by default in ACE."],

    "Script FF":
    ["This script is unused by default in ACE."]}

# ------------------------------------------------------------
# Move Script Tags - Used in the search bar
# ------------------------------------------------------------

MoveScriptTagsList = {"Script 00": ["base"],
                      "Script 01": ["sleep"],
                      "Script 02": ["poison"],
                      "Script 03": ["absorb"],
                      "Script 04": ["burn"],
                      "Script 05": ["freeze"],
                      "Script 06": ["paralysis"],
                      "Script 07": ["explosion", "self-destruct", "faint"],
                      "Script 08": ["double shock"],
                      "Script 09": ["mirror move", "calling move"],
                      "Script 0A": ["swords dance", "raise"],
                      "Script 0B": ["iron defence", "harden", "raise"],
                      "Script 0C": ["agility", "raise"],
                      "Script 0D": ["raise"],
                      "Script 0E": ["amnesia", "raise"],
                      "Script 0F": ["raise"],
                      "Script 10": ["double team", "raise"],
                      "Script 11": ["gravity", "global"],
                      "Script 12": ["lower"],
                      "Script 13": ["lower"],
                      "Script 14": ["string shot", "scary face", "lower"],
                      "Script 15": ["lower"],
                      "Script 16": ["lower"],
                      "Script 17": ["smokescreen", "lower"],
                      "Script 18": ["lower"],
                      "Script 19": ["haze", "clear smog"],
                      "Script 1A": ["bide"],
                      "Script 1B": ["thrash", "outrage", "petal dance"],
                      "Script 1C": ["whirlwind", "baton pass", "switch"],
                      "Script 1D": ["multi hit", "multi-hit"],
                      "Script 1E": ["conversion"],
                      "Script 1F": ["flinch"],
                      "Script 20": ["absorb", "matcha gotcha"],
                      "Script 21": ["toxic"],
                      "Script 22": ["pay day", "happy hour"],
                      "Script 23": ["light screen", "team flag", "screen"],
                      "Script 24": ["tri-attack", "tri attack"],
                      "Script 25": ["rest", "restore"],
                      "Script 26": ["shift gear", "raise"],
                      "Script 27": ["electrify"],
                      "Script 28": ["venom drench"],
                      "Script 29": ["teleport"],
                      "Script 2A": ["wrap", "bind", "fire spin", "whirlpool", "sand tomb"],
                      "Script 2B": ["ion deluge", "global"],
                      "Script 2C": ["grassy", "misty", "electric", "psychic"],
                      "Script 2D": ["autotomise"],
                      "Script 2E": ["mist", "team flag"],
                      "Script 2F": ["focus energy"],
                      "Script 30": ["take down", "double-edge"],
                      "Script 31": ["confuse", "confusion", "teeter dance"],
                      "Script 32": ["future sight", "doom desire"],
                      "Script 33": ["volt tackle"],
                      "Script 34": ["aurora veil", "team flag", "screen"],
                      "Script 35": ["tailwind", "team flag"],
                      "Script 36": ["quick guard", "team flag", "protect"],
                      "Script 37": ["wide guard", "team flag", "protect"],
                      "Script 38": ["mat block", "team flag", "protect"],
                      "Script 39": ["transform"],
                      "Script 3A": ["lucky chant", "team flag"],
                      "Script 3B": ["trick or treat", "forest's curse", "add type"],
                      "Script 3C": ["embargo", "ban items"],
                      "Script 3D": ["heal block", "ban healing"],
                      "Script 3E": ["roost", "restore"],
                      "Script 3F": ["miracle eye"],
                      "Script 40": ["feint", "hyperspace hole"],
                      "Script 41": ["reflect"],
                      "Script 42": ["bug bite", "pluck", "incinerate"],
                      "Script 43": ["acupressure"],
                      "Script 44": ["psycho shift"],
                      "Script 45": ["power trick", "power shift", "speed swap"],
                      "Script 46": ["gastro acid"],
                      "Script 47": ["me first"],
                      "Script 48": ["copycat", "calling move"],
                      "Script 49": ["power swap", "guard swap", "heart swap"],
                      "Script 4A": ["worry seed", "simple beam", "entrainment"],
                      "Script 4B": ["magnet rise"],
                      "Script 4C": ["ice fang", "fire fang", "thunder fang"],
                      "Script 4D": ["trick room", "turn order", "global"],
                      "Script 4E": ["max guard", "protect"],
                      "Script 4F": ["substitute"],
                      "Script 50": ["hyper beam"],
                      "Script 51": ["rage"],
                      "Script 52": ["mimic", "alter moves"],
                      "Script 53": ["metronome", "calling move"],
                      "Script 54": ["leech seed"],
                      "Script 55": ["fell stinger"],
                      "Script 56": ["disable"],
                      "Script 57": ["power split", "guard split"],
                      "Script 58": ["wonder room", "global"],
                      "Script 59": ["telekinesis"],
                      "Script 5A": ["encore"],
                      "Script 5B": ["pain split"],
                      "Script 5C": ["magic room", "ban items", "global"],
                      "Script 5D": ["conversion 2"],
                      "Script 5E": ["Lock-On"],
                      "Script 5F": ["sketch", "alter moves"],
                      "Script 60": ["smack down", "thousand arrows", "grounded"],
                      "Script 61": ["sleep talk", "calling move"],
                      "Script 62": ["destiny bond"],
                      "Script 63": ["flame burst", "recoil"],
                      "Script 64": ["spite"],
                      "Script 65": ["soak", "magic powder"],
                      "Script 66": ["aromatherapy", "heal bell"],
                      "Script 67": ["after you", "turn order"],
                      "Script 68": ["round", "turn order"],
                      "Script 69": ["thief", "bestow"],
                      "Script 6A": ["mean look", "block"],
                      "Script 6B": ["nightmare", "sleep"],
                      "Script 6C": ["minimise", "miminize", "raise"],
                      "Script 6D": ["curse", "raise", "ghost", "lower"],
                      "Script 6E": ["echoed voice", "formula"],
                      "Script 6F": ["protect", "detect"],
                      "Script 70": ["spikes", "toxic spikes", "stealth rock", "sticky web", "steelsurge"],
                      "Script 71": ["foresight"],
                      "Script 72": ["perish song"],
                      "Script 73": ["weather", "sunny day", "rain dance", "sandstorm", "hail"],
                      "Script 74": ["endure", "protect"],
                      "Script 75": ["rollout", "ice ball", "formula"],
                      "Script 76": ["raise", "confuse", "confusion", "swagger", "flatter"],
                      "Script 77": ["fury cutter"],
                      "Script 78": ["infatuate", "infatuation", "attract"],
                      "Script 79": ["ally switch", "team flag", "redirection"],
                      "Script 7A": ["raise", "shell smash", "lower"],
                      "Script 7B": ["quash", "turn order"],
                      "Script 7C": ["safeguard", "team flag"],
                      "Script 7D": ["flame wheel", "scald"],
                      "Script 7E": ["reflect type"],
                      "Script 7F": ["rototiller", "raise"],
                      "Script 80": ["parting shot", "lower", "switch"],
                      "Script 81": ["rapid spin"],
                      "Script 82": ["defog", "lower"],
                      "Script 83": ["topsy turvy"],
                      "Script 84": ["crafty shield", "protect", "team flag"],
                      "Script 85": ["flower shield", "raise"],
                      "Script 86": ["fairy lock", "global"],
                      "Script 87": ["king's shield", "protect"],
                      "Script 88": ["alluring voice", "burning jealousy"],
                      "Script 89": ["spiky shield", "protect"],
                      "Script 8A": ["dragon cheer"],
                      "Script 8B": ["splash", "celebrate", "hold hands"],
                      "Script 8C": ["raise", "ancientpower"],
                      "Script 8D": ["lower"],
                      "Script 8E": ["belly drum", "raise"],
                      "Script 8F": ["psych up"],
                      "Script 90": ["aromatic mist", "coaching"],
                      "Script 91": ["powder"],
                      "Script 92": ["raise"],
                      "Script 93": ["lower"],
                      "Script 94": ["baneful bunker", "protect"],
                      "Script 95": ["strength sap", "restore"],
                      "Script 96": ["burning bulwark", "protect"],
                      "Script 97": ["toxic thread"],
                      "Script 98": ["laser focus"],
                      "Script 99": ["throat chop"],
                      "Script 9A": ["beat up", "multi-hit", "multi hit"],
                      "Script 9B": ["burn up", "restore"],
                      "Script 9C": ["defence curl", "raise"],
                      "Script 9D": ["recover", "restore"],
                      "Script 9E": ["chilly reception", "weather", "switch"],
                      "Script 9F": ["uproar", "global"],
                      "Script A0": ["stockpile"],
                      "Script A1": ["purify", "restore"],
                      "Script A2": ["shed tail", "switch"],
                      "Script A3": ["instruct", "calling move"],
                      "Script A4": ["beak blast"],
                      "Script A5": ["torment"],
                      "Script A6": ["shell trap"],
                      "Script A7": ["healing wish", "lunar dance", "faint", "restore"],
                      "Script A8": ["memento", "faint", "lower"],
                      "Script A9": ["spectral thief"],
                      "Script AA": ["mind blown", "steel beam", "chloroblast", "recoil"],
                      "Script AB": ["smellingsalts", "refresh", "wake-up slap", "sparkling aria"],
                      "Script AC": ["follow me", "spotlight", "rage powder", "redirection"],
                      "Script AD": ["nature power", "calling move"],
                      "Script AE": ["charge"],
                      "Script AF": ["taunt"],
                      "Script B0": ["helping hand", "double battle"],
                      "Script B1": ["trick", "swap"],
                      "Script B2": ["role play", "doodle"],
                      "Script B3": ["wish", "restore", "future"],
                      "Script B4": ["assist", "calling move"],
                      "Script B5": ["ingrain"],
                      "Script B6": ["aqua ring"],
                      "Script B7": ["magic coat"],
                      "Script B8": ["recycle"],
                      "Script B9": ["plasma fists"],
                      "Script BA": ["brick break", "psychic fangs", "raging bull"],
                      "Script BB": ["drowsy"],
                      "Script BC": ["knock off"],
                      "Script BD": ["steel roller", "ice spinner"],
                      "Script BE": ["syrup bomb"],
                      "Script BF": ["skill swap"],
                      "Script C0": ["imprison"],
                      "Script C1": ["stuff cheeks"],
                      "Script C2": ["grudge"],
                      "Script C3": ["snatch"],
                      "Script C4": ["make it rain"],
                      "Script C5": ["secret power"],
                      "Script C6": ["no retreat"],
                      "Script C7": ["tar shot"],
                      "Script C8": ["teatime"],
                      "Script C9": ["mud sport", "global"],
                      "Script CA": ["octolock"],
                      "Script CB": ["court change"],
                      "Script CC": ["max phantasm", "lower", "double battle"],
                      "Script CD": ["max knuckle", "raise", "double battle"],
                      "Script CE": ["clangorous soul", "raise"],
                      "Script CF": ["growth", "raise"],
                      "Script D0": ["obstruct", "protect"],
                      "Script D1": ["tidy up"],
                      "Script D2": ["water spot", "global"],
                      "Script D3": ["raise", "double battle"],
                      "Script D4": ["lower", "double battle"],
                      "Script D5": ["camouflage"],
                      "Script D6": ["jungle healing", "lunar blessing", "restore"],
                      "Script D7": ["triple arrows", "lower"],
                      "Script D8": ["take heart", "raise"],
                      "Script D9": ["silk trap", "protect"],
                      "Script DA": ["spicy extract"],
                      "Script DB": ["glaive rush"],
                      "Script DC": ["revival blessing"],
                      "Script DD": ["salt cure"],
                      "Script DE": ["mortal spin"],
                      "Script DF": ["fillet away"],
                      "Script E0": [""],
                      "Script E1": [""],
                      "Script E2": [""],
                      "Script E3": [""],
                      "Script E4": [""],
                      "Script E5": [""],
                      "Script E6": [""],
                      "Script E7": [""],
                      "Script E8": [""],
                      "Script E9": [""],
                      "Script EA": [""],
                      "Script EB": [""],
                      "Script EC": [""],
                      "Script ED": [""],
                      "Script EE": [""],
                      "Script EF": [""],
                      "Script F0": [""],
                      "Script F1": [""],
                      "Script F2": [""],
                      "Script F3": [""],
                      "Script F4": [""],
                      "Script F5": [""],
                      "Script F6": [""],
                      "Script F7": [""],
                      "Script F8": [""],
                      "Script F9": [""],
                      "Script FA": [""],
                      "Script FB": [""],
                      "Script FC": [""],
                      "Script FD": [""],
                      "Script FE": [""],
                      "Script FF": [""]}

DamageFormulaTagsList = {"Formula 00": ["base"],
                         "Formula 01": ["set damage", "level", "night shade", "seismic toss"],
                         "Formula 02": ["return", "frustration"],
                         "Formula 03": ["eruption", "water spout", "flail", "reversal",
                                        "wring out", "crush grip", "hard press"],
                         "Formula 04": ["dragon rage", "sonicboom"],
                         "Formula 05": ["low kick", "grass knot", "heat crash", "heavy slam"],
                         "Formula 06": ["gyro ball", "electro ball"],
                         "Formula 07": ["psywave", "magnitude", "triple kick", "rollout",
                                        "fury cutter", "present", "beat up", "spit up",
                                        "endeavour", "trump card", "round", "echoed voice",
                                        "last respects", "rage fist", "fickle beam", "temper flare"],
                         "Formula 08": ["punishment", "stored power"],
                         "Formula 09": ["super fang", "guardian of alola", "nature's madness",
                                        "final gambit", "ruination"],
                         "Formula 0A": ["fling", "natural gift"],
                         "Formula 0B": ["counter", "mirror coat", "metal burst", "comeuppance",
                                        "bide"],
                         "Formula 0C": ["z move", "max move"],
                         "Formula 0D": [""],
                         "Formula 0E": [""],
                         "Formula 0F": [""]}

# ------------------------------------------------------------
# Damage Formula Text - Same as for Move Scripts
# ------------------------------------------------------------
DamageFormulaText = {
    "Formula 00":
    ["This Damage Formula set the Base Power equal to its value in",
    "the Attack Data Table and does not apply any additional",
    "effects to it."],

    "Formula 01":
    ["This Damage Formula sets the amount of Damage equal to the",
    "given Pokemon's Level."],

    "Formula 02":
    ["This Damage Formula sets the Base Power differently",
    "depending on the Friendship Points that the given Pokemon",
    "has."],

    "Formula 03":
    ["This Damage Formula sets the Base Power differently",
    "depending on the amount of HP the given Pokemon has",
    "remaining."],

    "Formula 04":
    ["This Damage Formula sets the amount of Damage equal to 10",
    "times the multiple given."],

    "Formula 05":
    ["This Damage Formula sets the Base Power differently",
    "depending on the weight of the given Pokemon in relation to",
    "the User."],

    "Formula 06":
    ["This Damage Formula sets the Base Power differently",
    "depending on how the User's Speed compares with the given",
    "Target's Speed."],

    "Formula 07":
    ["This Damage Formula sets the Base Power differently",
    "depending on the argument given.",
    "Each possible value corresponds to a specific formula for a",
    "specific Move."],

    "Formula 08":
    ["This Damage Formula set the Base Power differently depending",
    "on how many positive/negative Stat Stages the given Pokemon",
    "has."],

    "Formula 09":
    ["This Damage Formula sets the amount of Damage equal to the",
    "given percent of the given Pokemon's remaining HP."],

    "Formula 0A":
    ["This Damage Formula sets the Base Power differently",
    "depending on the Held Item of the given Pokemon."],

    "Formula 0B":
    ["This Damage Formula sets the amount of Damage differently",
    "depending on the amount of Damage that the given Target has",
    "taken from Physical and/or Special Moves this turn."],

    "Formula 0C":
    ["This Damage Formula is for Z-Moves and Max Moves, which set",
    "the Base Power differently depending on the Move they were",
    "derived from."],

    "Formula 0D":
    ["This Damage Formula is unused in default ACE."],

    "Formula 0E":
    ["This Damage Formula is unused in default ACE."],

    "Formula 0F":
    ["This Damage Formula is unused in default ACE."]}

# ------------------------------------------------------------
# Script Conversion Dictionaries - Used in the Table Converter
# ------------------------------------------------------------

# Change old Move Scripts to their ACE equivalents
OldToNewScripts = {"08":"03", # Dream Eater
                   "11":"00", # No-Miss Move
                   "20":"9D", # Recover
                   "26":"00", # OHKO Move
                   "27":"00", # Razor Wind
                   "28":"00", # Super Fang
                   "29":"00", # Dragon Rage
                   "2B":"00", # High CHR
                   "2C":"1D", # Double Kick
                   "2D":"00", # Crash Move
                   "32":"0A", # Attack + 2
                   "33":"0B", # Def + 2
                   "34":"0C", # Speed + 2
                   "35":"0D", # SpA + 2
                   "36":"0E", # SpD + 2
                   "37":"0F", # Accuracy + 2
                   "38":"10", # Evasion + 2
                   "3A":"12", # Attack -2
                   "3B":"13", # Defence -2
                   "3C":"14", # Speed -2
                   "3D":"15", # SpA -2
                   "3E":"16", # SpD -2
                   "3F":"17", # Accuracy -2
                   "40":"18", # Evasion -2
                   "42":"02", # Poison
                   "43":"06", # Paralysis
                   "44":"12", # Attack + Lower Atk
                   "45":"13", # Attack + Lower Def
                   "46":"14", # Attack + Lower Spe
                   "47":"15", # Attack + Lower SpA
                   "48":"16", # Attack + Lower SpD
                   "49":"17", # Attack + Lower Acc
                   "4A":"18", # Attack + Lower Eva
                   "4B":"1F", # Sky Attack
                   "4C":"31", # Attack + Confusion
                   "4D":"1D", # Twineedle
                   "4E":"00", # Submission
                   "55":"00", # Splash
                   "57":"00", # Night Shade
                   "58":"00", # Psywave
                   "59":"00", # Counter
                   "5C":"00", # Snore
                   "60":"00", # 
                   "63":"00", # Flail
                   "65":"00", # False Swipe
                   "67":"00", # Priority Marker
                   "68":"1D", # Triple Kick
                   "6E":"00", # 
                   "79":"00", # Return
                   "7A":"00", # Present
                   "7B":"00", # Frustration 
                   "7E":"00", # Magnitude
                   "7F":"1C", # Baton Pass
                   "80":"00", # Pursuit
                   "82":"00", # Sonicboom
                   "83":"00", # 
                   "84":"9D", # Morning Sun
                   "85":"9D", # Moonlight
                   "86":"9D", # Synthesis
                   "87":"00", # Hidden Power
                   "88":"73", # Rain Dance
                   "89":"73", # Sunny Day
                   "8A":"0B", # Attack + Def +1
                   "8B":"0A", # Attack + Attack +1
                   "8D":"00", #
                   "90":"00", # Mirror Coat
                   "91":"00", # 
                   "92":"1F", # 
                   "93":"00", # 
                   "94":"32", # Future Sight
                   "95":"00", # 
                   "96":"00", # Stomp?
                   "97":"00", # Solarbeam
                   "98":"00", # Thunder
                   "9B":"00", # Fly
                   "A1":"00", # Spit Up
                   "A2":"9D", # Swallow
                   "A3":"00", # 
                   "A4":"73", # Hail
                   "A7":"04", # Will-O-Wisp
                   "A9":"00", # Facade
                   "AA":"00", # Focus Punch
                   "B6":"8D", # Attack + Lower Own Atk+Def
                   "B9":"00", # Revenge
                   "BD":"00", # Endeavour
                   "BE":"00", # Eruption
                   "C4":"00", # 
                   "C6":"30", # 1/3 Recoil
                   "C7":"31", # Teeter Dance
                   "C8":"04", # Blaze Kick 
                   "CA":"21", # Attack + Bad Poison
                   "CB":"00", # Weather Ball
                   "CC":"15", # Attack + Lower Own SpA
                   "CD":"8D", # Tickle
                   "CE":"8C", # Cosmic Power
                   "CF":"00", # Sky Uppercut
                   "D1":"02", # High CHR + Poison
                   "D3":"8C", # Calm Mind
                   "D4":"8C"} # Dragon Dance

# Change the old range values to the new system
OldToNewRanges = {"00":"1E",
                  "08":"2C",
                  "10":"11",
                  "20":"2E",
                  "01":"40",
                  "04":"80"}

# These old scripts should use the Self-Effect Flag always
SelfEffectFlagList = ["7F",
                      "8A",
                      "8B",
                      "8C",
                      "B6",
                      "CC"]

# These old scripts now have non-zero script arguments
OldToNewArguments = {"01":"19", # Sleep - Random 1-3 Turns
                     "03":"32", # Absorb Move - 50%
                     "08":"32", # Dream Eater - 50%
                     "0A":"01", # Stat Stage + 1
                     "0B":"01", # Stat Stage + 1
                     "0C":"01", # Stat Stage + 1
                     "0D":"01", # Stat Stage + 1
                     "0E":"01", # Stat Stage + 1
                     "0F":"01", # Stat Stage + 1
                     "10":"01", # Stat Stage + 1
                     "12":"01", # Stat Stage - 1
                     "13":"01", # Stat Stage - 1
                     "14":"01", # Stat Stage - 1
                     "15":"01", # Stat Stage - 1
                     "16":"01", # Stat Stage - 1
                     "17":"01", # Stat Stage - 1
                     "18":"01", # Stat Stage - 1
                     "1A":"02", # Bide - 2 Turns
                     "1B":"13", # Thrash Move - Random 2-3 Turns
                     "1C":"00", # Whirlwind - No Baton Pass
                     "1D":"15", # Random 2-5 Move
                     "20":"00", # Recover - Formula 0
                     "22":"00", # Make Money - Pay Day
                     "23":"05", # Light Screen
                     "24":"70", # Tri-Attack - Paralyse/Burn/Freeze
                     "25":"04", # Rest - Four Turns
                     "2A":"15", # Wrap Move
                     "2C":"02", # Double Kick - Hit Twice
                     "2E":"05", # Mist - Five Turns
                     "30":"19", # Recoil - 25%
                     "32":"02", # Stat Stage + 2
                     "33":"02", # Stat Stage + 2
                     "34":"02", # Stat Stage + 2
                     "35":"02", # Stat Stage + 2
                     "36":"02", # Stat Stage + 2
                     "37":"02", # Stat Stage + 2
                     "38":"02", # Stat Stage + 2
                     "3A":"02", # Stat Stage - 2
                     "3B":"02", # Stat Stage - 2
                     "3C":"02", # Stat Stage - 2
                     "3D":"02", # Stat Stage - 2
                     "3E":"02", # Stat Stage - 2
                     "3F":"02", # Stat Stage - 2
                     "40":"02", # Stat Stage - 2
                     "41":"05", # Reflect - Five Turns
                     "44":"01", # Stat Stage - 1
                     "45":"01", # Stat Stage - 1
                     "46":"01", # Stat Stage - 1
                     "47":"01", # Stat Stage - 1
                     "48":"01", # Stat Stage - 1
                     "49":"01", # Stat Stage - 1
                     "4A":"01", # Stat Stage - 1
                     "4D":"02", # Twineedle
                     "56":"04", # Diabled - Four Turns
                     "5A":"03", # Encore - Three Turns
                     "62":"01", # Destiny Bond - One Turn
                     "64":"04", # Spite - Four PP
                     "69":"00", # Thief
                     "68":"03", # Triple Kick - Hits Thrice
                     "6C":"02", # Minimise - +2 Evasion
                     "70":"00", # Spikes
                     "72":"04", # Perish Song - Four Turns
                     "73":"02", # Sandstorm
                     "76":"01", # Swagger
                     "7C":"05", # Safeguard - Five Turns
                     "7D":"00", # Don't Thaw Target
                     "7F":"01", # Baton Pass
                     "84":"01", # Heal More in Sun
                     "85":"01", # Heal More in Sun
                     "86":"01", # Heal More in Sun
                     "88":"01", # Rain Dance
                     "89":"03", # Sunny Day
                     "8A":"01", # Stat Stage + 1
                     "8B":"01", # Stat Stage + 1
                     "8C":"1F", # Raise All By + 1
                     "8E":"01", # Maximise Attack
                     "94":"03", # Future Sight - Three Turns
                     "9D":"00", # Heal 50% of maximum
                     "9F":"03", # Uproar - Five Turns
                     "A2":"05", # Swallow
                     "A4":"04", # Hail
                     "AC":"00", # Follow Me
                     "AE":"02", # Charge - Two Turns
                     "AF":"04", # Taunt - Three Turns
                     "B0":"01", # Helping Hand - One Turn
                     "B6":"03", # Lower Own Attack + Defence
                     "B7":"01", # Magic Coat - One Turn
                     "C6":"33", # 1/3 Recoil
                     "C9":"05", # Mud Sport - Five Turns
                     "CC":"02", # Lower Own SpA - 2
                     "CD":"03", # Lower Attack + Defence
                     "CE":"12", # Raise Defence + Sp. Defence
                     "D0":"03", # Raise Attack + Defence
                     "D2":"05", # Water Sport - Five Turns
                     "D3":"18", # Raise SpA + SpD
                     "D4":"05"} # Raise Atk + Speed

# These are old scripts which were replaced with Damage Formulae + Arguments
OldToNewDamageFormula = {"26":"D9", # Formula = 09, Arg = 0D
                         "28":"59", # Formula = 09, Arg = 05
                         "29":"44", # Formula = 04, Arg = 04
                         "57":"01", # Formula = 01, Arg = 00
                         "58":"37", # Formula = 07, Arg = 03
                         "59":"0B", # Formula = 0B, Arg = 00
                         "63":"43", # Formula = 03, Arg = 04
                         "75":"C7", # Formula = 07, Arg = 0C
                         "77":"D7", # Formula = 07, Arg = 0D
                         "79":"02", # Formula = 02, Arg = 00
                         "7A":"17", # Formula = 07, Arg = 01
                         "7B":"42", # Formula = 02, Arg = 04
                         "7E":"07", # Formula = 07, Arg = 00
                         "82":"24", # Formula = 04, Arg = 02
                         "90":"4B", # Formula = 0B, Arg = 04
                         "9A":"27", # Formula = 07, Arg = 02
                         "A1":"47", # Formula = 07, Arg = 04
                         "BD":"E7", # Formula = 07, Arg = 0E
                         "BE":"03", # Formula = 03, Arg = 00
                         "C4":"15"} # Formula = 05, Arg = 01

"""
================================================================================================
MAKE BOXES - These functions are used to make the different kinds of pop-up windows
================================================================================================
"""
#------------------------------------------------------------
# Make Info Box - Normal message box, nothing special
#------------------------------------------------------------
def MakeInfoBox(Root, Title, Header, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")
    Top.resizable(False, False)
    Top.attributes('-topmost',True)
    Top.attributes('-topmost',False)

    # Put the new window on top left corner of the old one
    x,y = (int(s) for s in Root.geometry().split("+")[1:])
    Top.geometry(f"+{x}+{y}")

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
# Make Yes/No Box - Message box with two options
#------------------------------------------------------------
def MakeYesNoBox(Root, Title, Header, Var, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")
    Top.resizable(False, False)
    Top.attributes('-topmost',True)
    Top.attributes('-topmost',False)

    # Put the new window on top left corner of the old one
    x,y = (int(s) for s in Root.geometry().split("+")[1:])
    Top.geometry(f"+{x}+{y}")

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
# Make Entry Box - You can enter a value of the given type
#------------------------------------------------------------
def MakeEntryBox(Root, Title, Header, Var, Type, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")
    Top.resizable(False, False)
    Top.attributes('-topmost',True)
    Top.attributes('-topmost',False)

    # Put the new window on top left corner of the old one
    x,y = (int(s) for s in Root.geometry().split("+")[1:])
    Top.geometry(f"+{x}+{y}")

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
            PrintError(e)
            PromptEntry.delete(1.0, "end-1c")
            PromptEntry.insert(1.0, Text[:-1])           
    
    PromptEntry = tk.Text(PromptFrame, width = 20, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    PromptEntry.bind("<KeyRelease>", (lambda _: ProcessEntry(PromptEntry.get(1.0, "end-1c"))))
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
# Make Address Entry Box - Like the above, but for addresses
#------------------------------------------------------------
def MakeAddressEntryBox(Root, Title, Header, Var, Text):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")
    Top.resizable(False, False)
    Top.attributes('-topmost',True)
    Top.attributes('-topmost',False)

    # Put the new window on top left corner of the old one
    x,y = (int(s) for s in Root.geometry().split("+")[1:])
    Top.geometry(f"+{x}+{y}")

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
    PromptEntry.bind("<KeyRelease>", (lambda _: ProcessEntry(PromptEntry.get(1.0, "end-1c"))))
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
# Make Info Box With Menu And Search Bar - Display text through combobox, search bar included
#------------------------------------------------------------
def MakeInfoBoxMenuSearch(Root, Title, Header, Text, MenuText, Var = None, Initial = None, TagsList = None):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")
    Top.resizable(False, False)
    Top.attributes('-topmost',True)
    Top.attributes('-topmost',False)

    # Put the new window on top left corner of the old one
    x,y = (int(s) for s in Root.geometry().split("+")[1:])
    Top.geometry(f"+{x}+{y}")

    # Make Frames
    HeaderTextFrame = tk.Frame(Top, bg = "Black")
    HeaderTextFrame.pack(fill = "x", pady = 10)

    InfoTextFrame = tk.Frame(Top, bg = "Black")
    InfoTextFrame.pack(fill = "x", pady = 10)

    MenuTextFrame = tk.Frame(Top, bg = "Black")
    MenuTextFrame.pack(fill = "none", pady = 10)

    SearchFrame = tk.Frame(Top, bg = "Black")
    SearchFrame.pack(pady = 5)

    MenuFrame = tk.Frame(Top, bg = "Black")
    MenuFrame.pack(fill = "x", pady = 5)
    
    OkayFrame = tk.Frame(Top, bg = "Black")
    OkayFrame.pack(fill = "x", pady = 5)

    # Make Header + Text
    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()
    for Line in Text:
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).pack()
    ttk.Label(MenuTextFrame, text = "You can press the up/down arrow Keys to navigate the menu.").pack()

    # Create Values list
    Values = []
    for Key in MenuText:
        Values.append(Key)

    # Define Tkinter Variables
    Option = tk.StringVar()
    CurrentOption = tk.IntVar(value = 0)

    # Set initial value if given
    if Initial is None:
        Option.set(list(MenuText.keys())[0])
        CurrentOption.set(0)
    else:
        Option.set(Initial)
        CurrentOption.set(list(MenuText.keys()).index(Option.get()))

    # Make Tag Display Label
    TagLabel = ttk.Label(MenuTextFrame, text = "Tags", font = ("Courier", SmallSize, "bold"))

    # Make Menu + Text Box
    def ChangeText():
        List = MenuText[Option.get()]
        CurrentOption.set(MenuDropDown.cget('values').index(Option.get()))

        MenuTextString = ""
        for Line in List:
            MenuTextString += Line + "\n"

        MenuTextBox.configure(state = "normal")
        MenuTextBox.delete(1.0, "end-1c")
        MenuTextBox.insert(1.0, MenuTextString.strip())
        MenuTextBox.configure(state = "disabled")

        if TagsList:
            Tags = TagsList[Option.get()]

            TagString = ""
            for Tag in Tags:
                TagString += Tag + ", "

            TagString = TagString.strip()[:-1]
            TagsTextBox.configure(state = "normal")
            TagsTextBox.delete(1.0, "end-1c")
            TagsTextBox.insert(1.0, TagString)
            TagsTextBox.configure(state = "disabled")

    MenuTextBox = stxt.ScrolledText(MenuTextFrame, width = 60, height = 4, state = "disabled", font = ("Courier", SmallSize))
    TagsTextBox = stxt.ScrolledText(MenuTextFrame, width = 55, height = 4, state = "disabled", bg = "Black", fg = "White", wra = "word", font = ("Courier", SmallSize))
    MenuDropDown = ttk.Combobox(MenuFrame, textvariable = Option, width = 20, values = Values, font = ("Courier", SmallSize))      
    MenuDropDown.bind("<<ComboboxSelected>>", lambda _: ChangeText())
    ChangeText()
    
    # Make Frame For Search Bar
    BarFrame = tk.Frame(SearchFrame, bg = "Black")

    # Make Search Bar Entry Widget
    def ProcessEntry(Text):        
        Values = []
        for Key in MenuText:
            if Text.lower() in " ".join(MenuText[Key]).lower():
                Values.append(Key)

            if TagsList:
                if Text.lower() in " ".join(TagsList[Key]).lower():
                    if Key not in Values:
                        Values.append(Key)

        MenuDropDown.configure(values = Values)

        if Text == "":
            ResultsLabel.configure(text = "--")
        else:
            ResultsLabel.configure(text = "Found {} results".format(len(Values)))

        if Option.get() not in Values:
            CurrentOption.set(0)
            
            if Values:
                Option.set(Values[0])
            else:
                MenuDropDown.configure(values = [Initial])
                Option.set(Initial)
            
        ChangeText()

    SearchBar = tk.Text(BarFrame, width = 20, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    SearchBar.bind("<KeyRelease>", (lambda _: ProcessEntry(SearchBar.get(1.0, "end-1c"))))

    # Make Clear Search Bar Button
    Cleared = tk.IntVar()
    Cleared.set(0)
    def ClearSearch():
        Cleared.set(0)
        SearchBar.delete(1.0, "end-1c")

        Values = []
        for Key in MenuText:
            Values.append(Key)

        MenuDropDown.configure(values = Values)
        ResultsLabel.configure(text = "--")
        CurrentOption.set(MenuDropDown.cget('values').index(Option.get()))

    SearchClear = ttk.Checkbutton(BarFrame, text = "X", variable = Cleared, command = ClearSearch)
    
    # Make Results Label
    ResultsLabel = ttk.Label(SearchFrame, text = "--", font = ("Courier", SmallSize))

    # Make Okay Button
    def QuitBox(Event = None):
        if Var is not None:
            Var.set(Option.get())
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Done", command = QuitBox)

    # Pack Everything
    MenuTextBox.pack(pady = 5)
    TagLabel.pack()
    TagsTextBox.pack(pady = 5)
    BarFrame.pack(pady = 5)
    SearchClear.pack(side = "left", padx = 5)
    SearchBar.pack(side = "left")
    ResultsLabel.pack()
    MenuDropDown.pack()
    OkayButton.pack()

    # Make HotKeys
    def MoveUp():
        CurrentOption.set(CurrentOption.get() - 1)
        Option.set(MenuDropDown.cget('values')[CurrentOption.get()])
        ChangeText()

    def MoveDown():
        CurrentOption.set(CurrentOption.get() + 1)
        Option.set(MenuDropDown.cget('values')[CurrentOption.get()])
        ChangeText()

    def HotKeyManager(Event):
        Key = Event.keysym
        Shift = Event.state & 1

        if OnAMac:
            Command = Event.state & 8
        else:
            Command = Event.state & 4

        if Key == "Up" and CurrentOption.get() > 0:
            MoveUp()

        if Key == "Down" and CurrentOption.get() < len(MenuDropDown.cget('values')) - 1:
            MoveDown()        

    Top.bind("<Return>", QuitBox)
    Top.bind("<KeyPress>", HotKeyManager)
    Top.wait_window()

#------------------------------------------------------------
# Make Multi-Choice Box - Allows you to choose from many options
#------------------------------------------------------------
def MakeMultiChoiceBox(Root, Title, Header, Var, Text, MenuText, InitialOption = None):
    Top = tk.Toplevel(Root)
    Top.title(Title)
    Top.configure(bg = "Black")
    Top.resizable(False, False)
    Top.attributes('-topmost',True)
    Top.attributes('-topmost',False)

    # Put the new window on top left corner of the old one
    x,y = (int(s) for s in Root.geometry().split("+")[1:])
    Top.geometry(f"+{x}+{y}")

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

    # Make Header + Text
    ttk.Label(HeaderTextFrame, text = Header, font = ("Courier", int(SmallSize*1.5))).pack()
    for Line in Text:
        ttk.Label(InfoTextFrame, text = Line, font = ("Courier", SmallSize)).pack()
    ttk.Label(MenuTextFrame, text = "You can press the up/down arrow Keys to navigate the menu.").pack()

    # Create Values list
    Values = []
    for Key in MenuText:
        Values.append(Key)

    # Define Option variable
    Option = tk.StringVar()

    # Define current option number
    CurrentOption = tk.IntVar(value = 0)

    # Set initial value if given
    if InitialOption is None:
        Option.set(list(MenuText.keys())[0])
        CurrentOption.set(0)
    else:
        Option.set(InitialOption)
        CurrentOption.set(list(MenuText.keys()).index(Option.get()))

    # Change Text Function
    def ChangeText():
        List = MenuText[Option.get()]
        CurrentOption.set(MenuDropDown.cget('values').index(Option.get()))

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
        Var.set(Option.get())
        Top.destroy()

    OkayButton = ttk.Button(OkayFrame, text = "Okay", command = QuitBox)
    OkayButton.pack()

    def MoveUp():
        CurrentOption.set(CurrentOption.get() - 1)
        Option.set(MenuDropDown.cget('values')[CurrentOption.get()])
        ChangeText()

    def MoveDown():
        CurrentOption.set(CurrentOption.get() + 1)
        Option.set(MenuDropDown.cget('values')[CurrentOption.get()])
        ChangeText()

    def HotKeyManager(Event):
        Key = Event.keysym
        Shift = Event.state & 1

        if OnAMac:
            Command = Event.state & 8
        else:
            Command = Event.state & 4

        if Key == "Up" and CurrentOption.get() > 0:
            MoveUp()

        if Key == "Down" and CurrentOption.get() < len(MenuDropDown.cget('values')) - 1:
            MoveDown()

    Top.bind("<Return>", QuitBox)
    Top.bind("<KeyPress>", HotKeyManager)
    Top.wait_window()
    
"""
================================================================================================
TABLE FUCNTIONS - Contains functions related to the different operations on a table, like converting
================================================================================================
"""
#------------------------------------------------------------
# Lists and Dictionaries used in the Table Functions
#------------------------------------------------------------
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

RangeConversion = {"User":"11", "Partner":"12", "Target":"1E", "User + Partner":"13",
                   "Target + Partner":"1C", "My Side":"23", "Foe Side":"2C",
                   "All But User":"2E", "Everyone":"2F", "Random":"80", "Last Attacker":"40"}

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
# Format Description - Process Move Description correctly
#------------------------------------------------------------
def FormatDescription(RawText):
    RawText = RawText.replace("|", "\n")

    try:
        Line1 = RawText.split("\n")[0].strip()
    except Exception as e:
        PrintError(e)
        Line1 = ""

    try:
        Line2 = RawText.split("\n")[1].strip()
    except Exception as e:
        PrintError(e)
        Line2 = ""

    try:
        Line3 = RawText.split("\n")[2].strip()
    except Exception as e:
        PrintError(e)
        Line3 = ""

    try:
        Line4 = RawText.split("\n")[3].strip()
    except Exception as e:
        PrintError(e)
        Line4 = ""

    NewText = "{}\n{}\n{}\n{}".format(Line1, Line2, Line3, Line4)
    return NewText

#------------------------------------------------------------
# Get Strings From Compiled Tables of Pointers
#------------------------------------------------------------
def GrabStringsFromTable(File):
    File = open(File, "rb")
    FileBytes = CreateFileBytes(File, 4)
    Strings = []
    String = ""
    for Line in FileBytes.strip().split("\n"):
        if not "08" in Line: # Strings in AGB never have 08 in them
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
            MakeInfoBox(Root, "Error!", "There was a problem!",
                        ["There was an error loading {} {}s.".format(Error.count("0"), Type.lower()),
                         "They were replaced with a default value."])
    
        return Table

    except Exception as e:
        PrintError(e)
        MakeInfoBox(Root, "Error!", "There was a problem!",
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
            TableLine.append(Entry[MoveScriptIndex - 1])  # Move Script
        except Exception as e:
            PrintError(e)
            TableLine.append("00")
            Error += "0"

        try:
            TableLine.append(int(Entry[BasePowerIndex - 1], 16)) # Base Power
        except Exception as e:
            PrintError(e)
            TableLine.append(0)
            Error += "1"

        try:
            TableLine.append(list(TypeConversion.keys())[list(TypeConversion.values()).index(Entry[TypeIndex - 1])])
        except Exception as e:
            PrintError(e)
            TableLine.append("Normal")
            Error += "2"

        try:
            A = int(Entry[AccuracyIndex - 1], 16)
            if A > 100:
                A = 100
            TableLine.append(A) # Accuracy
        except Exception as e:
            PrintError(e)
            TableLine.append(0)
            Error += "3"

        try:
            A = int(Entry[PowerPointIndex - 1], 16)
            if A > 99:
                A = 99
            TableLine.append(A) # Power Points
        except Exception as e:
            PrintError(e)
            TableLine.append(0)
            Error += "4"

        try:
            A = int(Entry[EffectChanceIndex - 1], 16)
            if A > 100:
                A = 100
            TableLine.append(A) # Effect Chance
        except:
            TableLine.append(0)
            Error += "5"

        try:
            TableLine.append(list(RangeConversion.keys())[list(RangeConversion.values()).index(Entry[RangeIndex - 1])])
        except Exception as e:
            PrintError(e)
            TableLine.append("Target")
            Error += "6"

        try:
            P = int(Entry[PriorityIndex - 1], 16)
            if P > 127:
                P = 256 - P
                P = -P
                
            TableLine.append(P) # Priority
        except Exception as e:
            PrintError(e)
            TableLine.append(0)
            Error += "7"

        try:
            MoveFlags = [0,0,0,0,0,0,0,0]
            F = int(Entry[MoveFlagIndex - 1], 16)

            for i in range(8):
                if F & 128 // 2**i != 0: # Flag is set
                    MoveFlags[i] = 1

            TableLine.append(MoveFlags)
        except Exception as e:
            PrintError(e)
            TableLine.append([0,0,0,0,0,0,0,0])
            Error += "8"

        try:
            TableLine.append(Entry[DamageFormulaIndex - 1]) # Damage Formula
        except Exception as e:
            PrintError(e)
            TableLine.append("00")
            Error += "9"

        try:
            TableLine.append(list(KindConversion.keys())[list(KindConversion.values()).index(Entry[MoveKindIndex - 1])])
        except Exception as e:
            PrintError(e)
            TableLine.append("Status")
            Error += "A"

        try:
            TableLine.append(int(Entry[ScriptArgIndex - 1], 16))
        except Exception as e:
            PrintError(e)
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
                    TableLine.append(Line.split("%")[0].strip()[0:12]) # Truncate at 12, anything after % is ignored
                except Exception as e:
                    PrintError(e)
                    TableLine.append("Move Name")
                    Error += "X"

            elif i == MoveScriptIndex:
                try:
                    TableLine.append(Line.split("%")[0].split(")")[1].replace(",", "").strip()[2:])
                except Exception as e:
                    PrintError(e)
                    TableLine.append("00")
                    Error += "0"

            elif i == BasePowerIndex:
                try:
                    TableLine.append(int(Line.split("%")[0].split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    PrintError(e)
                    TableLine.append(0)
                    Error += "1"

            elif i == TypeIndex:
                try:
                    TableLine.append(Line.split("%")[0].split(")")[1].replace(",", "").strip())
                except Exception as e:
                    PrintError(e)
                    TableLine.append("Normal")
                    Error += "2"

            elif i == AccuracyIndex:
                try:
                    TableLine.append(int(Line.split("%")[0].split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    PrintError(e)
                    TableLine.append(0)
                    Error += "3"

            elif i == PowerPointIndex:
                try:
                    TableLine.append(int(Line.split("%")[0].split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    PrintError(e)
                    TableLine.append(0)
                    Error += "4"

            elif i == EffectChanceIndex:
                try:
                    TableLine.append(int(Line.split("%")[0].split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    PrintError(e)
                    TableLine.append(0)
                    Error += "5"
                
            elif i == RangeIndex:
                try:
                    Range = Line.split("%")[0].split(")")[1].replace(",", "").strip()

                    C = {"MySide":"My Side", "FoeSide":"Foe Side",
                         "AllButUser":"All But User", "UserOrPartner":"User + Partner",
                         "TargetOrPartner":"Target + Partner", "LastHitMe":"Last Attacker"}

                    for Key in C:
                        if Range == Key:
                            Range = C[Key]
                            break
                    
                    TableLine.append(Range)
                except Exception as e:
                    PrintError(e)
                    TableLine.append("Target")
                    Error += "6"

            elif i == PriorityIndex:
                try:
                    P = int(Line.split("%")[0].split(")")[1].replace(",", "").strip())

                    if P > 127:
                        P = 256 - P
                        P = -P

                    TableLine.append(P)
                except Exception as e:
                    PrintError(e)
                    TableLine.append(0)
                    Error += "7"

            elif i == MoveFlagIndex:
                try:
                    F = Line.split("%")[0].split(")")[1].replace(",", "").strip()
                    MoveFlags = [0,0,0,0,0,0,0,0]

                    for i, Flag in enumerate(F.split("+")):
                        Flag = Flag.strip()[2:]

                        if int(Flag, 16) & 128 // 2**i:
                            MoveFlags[i] = 1

                    TableLine.append(MoveFlags)
                except Exception as e:
                    PrintError(e)
                    TableLine.append([0,0,0,0,0,0,0,0])
                    Error += "8"

            elif i == DamageFormulaIndex:
                try:
                    TableLine.append(Line.split("%")[0].split(")")[1].replace(",", "").strip()[2:])
                except Exception as e:
                    PrintError(e)
                    TableLine.append("00")
                    Error += "9"

            elif i == MoveKindIndex:
                try:
                    TableLine.append(Line.split("%")[0].split(")")[1].replace(",", "").strip())
                except Exception as e:
                    PrintError(e)
                    TableLine.append("Status")
                    Error += "A"

            elif i == ScriptArgIndex:
                try:
                    TableLine.append(int(Line.split("%")[0].split(")")[1].replace(",", "").strip()))
                except Exception as e:
                    PrintError(e)
                    TableLine.append(0)
                    Error += "B"

            elif i == DescriptionIndex: # Includes a Move Description Line
                try:
                    Text = Line.split("%")[0].split(")")[1].replace(",","").strip()
                    if Text != "":
                        TableLine.append(FormatDescription(Text))
                    else:
                        TableLine.append('')
                except Exception as e:
                    PrintError(e)
                    TableLine.append('')
                    Error += "C"

        if len(TableLine) < 14:
            TableLine = ["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]
            Error += "D"
            
        Table.append(TableLine)

    return Table, Error

#------------------------------------------------------------
# Display Error Lines
#------------------------------------------------------------
def DisplayErrorLines(Root, Error):
    ErrorLines = []
    
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

    MakeInfoBox(Root, "Error!", "There was a problem.", ErrorLines)
        
#------------------------------------------------------------
# Display Errors in Table
#------------------------------------------------------------
def LoadTableErrors(Root, Table, Error):
    if Error == "":
        MakeInfoBox(Root, "Success!", "The table was created!",
                    ["The table was created successfully.",
                     "It has {} Moves in total.".format(len(Table))])
    else:
        MakeInfoBox(Root, "Error!", "There was a problem.",
                       ["There was a problem loading the table.",
                        "Default values were provided for bad data.",
                        "The next pop-up will detail the errors."])

        DisplayErrorLines(Root, Error)

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
                case Index if Index == MoveNameIndex:
                    if type(Line) != str or Line == "":
                        print(Line)
                        Table[i][j] = "Move Name"
                        Error += "X"
                        
                case Index if Index == MoveScriptIndex: # Move Script
                    if Line.upper() not in HexBytes:
                        print(Line)
                        Table[i][j] = "00"
                        Error += "0"
                    else:
                        Table[i][j] = Line.upper()

                case Index if Index == BasePowerIndex: # Base Power
                    if type(Line) != int:
                        print(Line)
                        Table[i][j] = 0
                        Error += "1"

                case Index if Index == TypeIndex: # Type
                    if Line not in TypeConversion:
                        print(Line)
                        Table[i][j] = "Normal"
                        Error += "2"

                case Index if Index == AccuracyIndex: # Accuracy
                    if type(Line) != int:
                        print(Line)
                        Table[i][j] = 0
                        Error += "3"

                case Index if Index == PowerPointIndex: # Power Point
                    if type(Line) != int:
                        print(Line)
                        Table[i][j] = 0
                        Error += "4"

                case Index if Index == EffectChanceIndex: # Effect Chance
                    if type(Line) != int:
                        print(Line)
                        Table[i][j] = 0
                        Error += "5"

                case Index if Index == RangeIndex: # Move Range
                    if Line not in RangeConversion:
                        print(Line)
                        Table[i][j] = "Target"
                        Error += "6"

                case Index if Index == PriorityIndex: # Priority
                    if type(Line) != int:
                        print(Line)
                        Table[i][j] = 0
                        Error += "7"

                case Index if Index == MoveFlagIndex: # Move Flags
                    if len(Line) != 8:
                        print(Line)
                        Table[i][j] = [0,0,0,0,0,0,0,0]
                        Error += "8"
                        
                    else:
                        if not all(y in (0,1) for y in Line):
                            print(Line)
                            Table[i][j] = Line
                            Error += "8"

                case Index if Index == DamageFormulaIndex: # Damage Formula
                    if Line.upper() not in HexBytes:
                        print(Line)
                        Table[i][j] = "00"
                        Error += "9"
                    else:
                        Table[i][j] = Line.upper()

                case Index if Index == MoveKindIndex: # Move Kind
                    if Line != "Physical" and Line != "Special" and Line != "Status":
                        print(Line)
                        Table[i][j] = "Status"
                        Error += "A"

                case Index if Index == ScriptArgIndex: # Move Script
                    if type(Line) != int:
                        print(Line)
                        Table[i][j] = 0
                        Error += "B"

                case Index if Index == DescriptionIndex: # Move Description
                    if type(Line) != str:
                        print(Line)
                        Table[i][j] = ""
                        Error += "C"                   

    if Error != "":
        MakeInfoBox(Root, "Error!", "Table has errors",
                    ["One or more entries of the table has an error.",
                     "Invalid entries were replaced with default values.",
                     "The next pop-up will detail the errors."])

        DisplayErrorLines(Root, Error)

    if len(Table) == 0:
        Table = [["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]]

        MakeInfoBox(Root, "Error!", "There was a problem.",
                    ["There was a problem loading the table.",
                     "A blank one was provided instead.",
                     "It has {} Moves in total.".format(len(Table))])
        
    return Table

"""
================================================================================================
FORMULA ARGUMENT HELPERS - Used in the Damage Formula Argument field to help user choose the right one
================================================================================================
"""
#------------------------------------------------------------
# No Argument
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
    TargetPicker.bind("<<ComboboxSelected>>", lambda _: SetTarget())
    
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
    TargetPicker.bind("<<ComboboxSelected>>", lambda _: SetTarget())

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
    MultipleSlider = ttk.Scale(FrameB, variable = Multiple, length = 450, from_ = 1, to = 15, command = lambda _: SetMultiple(), orient = "horizontal")
    
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
    OptionPicker.bind("<<ComboboxSelected>>", lambda _: SetOption())
    
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
    TargetPicker.bind("<<ComboboxSelected>>", lambda _: SetTarget())

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
    TargetPicker.bind("<<ComboboxSelected>>", lambda _: SetTarget())

    PercentLabel = ttk.Label(FrameC, text = "Percent:", font = ("Courier", SmallSize))
    PercentPicker = ttk.Combobox(FrameC, textvariable = Percent, width = 4, values = Percents, font = ("Courier", SmallSize))
    PercentPicker.bind("<<ComboboxSelected>>", lambda _: SetPercent())

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
    TargetPicker.bind("<<ComboboxSelected>>", lambda _: SetTarget())

    OptionLabel = ttk.Label(FrameC, text = "Percent:", font = ("Courier", SmallSize))
    OptionPicker = ttk.Combobox(FrameC, textvariable = Option, width = 10, values = Options, font = ("Courier", SmallSize))
    OptionPicker.bind("<<ComboboxSelected>>", lambda _: SetOption())

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
    TargetPicker.bind("<<ComboboxSelected>>", lambda _: SetTarget())

    OptionLabel = ttk.Label(FrameC, text = "Percent:", font = ("Courier", SmallSize))
    OptionPicker = ttk.Combobox(FrameC, textvariable = Option, width = 12, values = list(Options.keys()), font = ("Courier", SmallSize))
    OptionPicker.bind("<<ComboboxSelected>>", lambda _: SetOption())

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

"""
================================================================================================
SCRIPT ARGUMENT HELPERS - Like above but for the Move Script Argument, there's more of these
================================================================================================
"""
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
            PrintError(e)
            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Input[:-1])
            
    AmountLabel = ttk.Label(FrameB, text = LabelText, font = ("Courier", SmallSize)) 
    AmountEntry = tk.Text(FrameB, width = Width, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize)) 
    AmountEntry.bind("<KeyRelease>", lambda _: SetAmount(AmountEntry.get(1.0, "end-1c")))
    AmountEntry.bind(Paste, lambda _: "break")

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
# Two Combo Boxes + One Flag
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which use two combo boxes and
one Flag
-------------------------------------------------------------
"""
def TwoComboBoxesOneFlag(WidgetFrame, FlagLabel, LabelTextA, LabelTextB, ListA, ListB, FinalValue, Changed, StringList, Width = 13, FlagBits = [56, 7, 3, 6]):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")
    FrameD = tk.Frame(WidgetFrame, bg = "Black")

    VarA = tk.StringVar()
    VarA.set(ListA[0])

    VarB = tk.StringVar()
    VarB.set(ListB[0])

    FlagBitA = FlagBits[0] # Combo Box A = Bottom Part of Value
    FlagBitB = FlagBits[1] # Combo Box B = Top Part of Value
    FlagShift = FlagBits[2]
    FlagBit = FlagBits[3] # This is for the Flag

    StringA = StringList[0]
    StringB = StringList[1]

    Flag = tk.IntVar()
    Flag.set(0)

    TextNormal = StringA.format(VarA.get(), VarB.get()) 
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SwitchText(Var, List):
        for i, Name in enumerate(List):
            if Var.get() == Name:
                if Flag.get() == 1:
                    TextLabel.configure(text = StringB.format(VarA.get(), VarB.get()))
                else:
                    TextLabel.configure(text = StringA.format(VarA.get(), VarB.get()))

                break

        return i

    def SwitchTextII():
        if Flag.get() == 1:
            TextLabel.configure(text = StringB.format(VarA.get(), VarB.get()))
        else:
            TextLabel.configure(text = StringA.format(VarA.get(), VarB.get()))

    # Define Checkbutton
    def SetFlag():
        SwitchTextII()
        FinalValue.set(FinalValue.get() | (1 << FlagBit)) # Set the flag

        if Flag.get() == 0: # Reset Flag
            FinalValue.set(FinalValue.get() ^ (1 << FlagBit)) # Reset the flag now that it's set
        
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    FlagButton = ttk.Checkbutton(FrameB, text = FlagLabel, var = Flag, command = SetFlag)

    # Define Comboboxes
    def SetVariableA():
        i = SwitchText(VarA, ListA)
        TopHalf = FinalValue.get() & FlagBitA
        FinalValue.set((Flag.get() << FlagBit) | TopHalf | i)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetVariableB():
        i = SwitchText(VarB, ListB)
        BottomHalf = FinalValue.get() & FlagBitB
        FinalValue.set((Flag.get() << FlagBit) | (i << FlagShift) | BottomHalf)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    VarLabelA = ttk.Label(FrameC, text = LabelTextA, font = ("Courier", SmallSize))
    VarPickerA = ttk.Combobox(FrameC, textvariable = VarA, width = Width, values = ListA, font = ("Courier", SmallSize))
    VarPickerA.bind("<<ComboboxSelected>>", lambda _: SetVariableA())

    VarLabelB = ttk.Label(FrameD, text = LabelTextB, font = ("Courier", SmallSize))
    VarPickerB = ttk.Combobox(FrameD, textvariable = VarB, width = Width, values = ListB, font = ("Courier", SmallSize))
    VarPickerB.bind("<<ComboboxSelected>>", lambda _: SetVariableB())

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack(pady = 5)
    FrameC.pack(pady = 5)
    FrameD.pack(pady = 5)
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    FlagButton.pack()
    VarLabelA.pack(side = "left", padx = 5)
    VarPickerA.pack(side = "left", padx = 5)
    VarLabelB.pack(side = "left", padx = 5)
    VarPickerB.pack(side = "left", padx = 5)

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
def SingleComboBoxWithSearch(WidgetFrame, String, LabelText, List, FinalValue, Changed, StringList = None, Width = 13, AddOne = True):
    # Create Frames
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")
    FrameD = tk.Frame(WidgetFrame, bg = "Black")

    # Create Tkinter Variables
    Var = tk.StringVar()
    Var.set(List[0])

    CurrentOption = tk.IntVar(value = 0)

    # Make Text Label
    if StringList is None:
        TextNormal = String.format(Var.get())
    else:
        TextNormal = String + "\n" + StringList[0]
        
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    # Make Results Label
    ResultsLabel = ttk.Label(FrameC, text = "--", font = ("Courier", SmallSize))

    # Make Search Bar Entry Widget
    def ProcessEntry(Text):
        Values = []
        for Name in List:
            if Text.lower() in Name.lower():
                Values.append(Name)

        VarPicker.configure(values = Values)

        if Text == "":
            ResultsLabel.configure(text = "--")
        else:
            ResultsLabel.configure(text = "Found {} results".format(len(Values)))

        if Var.get() not in Values:
            CurrentOption.set(0)
            
            if Values:
                Var.set(Values[0])
            else:
                VarPicker.configure(values = ["None"])
                Var.set("None")

        SetVariable()
    
    SearchBar = tk.Text(FrameB, width = 20, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
    SearchBar.bind("<KeyRelease>", (lambda _: ProcessEntry(SearchBar.get(1.0, "end-1c"))))

    # Make Clear Search Bar Button
    Cleared = tk.IntVar()
    Cleared.set(0)
    def ClearSearch():
        Cleared.set(0)
        SearchBar.delete(1.0, "end-1c")

        Values = []
        for Key in List:
            Values.append(Key)

        VarPicker.configure(values = Values)
        ResultsLabel.configure(text = "--")
        CurrentOption.set(VarPicker.cget('values').index(Var.get()))
    
    SearchClear = ttk.Checkbutton(FrameB, text = "X", variable = Cleared, command = ClearSearch)  

    # Create Menu
    def SetVariable():
        if AddOne:
            N = 1
        else:
            N = 0

        CurrentOption.set(VarPicker.cget('values').index(Var.get()))
            
        for i, Name in enumerate(List):
            if Var.get() == Name:
                if StringList is None:
                    TextLabel.configure(text = String.format(Var.get()))
                else:
                    TextLabel.configure(text = String + "\n" + StringList[i])
            
                FinalValue.set(i + N)
                break
            
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    VarLabel = ttk.Label(FrameD, text = LabelText, font = ("Courier", SmallSize)) 
    VarPicker = ttk.Combobox(FrameD, textvariable = Var, width = Width, values = List, font = ("Courier", SmallSize))
    VarPicker.bind("<<ComboboxSelected>>", lambda _: SetVariable())

    # Make Final Value Display Label
    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))
    SetVariable()

    # Pack Everything
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

    # Make HotKeys
    def MoveUp():
        CurrentOption.set(CurrentOption.get() - 1)
        Var.set(VarPicker.cget('values')[CurrentOption.get()])
        SetVariable()

    def MoveDown():
        CurrentOption.set(CurrentOption.get() + 1)
        Var.set(VarPicker.cget('values')[CurrentOption.get()])
        SetVariable()

    def HotKeyManager(Event):
        Key = Event.keysym
        Shift = Event.state & 1

        if OnAMac:
            Command = Event.state & 8
        else:
            Command = Event.state & 4

        if Key == "Up" and CurrentOption.get() > 0:
            MoveUp()

        if Key == "Down" and CurrentOption.get() < len(VarPicker.cget('values')) - 1:
            MoveDown()

    WidgetFrame.bind("<KeyPress>", HotKeyManager)

#------------------------------------------------------------
# Entry + One Combo Box
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which have an entry box and one
combobox.
-------------------------------------------------------------
"""
def AmountEntryOneComboBox(WidgetFrame, List, StringA, StringB, LabelTextA, LabelTextB, StringFlags, Low, High, WidthA, WidthB, FinalValue, Changed, FlagList = [240, 15, 4]):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

    Amount = tk.IntVar()
    Amount.set(0)

    StringFlag = tk.IntVar()
    StringFlag.set(0)

    Var = tk.StringVar()
    Var.set(List[0])

    TopBits = FlagList[0]
    LowBits = FlagList[1]
    ShiftBit = FlagList[2]

    print(TopBits, LowBits)

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
            TopHalf = FinalValue.get() & TopBits # Get top half of byte
            FinalValue.set(TopHalf | X)
            
            SwitchText()

            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Amount.get())

            VarPicker.configure(state = "normal")

        except Exception as e:
            PrintError(e)
            AmountEntry.delete(1.0, "end-1c")
            AmountEntry.insert(1.0, Input[:-1])

    def SetVariable():        
        for i, Name in enumerate(List):
            if Var.get() == Name:
                BottomHalf = FinalValue.get() & LowBits # Get bottom half of byte
                TopHalf = i << ShiftBit
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
    AmountEntry.bind(Paste, lambda _: "break")

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

    TextNormal = StringB.format(Amount.get())
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
            PrintError(e)
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
    AmountEntry.bind(Paste, lambda _: "break")

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
                PrintError(e)
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
    AmountEntry.bind(Paste, lambda _: "break")

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
    FlagButtonA.pack(side = "left", padx = 5, pady = 10)
    FlagButtonB.pack(side = "left", padx = 5, pady = 10)

#------------------------------------------------------------
# Two Flags
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which have two Flags.
-------------------------------------------------------------
"""
def MakeTwoFlags(WidgetFrame, StringList, FinalValue, Changed, FlagList, FlagBits):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")

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

    TextNormal = StringA
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))

    def SwitchText():
        match FlagA.get(), FlagB.get():
            case 0, 0:
                T = StringA
            case 0, 1:
                T = StringC
            case 1, 0:
                T = StringB
            case 1, 1:
                T = StringD
            
        TextLabel.configure(text = T)
        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    def SetFlag(FlagBit, Flag):
        FinalValue.set(FinalValue.get() | (1 << FlagBit)) # Set the flag

        if Flag.get() == 0: # Reset the Flag
            FinalValue.set(FinalValue.get() ^ (1 << FlagBit)) # Reset the flag now that it's set

        SwitchText()

    FlagButtonA = ttk.Checkbutton(FrameC, text = FlagTextA, variable = FlagA, command = lambda: SetFlag(FlagBitA, FlagA))
    FlagButtonB = ttk.Checkbutton(FrameC, text = FlagTextB, variable = FlagB, command = lambda: SetFlag(FlagBitB, FlagB))

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))

    FrameA.pack()
    FrameB.pack()
    FrameC.pack()
    FinalValueLabel.pack(pady = (0,10))
    TextLabel.pack(pady = 10)
    FlagButtonA.pack(pady = 10)
    FlagButtonB.pack(pady = 10)

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
# Two Sets Of Flags
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which use two different sets of
Flags.
-------------------------------------------------------------
"""
def TwoSetsOfFlags(WidgetFrame, String, FlagListA, FlagListB, LabelTextA, LabelTextB, FinalValue, Changed, FlagShift = 4):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")
    FrameD = tk.Frame(WidgetFrame, bg = "Black")
    FrameE = tk.Frame(WidgetFrame, bg = "Black")

    FrameA.pack()
    FrameB.pack(pady = (10,0))
    FrameC.pack()
    FrameD.pack()
    FrameE.pack()

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))
    FinalValueLabel.pack(side = "top")

    FlagVarsA = [tk.IntVar(value = 0) for i in range(len(FlagListA))]
    FlagVarsB = [tk.IntVar(value = 0) for i in range(len(FlagListB))]

    TextNormal = String
    TextLabel = ttk.Label(FrameA, text = TextNormal, font = ("Courier", SmallSize))
    TextLabel.pack()

    FlagLabelA = ttk.Label(FrameB, text = LabelTextA, font = ("Courier", SmallSize))
    FlagLabelA.pack()

    def SetFlagA(N, Var):
        FinalValue.set(FinalValue.get() | (1 << N))

        if Var.get() == 0:
            FinalValue.set(FinalValue.get() ^ (1 << N))

        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    for i, Var in enumerate(FlagVarsA):
        if i < 4:
            R = 0
        else:
            R = 1
            
        C = i % 4
        ttk.Checkbutton(FrameC, text = FlagListA[i], variable = FlagVarsA[i], command = lambda i = i: SetFlagA(i, FlagVarsA[i])).grid(row = R, column = C, padx = 10, pady = 5, sticky = "w")

    FlagLabelB = ttk.Label(FrameD, text = LabelTextB, font = ("Courier", SmallSize))
    FlagLabelB.pack()

    def SetFlagB(N, Var):
        FinalValue.set(FinalValue.get() | (1 << N) << FlagShift)

        if Var.get() == 0:
            FinalValue.set(FinalValue.get() ^ (1 << N) << FlagShift)

        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    for i, Var in enumerate(FlagVarsB):
        if i < 4:
            R = 0
        else:
            R = 1
            
        C = i % 4
        ttk.Checkbutton(FrameE, text = FlagListB[i], variable = FlagVarsB[i], command = lambda i = i: SetFlagB(i, FlagVarsB[i])).grid(row = R, column = C, padx = 10, pady = 5, sticky = "w")

#------------------------------------------------------------
# Multi-Flag + Combobox
#------------------------------------------------------------
"""
-------------------------------------------------------------
This function is for helpers which have multiple Flags that
the user can select any number of, plus one combobox.
-------------------------------------------------------------
"""
def MultiFlagOneBox(WidgetFrame, String, FlagList, FlagLabel, LabelText, BoxList, FlagShift, FinalValue, Changed, Width = 13):
    FrameA = tk.Frame(WidgetFrame, bg = "Black")
    FrameB = tk.Frame(WidgetFrame, bg = "Black")
    FrameC = tk.Frame(WidgetFrame, bg = "Black")
    FrameD = tk.Frame(WidgetFrame, bg = "Black")

    FrameA.pack()
    FrameB.pack(pady = (10,0))
    FrameC.pack()
    FrameD.pack()

    FinalValueLabel = ttk.Label(FrameA, text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())), font = ("Courier", SmallSize, "bold"))
    FinalValueLabel.pack(side = "top")

    FlagVars = [tk.IntVar(value = 0) for i in range(len(FlagList))]

    BoxVar = tk.StringVar()
    BoxVar.set(BoxList[0])

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

    def SetVariable():
        for i, Name in enumerate(BoxList):
            if BoxVar.get() == Name:
                BottomHalf = ~ ((255 >> FlagShift) << FlagShift) & FinalValue.get()
                FinalValue.set(i << FlagShift | BottomHalf)

                break

        FinalValueLabel.configure(text = "Argument Value: {} ({})".format(FinalValue.get(), hex(FinalValue.get())))
        Changed.set(True)

    VarLabel = ttk.Label(FrameD, text = LabelText, font = ("Courier", SmallSize)) 
    VarPicker = ttk.Combobox(FrameD, textvariable = BoxVar, width = Width, values = BoxList, font = ("Courier", SmallSize))
    VarPicker.bind("<<ComboboxSelected>>", lambda _: SetVariable())

    VarLabel.pack(side = "left")
    VarPicker.pack(side = "left")

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
# Future Turns
#------------------------------------------------------------
def FutureTurnsFunction(WidgetFrame, Args, FinalValue, Changed):
    StringA = "The {} in {}-{} turns, including this one.".format(Args[2], Args[0], "{}")
    StringB = "The {} in {} turns, including this one.".format(Args[2], "{}")
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
    Types = list(TypeConversion.keys())
    SingleComboBox(WidgetFrame, Args[0], "Type:", Types, FinalValue, Changed)

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

    if Args[1] == 0: # Use Flags
        MultiFlagList(WidgetFrame, String, Statuses, "Options:", FinalValue, Changed)
        
    if Args[1] == 1: # Use Single Combo box
        SingleComboBox(WidgetFrame, String, "Status:", Statuses, FinalValue, Changed)

#------------------------------------------------------------
# Major Status + Recoil Helper
#------------------------------------------------------------
def RecoilStatusArgument(WidgetFrame, Args, FinalValue, Changed):
    Text = "The User will take 1/{} of {} as Recoil\nand give the Target the {} Status.".format({}, Args[0], {})
    Statuses = ["Sleep", "Poison", "Burn", "Freeze", "Paralysis", "Bad Poison", "Confusion", "Infatuation"]
    AmountEntryOneComboBox(WidgetFrame, Statuses, Text, Text, "Status:", "Denominator:", [], 1, 31, 13, 2, FinalValue, Changed, FlagList = [224, 31, 5])

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
        SingleComboBox(WidgetFrame, String, "Weather:", Weathers, FinalValue, Changed)

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
            StringList = ["The User will copy the Target's Ability.",
                          "The User and their Partner will copy the Target's Ability.",
                          "The Target will copy the User's Ability.",
                          "The Target and their Partner will copy the User's Ability."]
            FlagList = ["Use Partner Too", "Switch Order"]
            FlagBits = [0, 1]
            MakeTwoFlags(WidgetFrame, StringList, FinalValue, Changed, FlagList, FlagBits)

        case 13: # Ability Replace
            String = "The Target's Ability will be replaced with {}."
            SingleComboBoxWithSearch(WidgetFrame, String, "Ability:", list(AbilityList.keys()), FinalValue, Changed)

        case 14: # Revival
            String = "{} Pokemon on the User's Party will be Revived."
            Options = ["A Random", "A Chosen", "All"]
            SingleComboBox(WidgetFrame, String, "Options:", Options, FinalValue, Changed)

        case 15: # Script 46
            StringList = ["The Target will have their Ability nullified for {} turns.",
                          "The Target will have their Ability nullified for {} turns\nif the User moved before them.",
                          "The Target will have their Ability nullified for between\n1-{} turns.",
                          "The Target will have their Ability nullified for between\n1-{} turns if the User moved before them."]
            FlagList = ["User Moved First?", "Random?"]
            FlagBits = [4, 5]
            AmountEntryTwoFlags(WidgetFrame, StringList, "Turns:", FinalValue, Changed, FlagList, FlagBits, 1, 15, 3)

        case 16: # Script A9
            StringList = ["The User will steal the Target's positive Stat Stages.",
                          "The User will steal the Target's negative Stat Stages.",
                          "The Target will steal the User's positive Stat Stages.",
                          "The Target will steal the User's negative Stat Stages."]
            FlagList = ["Negative", "Switch Order"]
            FlagBits = [0, 1]
            MakeTwoFlags(WidgetFrame, StringList, FinalValue, Changed, FlagList, FlagBits)

        case 17: # Imprison
            String = "The Target will be Imprisoned by the following Pokemon."
            Targets = ["User", "User's Partner", "Target's Partner"]
            MultiFlagList(WidgetFrame, String, Targets, "Target Options:", FinalValue, Changed)
    
    
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
    StringList = [Args[0].format("User and Target", "{}", "{}"), Args[0].format("Target", "{}", "{}")]
    Stats = ["HP", "Attack", "Defence", "Sp. Attack", "Sp. Defence", "Speed"]
    TwoComboBoxesOneFlag(WidgetFrame, "User = Target?", "Stat 1:", "Stat 2:", Stats, Stats, FinalValue, Changed, StringList, Width = 13, FlagBits = [56, 7, 3, 6])

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
    Types = list(TypeConversion.keys())
    Stats = ["Attack", "Defence", "Speed", "Sp. Attack", "Sp. Defence", "Accuracy", "Evasion"]
    TwoComboBoxes(WidgetFrame, String, "Type:", "Stat:", Types, Stats, FinalValue, Changed, StringList = None, Width = 13, FlagBits = [224, 31, 5])

#------------------------------------------------------------
# Status + Type
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper is for Move Scripts which take a Type and a
Major Status as an argument.
-------------------------------------------------------------
"""
def StatusAndType(WidgetFrame, Args, FinalValue, Changed):
    String = Args[0]
    Types = list(TypeConversion.keys())
    Statuses = ["Sleep", "Poison", "Burn", "Freeze", "Paralysis", "Bad Poison", "Confusion", "Infatuation"]
    TwoComboBoxes(WidgetFrame, String, "Type:", "Stat:", Types, Statuses, FinalValue, Changed, StringList = None, Width = 13, FlagBits = [224, 31, 5])


#------------------------------------------------------------
# Stats + Status
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
# Stats + Status II
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper is for Move Scripts which take a Type and a Stat
as an argument.
-------------------------------------------------------------
"""
def StatAndStatusII(WidgetFrame, Args, FinalValue, Changed):
    String = Args[0]
    Statuses = ["Sleep", "Poison", "Burn", "Freeze", "Paralysis", "Bad Poison", "Confusion", "Infatuation"]
    Stats = ["Attack", "Defence", "Speed", "Sp. Attack", "Sp. Defence"]
    MultiFlagOneBox(WidgetFrame, String, Stats, "Stats", "Status:", Statuses, 5, FinalValue, Changed)

#------------------------------------------------------------
# Trap Flags
#------------------------------------------------------------
"""
-------------------------------------------------------------
This helper is for Trap Flag scripts.
-------------------------------------------------------------
"""
def TrapFlagTargets(WidgetFrame, Args, FinalValue, Changed):
    String = "The {} Flag will be set on the Target\nand on the other given targets.\nIt will disappear when any of them leave the field.".format(Args[0])
    Targets = ["User", "User's Partner", "Target's Partner"]
    MultiFlagList(WidgetFrame, String, Targets, "Target Options:", FinalValue, Changed)
    
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

            case "Future": # Future effect helper
                FutureTurnsFunction(WidgetFrame, Args, FinalValue, Changed)

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

            case "StatStatus2":
                StatAndStatusII(WidgetFrame, Args, FinalValue, Changed)

            case "PercentStatus":
                RecoilStatusArgument(WidgetFrame, Args, FinalValue, Changed)

            case "TrapTarget":
                TrapFlagTargets(WidgetFrame, Args, FinalValue, Changed)

            case "StatusType":
                StatusAndType(WidgetFrame, Args, FinalValue, Changed)

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

"""
================================================================================================
TABLE FUNCTION BUTTON - These are the functions called by the Table Function Button
================================================================================================
"""
# -------------------------------------------------------
# Randomise Move Names Function
# -------------------------------------------------------    
def RandomiseMoveNames():
    global Table

    StartingWords = ["Fire", "Mighty", "Thunder", "Cold", "Ice",
                     "Drain", "Gusty", "Eerie", "Rage", "Boom",
                     "Air", "Spooky", "Time", "Power", "Guard",
                     "Tiny", "Huge", "Fury", "Double", "Body",
                     "Grass", "Poison", "Psy", "Steel", "Fairy",
                     "Spike", "Toxic", "Mind", "Buzz", "Orb",
                     "Magic", "Wonder", "Quick", "Evil", "Bright"]

    EndingWords = ["Fang", "Punch", "Wind", "Kiss", "Whirl",
                   "Tail", "Wing", "Slam", "Slap", "Slash",
                   "Swap", "Boost", "Burst", "Crunch", "Beam",
                   "Kick", "Swipe", "Seed", "Glare", "Voice",
                   "Bop", "Shot", "Blast", "Bolt", "Tear",
                   "Cannon", "Gun", "Dance", "Roar", "Screech",
                   "Room", "Attack", "Tackle", "Spin", "Dash"]

    List = []
    UsedList = []

    for i in range(len(Table)):
        Done = False

        while not Done:
            A = randint(0, 34)
            B = randint(0, 34)
            WordA = StartingWords[A]
            WordB = EndingWords[B]

            if [A,B] not in UsedList and WordA + " " + WordB not in List and WordA + WordB not in List:
                if len(WordA + " " + WordB) < 13:
                    List.append(WordA + " " + WordB)

                elif len(WordA + WordB) < 13:
                    List.append(WordA + WordB)
                
                UsedList.append([A,B])

                Done = True

    for i, Name in enumerate(List):
        Table[i][MoveNameIndex] = Name

    MakeInfoBox(Root, "Success!", "Move Names Changed!",
                ["The Move Names have been changed to randomised names."])

    Refresh()

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)

# -------------------------------------------------------
# Load Custom Move Names Function
# -------------------------------------------------------    
def LoadCustomMoveNames():
    global Table, InitialFolder
    TableNames = [Entry[MoveNameIndex] for Entry in Table]

    NamesFile = fd.askopenfilename(title = "Open Name File", initialdir = InitialFolder, filetypes = [("text files", "*.txt")])
    if NamesFile == "": # Cancelled
        return

    NamesFile = open(NamesFile, "r", encoding = "utf-8")
    InitialFolder = os.path.dirname(os.path.realpath(NamesFile.name))

    NewNames = 0
    for i, Name in enumerate(NamesFile.read().splitlines()):       
        TableNames[i] = Name[0:12] # Names can only be 12 characters long maximum
        NewNames += 1
    
    for i, Name in enumerate(TableNames):
        Table[i][MoveNameIndex] = Name

    match NewNames:
        case _ if NewNames < len(Table):
            MakeInfoBox(Root, "Warning!", "Name File Shorter Than Table",
                        ["The Name File loaded was shorter than the table.",
                         "Names past the length of the file were left unchanged."])

        case _ if NewNames > len(Table):
            MakeInfoBox(Root, "Warning!", "Name File Longer Than Table",
                        ["The Name File loaded was longer than the table.",
                         "Not all names in the file were used."])

        case _:
            MakeInfoBox(Root, "Success!", "Names were loaded",
                        ["All the names were loaded from the file!",
                         "The table now has new Move names."])

    Refresh()

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)

# -------------------------------------------------------
# Move Kind Set Function
# -------------------------------------------------------    
def SetMoveKind(Option):
    global Table

    match Option:
        case "Type":
            PhysicalTypes = ["Normal", "Flying", "Fighting", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel"]
            SpecialTypes = ["Fairy", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark"]

            NoChange = 0
            for i, Entry in enumerate(Table):
                BasePower = Entry[BasePowerIndex]
                Type = Entry[TypeIndex]

                if BasePower == 0: # Status Move
                    Table[i][MoveKindIndex] = "Status"
                    
                else:
                    if Type in PhysicalTypes:
                        Table[i][MoveKindIndex] = "Physical"

                    elif Type in SpecialTypes:
                        Table[i][MoveKindIndex] = "Special"

                    else:
                        NoChange += 1

            if NoChange == 0:
                MakeInfoBox(Root, "Success!", "Move Kinds Changed!",
                            ["The Move Kinds were changed so that Moves",
                             "are Physical or Special based on their Type."])
            else:
                MakeInfoBox(Root, "Success! But...", "Move Kinds Changed!",
                            ["The Move Kinds were changed so that Moves",
                             "are Physical or Special based on their Type.",
                             "However, some Move Kinds could not be changed."])

        case "Contact":
            for i, Entry in enumerate(Table):
                BasePower = Entry[BasePowerIndex]
                MoveFlags = Entry[MoveFlagIndex]
                ContactFlag = MoveFlags[7] # 1 = DC Flag Set

                if BasePower == 0:
                    Table[i][MoveKindIndex] = "Status"

                else:
                    if ContactFlag == 1: # Direct Contact Flag Set
                        Table[i][MoveKindIndex] = "Physical"
                    else:
                        Table[i][MoveKindIndex] = "Special"

            MakeInfoBox(Root, "Success!", "Move Kinds Changed!",
                        ["The Move Kinds were changed so that Moves",
                         "are Physical or Special depending on if they",
                         "make Direct Contact or not."])

    Refresh()

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)

"""
================================================================================================
MAIN PROGRAM - Here's the main event!
================================================================================================
"""
# ------------------------------------------------------------
# Open File Directory - Debug function to open folder containing program
# ------------------------------------------------------------
def OpenFileDirectory():
    CurrentDirectory = os.getcwd()

    if OnAMac:
        call(["open", CurrentDirectory])
    else:
        Popen('explorer "{}"'.format(CurrentDirectory))

# ------------------------------------------------------------
# Convert To Hex - Converts a decimal integer (ex: 10 -> 0A)
# ------------------------------------------------------------
def ConvertToHex(N): # N = decimal integer
    B = hex(N).upper()[2:] # Removes the leading '0x' and makes uppercase

    if N < 16: # Adds a leading zero if it's less than 0x10
        B = "0" + B

    return B

#------------------------------------------------------------
# Convert to 000 - Converts a decimal integer to a three character string
#------------------------------------------------------------
def ConvertToThree(N): # N = decimal integer
    if N < 10:
        return "00" + str(N)

    if N < 100:
        return "0" + str(N)

    return str(N)

# ------------------------------------------------------------
# Create File Bytes - Creates List of Bytes when reading binary files
# ------------------------------------------------------------
def CreateFileBytes(BinFile, N):
    ByteList = []
    Byte = BinFile.read(1)
    while Byte: # While the next byte is valid, do the following
        Value = int(bin(ord(Byte)), 2) # Get binary value and convert to decimal
        Byte = ConvertToHex(Value) # Convert to a hex byte
        ByteList.append(Byte)
        Byte = BinFile.read(1)

    FileBytes = ""
    for i, Byte in enumerate(ByteList): # Group the byte list in groups of N bytes
        if (i+1) % N == 0:
            FileBytes += Byte + "\n"
        else:
            FileBytes += Byte + " "

    return FileBytes

#------------------------------------------------------------
# Sanitise Characters - Removes Forbidden Characters From Text
#------------------------------------------------------------
def SanitiseText(Text):
    AllowedPunctuation = "!?,.'-:"
    NewText = ""
    for Letter in Text:
        if not Letter.isalpha() and not Letter.isdigit() and Letter != " " and Letter != "\n": # Character is punctuation
            if Letter in AllowedPunctuation:
                NewText += Letter
        else:
            NewText += Letter

    return NewText

#------------------------------------------------------------
# Global stuff
#------------------------------------------------------------
Table = []
MoveNameList = []

CurrentOpenFile = ""

#------------------------------------------------------------
# Debug Make Table - Used for testing - disable for release version!
#------------------------------------------------------------
def DebugMakeTable():
    global Table, CurrentOpenFile
    Table = [["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]]
    CurrentOpenFile = os.path.realpath(os.path.join(os.getcwd(), "Test Table.txt"))
    CurrentLabel.configure(text = "Open File: Test Table.txt")
    EnableEverything()
    Refresh()
    SaveFile(Table, CurrentOpenFile, True)

#------------------------------------------------------------
# Make GUI
#------------------------------------------------------------
Root = tk.Tk()
Root.title("Akame's Custom Engine")
Root.resizable(False, False)
Root.configure(bg = "Black")

s = ttk.Style()
s.theme_use('alt')

def GetPath(File):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, File)
    else:
        return File

if not OnAMac:
    Root.iconbitmap(GetPath("ACE.ico"))

# This is what the widgets look like when not disabled
s.configure("TRadiobutton", background = "black", foreground = "white", indicatorcolor = "grey")
s.configure("TCombobox", background = "white", foreground = "black")
s.configure("TMenuButton", background = "white", foreground = "black")
s.configure("TCheckbutton", background = "black", foreground = "white", indicatorcolor = "white", font = ('Courier', SmallSize - 2))
s.configure("TLabel", background = "black", foreground = "white", font = ('Courier', SmallSize, 'bold'))
s.configure("TFrame", background = "black", foreground = "white")
s.configure("TScale", background = "black", foreground = "white")
s.configure("TButton", background = "black", foreground = "white", font = ('Courier', SmallSize, 'bold'))

# This is what the widgets look like when disabled or hovered over (active)
s.map("TRadiobutton", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")], indicatorcolor = [("selected", "yellow")])
s.map("TCombobox", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")])
s.map("TMenuButton", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")])
s.map("TCheckbutton", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")], indicatorcolor = [("selected", "blue")])
s.map("TScale", background = [("active", "black"), ("disabled", "black")], foreground = [("active", "white"), ("disabled", "grey")])
s.map("TButton", background = [("active", "white"), ("disabled", "black")], foreground = [("active", "black"), ("disabled", "grey")])

# -------------------------------------------------------
# Make Frames - These are the main frames
# -------------------------------------------------------    
TopLayerFrame = tk.Frame(Root, bg = "Black")
TopLayerFrame.pack(side = "top", padx = 10, pady = 10)

ButtonFrame = tk.Frame(Root, bg = "Black")
ButtonFrame.pack(fill = "x", padx = 10, pady = 0)

EditorFrame = tk.Frame(Root, bg = "Black")
EditorFrame.pack(side = "left", padx = 10, pady = 10)

#------------------------------------------------------------
# Create Tkinter Variables
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

#------------------------------------------------------------
# Make the Icons at the top of the screen
#------------------------------------------------------------
BulbasaurFrame = tk.Frame(TopLayerFrame, bg = "Black")
IconFrame = tk.Frame(TopLayerFrame, bg = "Black")
TablePicFrame = tk.Frame(TopLayerFrame, bg = "Black")

BulbasaurPic = tk.PhotoImage(file = GetPath("Bulbasaur.png"))
BulbasaurPic = BulbasaurPic.zoom(6)
BulbasaurPic = BulbasaurPic.subsample(5)
BulbasaurLabel = ttk.Label(BulbasaurFrame, image = BulbasaurPic)
BulbasaurLabel.image = BulbasaurPic

TablePic = tk.PhotoImage(file = GetPath("Table.png"))
TablePic = TablePic.subsample(2)
TableLabel = ttk.Label(TablePicFrame, image = TablePic)
TableLabel.image = TablePic

#------------------------------------------------------------
# Make the labels in the middle of the top of the screen
#------------------------------------------------------------
LabelFrame = tk.Frame(IconFrame, bg = "Black")
MenuFrame = tk.Frame(IconFrame, bg = "Black")
MoveFinderFrame = tk.Frame(MenuFrame, bg = "Black")

MainLabel = ttk.Label(LabelFrame, text = "ACE Move Table Maker", font = ("Arial", int(1.5 * SmallSize), "bold"))
CurrentLabel = ttk.Label(MenuFrame, text = "{}".format(CurrentOpenFile))
CopyrightLabel = ttk.Label(LabelFrame, text = "Program by AkameTheBulbasaur, v{}".format(VerNum), font = ("Arial", SmallSize - 2))

MoveNumberLabel = ttk.Label(MenuFrame, text = "Move {} of {}".format(ConvertToThree(CurrentMoveNumber.get() + 1), ConvertToThree(len(Table))))

#------------------------------------------------------------
# Make the auto-save toggle
#------------------------------------------------------------
AutoSaveVar = tk.IntVar(value = 1)

def AutoSaveInfo():
    global AutoSave
    
    if AutoSaveVar.get() == 1:
        AutoSave = True
        MakeInfoBox(Root, "Auto-Save", "Auto-Save is on",
                    ["The human-readable table file will be",
                     "automatically saved when the table is",
                     "modified in the editor or by a function."])
    else:
        AutoSave = False
        MakeInfoBox(Root, "Auto-Save", "Auto-Save is off",
                    ["The human-readable table file will NOT",
                     "be automatically saved!",
                     "Make sure to click the Save Table button",
                     "or your changes will be lost!"])

AutoSaveButton = ttk.Checkbutton(LabelFrame, text = "Auto-Save", variable = AutoSaveVar, command = AutoSaveInfo)

#------------------------------------------------------------
# Make The Shortcut Help Menu
#------------------------------------------------------------
def ShowHelpMenu():
    if OnAMac:
        Mode = "CMD"
    else:
        Mode = "CTRL"

    MakeInfoBox(Root, "Shortcuts", "Shortcut Hotkeys",
                ["{} + N: New File".format(Mode),
                 "{} + O: Open File".format(Mode),
                 "{} + S: Save File".format(Mode),
                 "{} + Shift + S: Save File As".format(Mode),
                 "{} + Shift + X: Convert Table".format(Mode),
                 "{} + Shift + C: Compile Table".format(Mode),
                 "{} + Shift + A: Add Moves".format(Mode),
                 "{} + Shift + D: Delete Move".format(Mode),
                 "{} + Right Arrow: Move Forward".format(Mode),
                 "{} + Left Arrow: Move Backward".format(Mode),
                 "{} + H: Open This Menu".format(Mode),
                 "{} + Q: Quit Program".format(Mode)])

ShowHelp = tk.IntVar()
ShowHelp.set(0)

def DisplayHelp():
    ShowHelp.set(0)
    ShowHelpMenu()

ShowHelpButton = ttk.Checkbutton(MoveFinderFrame, text = "?", variable = ShowHelp, command = DisplayHelp)

#------------------------------------------------------------
# Make the Move Menu - Jump to a particular Move
#------------------------------------------------------------
def JumpToMove():
    # Gets the Move Number
    MoveNumber = int(CurrentMove.get().split("-")[0].strip()) - 1

    CurrentMoveNumber.set(MoveNumber)
    
    if CurrentMoveNumber.get() <= 0: # Disable Back, enable Forward
        BackButton.configure(state = "disabled")
        ForwardButton.configure(state = "normal")

    elif CurrentMoveNumber.get() >= len(Table) - 1: # Disable Forward, enable Back
        BackButton.configure(state = "normal")
        ForwardButton.configure(state = "disabled")

    else:
        BackButton.configure(state = "normal")
        ForwardButton.configure(state = "normal")
        
    Refresh()

def ProcessEntry():
    for i, Entry in enumerate(Table):
        Name = Entry[0].lower()
        if CurrentMove.get().lower() == Name:
            CurrentMove.set("{} - {}".format(ConvertToThree(i + 1), Name))
            JumpToMove()
            break            

MoveFinder = ttk.Combobox(MoveFinderFrame, textvariable = CurrentMove, width = 18, values = MoveNameList, font = ("Courier", SmallSize))
MoveFinder.bind("<<ComboboxSelected>>", lambda _: JumpToMove())
MoveFinder.bind("<Return>", lambda _: ProcessEntry())

#------------------------------------------------------------
# Edit Table Functions Block
#------------------------------------------------------------
TableFunctionFrame = tk.Frame(EditorFrame, bg = "Black")

def OpenTableFunctions():
    Function = tk.StringVar()
    Function.set("None")

    TableFunctions = {"Randomise Move Names":
                      ["Generates randomised, unique names for each Move",
                       "in the current table."],
                      "Load Custom Move Names":
                      ["Load a custom Move Name File for this table."],
                      "Type-Based Move Kind":
                      ["Set the Move Kind based on Type and Base Power",
                       "like they would have been pre-split."],
                      "Contact-Based Move Kind":
                      ["Set the Move Kind based on whether the Direct",
                       "Contact Flag is set.",
                       "This is a type of auto-DPSS."]}

    MakeMultiChoiceBox(Root, "Table Functions", "Choose A Function", Function,
                        ["You can run a function on the whole table",
                         "by choosing one from the menu below."],
                        TableFunctions, "Randomise Move Names")

    if Function.get() != "None":
        match Function.get():
            case "Randomise Move Names":
                RandomiseMoveNames()

            case "Load Custom Move Names":
                LoadCustomMoveNames()
                
            case "Type-Based Move Kind":
                SetMoveKind("Type")

            case "Contact-Based Move Kind":
                SetMoveKind("Contact")

TableFunctionButton = ttk.Button(TableFunctionFrame, text = "Table Functions", command = OpenTableFunctions)

#------------------------------------------------------------
# Edit Move Name Block
#------------------------------------------------------------
MoveNameFrame = tk.Frame(EditorFrame, bg = "Black")

def SanitiseName(Text):
    if MoveNameEntry.cget('state') == "normal" and not MoveNameEntry.tag_ranges("sel"):
        NewText = SanitiseText(Text)
        MoveNameEntry.delete(1.0, "end-1c")
        MoveNameEntry.insert(1.0, NewText)
        EditName(NewText)

def EditName(Name):
    if MoveNameEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        Name = Name[0:12]
        Table[i][MoveNameIndex] = Name
        
        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)

MoveNameLabel = ttk.Label(MoveNameFrame, text = "Move Name:")
MoveNameEntry = tk.Text(MoveNameFrame, width = 12, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
MoveNameEntry.bind("<KeyRelease>", (lambda _: SanitiseName(MoveNameEntry.get(1.0, "end-1c"))))
MoveNameEntry.bind(Paste, (lambda _: SanitiseName(MoveNameEntry.get(1.0, "end-1c"))))

# Move Name Help Menu
NameHelp = tk.IntVar()
NameHelp.set(0)

def MoveNameHelp():
    NameHelp.set(0)
    MakeInfoBox(Root, "Help", "Move Name", \
                ["This is the name of the Move.",
                 "This does not appear in the compiled Attack Data Table.",
                 "Instead, Move Names are compiled to a separate Move Name Table."])

MoveNameHelpButton = ttk.Checkbutton(MoveNameFrame, text = "?", variable = NameHelp, command = MoveNameHelp)

#------------------------------------------------------------
# Auto Move Filler Block
#------------------------------------------------------------
AutoFillMoveFrame = tk.Frame(EditorFrame, bg = "Black")

def AutoFillMove():
    PickedMove = tk.StringVar()
    PickedMove.set("None")
    MakeInfoBoxMenuSearch(Root, "Auto-Filler", "Auto-Fill Moves",
                        ["You may pick a Move from the dropdown list",
                         "and the program will automatically fill in the",
                         "current entry in the table with its values.",
                         "NOTE: Some newer Moves have names longer than",
                         "12 characters, so those Moves have a default",
                         "shorter name that will be filled in instead."],
                        AutoFillList, PickedMove, "None")

    if PickedMove.get() != "None":
        global Table
        Table[CurrentMoveNumber.get()] = PresetMoveList[PickedMove.get()]

        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)

AutoFillMoveButton = ttk.Button(AutoFillMoveFrame, text = "Move Auto-Filler", command = AutoFillMove)

#------------------------------------------------------------
# Edit Move Script Block
#------------------------------------------------------------
MoveScriptFrame = tk.Frame(EditorFrame, bg = "Black")

def EditMoveScript():
    global Table
    i = CurrentMoveNumber.get()

    Table[i][MoveScriptIndex] = MoveScript.get()

    Refresh()

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)

def ProcessMoveScript():
    Input = MoveScript.get().upper()
    Hex = "0123456789ABCDEF"
    
    for Letter in Hex:
        if Input == Letter:
            MoveScript.set("0" + Letter)
            EditMoveScript()

    if Input in HexBytes:
        MoveScript.set(Input)
        EditMoveScript()

MoveScriptLabel = ttk.Label(MoveScriptFrame, text = "Move Script:")
MoveScriptEntry = ttk.Combobox(MoveScriptFrame, textvariable = MoveScript, width = 2, values = HexBytes, font = ("Courier", SmallSize))
MoveScriptEntry.bind("<<ComboboxSelected>>", lambda _: EditMoveScript())
MoveScriptEntry.bind("<Return>", lambda _: ProcessMoveScript())

# Move Script Help Menu
ScriptHelp = tk.IntVar()
ScriptHelp.set(0)

def MoveScriptHelp():
    ScriptHelp.set(0)

    NewValue = tk.StringVar()
    NewValue.set("None")
    MakeInfoBoxMenuSearch(Root, "Help", "Move Scripts",
                        ["The Move Script is a Battle Script that is specifically",
                         "executed by a Move when it is selected in battle.",
                         "Select a script from the dropdown menu to see what it does.",
                         "Note: these are the defaults for ACE, your scripts may vary."],
                        MoveScriptText, NewValue, "Script {}".format(MoveScript.get()), MoveScriptTagsList)

    if NewValue.get() != "None":
        MoveScript.set(NewValue.get().replace("Script", "").strip())
        EditMoveScript()

MoveScriptHelpButton = ttk.Checkbutton(MoveScriptFrame, text = "?", variable = ScriptHelp, command = MoveScriptHelp)

#------------------------------------------------------------
# Edit Base Power Block
#------------------------------------------------------------
BasePowerFrame = tk.Frame(EditorFrame, bg = "Black")

def EditBasePower(Power):
    if BasePowerEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            Power = int(Power)
        except Exception as e:
            PrintError(e)
            Power = 0

        if Power > 255:
            Power = 255

        if Power < 0:
            Power = 0

        Table[i][BasePowerIndex] = Power
        
        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)

BasePowerLabel = ttk.Label(BasePowerFrame, text = "Base Power:")
BasePowerEntry = tk.Text(BasePowerFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
BasePowerEntry.bind("<KeyRelease>", (lambda _: EditBasePower(BasePowerEntry.get(1.0, "end-1c"))))

# Base Power Help Menu
PowerHelp = tk.IntVar()
PowerHelp.set(0)

def BasePowerHelp():
    PowerHelp.set(0)
    MakeInfoBox(Root, "Help", "Base Power",
                ["The Base Power of a Move generally indicates its strength.",
                 "This value can range from 0 to 255.",
                 "Setting this value to zero means the Move is Non-Damaging."])

BasePowerHelpButton = ttk.Checkbutton(BasePowerFrame, text = "?", variable = PowerHelp, command = BasePowerHelp)

#------------------------------------------------------------
# Edit Move Type Block
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

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)
    
TypeLabel = ttk.Label(TypeFrame, text = "Type:")
TypeEntry = ttk.Combobox(TypeFrame, textvariable = Type, width = 8, values = Types, font = ("Courier", SmallSize))
TypeEntry.bind("<<ComboboxSelected>>", EditType)

TypeHelp = tk.IntVar()
TypeHelp.set(0)

# Type Help Menu
def MoveTypeHelp():
    TypeHelp.set(0)
    MakeInfoBox(Root, "Help", "Move Type",
                ["This is the base Type of the Move."
                 "The actual Type when used in Battle may be different,"
                 "but will, by default, be the one given here."])

TypeHelpButton = ttk.Checkbutton(TypeFrame, text = "?", variable = TypeHelp, command = MoveTypeHelp)

#------------------------------------------------------------
# Edit Accuracy Block
#------------------------------------------------------------
AccuracyFrame = tk.Frame(EditorFrame, bg = "Black")

def EditAccuracy(Accuracy):
    if AccuracyEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            Accuracy = int(Accuracy)
        except Exception as e:
            PrintError(e)
            Accuracy = 0

        if Accuracy > 100:
            Accuracy = 100

        if Accuracy < 0:
            Accuracy = 0

        Table[i][AccuracyIndex] = Accuracy
        
        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)
    
AccuracyLabel = ttk.Label(AccuracyFrame, text = "Accuracy:")
AccuracyEntry = tk.Text(AccuracyFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
AccuracyEntry.bind("<KeyRelease>", (lambda _: EditAccuracy(AccuracyEntry.get(1.0, "end-1c"))))

# Accuracy Help Menu
AccHelp = tk.IntVar()
AccHelp.set(0)

def AccuracyHelp():
    AccHelp.set(0)
    MakeInfoBox(Root, "Help", "Accuracy",
                ["This is the base Accuracy of the Move.",
                 "This value can range from 0 to 100.",
                 "A higher Accuracy means the Move will hit more often.",
                 "An Accuracy of 0 means the Move bypasses Accuracy checks."])

AccuracyHelpButton = ttk.Checkbutton(AccuracyFrame, text = "?", variable = AccHelp, command = AccuracyHelp)

#------------------------------------------------------------
# Edit Power Points Block
#------------------------------------------------------------
PowerPointFrame = tk.Frame(EditorFrame, bg = "Black")

def EditPowerPoints(PowerPoints):
    if PowerPointEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            PowerPoints = int(PowerPoints)
        except Exception as e:
            PrintError(e)
            PowerPoints = 0

        if PowerPoints > 99:
            PowerPoints = 99

        if PowerPoints < 0:
            PowerPoints = 0

        Table[i][PowerPointIndex] = PowerPoints
        
        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)
    
PowerPointLabel = ttk.Label(PowerPointFrame, text = "Power Points:")
PowerPointEntry = tk.Text(PowerPointFrame, width = 2, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
PowerPointEntry.bind("<KeyRelease>", (lambda _: EditPowerPoints(PowerPointEntry.get(1.0, "end-1c"))))

# Power Point Help Menu
PPHelp = tk.IntVar()
PPHelp.set(0)

def PowerPointHelp():
    PPHelp.set(0)
    MakeInfoBox(Root, "Help", "Power Points",
                ["This is the default amount of Power Points that the Move can have.",
                 "This value can range from 0 to 99.",
                 "More Power Points means the Move can be used more.",
                 "This does not include the amount added by using Items such as PPUp or PPMax."])

PowerPointHelpButton = ttk.Checkbutton(PowerPointFrame, text = "?", variable = PPHelp, command = PowerPointHelp)

#------------------------------------------------------------
# Edit Effect Chance Block
#------------------------------------------------------------
EffectChanceFrame = tk.Frame(EditorFrame, bg = "Black")

def EditEffectChance(Chance):
    if EffectChanceEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            Chance = int(Chance)
        except Exception as e:
            PrintError(e)
            Chance = 0

        if Chance > 100:
            Chance = 100

        if Chance < 0:
            Chance = 0

        Table[i][EffectChanceIndex] = Chance
        
        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)
    
EffectChanceLabel = ttk.Label(EffectChanceFrame, text = "Effect Chance:")
EffectChanceEntry = tk.Text(EffectChanceFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
EffectChanceEntry.bind("<KeyRelease>", (lambda _: EditEffectChance(EffectChanceEntry.get(1.0, "end-1c"))))

# Effect Chance Help Menu
ChanceHelp = tk.IntVar()
ChanceHelp.set(0)

def EffectChanceHelp():
    ChanceHelp.set(0)
    MakeInfoBox(Root, "Help", "Effect Chance",
                ["This is the chance of the Move Script's effect activating (if it has one).",
                 "This values ranges from 0 to 100.",
                 "A higher value means the effect will occur more often.",
                 "Setting this to zero makes the effect always activate."])

EffectChanceHelpButton = ttk.Checkbutton(EffectChanceFrame, text = "?", variable = ChanceHelp, command = EffectChanceHelp)

#------------------------------------------------------------
# Edit Attack Range Block
#------------------------------------------------------------
RangeList = ["Target", "User", "Partner", "Foe Side", "My Side", "All But User", "Everyone", "Random", "Last Attacker", "User + Partner", "Target + Partner"]

RangeFrame = tk.Frame(EditorFrame, bg = "Black")

def EditRange(self):
    global Table
    i = CurrentMoveNumber.get()

    Table[i][RangeIndex] = Range.get()

    Refresh()

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)
    
RangeLabel = ttk.Label(RangeFrame, text = "Range:")
RangeEntry = ttk.Combobox(RangeFrame, textvariable = Range, width = 16, values = RangeList, font = ("Courier", SmallSize))
RangeEntry.bind("<<ComboboxSelected>>", EditRange)

# Range Help Menu
RHelp = tk.IntVar()
RHelp.set(0)

def RangeHelp():
    RHelp.set(0)
    MakeInfoBox(Root, "Help", "Range",
                ["This is the range of Pokemon who can be targeted by the Move.",
                 "Moves can be Single-Target or Spread Moves.",
                 "A Single-Target Move allows the Player to select one target out",
                 "of the options available.",
                 "A Spread Move will run the Move Script once for all of the",
                 "selected Pokemon (if they are available on the field).",
                 "A Move which sets a Global Flag or a Team Flag (i.e Safeguard)",
                 "should be set as a Single-Target Move, since the Flag is only",
                 "set once.\n",
                 "User = Single-Target, can only selected themselves",
                 "Target = Single-Target, can select any Pokemon other than themselves.",
                 "User + Partner = Single-Target, can select themselves or their Partner",
                 "Target + Partner = Single-Target, can select either opposing Pokemon.",
                 "My Side = Spread, affects both the User and Partner at once.",
                 "Foe Side = Spread, affects both opposing Pokemon at once.",
                 "All But User = Spread, affects all Pokemon except for the User.",
                 "Everyone = Spread, affects all Pokemon on the field at once.",
                 "Last Attacker = Single-Target, automatically selects the",
                 "last Pokemon to attack the User."
                 "Random = Single-Target, automatically selects a random Pokemon",
                 "from the ones available other than the User."])

RangeHelpButton = ttk.Checkbutton(RangeFrame, text = "?", variable = RHelp, command = RangeHelp)

#------------------------------------------------------------
# Edit Priority Block
#------------------------------------------------------------
PriorityFrame = tk.Frame(EditorFrame, bg = "Black")

def EditPriority(Priority):
    if PriorityEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()
        
        try:
            Priority = int(Priority)
        except Exception as e:
            PrintError(e)
            Priority = 0

        if Priority > 127:
            Priority = 127

        if Priority < 0:
            Priority = 0

        if Parity.get() == 1: # Negative Priority
            Priority = -Priority

        Table[i][PriorityIndex] = Priority
        
        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)
    
PriorityLabel = ttk.Label(PriorityFrame, text = "Priority:")
PriorityEntry = tk.Text(PriorityFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
PriorityEntry.bind("<KeyRelease>", (lambda _: EditPriority(PriorityEntry.get(1.0, "end-1c"))))

# Priority Help Menu
PriHelp = tk.IntVar()
PriHelp.set(0)

def PriorityHelp():
    PriHelp.set(0)
    MakeInfoBox(Root, "Help", "Priority",
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
        Table[i][PriorityIndex] = -Table[i][PriorityIndex]
        
    else:
        ParityButton.configure(text = "+")
        Parity.set(0)
        Table[i][PriorityIndex] = -Table[i][PriorityIndex]

    Refresh()

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)

ParityButton = ttk.Checkbutton(PriorityFrame, text = "+", variable = X, command = EditParity)

#------------------------------------------------------------
# Edit Move Flags Block
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

# Move Flag Help Menu
FlagHelp = tk.IntVar()
FlagHelp.set(0)

def MoveFlagHelp():
    FlagHelp.set(0)
    MakeInfoBox(Root, "Help", "Move Flags",
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
# Edit Damage Formula Block
#------------------------------------------------------------
DamageFormulaFrame = tk.Frame(EditorFrame, bg = "Black")

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

    Table[i][DamageFormulaIndex] = DamageValue

    Refresh()

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)

def ProcessDamageFormula():
    Input = DamageFormula.get().upper()
    Hex = "0123456789ABCDEF"
    
    for Letter in Hex:
        if Input == Letter:
            DamageFormula.set("0" + Letter)
            EditDamageFormula()

    if Input in HexBytes:
        DamageFormula.set(Input)
        EditDamageFormula()

DamageFormulaLabel = ttk.Label(DamageFormulaFrame, text = "Damage Formula:")
DamageFormulaEntry = ttk.Combobox(DamageFormulaFrame, textvariable = DamageFormula, width = 2, values = HexHalfBytes, font = ("Courier", SmallSize))
DamageFormulaEntry.bind("<<ComboboxSelected>>", lambda _: EditDamageFormula())
DamageFormulaEntry.bind("<Return>", lambda _: ProcessDamageFormula())

# Damage Formula Help Menu
FormulaHelp = tk.IntVar()
FormulaHelp.set(0)

def DamageFormulaHelp():
    FormulaHelp.set(0)

    NewValue = tk.StringVar()
    NewValue.set("-")
    MakeInfoBoxMenuSearch(Root, "Help", "Damage Formula",
                        ["The damage formula is used to determine the Base Power",
                         "the of the Move.",
                         "If this is set to anything other than zero, then the",
                         "game will run an additional routine to find the true",
                         "Base Power, which may use the Base Power given here."],
                        DamageFormulaText, NewValue, "Formula {}".format(DamageFormula.get()), DamageFormulaTagsList)
    
    if NewValue.get() != "-":
        DamageFormula.set(NewValue.get().replace("Formula", "").strip())
        EditDamageFormula()

DamageFormulaHelpButton = ttk.Checkbutton(DamageFormulaFrame, text = "?", variable = FormulaHelp, command = DamageFormulaHelp)

#------------------------------------------------------------
# Edit Damage Formula Argument Block
#------------------------------------------------------------
DamageArgumentFrame = tk.Frame(EditorFrame, bg = "Black")

def ProcessDamageArgument():
    Input = DamageArgument.get().upper()
    Hex = "0123456789ABCDEF"
    
    for Letter in Hex:
        if Input == Letter:
            DamageArgument.set("0" + Letter)
            EditDamageFormula()

    if Input in HexBytes:
        DamageArgument.set(Input)
        EditDamageFormula()

DamageArgumentLabel = ttk.Label(DamageArgumentFrame, text = "Formula Argument:")
DamageArgumentEntry = ttk.Combobox(DamageArgumentFrame, textvariable = DamageArgument, width = 2, values = HexHalfBytes, font = ("Courier", SmallSize))
DamageArgumentEntry.bind("<<ComboboxSelected>>", lambda _: EditDamageFormula())
DamageArgumentEntry.bind("<Return>", lambda _: ProcessDamageArgument())

# Damage Formula Argument Help Menu
FormulaArgHelp = tk.IntVar()
FormulaArgHelp.set(0)

def DamageFormulaArgHelp():
    FormulaArgHelp.set(0)
    Text = ""
    FormulaOption = FormulaArgumentHelpers[DamageFormula.get()][0]
    FormulaOptionArgs = FormulaArgumentHelpers[DamageFormula.get()][1]

    NewValue = tk.StringVar()
    NewValue.set("None")
    MakeFormulaArgHelperBox(Root, "Help", "Damage Formula Argument",
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
# Edit Move Kind Block
#------------------------------------------------------------
MoveKindFrame = tk.Frame(EditorFrame, bg = "Black")

Kinds = ["Physical", "Special", "Status"]

def EditMoveKind(self):
    global Table
    i = CurrentMoveNumber.get()

    Table[i][MoveKindIndex] = MoveKind.get()

    Refresh()

    if AutoSave:
        SaveFile(Table, CurrentOpenFile, True)
    
MoveKindLabel = ttk.Label(MoveKindFrame, text = "Move Kind:")
MoveKindEntry = ttk.Combobox(MoveKindFrame, textvariable = MoveKind, width = 8, values = Kinds, font = ("Courier", SmallSize))
MoveKindEntry.bind("<<ComboboxSelected>>", EditMoveKind)

# Move Kind Help Menu
KindHelp = tk.IntVar()
KindHelp.set(0)

def MoveKindHelp():
    KindHelp.set(0)
    MakeInfoBox(Root, "Help", "Move Kind",
                ["The Move Kind determines whether the Move is Physical, Special or Status.",
                 "Physical: Uses Attack/Defence when calculating Damage",
                 "Special: Uses Sp. Attack/Sp. Defence when calculating Damage",
                 "Status: Does not deal direct damage."])

MoveKindHelpButton = ttk.Checkbutton(MoveKindFrame, text = "?", variable = KindHelp, command = MoveKindHelp)

#------------------------------------------------------------
# Edit Script Argument Block
#------------------------------------------------------------
ScriptArgFrame = tk.Frame(EditorFrame, bg = "Black")

def EditScriptArg(Argument):
    if ScriptArgEntry.cget('state') == "normal":
        global Table
        i = CurrentMoveNumber.get()

        try:
            Argument = int(Argument)
        except Exception as e:
            PrintError(e)
            Argument = 0

        if Argument > 255:
            Argument = 255

        if Argument < 0:
            Argument = 0

        Table[i][ScriptArgIndex] = Argument

        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)
    
ScriptArgLabel = ttk.Label(ScriptArgFrame, text = "Script Argument:")
ScriptArgEntry = tk.Text(ScriptArgFrame, width = 3, height = 1, bg = "White", fg = "Black", font = ("Courier", SmallSize))
ScriptArgEntry.bind("<KeyRelease>", lambda _: EditScriptArg(ScriptArgEntry.get(1.0, "end-1c")))

# Script Argument Help Menu
ArgHelp = tk.IntVar()
ArgHelp.set(0)

def ScriptArgHelp():
    ArgHelp.set(0)

    Text = ""
    ScriptOption = ScriptArgumentHelpers[MoveScript.get()][0]
    ScriptOptionArgs = ScriptArgumentHelpers[MoveScript.get()][1]

    NewValue = tk.StringVar()
    NewValue.set("None")
    MakeScriptArgHelperBox(Root, "Help", "Script Argument",
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
# Table Entry Hex Viewer
#------------------------------------------------------------
TableHexFrame = tk.Frame(EditorFrame, bg = "Black")
TableHexLabel = ttk.Label(TableHexFrame, text = "Hex Viewer")

HexBytesize = 20
HexByteHSpace = 5
HexByteVSpace = 5

HexViewFrame = tk.Frame(EditorFrame, bg = "Black")
MoveScriptByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
BasePowerByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
TypeByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
AccuracyByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
PowerPointByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
EffectChanceByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
RangeByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
PriorityByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
MoveFlagsByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
DamageFormulaByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
MoveKindByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))
ScriptArgByte = ttk.Label(HexViewFrame, text = "00", font = ("Monaco", HexBytesize))

# Hex Viewer Help Menu
HexHelp = tk.IntVar()
HexHelp.set(0)

def HexViewerHelp():
    HexHelp.set(0)
    MakeInfoBox(Root, "Help", "Hex Viewer",
                ["This area shows what the compiled entry looks like in hexadecimal.",
                 "If a byte cannot be properly loaded/compiled, it will show up red."])

HexHelpButton = ttk.Checkbutton(TableHexFrame, text = "?", variable = HexHelp, command = HexViewerHelp)

#------------------------------------------------------------
# Move Description Editor - Max 4 lines, 19 letters per line
#------------------------------------------------------------
"""
-------------------------------------------------------------
Each line is truncated at 19 characters. If more than this
amount is entered, the extra characters are moved to the
next line. This does not have word wrapping.

If more than 19 characters are entered in the 4th line, it
will delete them and you will not be able to enter any more.
-------------------------------------------------------------
"""
DescriptionLabelFrame = tk.Frame(EditorFrame, bg = "Black")
DescriptionLabel = ttk.Label(DescriptionLabelFrame, text = "Move Description")

# Sanitise Description - Remove Forbidden Characters
def SanitiseDescription(Text):
    if DescriptionBox.cget('state') == "normal" and not DescriptionBox.tag_ranges("sel"):
        NewText = SanitiseText(Text)
        ProcessText(NewText)

# Process Description Text - Split NewLines + Truncate
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

        if len(Line1) > 20: # bleeds into the next line        
            Line2 = Line1[20:] + Line2
            Line1 = Line1[0:20]

        if len(Line2) > 20:
            Line3 = Line2[20:] + Line3
            Line2 = Line2[0:20]

        if len(Line3) > 20:
            Line4 = Line3[20:] + Line4
            Line3 = Line3[0:20]

        if len(Line4) > 20:
            Line4 = Line4[0:20]
            Lines.append(Line4[20:])

        Lines[0] = Line1
        Lines[1] = Line2
        Lines[2] = Line3
        Lines[3] = Line4

        NewText = "{}\n{}\n{}\n{}".format(Line1, Line2, Line3, Line4)

        OldText = DescriptionBox.get(1.0, "end-1c")
                     
        Table[CurrentMoveNumber.get()][DescriptionIndex] = NewText
        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)

TextBoxFrame = tk.Frame(EditorFrame, bg = "Black")
DescriptionBox = tk.Text(TextBoxFrame, width = 20, height = 4, bg = "White", fg = "Black", font = ("Courier", SmallSize))
DescriptionBox.bind("<KeyRelease>", (lambda _: SanitiseDescription(DescriptionBox.get(1.0, "end-1c"))))
DescriptionBox.bind(Paste, (lambda _: SanitiseDescription(DescriptionBox.get(1.0, "end-1c"))))

# Move Description Help Menu
DHelp = tk.IntVar()
DHelp.set(0)

def DescriptionHelp():
    DHelp.set(0)
    MakeInfoBox(Root, "Help", "Move Description",
                ["This is the description of the Move seen in the Move Viewer in game.",
                 "This can be up to four lines long, with 20 characters per line.",
                 "The Move Description is compiled into a separate table."])

DescriptionHelpButton = ttk.Checkbutton(DescriptionLabelFrame, text = "?", variable = DHelp, command = DescriptionHelp)

#------------------------------------------------------------
# Update Hex Viewer Function
#------------------------------------------------------------
def CompileToHexViewer():
    try:
        MoveScriptByte.configure(text = MoveScript.get(), foreground = "White")
    except Exception as e:
        PrintError(e)
        MoveScriptByte.configure(text = "00", foreground = "Red")

    try:
        BasePowerByte.configure(text = ConvertToHex(BasePower.get()), foreground = "White")
    except Exception as e:
        PrintError(e)
        BasePowerByte.configure(text = "00", foreground = "Red")

    try:
        TypeByte.configure(text = TypeConversion[Type.get()], foreground = "White")
    except Exception as e:
        PrintError(e)
        TypeByte.configure(text = "00", foreground = "Red")

    try:
        AccuracyByte.configure(text = ConvertToHex(Accuracy.get()), foreground = "White")
    except Exception as e:
        PrintError(e)
        AccuracyByte.configure(text = "00", foreground = "Red")

    try:
        PowerPointByte.configure(text = ConvertToHex(PowerPoints.get()), foreground = "White")
    except Exception as e:
        PrintError(e)
        PowerPointByte.configure(text = "00", foreground = "Red")

    try:
        EffectChanceByte.configure(text = ConvertToHex(EffectChance.get()), foreground = "White")
    except Exception as e:
        PrintError(e)
        EffectChanceByte.configure(text = "00", foreground = "Red")

    try:
        RangeByte.configure(text = RangeConversion[Range.get()], foreground = "White")
    except Exception as e:
        PrintError(e)
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
        PrintError(e)
        PriorityByte.configure(text = "00", foreground = "Red")

    try:
        MoveFlags = [A.get(), B.get(), C.get(), D.get(), E.get(), F.get(), G.get(), H.get()]

        FlagLine = 0
        for i, Flag in enumerate(MoveFlags):
            FlagLine += (128 // 2**i) * Flag
        
        MoveFlagsByte.configure(text = ConvertToHex(FlagLine), foreground = "White")
    except Exception as e:
        PrintError(e)
        MoveFlagsByte.configure(text = "00", foreground = "Red")
        
    try:
        DamageValue = DamageArgument.get()[1] + DamageFormula.get()[1]
        DamageFormulaByte.configure(text = DamageValue, foreground = "White")
    except Exception as e:
        PrintError(e)
        DamageFormulaByte.configure(text = "00", foreground = "Red")
        
    try:
        MoveKindByte.configure(text = KindConversion[MoveKind.get()], foreground = "White")
    except Exception as e:
        PrintError(e)
        MoveKindByte.configure(text = "00", foreground = "Red")
        
    try:
        ScriptArgByte.configure(text = ConvertToHex(ScriptArgument.get()), foreground = "White")
    except Exception as e:
        PrintError(e)
        ScriptArgByte.configure(text = "00", foreground = "Red")

#------------------------------------------------------------
# Update Tkinter Variables Function
#------------------------------------------------------------
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

    DamageValue = L[DamageFormulaIndex]
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
    
    MoveKind.set(L[MoveKindIndex])
    ScriptArgument.set(L[ScriptArgIndex])

    Description.set(L[DescriptionIndex])

#------------------------------------------------------------
# Update Display Function
#------------------------------------------------------------
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

    MoveNumberLabel.configure(text = "Move {} of {}".format(ConvertToThree(CurrentMoveNumber.get() + 1), ConvertToThree(len(Table))))

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

    Place = float(DescriptionBox.index("insert"))
    
    if modf(Place)[0] > 0.19:
        Place = Place + 1.0

    if DescriptionBox.get(1.0, "end-1c").strip() != Description.get().strip() or DescriptionBox.get(1.0, "end-1c").count("\n") > 3: # Text different than box       
        DescriptionBox.delete(1.0, "end-1c")
        DescriptionBox.insert("insert", Description.get().strip())

        DescriptionBox.mark_set("insert", Place)

    MoveFinder.configure(values = MoveNameList)
    CurrentMove.set(MoveNameList[CurrentMoveNumber.get()])

#------------------------------------------------------------
# Create New Table File Function
#------------------------------------------------------------
def CreateNewFile():
    global Table, InitialFolder

    Sure = tk.BooleanVar()
    MakeYesNoBox(Root, "Warning", "Create a New Table File?", Sure,
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
            MakeEntryBox(Root, "Enter A Number", "Number of Moves", TestLength, 1,
                         ["Enter the number of Moves to add to the table."])

            if TestLength.get() < 0:
                MakeInfoBox(Root, "Error!", "Invalid input!",
                            ["This input is invalid!",
                             "The number of Moves must be a positive number."])
                Length = ""

            elif TestLength.get() == 0:
                MakeInfoBox(Root, "Error!", "Invalid input!",
                            ["This input is invalid!",
                             "The number of Moves cannot be zero."])
                Length = ""

            else:
                Length = TestLength.get()

        if Length > 999:
            Length = 999

        OpenNames = tk.BooleanVar()
        MakeYesNoBox(Root, "Open File", "Open Name File?", OpenNames,
                     ["Would you like to load the names",
                      "of the Moves in the table from a file?"])
                     
        NamesList = ("Move Name\n"*Length).split("\n")[0:-1]

        Table = [[]] * Length
        for i in range(len(Table)):
            Table[i] = ["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]
        
        if OpenNames.get():
            NamesFile = fd.askopenfilename(title = "Open Name File", initialdir = InitialFolder, filetypes = [("text files", "*.txt")])

            if NamesFile != "": # Cancelled
                NamesFile = open(NamesFile, "r", encoding = "utf-8")

                InitialFolder = os.path.dirname(os.path.realpath(NamesFile.name))
                
                for i, Name in enumerate(NamesFile.read().splitlines()):
                    if i >= len(Table):
                        NamesList.append("Move Name")
                    
                    NamesList[i] = Name[0:12] # Names can only be 12 characters, so we should truncate

        for i, Name in enumerate(Table):
            Table[i][MoveNameIndex] = NamesList[i]
            
        if len(NamesList) != Length:
            MakeInfoBox(Root, "Warning!", "Warning!",
                        ["The length of the name list is different than the length of the table.",
                         "The current number of Moves is {}.".format(len(Table))])

        MakeInfoBox(Root, "Success!", "The table was created!",
                ["The table was created successfully.",
                 "It has {} Moves in total.".format(len(Table))])

        CurrentMoveNumber.set(0)
        EnableEverything()
        Refresh()
        SaveFile(Table, CurrentOpenFile, True)

NewFileButton = ttk.Button(ButtonFrame, text = "New Table", command = CreateNewFile)

#------------------------------------------------------------
# Open Existing Table File Function
#------------------------------------------------------------
def OpenFile():
    global CurrentOpenFile, InitialFolder
    MenuText = {"Human-Readable": ["This type of table is a plain text file."],
                "Compiled":["This type of table is a hex binary file."]}

    Option = tk.StringVar()
    Option.set("None")
    MakeMultiChoiceBox(Root, "Pick A Choice", "Which type of table?", Option,
                       ["You may open a human-readable or a compiled table.",
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
            open(FileName, "w", encoding = "utf-8").close()
            NewFile = open(NewFile, "rb")
            
        else:
            FileName = NewFile
            NewFile = open(FileName, "r", encoding = "utf-8")

        CurrentOpenFile = os.path.realpath(FileName)
        InitialFolder = os.path.dirname(CurrentOpenFile)
        CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(FileName)))

        Sure = tk.BooleanVar()
        Sure.set(False)
        MakeYesNoBox(Root, "Make Backup?", "Back up the table?", Sure,
                     ["Would you like to make a backup of the table you are opening?",
                      "This is recommended to do in case the table accidentally",
                      "becomes corrupted while editing."])

        if Sure.get():
            BackupFileName = "BACKUP " + os.path.basename(FileName)
            BackupFile = os.path.join(InitialFolder, BackupFileName)
            OriginalFile = os.path.join(InitialFolder, FileName)
            shutil.copy(OriginalFile, BackupFile)
        
        global Table
        Table = []

        Error = ""

        if Option.get() == "Compiled": # Load from bytes, this is easier
            FileBytes = CreateFileBytes(NewFile, 12)
            Table, Error = MakeTableFromCompiled(FileBytes, Error)

            Sure = tk.BooleanVar()
            MakeYesNoBox(Root, "Open Table", "Open compiled Move Name Table?", Sure,
                         ["Would you like to load the Move Names from",
                          "a COMPILED Move Name Table?"])

            if Sure.get(): # Load Move Name Table
                NameFile = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = [("binary hex file", "*.bin")])

                if NameFile is not None:
                    InitialFolder = os.path.dirname(os.path.realpath(NameFile))
                    Table = ParsePointerTable(NameFile, Table, "Name")

            Sure = tk.BooleanVar()
            MakeYesNoBox(Root, "Open Table", "Open compiled Move Description Table?", Sure,
                         ["Would you like to load the Move Description from",
                          "a COMPILED Move Description Table?"])

            if Sure.get(): # Load Move Name Table
                DescFile = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = [("binary hex file", "*.bin")])

                if DescFile is not None:
                    InitialFolder = os.path.dirname(os.path.realpath(DescFile))
                    Table = ParsePointerTable(DescFile, Table, "Description")

        else: # Parse from text, only needs one file
            FileStuff = NewFile.read().split("\n\n")
            Table, Error = MakeTableFromText(FileStuff, Error)

        # Post-process the table and load any error messages encountered
        Table = ProcessTable(Root, Table)
        LoadTableErrors(Root, Table, Error)

        # Refresh the screen
        CurrentMoveNumber.set(0)
        EnableEverything()
        Refresh() 
        EnableEverything()
        
    else:
        return

OpenFileButton = ttk.Button(ButtonFrame, text = "Open Table", command = OpenFile)

#------------------------------------------------------------
# Save Currently-Opened Table File Function
#------------------------------------------------------------
def SaveFile(Table, FileName, Silent = False):
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
                Item = Item.strip().replace("\n", " | ")
                TableText += "(Description) {}\n\n".format(Item.strip())

    NewFile = open(FileName, "w", encoding = "utf-8")
    NewFile.write(TableText.strip())
    NewFile.close()

    if not Silent:
        MakeInfoBox(Root, "Complete", "Table Saved!",
                    ["The current table was successfully saved!"])

SaveButton = ttk.Button(ButtonFrame, text = "Save Table", command = lambda: SaveFile(Table, CurrentOpenFile))

#------------------------------------------------------------
# Save Currently-Opened Table File As New Table File Function
#------------------------------------------------------------
def SaveFileAs():
    global CurrentOpenFile, InitialFolder
    Edit = tk.BooleanVar()
    MakeYesNoBox(Root, "New File", "Save A Copy", Edit,
                ["Would you like to switch to editing the new file",
                 "after you save a copy of this one?"])
    
    NewFile = fd.asksaveasfile(initialdir = InitialFolder, initialfile = "New Table", defaultextension = ".txt")

    if NewFile is not None:        
        if not Edit.get():
            TempFile = CurrentOpenFile
            CurrentOpenFile = os.path.realpath(NewFile.name)
            InitialFolder = os.path.dirname(CurrentOpenFile)
            SaveFile(Table, CurrentOpenFile)
            NewFile.close()
            CurrentOpenFile = TempFile
            CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(CurrentOpenFile)))
        else:
            CurrentOpenFile = os.path.realpath(NewFile.name)
            InitialFolder = os.path.dirname(CurrentOpenFile)
            CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(NewFile.name)))
            NewFile.close()
            SaveFile(Table, CurrentOpenFile)

SaveAsButton = ttk.Button(ButtonFrame, text = "Save Table As", command = SaveFileAs)

#------------------------------------------------------------
# Compile Current Table File To Hex Binary Function
#------------------------------------------------------------
def CompileTable(Table):
    global InitialFolder
    MenuText = {"Attack Data Table": ["This is the main Attack Data Table.",
                                      "This can be completely compiled without needing an address."],
                "Move Name Table": ["This is the table of pointers for Move Names",
                                    "This requires an address beforehand."],
                "Move Description Table": ["This is the table of pointers for Move Descriptions",
                                    "This requires an address beforehand."]}

    Option = tk.StringVar()
    Option.set("None")
    MakeMultiChoiceBox(Root, "Pick A Choice", "Which table should be compiled?", Option,
                       ["There are three possible tables which could be compiled.",
                        "Please select one."], MenuText, "Attack Data Table")

    if Option.get() == "Attack Data Table":
        NewFile = fd.asksaveasfile(initialdir = InitialFolder, initialfile = "Compiled ADT", defaultextension = ".bin")

        if NewFile is not None:
            FileName = os.path.realpath(NewFile.name)
            InitialFolder = os.path.dirname(FileName)
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
                ByteList.append(int(RangeConversion[Entry[RangeIndex]], 16))

                if Entry[PriorityIndex] < 0:
                    P = 256 + Entry[PriorityIndex]
                else:
                    P = Entry[PriorityIndex]
                    
                ByteList.append(P)

                FlagLine = 0
                for i, Flag in enumerate(Entry[MoveFlagIndex]):
                    FlagLine += (128 // 2**i) * Flag

                ByteList.append(FlagLine)
                ByteList.append(int(Entry[DamageFormulaIndex], 16))
                ByteList.append(int(KindConversion[Entry[MoveKindIndex]], 16))
                ByteList.append(Entry[ScriptArgIndex])

            NewFile.write(bytes(ByteList))
            NewFile.close()
            MakeInfoBox(Root, "Success", "Compilation complete!",
                        ["The table was compiled to a file successfully!"])

    elif Option.get() == "Move Name Table" or Option.get() == "Move Description Table":
        if Option.get() == "Move Name Table":
            SplitPoint = 13
            FileName = "Compiled Names"
        else:
            SplitPoint = 77
            FileName = "Compiled Descriptions"

        NewFile = fd.asksaveasfile(initialdir = InitialFolder, initialfile = FileName, defaultextension = ".bin")

        if NewFile is not None:
            Address = tk.StringVar()
            MakeAddressEntryBox(Root, "Enter Address", "Enter the starting address", Address,
                                ["Enter the starting address for the table in the following form:",
                                 "08AABBCC",
                                 "Where AABBCC is a placeholder for the offset of your table.",
                                 "Use placeholder 0's (i.e. 0x12345 -> 08012345)"])

            Extend = tk.BooleanVar()
            MakeYesNoBox(Root, "Question", "Future-proof the table?", Extend,
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
                    Text = Entry[MoveNameIndex]
                else:
                    Text = Entry[DescriptionIndex]

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
                        Array[i] = int(TextToBytes[Letter], 16)
                    except:
                        pass

                Array[i+1] = 255

                for Byte in Array:
                    TextByteList.append(Byte)

                PointerByteList.append(P & 255)
                PointerByteList.append((P & 65280) >> 8)
                PointerByteList.append((P & 16711680) >> 16)
                PointerByteList.append((P & 4278190080) >> 24)

                P = P + ArrayLength
                        
            NewFile.write(bytes(PointerByteList))
            NewFile.write(bytes(TextByteList))
            NewFile.close()
            MakeInfoBox(Root, "Success", "Compilation complete!",
                        ["The table was compiled to a file successfully!"])

    else:
        return

CompileButton = ttk.Button(ButtonFrame, text = "Compile Table", command = lambda: CompileTable(Table))

ButtonHSpacing = 30
ButtonVSpacing = 5

#------------------------------------------------------------
# Convert Old-Form Hex Binary Table To New Form Table Function
#------------------------------------------------------------
def ConvertTable():
    global InitialFolder
    Sure = tk.BooleanVar()
    MakeYesNoBox(Root,  "Convert Table?", "Convert an old table?", Sure,
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
            shutil.move(OldTable, MovedFile)

            MakeInfoBox(Root, "Announcement!", "Old Table Moved",
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
                        if Byte in OldToNewScripts:
                            NewTableString += OldToNewScripts[Byte] + " "
                        else:
                            NewTableString += Byte + " "

                        Script = Byte
                    
                    case 6: # Move Range
                        if Byte in OldToNewRanges:
                            NewTableString += OldToNewRanges[Byte] + " "
                        else:
                            NewTableString += Byte + " "
                    
                    case 8: # Move Flags
                        if Script in SelfEffectFlagList:
                            NewTableString += hex(int(Byte, 16) + 64).upper()[2:] + " "
                        else:
                            NewTableString += Byte + " "

                    case 9: # Damage Formula
                        if Script in OldToNewDamageFormula:
                            NewTableString += OldToNewDamageFormula[Script] + " "
                        else:
                            NewTableString += Byte + " "

                    case 11: # Script Argument
                        if Script in OldToNewArguments:
                            NewTableString += OldToNewArguments[Script] + " "
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
        NewTable, Error = MakeTableFromCompiled(FileBytes, Error)

        Names = tk.BooleanVar()
        MakeYesNoBox(Root, "Open Name File?", "Conversion Success!", Names,
                        ["The table was converted successfully!",
                         "Would you like to open a HUMAN-READABLE name file",
                         "for the new table?"])

        if Names.get():
            Length = len(NewTable)
                     
            NamesList = ("Move Name\n"*Length).split("\n")[0:-1]
            NamesFile = fd.askopenfilename(title = "Open Table", initialdir = InitialFolder, filetypes = [("text files", "*.txt")])
            NamesFile = open(NamesFile, "r", encoding = "utf-8")

            InitialFolder = os.path.dirname(os.path.realpath(NamesFile.name))
            
            for i, Name in enumerate(NamesFile.read().splitlines()):
                if i >= len(NewTable):
                    NamesList.append("Move Name")
                
                NamesList[i] = Name[0:12] # Names can only be 12 characters, so we should truncate

            for i, Name in enumerate(NewTable):
                NewTable[i][MoveNameIndex] = NamesList[i]
                
            if len(NamesList) != Length:
                MakeInfoBox(Root, "Warning!", "Warning!",
                            ["The length of the name list is different than the length of the table.",
                             "The current number of Moves is {}.".format(len(NewTable))])

        SaveFile(NewTable, NewText, True)

        OpenNew = tk.BooleanVar()
        MakeYesNoBox(Root, "Open File", "Open newly converted table?", OpenNew,
                        ["Conversion success!",
                         "Would you like to open the newly converted table",
                         "in the editor?"])

        if OpenNew.get():
            global Table, CurrentOpenFile
            NewFile = open(NewText, "r", encoding = "utf-8")
            CurrentOpenFile = os.path.realpath(NewText)
            InitialFolder = os.path.dirname(CurrentOpenFile)
            CurrentLabel.configure(text = "Open File: {}".format(os.path.basename(NewText)))

            Table = []
            Error = ""
            FileStuff = NewFile.read().split("\n\n")
            Table, Error = MakeTableFromText(FileStuff, Error)
            
            Table = ProcessTable(Root, Table)
            LoadTableErrors(Root, Table, Error)
            
            CurrentMoveNumber.set(0)
            EnableEverything()
            Refresh() 
            EnableEverything()
          
ConvertButton = ttk.Button(ButtonFrame, text = "Convert Table", command = ConvertTable)

#------------------------------------------------------------
# Move Backwards In Table
#------------------------------------------------------------
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

#------------------------------------------------------------
# Move Forwards In Table
#------------------------------------------------------------
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

#------------------------------------------------------------
# Add Move To Table Function
#------------------------------------------------------------
def AddMove():
    global Table
    Table.append(["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""])
    CurrentMoveNumber.set(len(Table) - 1)

# Function That The Button Actually Calls
def AddMoves():
    Length = ""

    if len(Table) >= 999: # Cannot add more Moves if already at 999
        MakeInfoBox(Root, "Error!", "Cannot add more!",
                    ["The table is already at its maximum length!",
                     "Please delete entries before adding more."])
        return

    TestLength = tk.IntVar()
    while type(Length) != int:
        TestLength.set(0)
        MakeEntryBox(Root, "Enter A Number", "Number of Moves", TestLength, 1,
                     ["Enter the number of Moves to add to the table."])

        if TestLength.get() < 0:
            MakeInfoBox(Root, "Error!", "Invalid input!",
                        ["This input is invalid!",
                         "The number of Moves must be a positive number."])
            Length = ""

        elif len(Table) + TestLength.get() > 999: # Table definitely has less than 999 cause we checked for this earlier
            Length = 999 - len(Table) # Only add enough to maximise it.
            MakeInfoBox(Root, "Error!", "Too many Moves!",
                        ["Tables can only support a length of up to 999.",
                         "Only {} Moves will be added.".format(Length)])

        else:
            Length = TestLength.get()

    for i in range(Length):
        AddMove()

    if CurrentMoveNumber.get() > 0:
        BackButton.configure(state = "normal")

    ForwardButton.configure(state = "disabled")

    if Length != 0:
        MakeInfoBox(Root, "Success!", "A new Move was added!",
                    ["The table was modified successfully.",
                     "There are now {} Moves in total.".format(len(Table))])

        Refresh()

        if AutoSave:
            SaveFile(Table, CurrentOpenFile, True)

AddMoveButton = ttk.Button(ButtonFrame, text = "Add Moves", command = AddMoves)

#------------------------------------------------------------
# Delete The Current Move From Table Function
#------------------------------------------------------------
def DeleteMove():
    global Table

    Sure = tk.BooleanVar()
    Sure.set(False)
    MakeYesNoBox(Root, "Warning!", "Warning!", Sure,
                 ["You are about to remove the current Move from the table.",
                  "This action cannot be undone.",
                  "Would you still like to proceed?"])

    if Sure.get():
        if len(Table) <= 1: # Only one Move left
            MakeInfoBox(Root, "Error", "Warning!",
                        ["This is the only Move left in the table!",
                         "It cannot be fully deleted.",
                         "It will instead be replaced with an empty Move."])

            Table = [["Move Name", "00", 0, "Normal", 0, 0, 0, "Target", 0, [0,0,0,0,0,0,0,0], "00", "Status", 0, ""]]
            Refresh()

            if AutoSave:
                SaveFile(Table, CurrentOpenFile, True)
            
        else:
            i = CurrentMoveNumber.get()
            Table.pop(i)

            if i > len(Table) - 1:
                CurrentMoveNumber.set(len(Table) - 1)

            Refresh()

            if AutoSave:
                SaveFile(Table, CurrentOpenFile, True)

DeleteMoveButton = ttk.Button(ButtonFrame, text = "Delete Move", command = DeleteMove)

#------------------------------------------------------------
# Disable Widgets Function
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
    TableFunctionButton.configure(state = "disabled")
    AutoFillMoveButton.configure(state = "disabled")

#------------------------------------------------------------
# Enable Widgets Function
#------------------------------------------------------------
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
    TableFunctionButton.configure(state = "normal")
    AutoFillMoveButton.configure(state = "normal")

    if len(Table) > 1:
        ForwardButton.configure(state = "normal")
#------------------------------------------------------------
# Place everything
#------------------------------------------------------------
# Icon Frame
BulbasaurFrame.pack(side = "left", padx = 50)
BulbasaurLabel.pack()

IconFrame.pack(side = "left", padx = 10)
AutoSaveButton.pack(pady = 5)
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
TableFunctionFrame.grid(row = 0, column = 0, padx = 15, pady = 5, sticky = "w")
TableFunctionButton.pack(padx = 80)

MoveNameFrame.grid(row = 0, column = 1, padx = 15, pady = 5, sticky = "w")
MoveNameHelpButton.pack(side = "left")
MoveNameLabel.pack(side = "left", padx = (0,5))
MoveNameEntry.pack(side = "left")

AutoFillMoveFrame.grid(row = 0, column = 2, padx = 15, pady = 5, sticky = "w")
AutoFillMoveButton.pack(padx = 20)

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
    Command = "Command"
else:
    Command = "Control"

# Shortcuts
ShortcutSave = "<{}-s>".format(Command)
ShortcutSaveAs = "<{}-Shift-S>".format(Command)
ShortcutOpen = "<{}-o>".format(Command)
ShortcutNew = "<{}-n>".format(Command)
ShortcutCompile = "<{}-Shift-C>".format(Command)
ShortcutConvert = "<{}-Shift-X>".format(Command)
ShortcutForward = "<{}-Right>".format(Command)
ShortcutBackward = "<{}-Left>".format(Command)
ShortcutHelp = "<{}-h>".format(Command)
ShortcutAdd = "<{}-Shift-A>".format(Command)
ShortcutDelete = "<{}-Shift-D>".format(Command)
ShortcutDebug = "<{}-d>".format(Command)
ShortcutQuit = "<{}-q>".format(Command)

# Bind to Root window
Root.bind(ShortcutSave, lambda _: SaveFile(Table, CurrentOpenFile))
Root.bind(ShortcutSaveAs, lambda _: SaveFileAs())
Root.bind(ShortcutOpen, lambda _: OpenFile())
Root.bind(ShortcutNew, lambda _: CreateNewFile())
Root.bind(ShortcutCompile, lambda _: CompileTable(Table))
Root.bind(ShortcutConvert, lambda _: ConvertTable())
Root.bind(ShortcutForward, lambda _: GoForward())
Root.bind(ShortcutBackward, lambda _: GoBackward())
Root.bind(ShortcutHelp, lambda _: ShowHelpMenu())
Root.bind(ShortcutAdd, lambda _: AddMoves())
Root.bind(ShortcutDelete, lambda _: DeleteMove())
Root.bind(ShortcutDebug, lambda _: OpenFileDirectory())
Root.bind(ShortcutQuit, lambda _: Root.destroy())

#------------------------------------------------------------
# Main Loop
#------------------------------------------------------------
DisableEverything()
#DebugMakeTable()
Root.mainloop()
