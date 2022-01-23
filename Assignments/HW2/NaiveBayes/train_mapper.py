#!/usr/bin/env python
"""
Mapper reads in text documents and emits word counts by class.
INPUT:                                                    
    DocID \t true_class \t subject \t body                
OUTPUT:                                                   
    partitionKey \t word \t class0_partialCount,class1_partialCount       
    

Instructions:
    You know what this script should do, go for it!
    (As a favor to the graders, please comment your code clearly!)
    
    A few reminders:
    1) To make sure your results match ours please be sure
       to use the same tokenizing that we have provided in
       all the other jobs:
         words = re.findall(r'[a-z]+', text-to-tokenize.lower())
         
    2) Don't forget to handle the various "totals" that you need
       for your conditional probabilities and class priors.
       
Partitioning:
    In order to send the totals to each reducer, we need to implement
    a custom partitioning strategy.
    
    We will generate a list of keys based on the number of reduce tasks 
    that we read in from the environment configuration of our job.
    
    We'll prepend the partition key by hashing the word and selecting the
    appropriate key from our list. This will end up partitioning our data
    as if we'd used the word as the partition key - that's how it worked
    for the single reducer implementation. This is not necessarily "good",
    as our data could be very skewed. However, in practice, for this
    exercise it works well. The next step would be to generate a file of
    partition split points based on the distribution as we've seen in 
    previous exercises.
    
    Now that we have a list of partition keys, we can send the totals to 
    each reducer by prepending each of the keys to each total.
       
"""

import re                                                   
import sys                                                  
import numpy as np      

from operator import itemgetter
import os

#################### YOUR CODE HERE ###################

# get the number of reducers from environment variable
N = int(os.getenv('mapreduce_job_reduces', default=1))

# helper function
def makeKeyHash(key, num_reducers = N):
    """
    Mimic the Hadoop string-hash function.
    
    key             the key that will be used for partitioning
    num_reducers    the number of reducers that will be configured
    """
    byteof = lambda char: int(format(ord(char), 'b'), 2)
    current_hash = 0
    for c in key:
        current_hash = (current_hash * 31 + byteof(c))
    return current_hash % num_reducers


# helper function
def getPartitions(num_reducers = N):
    """
    Args:   number of reducers
    Returns:    partition_keys (sorted list of strings)
                
    """
    # use the first N uppercase letters as custom partition keys, where N is number of reducers
    KEYS = list(map(chr, range(ord('A'), ord('Z')+1)))[:num_reducers]
    partition_keys = sorted(KEYS, key=lambda k: makeKeyHash(k,num_reducers))

    return partition_keys

# make the parition keys
pKeys = getPartitions(N)

# initialize totals counters for:
# ham, spam docs
docTotalCount = np.array([0,0])
# ham, spam words
wordTotalCount = np.array([0,0])

# read lines and tally
for line in sys.stdin: 
    # parse input
    docID, _class, subject, body = line.lower().split('\t')
    # tokenize
    words = re.findall(r'[a-z]+', subject + ' ' + body)
    
    # increment the totals & set partial counts based on this class
    # if ham...
    if _class == '0':
        docTotalCount[0] += 1                             # add this document to ham docs seen
        wordTotalCount[0] += len(words)                   # add all the words in this doc to the total number of ham words
        class0_partialCount, class1_partialCount  = (1,0) # all the words in this doc will have +1 for ham
    # if spam...
    else:
        docTotalCount[1] += 1
        wordTotalCount[1] += len(words)
        class0_partialCount, class1_partialCount  = (0,1)
        
    # go through words and print 
    for word in words:
        traced_key = pKeys[makeKeyHash(word, N)]
        print(f"{traced_key}\t{word}\t{class0_partialCount},{class1_partialCount}")


# emit totals with special key (order inversion) to all reducers specified by partition keys 
for pk in pKeys:
    print(f"{pk}\t*docTotalCount\t{docTotalCount[0]},{docTotalCount[1]}")
    print(f"{pk}\t*wordTotalCount\t{wordTotalCount[0]},{wordTotalCount[1]}")




















#################### (END) YOUR CODE ###################