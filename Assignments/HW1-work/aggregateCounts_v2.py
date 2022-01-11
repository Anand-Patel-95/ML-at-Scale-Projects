#!/usr/bin/env python
"""
This script reads word counts from STDIN and aggregates
the counts for any duplicated words.

INPUT & OUTPUT FORMAT:
    word \t count
USAGE (standalone):
    python aggregateCounts_v2.py < yourCountsFile.txt

Instructions:
    For Q7 - Your solution should not use a dictionary or store anything   
             other than a single total count - just print them as soon as  
             you've added them. HINT: you've modified the framework script 
             to ensure that the input is alphabetized; how can you 
             use that to your advantage?
"""

# imports
import sys


################# YOUR CODE HERE #################
word_prev = None
total_count = 0

# stream over lines from Standard Input
for line in sys.stdin:
    # extract words & counts
    word, count  = line.split()
    # print(f"line: {word} {count}")
   
    if word == word_prev:
        # if the same word, add to count
        word_prev = word
        total_count += int(count)
    else:
        # if previous word exists, emit previous word & count
        if word_prev:
            print("{}\t{}".format(word_prev, total_count))
        
        # set new word_prev and total_count
        word_prev = word
        total_count = int(count)
    
    # print(f"current: {word_prev} {total_count}")
        

# print out the last word and total count
# since it will not print in loop until word changes
print("{}\t{}".format(word_prev, total_count))


################ (END) YOUR CODE #################
