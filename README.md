# pyDactor
Redact images with googles tesseract ocr tool


INSTALL
sudo apt-get install tesseract-ocr
git clone ....

SETUP
•Put the redaction script into the folder with images to redact
•Create a wordlist file
•Put each word you want to redact on its own line

EXECUTION
python -f '.' -w 'wordlist.txt'
