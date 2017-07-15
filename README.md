# pyDactor
pyDactor is a tool I wrote to assist in writing reports.
It allows assessors to quickly and reliably redact images of sensitive data (names, IPs, password hashes, etc.)
I built pyDactor using the Google Tesseract OCR python API: tesserocr.
You provide pyDactor with a file or the directory with all the files you wish to redact.
You also provide a regular expression selecting the characters, or words that you want deleted.
pyDactor reads in the images one at a time; using the tesserocr library it reads the text in the images and gets their location in the image.
Each line is then run through the regular expression provided and any matched characters are drawn over with black boxes using the PIL library.

<br>
If installing tesserocr doesn't work out. There is an ELF32 binary version available for download as well.
<br>

<b>Dependencies</b>
<ul>
<li>tesserocr - https://github.com/sirfz/tesserocr</li>
<li>PIL - https://askubuntu.com/questions/156484/how-do-i-install-python-imaging-library-pil</li>
</ul>

<b>Install</b>
<br>
<code>
git clone https://github.com/hulto/pyDactor.git
</code>
<br>
<code>
cd pyDactor
</code>
<br>


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
