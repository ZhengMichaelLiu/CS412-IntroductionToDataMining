"""

Frequent Pattern Mining

This question aims to provide you a better understanding of frequent pattern mining algorithm Apriori and closed pattern mining algorithm like CLOSET.

    1. Implement Apriori algorithm to mine frequent pattern from a transaction dataset
    
    2. Implement an algorithm to mine closed frequent pattern from the same dataset. You can either write a code to extract closed patterns from the result that you got in Part 1 or code CLOSET.
       Input Format

The input dataset is a transaction dataset.
The first line of the input corresponds to the minimum support.
Each following line of the input corresponds to one transaction. Items in each transaction are seperated by a space.
Please refer to the sample input below. In sample input 0, the minimum support is 2, and the dataset contains 3 transactions and 5 item types (A, B, C, D and E).

Output Format

The output are the frequent patterns you mined out from the input dataset.
Each line in the output should be of the format :

Support [frequent pattern]

Frequent patterns should be listed in a descending order based on support. e.g. 3 [C] is listed before 2 [A].
Ties should be resolved based on lexicographical order. e.g. 2 [A] is listed before 2 [A C]
Items within each pattern should be listed in lexicographical order as well seperated by a single space. e.g. 2 [B C D]
First print the frequent patterns and then closed pattern. Seperate the output for two parts by an empty line. In sample output 0, first 9 lines correspond to frequent patterns and last 3 lines correspond to closed pattern.

Sample Input 0

2
B A C E D
A C
C B D

Sample Output 0

3 [C]
2 [A]
2 [A C]
2 [B]
2 [B C]
2 [B C D]
2 [B D]
2 [C D]
2 [D]

3 [C]
2 [A C]
2 [B C D]

Sample Input 1

2
data mining
frequent pattern mining
mining frequent patterns from the transaction dataset
closed and maximal pattern mining
Sample Output 1

4 [mining]
2 [frequent]
2 [frequent mining]
2 [mining pattern]
2 [pattern]

4 [mining]
2 [frequent mining]
2 [mining pattern]

"""

import sys
import itertools
import operator

# Read All of the input
DataBase = []

for line in sys.stdin.read().splitlines():
    current_line_collapsed = line.split(" ")
    DataBase.append(current_line_collapsed)

# Read minimum support number
min_sup = int(DataBase[0][0])

"""
findsubsets(S, m)

Find and return all subsets of a set, S, with given length, m
"""
def findsubsets(S, m):
    return set(itertools.combinations(S, m))

"""
has_infrequent_subset(level_k_candidate, level_k_minus_1_itemset, level_k_minus_1)

check if itemsets candidates contain an itemset that have infrequent subset
"""
def has_infrequent_subset(level_k_candidate, level_k_minus_1_itemset, level_k_minus_1):
    current_subsets = findsubsets(level_k_candidate, level_k_minus_1)
    for each_subset in current_subsets:
        if list(each_subset) not in level_k_minus_1_itemset:
            return True
    return False

"""
apriori_gen(level_k_minus_1_itemset)

Find and return level k itemsets with given level k-1 itemsets
"""
def apriori_gen(level_k_minus_1_itemset):
    level_k_itemset = []
    for itemset1 in level_k_minus_1_itemset:
        for itemset2 in level_k_minus_1_itemset:
            length_of_itemsets = len(itemset1)
            difference = 0
            current_join = set()
            for i in range(0, length_of_itemsets):
                if itemset1[i] not in itemset2:
                    difference = difference + 1
            if difference == 1:
                current_join = set(itemset1)|set(itemset2) # set
                check_append = True
                if (has_infrequent_subset(current_join, level_k_minus_1_itemset, length_of_itemsets) == False):
                    for each_mem in level_k_itemset:
                        if set(each_mem) == current_join:
                            check_append = False
                    if check_append == True:
                        level_k_itemset.append(list(current_join))
    return level_k_itemset


Different_level_itemsets = []

# L1 = find_frequent_1_itemsets(DataBase)
L1 = set()

for index in range(1, len(DataBase)):
    current_row_to_set = set(DataBase[index])
    L1 = L1.union(current_row_to_set)

level_1_itemset_set = list(L1)
level_1_itemset = []

for each_item in level_1_itemset_set:
    count = 0
    for index in range(1, len(DataBase)):
        if each_item in DataBase[index]:
            count = count + 1
    if count >= min_sup:
        level_1_itemset.append([each_item])

Different_level_itemsets.append(level_1_itemset)

k = 1
while(len(Different_level_itemsets[k-1]) != 0):
    level_k_itemset = apriori_gen(Different_level_itemsets[k-1])

    level_k_itemset_append = []
    for each_item in level_k_itemset:
        count = 0
        for index in range(1, len(DataBase)):
            if set(each_item).issubset(set(DataBase[index])) == True:
                count = count + 1
        if count >= min_sup:
            level_k_itemset_append.append(each_item)

    Different_level_itemsets.append(level_k_itemset_append)
    k = k + 1
# sort
for i in range(0, len(Different_level_itemsets)):
    for j  in range(0, len(Different_level_itemsets[i])):
        Different_level_itemsets[i][j] = sorted(Different_level_itemsets[i][j])
    Different_level_itemsets[i] = sorted(Different_level_itemsets[i])


table_for_support_number = []
for each_level_set in Different_level_itemsets:
    for each_itemset in each_level_set:
        count = 0
        for i in range(0, len(DataBase)):
            if set(each_itemset).issubset(DataBase[i]):
                count = count + 1
        table_for_support_number.append([count, each_itemset])

table_for_support_number = sorted(table_for_support_number, key = operator.itemgetter(1))
table_for_support_number = sorted(table_for_support_number, key = operator.itemgetter(0), reverse = True)

for each_tuple in table_for_support_number:
    print(each_tuple[0], '[%s]' % ' '.join(map(str, each_tuple[1])))

print('')

closed_set = []
for item1 in table_for_support_number:
    ok = True
    for item2 in table_for_support_number:
        if item1 != item2:
            if set(item1[1]).issubset(set(item2[1])) and item1[0] == item2[0]:
                ok = False
    if ok == True:
        closed_set.append(item1)

for each_tuple in closed_set:
    print(each_tuple[0], '[%s]' % ' '.join(map(str, each_tuple[1])))
