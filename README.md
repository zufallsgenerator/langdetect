Simple Language Detection System 0.1

This is a set of python (tested with version 2.4.4 and 2.6.1) scripts that generates a set of trigrams and 
quadgrams from a corpus to generate frequency tables which are used
for language identification. 
This is a quick hack that I decided to publish. There are already 
much better systems around, but I wanted to try out a simple idea.

The files are the following:

license.txt        - MIT license file
readme.txt         - this file
train.py           - build frequency tables from a corpora
languageprofile.py - the language profile / frequency table class
detect.py          - uses the frequency tables in the folder freq
                     to detect the language of the given input file

freq/*.txt         - frequency tables for languages
corpus/<lang>/*    - add text files here from each language and run
                     train.py to generate frequency tables
              
example.py         - Example of language detection              
examples/test1.txt - Small Swedish text
examples/test2.txt - Small English text
examples/test3.txt - Small German text
                     
There's no corpus included, since I only randomly grabbed text from
wikipedia, online newspapers etc and generated a frequency tables.

You can do that yourself, for whatever language you want to detect.
I originally had a norwegian corpus aswell, but the problem was that
the norwegian frequency tables got an unproportinately high scoring,
so that it was almost a tie between German and Norwegian on a German
text, and Swedish was identified as Norwegian.

Christer Byström, March 2009
