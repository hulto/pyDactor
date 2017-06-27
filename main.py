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
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#Makes use of tesseract-ocr project
#https://github.com/tesseract-ocr/
import api
import getopt
import sys
import os


def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hqrf:e:", ["help", "quite", "recursive", "file=", "expression="])
  except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
  quite = False
  recursive = False
  filePath = ""
  regExpr = ""
  for o, a in opts:
    if o == '-h':
      usage()
      sys.exit()
    elif o == '-f':
      filePath = a
    elif o == '-e':
      regExpr = a
    elif o == '-r':
      recursive = True
    elif o == '-q':
      quite = True
    
  if os.path.isdir(filePath):
    #Run on all files in dir
    if(recursive):
      for dirname, dirnames, filenames in os.walk(filePath):
        # print path to all subdirectories first.
        for subdirname in dirnames:
          print(os.path.join(dirname, subdirname))

        # print path to all filenames.
        for filename in filenames:
          print(os.path.join(dirname, filename)) 
          api.main(os.path.join(dirname, filename), regExpr, quite)
    else:
      for filename in os.listdir(filePath):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.gif') or filename.endswith('.tif'):
          print filename
          api.main(filePath + '/' + filename, regExpr, quite)
         
 
  elif os.path.isfile(filePath):
    api.main(filePath,regExpr,quite)




main()
