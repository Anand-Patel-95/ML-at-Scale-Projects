#!/usr/bin/env python
"""
Reducer takes words with their class and partial counts and computes totals.
INPUT:
    word \t class \t partialCount 
OUTPUT:
    word \t class \t totalCount  
"""
import re
import sys

# initialize trackers
current_word = None
spam_count, ham_count = 0,0

# read from standard input
for line in sys.stdin:
    # parse input
    word, is_spam, count = line.split('\t')
    
############ YOUR CODE HERE #########
    # input stream is sorted, so check if current word is the word:
    if current_word == word:
        # add to the appropriate spam/ham counter
        if is_spam == "1":
            spam_count += int(count)
        else:
            ham_count += int(count)
    else:
        # if current_word exists, we are switching to new word so emit
        if current_word:
            print(f"{current_word}\t{1}\t{spam_count}")
            print(f"{current_word}\t{0}\t{ham_count}")
        
        # set new word to current
        current_word = word
        # add to the appropriate spam/ham counter
        spam_count, ham_count = 0,0 # reset the spam/ham counters
        if is_spam == "1":
            spam_count = int(count)
        else:
            ham_count = int(count)

# print out last record
print(f"{current_word}\t{1}\t{spam_count}")
print(f"{current_word}\t{0}\t{ham_count}")




############ (END) YOUR CODE #########