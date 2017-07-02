# pyDactor
Redact images with googles tesseract ocr tool



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
