"""

Attribute Selection

Given a training dataset with several categorical attributes and a target label, you have to identify the best attribute for splitting the dataset.
You have to choose the best attribute based on their information gain, gain ratio value and gini index.
For this problem, assume that gini index can be defined over a multi-valued attribute having  distinct attribute-values as,

gini(D) = 1 - \sum_{i=1}^n(p_i)^2

Input Format

First line of the input contains the number of lines (1+ number of training instances).
Second line contains the name of the attributes and the target label (last) comma separated.
The following lines are training instances which are comma-separated: the first categorical attribute value, second categorical attribute, and so on and finally the target label value.

Example input,

6
income,age,buycomputer
high,mid,Yes
high,mid,No
high,young,Yes
low,young,Yes
low,old,Yes

Constraints

None

Output Format

The output will be the best attribute based on information gain followed by the best attribute based on gain ratio and gini index on separate lines.

Example output of the given input,

age
age
age

Sample Input 0

15
age,income,student,creditrating,buyscomputer?
l30,high,no,fair,no
l30,high,no,excellent,no
31to40,high,no,fair,yes
g40,medium,no,fair,yes
g40,low,yes,fair,yes
g40,low,yes,excellent,no
31to40,low,yes,excellent,yes
l30,medium,no,fair,no
l30,low,yes,fair,yes
g40,medium,yes,fair,yes
l30,medium,yes,excellent,yes
31to40,medium,no,excellent,yes
31to40,high,yes,fair,yes
g40,medium,no,excellent,no
Sample Output 0

age
age
age

"""

import sys
import math

Database = []
for line in sys.stdin.read().splitlines():
    current_line_collapsed = line.split(",")
    Database.append(current_line_collapsed)

# first line is attribute line
data_num = int(Database[0][0]) - 1
# last one is label
attri_num = int(len(Database[1])) - 1
attri = Database[1][:-1]

label_class = []
label_class_check = []
for i in range(0, data_num):
    if Database[2 + i][-1] not in label_class_check:
        label_class_check.append(Database[2 + i][-1])
        label_class.append([Database[2 + i][-1], 1])
    else:
        for each_tuple in label_class:
            if each_tuple[0] == Database[2 + i][-1]:
                each_tuple[1] = each_tuple[1] + 1

# information_gain
    # entrophy of original data
Info_D = 0
for each_label in label_class:
    Info_D = Info_D - (each_label[1] / data_num) * math.log2((each_label[1] / data_num))

# calculate entrophy of after splitting by each attribute
gain_list = []
for i in range(0, attri_num):
    current_attri_class = []
    current_attri_class_check =[]
    for j in range(0, data_num):
        if Database[2 + j][i] not in current_attri_class_check:
            current_attri_class_check.append(Database[2 + j][i])
            current_attri_class.append([Database[2 + j][i], 1])
        else:
            for each_tuple in current_attri_class:
                if each_tuple[0] == Database[2 + j][i]:
                    each_tuple[1] = each_tuple[1] + 1
    # OK
    info_Dj_list = []
    # Above, for current attribute, count the number of different classes and number of data with that class
    for each_tuple in current_attri_class:
        count = []
        count_check = []
        
        for k in range(0, data_num):
            if each_tuple[0] == Database[2 + k][i]:
                if Database[2 + k][-1] not in count_check:
                    count_check.append(Database[2 + k][-1])
                    count.append([Database[2 + k][-1], 1])
                else:
                    for each_check in count:
                        if each_check[0] == Database[2 + k][-1]:
                            each_check[1] = each_check[1] + 1

        info_Dj = 0
        for each in count:
            info_Dj = info_Dj - each[1] / each_tuple[1] * math.log2(each[1] / each_tuple[1])
        info_Dj_list.append(info_Dj)

    info_AD = 0
    for x in range(0, len(info_Dj_list)):
        info_AD = info_AD + (current_attri_class[x][1] / data_num) * info_Dj_list[x]

    Gain_A = Info_D - info_AD
    gain_list.append(Gain_A)

index_of_largegain = gain_list.index(max(gain_list))
print(attri[index_of_largegain])


# gain ratio value
gain_ratio_list = []
    # already have gain_list
    # calculate splitInfo_AD
splitinfo_list = []
for i in range(0, attri_num):
    current_attri_class = []
    current_attri_class_check =[]
    for j in range(0, data_num):
        if Database[2 + j][i] not in current_attri_class_check:
            current_attri_class_check.append(Database[2 + j][i])
            current_attri_class.append([Database[2 + j][i], 1])
        else:
            for each_tuple in current_attri_class:
                if each_tuple[0] == Database[2 + j][i]:
                    each_tuple[1] = each_tuple[1] + 1
    # OK
    splitinfo = 0
    for each_tuple in current_attri_class:
        splitinfo = splitinfo - (each_tuple[1] / data_num) * math.log2(each_tuple[1] / data_num)
    splitinfo_list.append(splitinfo)

for i in range(0, attri_num):
    gain_ratio = gain_list[i] / splitinfo_list[i]
    gain_ratio_list.append(gain_ratio)

index_of_largeratio = gain_ratio_list.index(max(gain_ratio_list))
print(attri[index_of_largeratio])


# gini index
pi_2 = 0
for each_label in label_class:
    pi_2 = pi_2 + math.pow((each_label[1] / data_num), 2)
gini_D = 1 - pi_2

delta_gain_list = []
for i in range(0, attri_num):   # for each attri
    current_attri_class = []
    current_attri_class_check =[]
    for j in range(0, data_num):
        if Database[2 + j][i] not in current_attri_class_check:
            current_attri_class_check.append(Database[2 + j][i])
            current_attri_class.append([Database[2 + j][i], 1])
        else:
            for each_tuple in current_attri_class:
                if each_tuple[0] == Database[2 + j][i]:
                    each_tuple[1] = each_tuple[1] + 1
    # OK
    gini_Dj_list = []
    for each_tuple in current_attri_class:
        count = []
        count_check = []
        
        for k in range(0, data_num):
            if each_tuple[0] == Database[2 + k][i]:
                if Database[2 + k][-1] not in count_check:
                    count_check.append(Database[2 + k][-1])
                    count.append([Database[2 + k][-1], 1])
                else:
                    for each_check in count:
                        if each_check[0] == Database[2 + k][-1]:
                            each_check[1] = each_check[1] + 1

        p_ij_2 = 0
        gini_Dj = 0
        for each in count:
            p_ij_2 = p_ij_2 + math.pow(each[1] / each_tuple[1], 2)
        gini_Dj = 1 - p_ij_2
        gini_Dj_list.append(gini_Dj)

    gini_AD = 0
    for x in range(0, len(gini_Dj_list)):
        gini_AD = gini_AD + (current_attri_class[x][1] / data_num) * gini_Dj_list[x]

    delta_gini_A = gini_D - gini_AD
    delta_gain_list.append(delta_gini_A)

index_of_largegini = delta_gain_list.index(max(delta_gain_list))
print(attri[index_of_largegini])