import math, random

def train_test():
    votes = []
    with open('tic-tac-toe.data') as f:
        for line in f:
            data = line[:-1].split(',')
            votes.append(data)

    random.shuffle(votes)
    n = len(votes)
    train = math.floor(n * 0.8)
    test = n - train
    trainl= ""
    testl = ""
    for i in range(n):
        s = ""
        for j in votes[i]:
            s += j+" "
        if i < train:
            trainl += s+"\n"
        else:
            testl += s+"\n"

    fh = open("train.txt", "w")
    fh.write(trainl)
    fh.close()

    fh1 = open("test.txt", "w")
    fh1.write(testl)
    fh1.close()


train_test()