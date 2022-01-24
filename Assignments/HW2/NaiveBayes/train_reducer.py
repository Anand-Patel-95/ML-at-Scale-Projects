#!/usr/bin/env python
"""
Reducer aggregates word counts by class and emits frequencies.

INPUT:
    partitionKey \t word \t class0_partialCount,class1_partialCount
OUTPUT:
    word \t ham_count,spam_count,P(ham|word),P(spam|word)
    
Instructions:
    Again, you are free to design a solution however you see 
    fit as long as your final model meets our required format
    for the inference job we designed in Question 8. Please
    comment your code clearly and concisely.
    
    A few reminders: 
    1) Don't forget to emit Class Priors (with the right key).
    2) In python2: 3/4 = 0 and 3/float(4) = 0.75
"""
##################### YOUR CODE HERE ####################
import sys
import numpy as np

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
            relative_freqs = current_counts / wordTotalCount # rel_freq ham, rel_freq spam
            print(f"{current_word}\t{current_counts[0]},{current_counts[1]},{relative_freqs[0]},{relative_freqs[1]}")
        # set new word as current, along with its counts as current count
        current_word = word
        current_counts = np.array(counts)

# emit last record
relative_freqs = current_counts / wordTotalCount # rel_freq ham, rel_freq spam
print(f"{current_word}\t{current_counts[0]},{current_counts[1]},{relative_freqs[0]},{relative_freqs[1]}")

# calculate and emit priors
ClassPriors = docTotalCount / sum(docTotalCount)
print(f"ClassPriors\t{docTotalCount[0]},{docTotalCount[1]},{ClassPriors[0]},{ClassPriors[1]}")




##################### (END) CODE HERE ####################