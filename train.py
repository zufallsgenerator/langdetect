#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Simple Language Detection System 0.1
#
# Copyright (c) 2009 Christer Byström
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

#
# This script expects a directory structure with a folder with 
# corpora for each language in the sub folders, like the following:
#
# corpus/
# corpus/en
# corpus/de
# corpus/fr
# 
# Where the last folders contains corpus for each language (in the 
# example, the folder names are ISO-639-1 language codes).
#
# The output ist frequency tables, output in the folder freq with 
# names as the folders, but with .txt added.
# 

import sys
import os
from languageprofile import *

CORPUS_PATH = "corpus"
FREQ_PATH = "freq"


def parse_lang(lang):
    profile = LanguageProfile()
    langpath = CORPUS_PATH + "/" + lang
    for filename in os.listdir(langpath):
        fullpath = langpath + "/" + filename
        if os.path.isfile(fullpath):
            profile.parse_file(fullpath)

    return profile


def init():

    profiles = dict()

    lang_keys = os.listdir(CORPUS_PATH)

    for lang_key in lang_keys:
        print "Parsing language: " + lang_key
        profiles[lang_key] = parse_lang(lang_key)

    for lang_key in lang_keys:
        print "Normalizing language: " + lang_key
        profiles[lang_key].discount_for_global()
        print "Saving language: " + lang_key
        profiles[lang_key].save_profile(FREQ_PATH + "/" + lang_key + ".txt")
    
        
if __name__ == "__main__": init()
