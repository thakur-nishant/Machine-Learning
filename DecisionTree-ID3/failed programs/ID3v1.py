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

        self.visted = []
        self.stat = self.statistics(self.votes, self.attributes)

        self.eS = self.entropy(self.stat, self.attributes[-1])
        print("Entropy(S) =", self.eS)


    def entropy(self, data, attr):
        entropy = 0
        if attr == self.attributes[-1]:
            for key in data[attr]:
                if key != 'total':
                    p = data[attr][key]['total']/data[attr]['total']
                    entropy += p * math.log2(p)
        else:
            for key in data:
                if key != 'total':
                    p = data[key]/data['total']
                    entropy += p * math.log2(p)
        return -entropy


    def statistics(self, votes, attributes):
        data = {}

        for attr in attributes:
            data[attr] = {}
            data[attr]['total'] = 0

        for vote in votes:
            for j in attributes:
                key = attributes.index(j)
                if vote[key] in data[attributes[key]]:
                    if vote[-1] in data[attributes[key]][vote[key]]:
                        data[attributes[key]][vote[key]][vote[-1]] += 1
                    else:
                        data[attributes[key]][vote[key]][vote[-1]] = 1
                    data[attributes[key]][vote[key]]['total'] += 1
                else:
                    data[attributes[key]][vote[key]] = {}
                    data[attributes[key]][vote[key]]['total'] = 1
                    data[attributes[key]][vote[key]][vote[-1]] = 1
                data[attributes[key]]['total'] += 1
        print(len(attributes),data)
        return  data


