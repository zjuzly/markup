import sys, re
from util import *
from handlers import *
from rules import *


class Parser:

    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:
                        break
                    
        
        self.handler.end('document')


class BasicTextParser(Parser):
    
    def __init__(self, handler):
        Parser.__init__(self, handler) 
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([.a-zA-Z_]+@[.0-9a-zA-Z]+)', 'mail')


handler = HTMLRender()
parser = BasicTextParser(handler)

parser.parse(sys.stdin)


#print('<html>\n\t<head>\n\t\t<title>......</title>\n\t</head>\n\t<body>')
#
#title = True
#for block in blocks(sys.stdin):
#	block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
#	if title:
#		print('<h1>')
#		print(block)
#		print('</h1>')
#		title = False
#	else:
#		print('<p>')
#		print(block)
#		print('</p>')
#print('\n\t</body></html>')
