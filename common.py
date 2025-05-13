CODEPOINT_BASE_SADALIAN = 0xF2000 #Code point base of Sadalian (i.e. Sadalese rev7+)
INITIAL_LIST = 'bpmfdtnsjclygkxhrq`w'
MIDDLE_LIST = '`ouavzeiy'
FINAL_LIST = '`iumnxptk'
NUM_SPECIALS = 44
CODEPOINT_PUNCTUATION_STARTS_SADALIAN = CODEPOINT_BASE_SADALIAN+len(INITIAL_LIST)*len(MIDDLE_LIST)*len(FINAL_LIST)
CODEPOINT_END_SADALIAN = CODEPOINT_PUNCTUATION_STARTS_SADALIAN+NUM_SPECIALS
PUNCTUATION_MAP = [",",".",":","?","!","[","]"]

def sScriptCode(string):
	if string.startswith("'"): # tonals
		return CODEPOINT_BASE_SADALIAN+len(INITIAL_LIST)*len(MIDDLE_LIST)*len(FINAL_LIST)+(int(string[1:]))
	elif string in PUNCTUATION_MAP: # punctuations
		return CODEPOINT_BASE_SADALIAN+len(INITIAL_LIST)*len(MIDDLE_LIST)*len(FINAL_LIST)+12+PUNCTUATION_MAP.index(string)
	elif string.startswith("#"): # numerals
		return CODEPOINT_BASE_SADALIAN+len(INITIAL_LIST)*len(MIDDLE_LIST)*len(FINAL_LIST)+28+(int(string[1:], 16))
	i = 0

	initial = INITIAL_LIST.find(string[i])
	if initial == -1:
		initial = INITIAL_LIST.find('`')
	else:
		i += 1

	middle = MIDDLE_LIST.find('`')
	if i < len(string):
		middle = MIDDLE_LIST.find(string[i])
		if middle == -1:
			middle = MIDDLE_LIST.find('`')
		else:
			i += 1

	final = FINAL_LIST.find('`')
	if i < len(string):
		final = FINAL_LIST.find(string[i])
		if final == -1:
			final = FINAL_LIST.find('`')
		else:
			i += 1

	return initial*len(MIDDLE_LIST)*len(FINAL_LIST)+middle*len(FINAL_LIST)+final+CODEPOINT_BASE_SADALIAN

#For Sadalese rev2+ and Sadalian
def sScriptDecode2(codePoint):
	if codePoint >= CODEPOINT_END_SADALIAN:
		raise Exception('Toned characters does not work with this function.')
	relativeCodepoint = codePoint-CODEPOINT_BASE_SADALIAN
	if relativeCodepoint >= len(INITIAL_LIST)*len(MIDDLE_LIST)*len(FINAL_LIST):
		specialCharacter = relativeCodepoint-len(INITIAL_LIST)*len(MIDDLE_LIST)*len(FINAL_LIST)+1
		initial, middle, final = 0, 0, 0
	else:
		specialCharacter = 0
		final = relativeCodepoint%len(FINAL_LIST)
		middle = int(relativeCodepoint/len(FINAL_LIST))%len(MIDDLE_LIST)
		initial = int(relativeCodepoint/len(FINAL_LIST)/len(MIDDLE_LIST))%len(INITIAL_LIST)
	return specialCharacter, initial, middle, final

def sScriptDecode(codePoint):
	if codePoint < CODEPOINT_BASE_SADALIAN and codePoint >= CODEPOINT_END_SADALIAN:
		return "'%i"%(codePoint-CODEPOINT_TONE_BASE+1)
	specialCharacter, initial, middle, final = sScriptDecode2(codePoint)
	if specialCharacter != 0:
		if specialCharacter >= 1 and specialCharacter <= 7: # tones
			return "'"+str(specialCharacter) 
		elif specialCharacter >= 13 and specialCharacter <= 28: # punctuation
			if specialCharacter-13 < len(PUNCTUATION_MAP):
				return PUNCTUATION_MAP[specialCharacter-13]
			else:
				return "(This position shall not be used)"
		elif specialCharacter >= 29 and specialCharacter <= 44: # numeral
			return f"#{specialCharacter-29:1x}"
		else:
			return "(This position shall not be used)"
	#Removes trailing `
	ret = INITIAL_LIST[initial]+MIDDLE_LIST[middle]+(FINAL_LIST[final] if FINAL_LIST[final] != "`" else "")

	if INITIAL_LIST[initial] == "`" and MIDDLE_LIST[middle] != "`": #If the vowel doesn't have any consonant before it, drop the initial consonant
		if MIDDLE_LIST[middle] != "y": # (except for `y, which always requires a consonant prefix)
			ret = ret[1:]
	elif INITIAL_LIST[initial] == "`" and MIDDLE_LIST[middle] == "`": #If both initial and middle are `, drop one of them.
		ret = ret[1:]
	elif INITIAL_LIST[initial] != "`" and MIDDLE_LIST[middle] == "`" and FINAL_LIST[final] == "`": #If there is only the initial consonent, remove anything tailing.
		ret = ret[0]
	return ret

def sScriptRomanize(charName):
	if charName.startswith("'") or charName.startswith("#"):
		return charName
	charName = charName[0] + charName[1:].replace("y", "ue")
	charName = charName.replace("v", "uh").replace("z", "oe")
	charName = charName.replace("j", "dz").replace("c", "ts").replace("x", "ng").replace("r", "gw").replace("q", "kw")
	if charName.startswith("`ue"):
		charName = charName.replace("`ue", "ue")
	return charName
