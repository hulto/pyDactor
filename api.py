'''
pyDactor - Jack McKenna (Hulto)
Copyright (C) 2017 Jack McKenna

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


import tesserocr
from PIL import Image
import re

class Letter:
  """Class to hold each letter with it position"""
  def __init__(self,chr, left, top, right, bottom):
    self.left = left
    self.top = top
    self.right = right
    self.bottom = bottom
    self.chr = chr
  def __str__(self):
    return displayLtr(self)

class BoxString:
  def __init__(self, chrs):
     self.chrs = chrs
     self.litString = ''
     for x in chrs:
       self.litString += str(x.chr)
  def __str__(self):
    return self.litString

class BoxLine:
  def __init__(self, wrds):
    self.wrds = []
    self.wrds = wrds
    self.litString = ''
    for x in wrds:
      self.litString += ' ' + str(x)
    self.litString = self.litString.strip() 
  def __str__(self):
    return self.litString
  def GetWords(self):
    return self.wrds


def displayLtr(ltr):
  return str(ltr.chr) + ' ' + str(ltr.left) + ' ' + str(ltr.top) + ' ' + str(ltr.right) + ' ' + str(ltr.bottom)


"""
1. Open Image file
1.5  Get total length without spaces or new lines to be used as a counter later
2. Read file for line breaks
3. Read lines for words ' '
4. Get character bounding boxes for each char

"""
def parse(api, img, exp):
  delArr = []
  arr = []
  api.SetImage(img)
  textBlock = api.GetUTF8Text()
  #print textBlock
  boxLines = api.GetBoxText(0).split('\n');
  max = len(''.join(textBlock.split()))
  i = 0
  data = []
  for x in textBlock.split('\n'):
    """
    Perform Regex expressions
    Get groups
    Replace
    """
    r = re.findall(exp, str(x))
    if( r != None ):
      tmp = str(x)
      for a in r:
        l = len(a)
        tmp = re.sub(a, "*"*l, tmp)
      x = tmp
      """
      Continue
      """
      
    #print str(x)    

    #Create new line
    wrds = []
    for y in x.split(' '):
      #Create new word
      chrs = []
      
      
      #Set max top and bottom for proper blocking
      maxTop = img.size[1]
      maxBottom = 0
      
      ii = i
      for k in range(0, len(y)):
        
        if int(boxLines[ii].split(' ')[2]) < maxTop:
          maxTop = int(boxLines[ii].split(' ')[2])
        if int(boxLines[ii].split(' ')[4]) > maxBottom:     
          maxBottom = int(boxLines[ii].split(' ')[4])
        ii+=1
 
      for j in range(0, len(y)):
        #print 'bottom ' + str(maxBottom) + ' top ' + str(maxTop) 
        ltr = Letter(boxLines[i].split(' ')[0], int(boxLines[i].split(' ')[1]), maxTop, int(boxLines[i].split(' ')[3]), maxBottom)
        if y[j] is '*':
          delArr.append(ltr)
        """
        
        Add Letter to array to be blocked out
        """
#        displayLtr(ltr)
        chrs.append(ltr)
        i+=1
      boxString = BoxString(chrs)
      #print '[WORD] ' + str(boxString)
      wrds.append(boxString)
    boxLine = BoxLine(wrds)
    #print '[LINE] ' + str(boxLine)
    data.append(boxLine)
#  print "from parse(data[0]): " + str(data[0])
  return delArr

#Redact word from filename give the boundingbox
def redactWord(img, left, top, right, bottom, buffer, color):
  pix = img.load()
  width, height = img.size
  i = 0
  #Fuck you for switching my coordinate plane @tesserocr
  t = height-bottom
  b = height-top

  top = t
  bottom = b
  

  #Iterate through bounded area coloring out pixels
  for x in range(left-buffer, right+buffer):
    for y in range(top-buffer, bottom+buffer):
      pix[x,y] = color
      i = i+1
#  print "Redacted " + str(i) + " pixels"


def main(imagePath, regExp, quite):
  img = Image.open(imagePath);
  api = tesserocr.PyTessBaseAPI("/usr/share/tesseract-ocr/tessdata","eng") 
  api.SetVariable("tessedit_char_whitelist","ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:;\"'{}[]\|,./<>?!@#$%^&*()_+-=~`")
  #api.SetImage(img)
  #print api.GetUTF8Text() 
  data = parse(api, img, regExp)
  #blank(data, "^coalfire|^kali|ATD") 
  for x in data:
    redactWord(img, x.left, x.top, x.right, x.bottom, 0, 0) 
  if(quite):
    img.save(imagePath.split('.')[len(imagePath.split('.'))-2] + '.safe' + '.' + imagePath.split('.')[len(imagePath.split('.'))-1])
  else:
    img.show()
  



#main('test1.png', "^coalfire|^kali|ATD")
