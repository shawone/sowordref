# Author: Nicolas Chevalier
# https://github.com/shawone/sowordref.git
#
# Wordreference parsing
#! /bin/sh
""":"
exec python $0 ${1+"$@"}
"""

import urllib2
import contextlib
import sys
import cStringIO
import argparse

from HTMLParser import HTMLParser
from pprint import pprint

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    yield
    sys.stdout = save_stdout

class MyHTMLParser(HTMLParser):
    flagtranslation = None
    flagstrong = None
    flagabbr = None
    flagnewline = None
    flagspan = None
    splitfirstword = None
    listeline = []

    def __init__(self, websrc):
        HTMLParser.__init__(self)
        self.feed(websrc.read())

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            attrD = dict(attrs)
            for key in attrD:
                if key == "id":
                    self.flagtranslation = True
                else:
                    self.flagtranslation = None
        
        if tag == 'em':
            self.flagabbr = True
        if tag == 'span':
            self.flagspan = True
        if tag == 'strong':
            self.flagstrong = True

    def handle_endtag(self, tag):
        if tag == 'em':
            self.flagabbr = None
        if tag == 'span':
            self.flagspan = None
        if tag == 'tr':
            for k in self.listeline:
                if len(k) != 2:
                    sys.stdout.write(k)
                if len(k) == 2:
                    if len(k[0]) != 1 and len(k[1]) != 1:
                        sys.stdout.write(k)
            self.listeline = []
        if tag == 'strong':
            self.flagstrong = None

    def handle_data(self, data):
        if self.flagtranslation == True and self.flagabbr == None:
            if self.flagstrong == True:
                self.splitfirstword = False
                self.listeline.append("\n\033[31m"+data+"\033[0m ")
            else:
                if data.startswith("Next"):
                    endprogram(False)
                self.listeline.append(data)
        if self.flagabbr == True:
            if self.flagspan == True and self.splitfirstword == False:
                self.listeline.append("\033[34m"+data+"\033[0m ")
                self.splitfirstword = True

def endprogram(state):
    if state == False:
        print "\n\nsource: http://www.wordreference.com\n(END)\n" 
        exit(0)
    else:
        print "\n\nsource: http://www.wordreference.com\n(END)\n" 

def argparser():
    reload(sys)
    sys.setdefaultencoding("UTF8")

    flagerror = None
    langsrc = "fr"
    langdst = "en"    
    parser = argparse.ArgumentParser()

    parser.add_argument("word", help="word to translate", type=str)
    parser.add_argument("-i", "--langsource", 
                        help="language source (ex: en) iso 639-1 https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes")
    parser.add_argument("-o", "--langdestination", 
                        help="language source (ex: fr) iso 639-1 https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes")

    args = parser.parse_args()

    if (args.langsource and not args.langdestination) or (args.langdestination and not args.langsource):
        parser.error("Please use -i <language> and -o <language> together (fr => eng by default)")

    if args.langsource and args.langdestination:
        langsrc = args.langsource
        langdst = args.langdestination

    if args.word:
        word = args.word
        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        with nostdout():
            try:
                response = opener.open("http://www.wordreference.com/"+langsrc+langdst+"/"+word)
            except urllib2.URLError:
                flagerror = True
        if flagerror == True:
            print "Request Http Error, please check your connection"
            exit (0)
        print "========= Wordreference Translation of " + word + ": " + langsrc  + " => " + langdst  + "  ==========="
        myparser = MyHTMLParser(response)
        endprogram(True)

def main():
    argparser()

if __name__ == "__main__":
    main()
