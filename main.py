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
