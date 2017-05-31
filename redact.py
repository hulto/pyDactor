'''
pyDactor - Jack McKenna (Hulto)
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

#Displays proper usage
def usage():
    print "Usage python redact.py -f '.' -w 'path/to/wordlist.txt'\
      -h help\n\
      -w wordlist file\n\
      -f path to image file(s) [should be '.']"

#Main execution
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


#Main funciton takes in path to files and wordlist
def main(path, wordlist):
  #cleansup workspacs
  cleanup(path)
  #Iterates through all files in directory
  filelist = [f for f in os.listdir(path)]
  for f in filelist:
    #Checks for png and jpg files
    if f.endswith('.png') or f.endswith('.jpg'):
      print f
      #runs tesseract ocr on them with hocr flag
      # $ tesseract <image> <imagename> hocr
      tess(f)
      #Launches redaction
      rundact(f, wordlist)
  #Clean up .hocr files afterwards
  cleanup(path)

  
def cleanup(path):
  #Iterate through directory
  filelist = [f for f in os.listdir(path) if f.endswith('.hocr') ]
  for f in filelist:
    #Remove all files with .hocr file ending
    os.remove(f)

#Execute tesseract binary: https://github.com/tesseract-ocr/
def tess(filename):
  os.system('tesseract ' + filename + ' ' + filename.split('.')[len(filename.split('.'))-2] + ' hocr')

#Runs redaction
def rundact(filenames, wordlist):
  #Get words from word list 
  fo = open(wordlist)
  linesArr = fo.read().split('\n')
  #Generate <image name>.hocr file path
  x = filenames
  newX = x.split('.')[len(x.split('.'))-2] + '.hocr'
  resArr = []
  #Parse hocr XML for bounding boxes
  XMLArr = parseXML(newX)
  #Iterate through wordlist checking XML 
  #document for instances of words t be redacted
  for y in linesArr[:-1]:
    for i in range(0, len(XMLArr)):
      if y in XMLArr[i][4]:
        print XMLArr[i][4]
        print 'found ' + y + ' in text'
        #Store entries to be redacted in resArr
        resArr.append(XMLArr[i])
  print resArr
  ptArr = []
  #Iterate through resArr storing only the points and not the text
  for a in resArr:
    print a[1]
    #Create list of points to redact
    ptArr.append([int(a[0]), int(a[1]), int(a[2]), int(a[3])])
  redactImage(x, ptArr) 

#file - .hocr file
def parseXML(file):
  strArr = []
  i = 0
  xmldoc = minidom.parse(file)
  #Get applicable elemnts
  span = xmldoc.getElementsByTagName("span")
  for a in span:
    if a.getAttribute('class') == 'ocrx_word':
      if a.firstChild.nodeValue != None:
        #Store bounding box
        boxArr = a.getAttribute('title').split(' ')
        #Store text value
        entry = boxArr[1] + ' ' + boxArr[2] + ' ' + boxArr[3] + ' ' + boxArr[4][:-1] + ' ' + a.firstChild.nodeValue
        #print entry
        strArr.append(entry.split(' '))
  return strArr

#NOT USED
#itterate through ptArray looking for strings in wordlist
#ptArray - array of points and text
#strings - wordlist of words to redact
def findStrings(filename, ptArray, strings): 
  for x in ptArray:
    print x 
  #iterate through ptArray
  #Check for if string from strings is present
  #call redactWord

#Redact image given a set of points
def redactImage(filename, arr):
  img = Image.open(filename)
  #Iterate through points
  for x in arr:
    #Redact each word
   redactWord(img, x[0], x[1], x[2], x[3], 0, 0)
  #Display image
  img.show()

#Redact word from filename give the boundingbox
def redactWord(img, left, top, right, bottom, buffer, color):
  pix = img.load()
  i = 0
  #Iterate through bounded area coloring out pixels
  for x in range(left-buffer, right+buffer):
    for y in range(top-buffer, bottom+buffer):
      pix[x,y] = color
      i = i+1
  print "Redacted " + str(i) + " pixels"


main(pth, wordlist)
