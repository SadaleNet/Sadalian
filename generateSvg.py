#!/usr/bin/python3
#coding=utf8
from common import *
import pathlib

THICKNESS = 1.0 #Keep it low and let fontforge thicken it
WIDTH = 520.0
DOUBLE_SLASH_SPACING = WIDTH*0.75
SLASH_WIDTH = WIDTH*0.5
LEFTMOST = WIDTH/2 +100
TOPMOST = 140
BOTTOMMOST = 1800
ANNOTATION_SPACING = 150
ANNOTATION_X = LEFTMOST+WIDTH*1.5+ANNOTATION_SPACING

PUNCTUATION_WIDTH = WIDTH*0.75

header = '''
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="2048"
   height="2048"
   version="1.1">
'''

footer = '</svg>'

class Pos:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

def drawLine(p1, p2):
	return '''
		<path
	   d="m %f,%f %f,%f"
	   style="fill:none;stroke:#000000;stroke-width:%f;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />
	''' % (p1.x, p1.y, p2.x-p1.x, p2.y-p1.y, THICKNESS)

def drawSmileArc(origin, radius):
	p1 = Pos(origin.x-radius, origin.y)
	p2 = Pos(origin.x, origin.y+radius)
	p3 = Pos(origin.x+radius, origin.y)
	return drawLine(p1, p2) + drawLine(p2, p3)

def drawFrownArc(origin, radius):
	p1 = Pos(origin.x-radius, origin.y)
	p2 = Pos(origin.x, origin.y-radius)
	p3 = Pos(origin.x+radius, origin.y)
	return drawLine(p1, p2) + drawLine(p2, p3)

def drawRect(p1, p3):
	p2 = Pos(p1.x, p3.y)
	p4 = Pos(p3.x, p1.y)
	return drawLine(p1, p2) + drawLine(p2, p3) + drawLine(p3, p4) + drawLine(p4, p1)

def drawZigZag(p1, p2, count):
	ret = ''
	for i in range(count):
		if i%2 == 0:
			ret += drawLine(Pos(p1.x, p1.y+(p2.y-p1.y)*i/count), Pos(p2.x, p1.y+(p2.y-p1.y)*(i+1)/count))
		else:
			ret += drawLine(Pos(p2.x, p1.y+(p2.y-p1.y)*i/count), Pos(p1.x, p1.y+(p2.y-p1.y)*(i+1)/count))
	return ret
	
def constructCharacter(codePoint):
	ret = ''
	specialCharacter, initial, middle, final = sScriptDecode2(codePoint)
	print([specialCharacter, initial, middle, final])
	if specialCharacter != 0:
		x = 100
		if specialCharacter in list(range(1,13)): #tone
			if specialCharacter == 1:
				ret += drawLine(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, TOPMOST))
				ret += drawLine(Pos(x, TOPMOST+PUNCTUATION_WIDTH*0.8), Pos(x+PUNCTUATION_WIDTH, TOPMOST+PUNCTUATION_WIDTH*0.8))
				ret += drawLine(Pos(x, TOPMOST+PUNCTUATION_WIDTH*0.8*2), Pos(x+PUNCTUATION_WIDTH, TOPMOST+PUNCTUATION_WIDTH*0.8*2))
			elif specialCharacter == 2:
				ret += drawLine(Pos(x, TOPMOST+PUNCTUATION_WIDTH), Pos(x+PUNCTUATION_WIDTH, TOPMOST))
				ret += drawLine(Pos(x, TOPMOST+PUNCTUATION_WIDTH*2), Pos(x+PUNCTUATION_WIDTH, TOPMOST+PUNCTUATION_WIDTH))
			elif specialCharacter == 3:
				ret += drawLine(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, TOPMOST))
				ret += drawLine(Pos(x, TOPMOST+PUNCTUATION_WIDTH), Pos(x+PUNCTUATION_WIDTH, TOPMOST+PUNCTUATION_WIDTH))
			elif specialCharacter == 4:
				ret += drawLine(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, TOPMOST+PUNCTUATION_WIDTH))
			elif specialCharacter == 5:
				ret += drawLine(Pos(x, TOPMOST+PUNCTUATION_WIDTH), Pos(x+PUNCTUATION_WIDTH, TOPMOST))
			elif specialCharacter == 6:
				ret += drawLine(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, TOPMOST))
			elif specialCharacter == 7: # Sounds like the tone 4 in Mandarin
				ret += drawLine(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, TOPMOST+PUNCTUATION_WIDTH))
				ret += drawLine(Pos(x, TOPMOST+PUNCTUATION_WIDTH), Pos(x+PUNCTUATION_WIDTH, TOPMOST+PUNCTUATION_WIDTH*2))
		elif specialCharacter in list(range(13,29)): # Punctuation
			strokes = [False, False, False] # upper, mid, lower
			if specialCharacter == 13: # Punctuations: comma
				strokes = [False, False, True]
			elif specialCharacter == 14: # Punctuations: period
				strokes = [True, True, True]
			elif specialCharacter == 15: # Punctuations: colon
				strokes = [True, False, True]
			elif specialCharacter == 16: # Punctuations: question mark
				strokes = [True, True, False]
			elif specialCharacter == 17: # Punctuations: exclaim
				strokes = [False, True, True]
			elif specialCharacter == 18: # Punctuations: open quotes
				strokes = [False, True, False]
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH/2, BOTTOMMOST), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST))
			elif specialCharacter == 19: # Punctuations: closing quotes
				strokes = [False, True, False]
				ret += drawLine(Pos(x, BOTTOMMOST), Pos(x+PUNCTUATION_WIDTH/2, BOTTOMMOST))
			if strokes[0]:
				ret += drawLine(Pos(x, BOTTOMMOST-PUNCTUATION_WIDTH), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST-PUNCTUATION_WIDTH))
			if strokes[1]:
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH/2, BOTTOMMOST), Pos(x+PUNCTUATION_WIDTH/2, BOTTOMMOST-PUNCTUATION_WIDTH))
			if strokes[2]:
				ret += drawLine(Pos(x, BOTTOMMOST), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST))
		elif specialCharacter in list(range(29,45)): # Numerals
			ret += drawLine(Pos(x, TOPMOST), Pos(x, BOTTOMMOST))
			if specialCharacter == 29: # 0
				pass
			elif specialCharacter == 30: # 1
				ret += drawZigZag(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)/2), 1)
			elif specialCharacter == 31: # 2
				ret += drawZigZag(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)*2/3), 2)
			elif specialCharacter == 32: # 3
				ret += drawZigZag(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 3)
			elif specialCharacter == 33: # 4
				ret += drawZigZag(Pos(x, TOPMOST), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 4)
			elif specialCharacter == 34: # 5
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)/2))
			elif specialCharacter == 35: # 6
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/3))
				ret += drawZigZag(Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/3), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 1)
			elif specialCharacter == 36: # 7
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/3))
				ret += drawZigZag(Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/3), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 2)
			elif specialCharacter == 37: # 8
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/4))
				ret += drawZigZag(Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/4), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 3)
			elif specialCharacter == 38: # 9
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/5))
				ret += drawZigZag(Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/5), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 4)
			elif specialCharacter == 39: # 10
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/3))
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)*1/3), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/3))
			elif specialCharacter == 40: # 11
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/3))
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)*1/3), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/3))
				ret += drawZigZag(Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/3), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 1)
			elif specialCharacter == 41: # 12
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/4))
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)*1/4), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/4))
				ret += drawZigZag(Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/4), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 2)
			elif specialCharacter == 42: # 13
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/5))
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)*1/5), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/5))
				ret += drawZigZag(Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/5), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 3)
			elif specialCharacter == 43: # 14
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/6))
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)*1/6), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/6))
				ret += drawZigZag(Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/6), Pos(x+PUNCTUATION_WIDTH, BOTTOMMOST), 4)
			elif specialCharacter == 44: # 15
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*1/4))
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)*1/4), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*2/4))
				ret += drawLine(Pos(x+PUNCTUATION_WIDTH, TOPMOST+(BOTTOMMOST-TOPMOST)*2/4), Pos(x, TOPMOST+(BOTTOMMOST-TOPMOST)*3/4))
		return ret

	leftMost = -1 #The index of left-most verticle stroke
	rightMost = -1 #The index of right-most verticle stroke
	basePivot = [Pos(), Pos(), Pos()]
	middlePivot = [Pos(), Pos(), Pos()]
	middlePivotAvailable = [False, False, False]
	rootAtTop = (int(initial/2)%2 == 0)
	hasHook = (initial%2 == 1)

	#Construct the initial strokes(except the hook)
	baseY = TOPMOST
	if not rootAtTop:
		baseY = BOTTOMMOST
	if "bpmf".find(INITIAL_LIST[initial]) != -1: #initials is one of "bpmf". Circles.
		if rootAtTop:
			ret += drawRect(Pos(LEFTMOST, baseY), Pos(LEFTMOST+WIDTH, baseY+WIDTH))
			basePivot[0] = Pos(LEFTMOST, baseY+WIDTH)
			basePivot[1] = Pos(LEFTMOST+WIDTH*0.5, baseY+WIDTH)
			basePivot[2] = Pos(LEFTMOST+WIDTH, baseY+WIDTH)
		else:
			ret += drawRect(Pos(LEFTMOST, baseY), Pos(LEFTMOST+WIDTH, baseY-WIDTH))
			basePivot[0] = Pos(LEFTMOST, baseY-WIDTH)
			basePivot[1] = Pos(LEFTMOST+WIDTH*0.5, baseY-WIDTH)
			basePivot[2] = Pos(LEFTMOST+WIDTH, baseY-WIDTH)
	elif "dtns".find(INITIAL_LIST[initial]) != -1: #initials is one of "dtns". Single dash.
		ret += drawLine(Pos(LEFTMOST, baseY), Pos(LEFTMOST+WIDTH, baseY))
		basePivot[0] = Pos(LEFTMOST, baseY)
		basePivot[1] = Pos(LEFTMOST+WIDTH*0.5, baseY)
		basePivot[2] = Pos(LEFTMOST+WIDTH, baseY)
	elif "jcly".find(INITIAL_LIST[initial]) != -1: #initials is one of "jcly". double dashes
		ret += drawLine(Pos(LEFTMOST, baseY), Pos(LEFTMOST+WIDTH, baseY))
		if rootAtTop:
			baseY += WIDTH/2
		else:
			baseY -= WIDTH/2
		ret += drawLine(Pos(LEFTMOST, baseY), Pos(LEFTMOST+WIDTH, baseY))
		basePivot[0] = Pos(LEFTMOST, baseY)
		basePivot[1] = Pos(LEFTMOST+WIDTH*0.5, baseY)
		basePivot[2] = Pos(LEFTMOST+WIDTH, baseY)
	elif "gkxh".find(INITIAL_LIST[initial]) != -1: #initials is one of "gkxh". semicircle
		if rootAtTop:
			ret += drawFrownArc(Pos(LEFTMOST+WIDTH*0.5, baseY+WIDTH/2), WIDTH/2)
			basePivot[0] = Pos(LEFTMOST, baseY+WIDTH/2)
			basePivot[1] = Pos(LEFTMOST+WIDTH*0.5, baseY)
			basePivot[2] = Pos(LEFTMOST+WIDTH, baseY+WIDTH/2)
		else:
			ret += drawSmileArc(Pos(LEFTMOST+WIDTH*0.5, baseY-WIDTH/2), WIDTH/2)
			basePivot[0] = Pos(LEFTMOST, baseY-WIDTH/2)
			basePivot[1] = Pos(LEFTMOST+WIDTH*0.5, baseY)
			basePivot[2] = Pos(LEFTMOST+WIDTH, baseY-WIDTH/2)
	elif "rq`w".find(INITIAL_LIST[initial]) != -1: #initials is one of "rq`w". Inverted semi circle
		if rootAtTop:
			ret += drawSmileArc(Pos(LEFTMOST+WIDTH*0.5, baseY), WIDTH/2)
			basePivot[0] = Pos(LEFTMOST, baseY)
			basePivot[1] = Pos(LEFTMOST+WIDTH*0.5, baseY+WIDTH/2)
			basePivot[2] = Pos(LEFTMOST+WIDTH, baseY)
		else:
			ret += drawFrownArc(Pos(LEFTMOST+WIDTH*0.5, baseY), WIDTH/2)
			basePivot[0] = Pos(LEFTMOST, baseY)
			basePivot[1] = Pos(LEFTMOST+WIDTH*0.5, baseY-WIDTH/2)
			basePivot[2] = Pos(LEFTMOST+WIDTH, baseY)

	tailY = TOPMOST
	if rootAtTop:
		tailY = BOTTOMMOST

	#Construct the middle strokes and the hook for the initial and alt
	verticleStrokes = ["aeiou`".find(MIDDLE_LIST[middle]) != -1, "eyv`u".find(MIDDLE_LIST[middle]) != -1, "iyz`o".find(MIDDLE_LIST[middle]) != -1]
	halfVerticleStrokes = [False, "o".find(MIDDLE_LIST[middle]) != -1, "u".find(MIDDLE_LIST[middle]) != -1] # half-stroke
	#Determine the leftMost and rightMost
	for i in range(len(verticleStrokes)):
		if verticleStrokes[i]:
			if leftMost == -1:
				leftMost = i
			rightMost = i

	#Draw full verticle stroke
	for i in range(len(verticleStrokes)):
		if verticleStrokes[i]:
			#Draw the verticle stroke
			ret += drawLine(basePivot[i], Pos(basePivot[i].x, tailY))
			middlePivot[i] = Pos(basePivot[i].x, (basePivot[i].y+tailY)/2)
			middlePivotAvailable[i] = True

			#Draw the hook
			if hasHook and i == leftMost:
				if rootAtTop:
					ret += drawLine(Pos(basePivot[i].x, tailY), Pos(basePivot[i].x-SLASH_WIDTH, tailY-SLASH_WIDTH))
				else:
					ret += drawLine(Pos(basePivot[i].x, tailY), Pos(basePivot[i].x-SLASH_WIDTH, tailY+SLASH_WIDTH))
		else:
			middlePivot[i] = Pos(basePivot[i].x, (basePivot[i].y+tailY)/2)

	#Draw half verticle stroke
	for i in range(len(halfVerticleStrokes)):
		if halfVerticleStrokes[i]:
			ret += drawLine(basePivot[i], Pos(basePivot[i].x, (basePivot[i].y+tailY)/2))

	#Construct the finals
	yAdjustment = 0.0
	leftMostMiddlePivotUsed = middlePivot[leftMost]
	if FINAL_LIST[final] == 'i':
		if hasHook:
			yAdjustment = -WIDTH/3 if rootAtTop else WIDTH/3
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y-WIDTH/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+yAdjustment))
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+yAdjustment), Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y+WIDTH/2+yAdjustment))
	elif FINAL_LIST[final] == 'u':
		if hasHook:
			yAdjustment = -WIDTH/3 if rootAtTop else WIDTH/3
		midPoint = Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y+yAdjustment)
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y-WIDTH/2+yAdjustment), midPoint)
		ret += drawLine(midPoint, Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+WIDTH/2+yAdjustment))
	elif FINAL_LIST[final] == 'm':
		if hasHook and not rootAtTop:
			yAdjustment = WIDTH/2
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y-WIDTH/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+yAdjustment))
	elif FINAL_LIST[final] == 'n':
		if hasHook:
			yAdjustment = -WIDTH/3 if rootAtTop else WIDTH/3
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+yAdjustment))
	elif FINAL_LIST[final] == 'x':
		if hasHook and rootAtTop:
			yAdjustment = -WIDTH/2
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y+WIDTH/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+yAdjustment))
	elif FINAL_LIST[final] == 'p':
		if hasHook and not rootAtTop:
			yAdjustment = WIDTH/2
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y-WIDTH/2-DOUBLE_SLASH_SPACING/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y-DOUBLE_SLASH_SPACING/2+yAdjustment))
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y-WIDTH/2+DOUBLE_SLASH_SPACING/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+DOUBLE_SLASH_SPACING/2+yAdjustment))
	elif FINAL_LIST[final] == 't':
		if hasHook:
			yAdjustment = -WIDTH/3 if rootAtTop else WIDTH/3
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y-DOUBLE_SLASH_SPACING/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y-DOUBLE_SLASH_SPACING/2+yAdjustment))
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y+DOUBLE_SLASH_SPACING/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+DOUBLE_SLASH_SPACING/2+yAdjustment))
	elif FINAL_LIST[final] == 'k':
		if hasHook and rootAtTop:
			yAdjustment = -WIDTH/2
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y+WIDTH/2-DOUBLE_SLASH_SPACING/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y-DOUBLE_SLASH_SPACING/2+yAdjustment))
		ret += drawLine(Pos(leftMostMiddlePivotUsed.x-WIDTH/2, leftMostMiddlePivotUsed.y+WIDTH/2+DOUBLE_SLASH_SPACING/2+yAdjustment), Pos(leftMostMiddlePivotUsed.x, leftMostMiddlePivotUsed.y+DOUBLE_SLASH_SPACING/2+yAdjustment))

	return ret

def generateSvg(path, codePoint):
	f = open(path, 'w+')
	f.write(header)
	f.write(constructCharacter(codePoint))
	f.write(footer)
	f.close()

pathlib.Path("./generatedGlyphs").mkdir(parents=True, exist_ok=True)

for i in range(CODEPOINT_BASE_SADALIAN, CODEPOINT_END_SADALIAN): 
	generateSvg("./generatedGlyphs/"+str(i)+".svg", i)

