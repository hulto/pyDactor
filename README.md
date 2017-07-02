# pyDactor
pyDactor is a tool I wrote to assist in writing reports.
It allows assessors to quickly and reliably redact images of sensitive data (names, IPs, password hashes, etc.)
I built pyDactor using the Google Tesseract OCR python API: tesserocr.
You provide pyDactor with a file or the directory with all the files you wish to redact.
You also provide a regular expression selecting the characters, or words that you want deleted.
pyDactor reads in the images one at a time; using the tesserocr library it reads the text in the images and gets their location in the image.
Each line is then run through the regular expression provided and any matched characters are drawn over with black boxes using the PIL library.



INSTALL

sudo apt-get install tesseract-ocr

git clone https://github.com/hulto/pyDactor.git


SETUP

•Put the redaction script into the folder with images to redact

•Create a wordlist file

•Put each word you want to redact on its own line


<b>Usage:</b>
<br>
<code>
python main.py -f '/path/to/image(s)' -e 'regular.expression' [-q]
</code>
<br>
<code>
-f    file path
</code>
<br>
<code>
-e    regular expression
</code>
<br>
<code>
-q    quite mode won't open image after processing, instead will save to disk.
</code>
