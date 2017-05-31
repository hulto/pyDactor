'''
<one line to give the program's name and a brief idea of what it does.>
Copyright (C) <year>  <name of author>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

#Makes use of tesseract-ocr project
#https://github.com/tesseract-ocr/

from PIL import Image
import getopt
import sys
from xml.dom import minidom
import os


def usage():
    print "Usage python redact.py </path/to/files>\n\
      -a automatic\n\
      -h help\n\
      -w wordlist file\n\
      -d delimiter"

pth = ""
wordlist = ""

try:
  opts, args = getopt.getopt(sys.argv[1:], "hf:w:", ["help", "file(s) path", "wordlist path"])
except getopt.GetoptError as err:
  print str(err)
  usage()
  sys.exit(2)
for o, a in opts:
  if o == "-h":
    usage()
    sys.exit
  elif o == "-f":
    pth = a
  elif o == "-w":
    wordlist = a
  else:
    assert False, "unhandled option"
if len(pth) < 1 or len(wordlist) < 1:
  usage()
  sys.exit(2)

#pth = raw_input("Please enter path of images\n")
#wordlist = raw_input("Please enter path of word list\n")



def main(path, wordlist):
  cleanup(path)
  filelist = [f for f in os.listdir(path)]
  for f in filelist:
    if f.endswith('.png') or f.endswith('.jpg'):
      print f
      tess(f)
      rundact(f, wordlist)
  cleanup(path)

  
def cleanup(path):
  filelist = [f for f in os.listdir(path) if f.endswith('.hocr') ]
  for f in filelist:
    os.remove(f)

def tess(filename):
  os.system('tesseract ' + filename + ' ' + filename.split('.')[len(filename.split('.'))-2] + ' hocr')

#Interpret user input
#defGetInput

testFileNames = ['test.hocr']

def rundact(filenames, wordlist):
  #execute tesseract  
  fo = open(wordlist)
  linesArr = fo.read().split('\n')
  x = filenames
  newX = x.split('.')[len(x.split('.'))-2] + '.hocr'
  resArr = []
  XMLArr = parseXML(newX)
  for y in linesArr[:-1]:
    for i in range(0, len(XMLArr)):
      if y in XMLArr[i][4]:
        print XMLArr[i][4]
        print 'found ' + y + ' in text'
        resArr.append(XMLArr[i])
  print resArr
  ptArr = []
  for a in resArr:
    print a[1]
    ptArr.append([int(a[0]), int(a[1]), int(a[2]), int(a[3])])
  redactImage(x, ptArr) 

#files - list of .hocr files
def parseXML(file):
  strArr = []
  i = 0
  xmldoc = minidom.parse(file)
  span = xmldoc.getElementsByTagName("span")
  for a in span:
    if a.getAttribute('class') == 'ocrx_word':
      if a.firstChild.nodeValue != None:
        boxArr = a.getAttribute('title').split(' ')
        entry = boxArr[1] + ' ' + boxArr[2] + ' ' + boxArr[3] + ' ' + boxArr[4][:-1] + ' ' + a.firstChild.nodeValue
        #print entry
        strArr.append(entry.split(' '))
  return strArr

#itterate through ptArray looking for strings in wordlist
#ptArray - array of points and text
#strings - wordlist of words to redact
def findStrings(filename, ptArray, strings): 
  for x in ptArray:
    print x 
  #iterate through ptArray
  #Check for if string from strings is present
  #call redactWord

pointArray = [[346,13,468,33],[10,13,329,39]]

def redactImage(filename, arr):
  img = Image.open(filename)
  for x in arr:
   redactWord(img, x[0], x[1], x[2], x[3], 0, 0)
  img.show()

#Redact word from filename give the boundingbox
def redactWord(img, left, top, right, bottom, buffer, color):
  pix = img.load()
  i = 0
  for x in range(left-buffer, right+buffer):
    for y in range(top-buffer, bottom+buffer):
      pix[x,y] = color
      i = i+1
  print "Redacted " + str(i) + " pixels"


main(pth, wordlist)
