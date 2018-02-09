import math

class ID3():
    def __init__(self):
        self.votes = []
        with open('playball-attr.txt') as f:
            for line in f:
                self.attributes = line[:-1].split(',')
        # print(self.attributes)
        with open('playball.txt') as f:
            for line in f:
                data = line[:-1].split(',')
                self.votes.append(data)


    def entropy(self, attr):
        entropy = 0
        for key in attr:
            if key != 'total':
                p = attr[key] / attr['total']
                entropy += p * math.log2(p)

        return -entropy


    def statistic(self, ):


