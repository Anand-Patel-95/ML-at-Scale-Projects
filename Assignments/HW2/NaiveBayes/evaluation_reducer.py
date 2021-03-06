#!/usr/bin/env python
"""
Reducer to calculate precision and recall as part
of the inference phase of Naive Bayes.
INPUT:
    ID \t true_class \t P(ham|doc) \t P(spam|doc) \t predicted_class
OUTPUT:
    precision \t ##
    recall \t ##
    accuracy \t ##
    F-score \t ##
         
Instructions:
    Complete the missing code to compute these^ four
    evaluation measures for our classification task.
    
    Note: if you have no True Positives you will not 
    be able to compute the F1 score (and maybe not 
    precision/recall). Your code should handle this 
    case appropriately feel free to interpret the 
    "output format" above as a rough suggestion. It
    may be helpful to also print the counts for true
    positives, false positives, etc.
"""
import sys

# initialize counters
FP = 0.0 # false positives
FN = 0.0 # false negatives
TP = 0.0 # true positives
TN = 0.0 # true negatives

# read from STDIN
for line in sys.stdin:
    # parse input
    docID, class_, pHam, pSpam, pred = line.split()
    # emit classification results first
    print(line[:-2], class_ == pred)
    
    # then compute evaluation stats
#################### YOUR CODE HERE ###################
    if class_ == "1":
        # actually positive
        if class_ == pred:
            TP += 1 # correctly predicted true positive
        else:
            FN += 1 # incorrectly predicted negative
    else:
        # actually negative
        if class_ == pred:
            TN += 1 # correctly predicted true negative
        else:
            FP += 1 # incorrectly predicted positive


# Print the counts
print(f"# Documents:\t{FP+FN+TP+TN}")
print(f"True Positives:\t{TP}")
print(f"True Negatives:\t{TN}")
print(f"False Positives:\t{FP}")
print(f"False Negatives:\t{FN}")


# Calculate and print the summary statistics

Accuracy = (TP + TN)/(FP+FN+TP+TN)
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)

if TP != 0:
    Precision = TP / (TP + FP)
    Recall = TP / (TP + FN)
    F_score = TP / (TP + 0.5*(FP + FN))
else:
    Precision = 0
    Recall = 0
    F_score = 0

print(f"Accuracy\t{Accuracy}")
print(f"Precision\t{Precision}")
print(f"Recall\t{Recall}")
print(f"F-Score\t{F_score}")





#################### (END) YOUR CODE ###################
    