"""
Homework1.py

"""
import sys
from operator import itemgetter
from scipy.spatial.distance import minkowski as mink
from scipy.spatial.distance import chebyshev as cheb
from scipy.spatial.distance import cosine
from sklearn.decomposition import PCA


file = open("TextFile1.txt", "r")
file2 = open("TextFile2.txt", "w")
# Line 1 : D (number of data dimensions that can be between 1 to 1000)
D = int(file.readline())

# Line 2 : N (number of patients between 1 to 1000)
N = int(file.readline())

dont_care = file.readline()
dont_care2 = file.readline()

"""
Parameter list 
"""
# Line 3: the type_num of distance metric
# 1 : Manhattan distance
# 2 : Euclidean distance
# 3 : Supremum  distance
# 4 : Cosine similarity
type_of_distance = [1, 2, 3, 4]

# Line 4 : the number of PCA to use to transform the original dataset to a new space
# -1 : no PCA
# not -1 : apply PCA
num_of_PCA = [-1, 1, 2, 10, 100, 1000]

# Line 5 : Patient P data that contains D integers.
data_of_P = file.readline()
array_of_P = [int(s) for s in data_of_P.split()]

original_data_set = []
original_data_set.append(array_of_P)

for i in range(0, N):
    curr_data = file.readline()
    array_of_curr_data = [int(s) for s in curr_data.split()]
    original_data_set.append(array_of_curr_data)


for n_comp in num_of_PCA:
    if n_comp != -1:
        # need to transform first
        pca = PCA(n_components=n_comp)
        new_data_set = pca.fit_transform(original_data_set)
       

    for type_num in type_of_distance:

        distance_array = []
        similarity_array = []

        if n_comp == -1:
            array_of_P = original_data_set[0]
            for i in range(1, N + 1):
                array_of_curr_data = original_data_set[i]

                distance = 0
                similarity = 0

                if type_num == 1:
                    distance = mink(array_of_P, array_of_curr_data, 1, None)
                    distance_array.append((i, distance))

                elif type_num == 2:
                    distance = mink(array_of_P, array_of_curr_data, 2, None)
                    distance_array.append((i, distance))

                elif type_num == 3:
                    distance = cheb(array_of_P, array_of_curr_data)
                    distance_array.append((i, distance))

                elif type_num == 4:
                    similarity = 1 - cosine(array_of_P, array_of_curr_data)
                    similarity_array.append((i, similarity))

            if type_num == 1 or type_num == 2 or type_num == 3:
                distance_array.sort(key=itemgetter(1))

            elif type_num == 4:
                similarity_array.sort(key=itemgetter(1), reverse=True)

            if type_num == 1 or type_num == 2 or type_num == 3:
                for i in range(0, 5):
                    #string = ('Original data', '. Distance type_num : ', type_num, '.....', i, 'th', 'id : ', distance_array[i][0], '\n')
                    #s = str(string)
                    #file2.write(s)
                    print( 'Original Data Set', 'Distance Type:', type_num, '.....' , i + 1 ,'th, id : ', distance_array[i][0])
                    


            else:
                for i in range(0, 5):
                    #string = ('Original data', '. Distance type_num : ', type_num, '.....', i, 'th', 'id : ', similarity_array[i][0],'\n')
                    #s = str(string)
                    #file2.write(s)
                    print( 'Original Data Set', 'Distance Type:', type_num, '.....' , i + 1,'th, id : ', similarity_array[i][0])
                    

        else:
            """
            explained_variance = pca.explained_variance_ratio_
            total_ev = 0
            for i in range(0, n_comp-1):
                total_ev = total_ev + explained_variance[i]
            """

            new_array_of_P = new_data_set[0]
            for i in range(1, N + 1):
                new_array_of_curr_data = new_data_set[i]

                distance = 0
                similarity = 0

                if type_num == 1:
                    distance = mink(new_array_of_P, new_array_of_curr_data, 1, None)
                    distance_array.append((i, distance))
                elif type_num == 2:
                    distance = mink(new_array_of_P, new_array_of_curr_data, 2, None)
                    distance_array.append((i, distance))
                elif type_num == 3:
                    distance = cheb(new_array_of_P, new_array_of_curr_data)
                    distance_array.append((i, distance))
                elif type_num == 4:
                    similarity = 1 - cosine(new_array_of_P, new_array_of_curr_data)
                    similarity_array.append((i, similarity))

            if type_num == 1 or type_num == 2 or type_num == 3:
                distance_array.sort(key=itemgetter(1))
            elif type_num == 4:
                similarity_array.sort(key=itemgetter(1), reverse=True)

            if type_num == 1 or type_num == 2 or type_num == 3:
                for i in range(0, 5):
                    #string = ('PCA Components : ', n_comp, '. Distance type_num : ', type_num, '.....', i, 'th', 'id : ', distance_array[i][0],'\n')
                    #s = str(string)
                    #file2.write(s)
                    print( 'PCA Components:', n_comp, 'Distance Type:', type_num, '.....' , i + 1 ,'th, id : ', distance_array[i][0])
                    #print('Total Explained variance : ', total_ev)

            else:
                for i in range(0, 5):
                    #string = ('PCA Components : ', n_comp, '. Distance type_num : ', type_num, '.....', i, 'th', 'id : ', similarity_array[i][0],'\n')
                    #s = str(string)
                    #file2.write(s)
                    print( 'PCA Components:', n_comp, 'Distance Type:', type_num, '.....' , i + 1,'th, id : ', similarity_array[i][0])
                    #print('Total Explained variance : ', total_ev)


file.close()
file2.close()
