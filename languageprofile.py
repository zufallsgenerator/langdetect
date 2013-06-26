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
# This script contains the language profile class, holding tri- and
# quadgrams of letters along with their relative frequency. 
# 
# It has the ability to generate frequency tables from corpora aswell
# as loading them. It can also compare language profiles and return
# a scoring for the likeness of the two language profiles (used for
# language detection).
# 

import os
import re

class LanguageProfile:
    """Language profile using triagrams with relative frequency scores"""
    MAX_ENTRIES = 200
    DISCOUNT_FACTOR = 0.8
    global_parts = dict()
    def __init__(self):
        self.parts = dict()
        self.sorted_keys = []
        self.sorted_dict = dict()
        self.from_file = False
        self.garbagefilter = re.compile("[0-9]+")

    def load_profile(self, filename):
        """Load a per-parsed profile from a file"""
        if not os.path.isfile(filename):
            print "Not a file: " + filename
            return
            
            
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        self.sorted_keys = []

        for line in lines:
            parts = [part.rstrip().lstrip().lower() for part in line.split(" ")]
            if len(parts) > 1:
                self.sorted_keys.append(parts[1])
                self.sorted_dict[parts[1]] = parts[0]

                # Set flag, flagging us as a profile loaded from a file
                self.from_file = True
  
    def _remove_garbage(self, word):
        ary = []    
        for c in word:
            if ord(c) > 64:
                ary.append(c)
        return str.join("",ary)
  
    def parse_file(self, filename):
        """Parse a file and add to language profile"""
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
    
        result = dict()
        for line in lines:
            words = [ self._remove_garbage(word.rstrip().lstrip().lower()) for word in line.split()]
                # Get parts
            for word in words:
                wordlen = len(word)
                
                if wordlen > 2:
                    for maxlen in xrange(3,6):
                        for i in xrange(0,wordlen-maxlen+1):
                            key = word[i:(i+maxlen)]
                            if self.parts.has_key(key):
                                self.parts[key] += 1
                            else:
                                self.parts[key] = 1
                                # If I add it the first time, add an extra entry for global parts
                                if self.global_parts.has_key(key):
                                    self.global_parts[key] += 1
                                else:
                                    self.global_parts[key] = 1
                
                  
              
    def _get_sorted_parts(self):
        """Get sorted key list, based on value of dictionary"""
        d = self.parts
        return sorted(d, key = lambda cur_key: -d[cur_key])
 
    def _print_dict(self, d, keys):
        for key in keys:
            print str(d[key]) + " " + key 

    def discount_for_global(self):
        """Recalculate the score for a part, make it smaller if it occurs in other languages
             This function could be improved with discount relative to the word scoring of 
             other languages.
        """
        d = self.parts
        g = self.global_parts
        for key in d.keys():
            if g[key]:
                # Too high language discount makes it hard on languages that share many
                # commonalites with other languages
                d[key] = d[key] * ( self.DISCOUNT_FACTOR**g[key] ) 
        
            
    def _normalize_keys(self):
        if self.from_file:
            return
            
        d = self.parts
        # Normalize
        sum = 0
        for key in d.keys():
            sum += d[key] 
            
        sorted_keys = self._get_sorted_parts()[0:self.MAX_ENTRIES]
        
        if len(sorted_keys) == 0:
                return
        
        top_key = sorted_keys[0] # TODO: What if we have an empty list?
        normalized = float(100 * sum / d[top_key])
        
        self.sorted_dict = sorted_dict = dict()
        
        for key in sorted_keys:
            sorted_dict[key] = int(round((d[key] * normalized) / sum))
            
        self.sorted_keys = sorted_keys
    
    def print_freq(self):
        # Get sorted keys
        self._normalize_keys()
        self._print_dict(self.sorted_dict, self.sorted_keys)
        
    def save_profile(self, path):
        # Get sorted keys
        self._normalize_keys()
        fout = open(path,"w")
        for key in self.sorted_keys:
            line = (str(self.sorted_dict[key]) + " " + key + "\n") #.encode("utf-8")
            fout.write(line)
        fout.close()
        
    def compare(self, other):
        """Compare a profile to another """
        self._normalize_keys()
        other._normalize_keys()
        
        other_keys = other.sorted_keys
        
        other_len = len(other_keys)
        self_len = len(self.sorted_keys)
        
        # Sanity check
        if other_len == 0 or self_len == 0:
          print "ERROR!"
          return 0
        
        co_occur = 0.0
                        
        for other_key in other.sorted_keys:
            if self.sorted_dict.has_key(other_key):
                self_score = int(self.sorted_dict[other_key])
                other_score = int(other.sorted_dict[other_key])
#                print "Match: " + other_key + " " + str(self_score) 
                co_occur += (1 + ( self_score * 0.2))
            
        
        co_occur_normalized = round((co_occur * self.MAX_ENTRIES) / other_len)
        
        return co_occur_normalized
