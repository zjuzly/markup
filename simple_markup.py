import sys, re
from util import *

print('<html>\n\t<head>\n\t\t<title>......</title>\n\t</head>\n\t<body>')

title = True
for block in blocks(sys.stdin):
	block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
	if title:
		print('<h1>')
		print(block)
		print('</h1>')
		title = False
	else:
		print('<p>')
		print(block)
		print('</p>')
print('\n\t</body></html>')
