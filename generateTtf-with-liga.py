#!/usr/bin/python3
#coding=utf8

from common import *
import sys
import math
import fontforge
import pathlib

specialCharacterNames = [
	"SADALIAN TONE ONE",
	"SADALIAN TONE TWO",
	"SADALIAN TONE THREE",
	"SADALIAN TONE FOUR",
	"SADALIAN TONE FIVE",
	"SADALIAN TONE SIX",
	"SADALIAN TONE SEVEN",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"SADALIAN COMMA",
	"SADALIAN FULL STOP",
	"SADALIAN COLON",
	"SADALIAN QUESTION MARK",
	"SADALIAN EXCLAMATION MARK",
	"SADALIAN LEFT QUOTATION MARK",
	"SADALIAN RIGHT QUOTATION MARK",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"(This position shall not be used)",
	"SADALIAN DIGIT ZERO",	
	"SADALIAN DIGIT ONE",
	"SADALIAN DIGIT TWO",
	"SADALIAN DIGIT THREE",
	"SADALIAN DIGIT FOUR",
	"SADALIAN DIGIT FIVE",
	"SADALIAN DIGIT SIX",
	"SADALIAN DIGIT SEVEN",
	"SADALIAN DIGIT EIGHT",
	"SADALIAN DIGIT NINE",
	"SADALIAN DIGIT TEN",
	"SADALIAN DIGIT ELEVEN",
	"SADALIAN DIGIT TWELVE",
	"SADALIAN DIGIT THIRTEEN",
	"SADALIAN DIGIT FOURTEEN",
	"SADALIAN DIGIT FIFTEEN",
]

char_name_mapping = {
	'`': 'grave',
	"'": 'quotesingle',
	'"': 'quotedbl',
	'(': 'parenleft',
	')': 'parenright',
	',': 'comma',
	'.': 'period',
	'/': 'slash',
	'\\': 'backslash',
	':': 'colon',
	';': 'semicolon',
	'?': 'question',
	'[': 'bracketleft',
	']': 'bracketright',
	'#': 'numbersign',
	'!': 'exclam',
	'0': 'zero',
	'1': 'one',
	'2': 'two',
	'3': 'three',
	'4': 'four',
	'5': 'five',
	'6': 'six',
	'7': 'seven',
	'8': 'eight',
	'9': 'nine',
}

# Provides an alternative way to enter the punctuation
punctuation_keyboard_remap = {
	':': ';',
	'?': '/',
	'!': '\\',
	'[': '(',
	']': ')',
}

MONO_WIDTH = 1100
def generateFont(styleName):	
	liga_table = {"'": ""}

	font = fontforge.font()
	font.ascent = 1800
	font.descent = 248
	font.upos = -124
	font.weight = styleName
	font.familyname = "Sadalian"
	font.fontname = font.familyname+font.weight
	font.fullname = font.familyname+" "+font.weight
	font.copyright = "(C) Sadale.net, all rights reserved"
	font.addLookup("table",
		"gsub_ligature", (), ( (("liga",(("DFLT",("dflt")),("latn",("dflt")))),) ) )
	font.lookupSetStoreLigatureInAfm("table", False)
	font.addLookupSubtable("table", "subtable")

	# Add punctuation characters
	for i in range(CODEPOINT_BASE_SADALIAN, CODEPOINT_END_SADALIAN):
		if i >= CODEPOINT_PUNCTUATION_STARTS_SADALIAN:
			if specialCharacterNames[i-CODEPOINT_PUNCTUATION_STARTS_SADALIAN] == "(This position shall not be used)":
				continue
			char = font.createChar(i, specialCharacterNames[i-CODEPOINT_PUNCTUATION_STARTS_SADALIAN].replace(" ","_"))
			char.width = round(MONO_WIDTH*0.65)
		else:
			char = font.createChar(i, ("SADALIAN SYLLABLE "+sScriptRomanize(sScriptDecode(i)).upper()).replace('`', '-').replace(" ","_"))
			char.width = MONO_WIDTH
		liga = sScriptDecode(i)

		if liga.startswith("#"):
			if liga[1].isnumeric():
				liga = liga[1:] # remove the hash for the numbers
			else:
				liga = liga.replace("#", "'") # For higher numerals, uses 'a 'b 'c 'e 'd 'f to type
		liga = liga.replace('`', '"')
		liga_table[liga] = chr(i)
		liga_table[liga+" "] = chr(i)
		liga_seq = tuple(i if i not in char_name_mapping else char_name_mapping[i] for i in liga)
		char.addPosSub("subtable", liga_seq)
		char.addPosSub("subtable", liga_seq + ('space',))
		if liga in punctuation_keyboard_remap.keys():
			liga2 = punctuation_keyboard_remap[liga]
			liga_table[liga2] = chr(i)
			liga_table[liga2+" "] = chr(i)
			liga2_seq = tuple(i if i not in char_name_mapping else char_name_mapping[i] for i in liga2)
			char.addPosSub("subtable", liga2_seq)
			char.addPosSub("subtable", liga2_seq + ('space',))

		char.importOutlines("generatedGlyphs/"+str(i)+".svg", ("correctdir"))
		if styleName.find("Bold") != -1:
			char.stroke("circular", 180, "round", "round")
		else:
			char.stroke("circular", 120, "round", "round")
		char.removeOverlap()
		char.simplify()

	#Add a space character
	spaceChar = font.createChar(ord(" "))
	spaceChar.width = MONO_WIDTH

	#Add a splitter character
	sepChar = font.createChar(ord("'"))
	sepChar.width = 0

	#Add extra characters:
	charmap = {
		'0': '#0',
		'1': '#1',
		'2': '#2',
		'3': '#3',
		'4': '#4',
		'5': '#5',
		'6': '#6',
		'7': '#7',
		'8': '#8',
		'9': '#9',
		'"': '`',
		'(': '[',
		')': ']',
	}

	for i in PUNCTUATION_MAP:
		charmap[i] = i
	for i in INITIAL_LIST:
		charmap[i] = i
	for i in MIDDLE_LIST:
		if i == 'y': #y is for the consonant in Sadalian. For vowel, use -y.
			continue
		charmap[i] = '-'+i

	# Since we've replaced ` with ", no need to have ` in the charmap anymore.
	del charmap['`']
	
	for k, v in punctuation_keyboard_remap.items():
		if k == '(' or k == ')':
			continue # already handled in charmap
		charmap[v] = k

	for c in charmap:
		font.selection.select(("unicode",), sScriptCode(charmap[c]))
		font.copy()
		font.selection.none()
		font.selection.select(("unicode",), ord(c))
		font.paste()
		font.selection.none()

	font.selection.all()
	print("Rounding...")
	font.round()

	if styleName.find("Italic") != -1:
		print("italicizing...")
		font.italicize()
	print("Saving...")
	pathlib.Path("./generatedFont").mkdir(parents=True, exist_ok=True)
	font.save("generatedFont/"+font.fontname+".sfd")
	font.generate("generatedFont/"+font.fontname+".ttf")
	
	return liga_table

liga_table = generateFont("Regular")
generateFont("Italic")
generateFont("Bold")
generateFont("BoldItalic")

with open("generatedFont/qss_mapping.py", "w") as f:
	f.write("QSS_MAP = ")
	f.write(str(liga_table))
	
