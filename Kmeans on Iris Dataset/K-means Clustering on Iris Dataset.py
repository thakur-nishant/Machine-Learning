import random
from math import floor
import collections


def kmeans_clustering():
    iris = []
    with open('iris.data') as f:
        for line in f:
            data = line[:-1].split(',')
            iris.append(data)

    random.shuffle(iris)
    n = len(iris)
    train = floor(n * 0.8)
    test = n - train
    # rand_mean = random.sample(range(0, train), 3)
    # kmean = [iris[rand_mean[0]], iris[rand_mean[1]], iris[rand_mean[2]]]
    kmean = random.sample(iris[:train], 3)
    flag = True
    while flag:
        kcluster = [[], [], []]
        next_centroid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for data in range(train):
            dist = [0, 0, 0]
            for k in range(3):
                for i in range(4):
                    try:
                        dist[k] = floor(dist[k]) + (abs(float(iris[data][i]) - float(kmean[k][i])) ** 2)
                    except ValueError:
                        pass
            min_val = min(dist)
            min_index = dist.index(min_val)
            kcluster[min_index].append(iris[data])
            for i in range(4):
                next_centroid[min_index][i] += float(iris[data][i])

        for i in range(3):
            # print(kcluster[i])
            for j in range(4):
                if len(kcluster[i]):
                    next_centroid[i][j] = next_centroid[i][j] / len(kcluster[i])
                else:
                    next_centroid[i][j] = 0.0
        # print(next_centroid)

        if next_centroid == kmean:
            flag = False
        else:
            kmean = next_centroid

    # print(kmean)

    cluster_name = ['', '', '']
    for i in range(3):
        name = []
        for j in range(len(kcluster[i])):
            name.append(kcluster[i][j][4])
        count = collections.Counter(name)
        if not count:
            cluster_name[i] = 'Iris-noise\\n'
        else:
            cluster_name[i] = (count.most_common(1)[0][0])

    # print(cluster_name)

    correct = 0
    for data in range(train, n):
        dist = [0, 0, 0]
        for k in range(3):
            for i in range(4):
                try:
                    dist[k] = floor(dist[k]) + (abs(float(iris[data][i]) - float(kmean[k][i])) ** 2)
                except ValueError:
                    pass
        min_val = min(dist)
        min_index = dist.index(min_val)
        print(iris[data],"=",cluster_name[min_index])
        if iris[data][4] == cluster_name[min_index]:
            correct += 1

    accuracy = correct / test * 100
    print("accuracy =", accuracy)
    return accuracy


# running kmeans clustering over 1000 times on iris dataset to get avgerage accuracy
avg_accuracy = 0
for x in range(2):
    print("Iteration #", x + 1)
    current_accuracy = kmeans_clustering()
    avg_accuracy += current_accuracy

avg_accuracy = avg_accuracy / 2

print("average accuracy =", avg_accuracy)
