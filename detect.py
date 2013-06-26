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
# This script reads in frequency tables for different languages
# and compares them with a text file whose language is to be
# determined.
#
# This script expect frequency tables in the folder "freq", with 
# names of the form <language code>.txt
#
# It outputs the language scoring for each language in the folder
# "freq"
#

import sys
import os
from languageprofile import *

if len(sys.argv) < 2:
  print "Usage: " + sys.argv[0] + " [file]"
  sys.exit(1)
  
path = sys.argv[1]
  

profiles = dict()

FREQ_PATH = "freq"

for filename in os.listdir(FREQ_PATH):
    key = filename.split(".")[0]
    cur_profile = LanguageProfile()
    try:
        fullpath = FREQ_PATH + "/" + filename
        if os.path.isfile(fullpath):
            cur_profile.load_profile(fullpath)
            profiles[key] = cur_profile         
    except IOError:
        print "Error parsing file " + fullpath
    
    

detect_profile = LanguageProfile()

detect_profile.parse_file(path)

scores = dict()

for profile_key in profiles.keys():
    cur_profile = profiles[profile_key]
    scores[profile_key] = cur_profile.compare(detect_profile)

max_score = max(scores.values())

for score_key in scores.keys():
    if max_score == 0:
        scores[score_key] = 0
    else:
        scores[score_key] = int(round((scores[score_key] / max_score) * 100))

sorted_score_keys = sorted(scores, key = lambda cur_key: -scores[cur_key])

for key in sorted_score_keys:
    print key + " score: " + str(scores[key])

