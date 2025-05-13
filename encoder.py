from generatedFont.qss_mapping import QSS_MAP
import sys

def qss_encode(content):
	ret = ""
	buf = ""
	for c in content:
		if buf+c in QSS_MAP:
			buf += c
		else:
			if buf in QSS_MAP:
				ret += QSS_MAP[buf]
			else:
				ret += buf
			buf = c

	if buf in QSS_MAP:
		ret += QSS_MAP[buf]
	else:
		ret += buf
	return ret

for line in sys.stdin:
	print(qss_encode(line), end='')
