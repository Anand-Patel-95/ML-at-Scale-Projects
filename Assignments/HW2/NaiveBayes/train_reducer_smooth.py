#!/usr/bin/env python

import os
import sys                                                  
import numpy as np  

#################### YOUR CODE HERE ###################

# get the vocabulary size from environment variables
# total ENRON = 5065, Chinese dataset = 6, ENRON training = 4555
V = int(os.getenv('VOCAB', default=6)) # default to chinese dataset size if nothing is specified

# get the smoothing parameter, default is +1
k = int(os.getenv('SMOOTH', default=1))

# initialize counts
# ham, spam docs
docTotalCount = np.array([0.0,0.0])
# ham, spam words
wordTotalCount = np.array([0.0,0.0])
current_word = None
current_counts = np.array([0.0,0.0])

# read in records
for line in sys.stdin:
    pk, word, count_bundle = line.split('\t')           # unpack the line
    counts = [int(n) for n in count_bundle.split(',')]  # unpack the counts class0_partialCount,class1_partialCount
    
    # check for special keys
    if word == "*docTotalCount":
        docTotalCount += counts
    elif word == "*wordTotalCount":
        wordTotalCount += counts
    # check if current word is this word
    elif word == current_word:
        # increment this word's current counts
        current_counts += counts
    else:
        # new word, emit the last one
        if current_word:
            relative_freqs = (current_counts + [k, k]) / (wordTotalCount + [V, V]) # rel_freq ham, rel_freq spam
            print(f"{current_word}\t{current_counts[0]},{current_counts[1]},{relative_freqs[0]},{relative_freqs[1]}")
        # set new word as current, along with its counts as current count
        current_word = word
        current_counts = np.array(counts)

# emit last record
relative_freqs = (current_counts + [k, k]) / (wordTotalCount + [V, V]) # rel_freq ham, rel_freq spam
print(f"{current_word}\t{current_counts[0]},{current_counts[1]},{relative_freqs[0]},{relative_freqs[1]}")

# calculate and emit priors
ClassPriors = docTotalCount / sum(docTotalCount)
print(f"ClassPriors\t{docTotalCount[0]},{docTotalCount[1]},{ClassPriors[0]},{ClassPriors[1]}")



#################### (END) YOUR CODE ###################