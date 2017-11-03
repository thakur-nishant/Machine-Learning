import random
from math import floor

iris = []
with open('iris.data') as f:
    for line in f:
        data = line.split(',')
        iris.append(data)

random.shuffle(iris)
n = len(iris)
test = floor(n * 0.8)
train = n - test
rand_mean = random.sample(range(0,test),3)
kmean = [iris[rand_mean[0]], iris[rand_mean[1]], iris[rand_mean[2]]]
flag = True
while flag:
    kcluster = [[],[],[]]
    next_centroid = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for data in range(test):
        dist = [0,0,0]
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
            next_centroid[i][j] = next_centroid[i][j]/len(kcluster[i])

    # print(next_centroid)

    if next_centroid == kmean:
        flag = False
    else:
        kmean = next_centroid


print(kmean)
for i in range(3):
    print(kcluster[i])
