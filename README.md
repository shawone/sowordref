sowordref
=========

wordreference translation in your shell


usage
=========

usage: <br/>
<pre>wordref.py [-h] [-i LANGSOURCE] [-o LANGDESTINATION] word</pre>
<br/>
optional arguments: <br/> 
  -i LANGSOURCE  / -o LANGDESTINATION : <br/>
  language source (ex: en) iso 639-1 https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes <br/>
<br/>
<br/>
<br/>
Example: <br/>
<pre>python wordref.py bonjour</pre>
<br/>
Output:<br/>
<br/>
<p align="center">
<img width="800" height="400" src="https://raw.githubusercontent.com/shawone/sowordref/master/github-cap.png">
<p/>
<br/>
Example: <br/>
<pre>python wordref.py thanks -i en -o ja</pre>
<br/>
Output:<br/>
<br/>
<p align="center">
  <img width="800" height="200" src="https://raw.githubusercontent.com/shawone/sowordref/master/github-en-ja.png">
<p/>
<br/>
<br/>
<br/>

Installation
============
<pre>
sudo cp wordref.py /usr/bin/translate
translate -h
translate bonjour
</pre>
