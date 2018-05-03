import sys

# Create stopwords list
stopwords = ['a', 'an', 'are', 'as', 'at', 'by', 'be', 'for', 'from', 
             'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 
             'to', 'was', 'were', 'will', 'with']
"""
# Read All of the input
DataBase = []

for line in sys.stdin.read().splitlines():
    current_line_collapsed = line.split(" ")
    DataBase.append(current_line_collapsed)


DataBase = [['4'],
            ['Clustering','and','classification','are','important','problems','in','machine','learning.'],
            ['There','are','many','machine','learning','algorithms','for','classification','and','clustering','problems.'],
            ['Classification', 'problems', 'require', 'training', 'data.'],
            ['Most', 'clustering', 'problems', 'require', 'user-specified', 'group', 'number.'],
            ['SVM,', 'LogisticRegression', 'and', 'NaiveBayes', 'are', 'machine', 'learning', 'algorithms', 'for', 'classification', 'problems.'],
            ['k-means,', 'AGNES', 'and', 'DBSCAN', 'are', 'clustering', 'algorithms.'],
            ['Dimension', 'reduction', 'methods', 'such', 'as', 'PCA', 'are', 'also', 'learning', 'algorithms', 'for', 'clustering', 'problems.']
           ]
"""
DataBase = [['3'],
            ['b', 'and', 'c', 'd', 'and', 'e', 'f'],
            ['b', 'c', 'd', 'e', 'f'],
            ['b', 'and', 'c', 'd', 'b', 'e', 'g', 'f']
           ]


# Read minimum support number
min_sup = int(DataBase[0][0])

# remove stopwords
cleaned_database =[]
for i in range(1,len(DataBase)):
    cleaned_line = []
    for each_word in DataBase[i]:
        if each_word.lower() not in stopwords:
            cleaned_line.append(each_word.lower())
    cleaned_database.append(cleaned_line)

# print(cleaned_database)

# remove period
for i in range(0, len(cleaned_database)):   # each sentense
    if cleaned_database[i][-1][-1] == '.':  # last word, last sysmol
        cleaned_database[i][-1] = cleaned_database[i][-1].replace('.', '')

# print(cleaned_database)

converted_database = []
for i in range(0, len(cleaned_database)): # each sentense
    current_line = []
    items  = []
    j = 0
    while j < len(cleaned_database[i]): # each word
        items = []
        if cleaned_database[i][j][-1] != ',':
            if (j + 1) < len(cleaned_database[i]):
                if cleaned_database[i][j+1] != 'and':
                    current_line.append(cleaned_database[i][j])
                elif cleaned_database[i][j+1] == 'and':
                    items.append(cleaned_database[i][j])
                    j = j + 2
                    items.append(cleaned_database[i][j])
                    items = sorted(items)
                    current_line.append(items)
                    items = []
            elif (j + 1) == len(cleaned_database[i]):
                current_line.append(cleaned_database[i][j])
        else:
            while(cleaned_database[i][j][-1] == ','):
                cleaned_database[i][j] = cleaned_database[i][j].replace(',', '')
                items.append(cleaned_database[i][j])
                j = j + 1
            items.append(cleaned_database[i][j])
            j = j + 2
            items.append(cleaned_database[i][j])
            items = sorted(items)
            current_line.append(items)
            items = []
        j = j + 1
    converted_database.append(current_line)

# print(converted_database)
# Finished dataset conversion

# find frequent length one items
L1 = []
for each_sequence in converted_database:
    for i in range(0, len(each_sequence)):
        if isinstance(each_sequence[i], list):
            for j in range(0, len(each_sequence[i])):
                if each_sequence[i][j] not in L1:
                    L1.append(each_sequence[i][j])
        else:
            if each_sequence[i] not in L1:
                L1.append(each_sequence[i])

Differet_level = []

L1_list = []
for each_item in L1:
    count = 0
    for each_sequence in converted_database:
        for i in range(0, len(each_sequence)):
            if isinstance(each_sequence[i], list):
                for j in range(0, len(each_sequence[i])):
                    if each_sequence[i][j] == each_item:
                        count = count + 1
                        break
            else:
                if each_sequence[i] == each_item:
                    count = count + 1
                    break
    if count >= min_sup:
        L1_list.append(each_item)

Differet_level.append(L1_list)
# print(Differet_level)

def generate_comb(level_k_minus_1, k):
    if k == 1: # level 2
        result = []
        for each_item in level_k_minus_1:
            for each_other_item in level_k_minus_1:
                result.append([each_item, each_other_item])

        for i in range(0, len(level_k_minus_1)):
            for j in range(i+1, len(level_k_minus_1)):
                small_result = []
                small_result.append(level_k_minus_1[i])
                small_result.append(level_k_minus_1[j])
                small_result = sorted(small_result)
                result.append([small_result])

        return result
    else:
        result = []
        # create a list contain each item and removed first
        remove_first = []
        for each_item in level_k_minus_1:
            if isinstance(each_item[0], list) == False:
                current_removed = []
                for i in range(1, len(each_item)):
                    current_removed.append([each_item[i]])
                remove_first.append([each_item, current_removed])

            elif isinstance(each_item[0], list) == True:
                for a in range(0, len(each_item[0])):
                    for b in range(0, len(each_item[0])):
                        if b != a:
                            small_part.append(each_item[0][b])
                        current_removed.append(small_part)
                        for c in range(1, len(each_item)):
                            current_removed.append([each_item[i]])
                        remove_first.append([each_item, current_removed])
        print(remove_first)        

        # create a list contain each item and removed last
        remove_last= []
        for each_item in level_k_minus_1:
            if isinstance(each_item[-1], list) == False:
                current_removed = []
                for i in range(0, len(each_item)-1):
                    current_removed.append([each_item[i]])
                remove_last.append([each_item, current_removed])

            elif isinstance(each_item[-1], list) == True:
                for a in range(0, len(each_item[-1])):
                    for b in range(0, len(each_item[-1])):
                        if b != a:
                            small_part.append(each_item[-1][b])
                        current_removed.append(small_part)
                        for c in range(1, len(each_item)-1):
                            current_removed.append([each_item[i]])
                        current_removed.append(small_part)
                        remove_first.append([each_item, current_removed])
        print(remove_last)
        merged_list = []
       
        for current_remove_first in remove_first:
            for current_remove_last in remove_last:
                new_item = []
                if current_remove_first[0] != current_remove_last[0] and current_remove_first[1] == current_remove_last[1]:
                    # merge two items
                    for length in range(0, len(current_remove_first[0])):
                        new_item.append(current_remove_first[0][length])
                    for i in range(0,len(current_remove_last[0])):
                        if current_remove_last[0][i] not in new_item:
                            new_item.append(current_remove_last[0][i])
                            # print(new_item)
                    merged_list.append(new_item)
        # print(merged_list)
        # After merge, check infrequent subsets, prune
        for each_new_comb in merged_list:
            # print(level_k_minus_1)
            valid = True
            subset_list = []
            for i in range(0, len(each_new_comb)):
                for j in range(i + 1, len(each_new_comb)):
                    subset_list.append([each_new_comb[i], each_new_comb[j]])
            for each_subset in subset_list:
                # print(each_subset)
                if each_subset not in level_k_minus_1:
                    valid = False
            if valid == True:
                result.append(each_new_comb)
        return result
# Generate all

k = 1

while(len(Differet_level[k-1]) != 0):
    level_k_sequence_candidate = generate_comb(Differet_level[k-1], k)

    level_k_sequence = []
    # for each candidate, check if it has enough support
    for i in range(0, len(level_k_sequence_candidate)): # each candidate
        count = 0
        for j in range(0, len(converted_database)): # loop through all of the sequence in database
            # for each sequence, create found index of each part
            index_list = []
            for x in range(0, len(level_k_sequence_candidate[i])):  # each elements in current candidate
                for y in range(0, len(converted_database[j])):
                    if isinstance(level_k_sequence_candidate[i][x], list) == False and isinstance(converted_database[j][y], list) == True:
                        if level_k_sequence_candidate[i][x] in converted_database[j][y] and y not in index_list:
                            index_list.append(y)
                            break
                    elif isinstance(level_k_sequence_candidate[i][x], list) == True and isinstance(converted_database[j][y], list) == True:
                        if set(converted_database[j][y]).issubset(level_k_sequence_candidate[i][x]) and y not in index_list:
                            index_list.append(y)
                            break
                    elif isinstance(level_k_sequence_candidate[i][x], list) == False and isinstance(converted_database[j][y], list) == False:
                        if level_k_sequence_candidate[i][x] == converted_database[j][y] and y not in index_list:
                            index_list.append(y)
                            break
                    elif isinstance(level_k_sequence_candidate[i][x], list) == True and isinstance(converted_database[j][y], list) == False:
                        continue
                if len(index_list) == len(level_k_sequence_candidate[i]) and sorted(index_list) == index_list:
                    count = count + 1
        if count >= min_sup:
            level_k_sequence.append(level_k_sequence_candidate[i])
    Differet_level.append(level_k_sequence)
    # print(level_k_sequence)
    k = k + 1

#level_k_sequence_candidate = generate_comb(Differet_level[k-1], k)
# print(level_k_sequence)

for each_comb in Differet_level[k-2]:
    print(min_sup, '[%s]' % ' '.join(map(str, each_comb)))
