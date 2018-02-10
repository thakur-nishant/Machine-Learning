import math

class ID3:
    def __init__(self):
        self.votes = []
        with open('attributes.txt') as f:
            for line in f:
                self.attributes = line[:-1].split(',')
        # print(self.attributes)
        with open('house-votes-84.data') as f:
            for line in f:
                data = line[:-1].split(',')
                self.votes.append(data)

        self.visted = []
        self.stat = self.statistics(self.votes, self.attributes)

        self.eS = self.entropy(self.stat, attr = self.attributes[0])
        print("Entropy(S) =", self.eS)
        # for i in self.votes:
        #     print(i)
        self.stat = self.statistics(self.votes, self.attributes)
        gain = self.gain(self.eS, self.stat)
        print(gain)

        select = (max(gain, key=gain.get))
        print("selected:",select)
        self.visted.append(select)
        ind = self.attributes.index(select)
        for key in self.stat[select].keys():
            # print(self.stat)
            if key != 'total':
                self.eS = self.entropy(self.stat[select][key], None)
                print("Entropy(S-"+key+") =", self.eS)

                if abs(self.eS) != 0:
                    newV = []
                    for i in self.votes:
                        if i[ind] == key:
                            newV.append(i)

                    stat1 = self.statistics(newV, self.attributes)
                    gain1 = self.gain(self.eS, stat1)
                    print(gain1)
                    if gain1:
                        select1 = (max(gain1, key = gain1.get))
                        print("selected:", select1)
                        self.visted.append(select1)
                        ind1 = self.attributes.index(select1)

                        for key1 in stat1[select1]:
                            # print(self.stat)
                            if key1 != 'total':
                                print(key1, stat1[select1][key1])
                                self.eS1 = self.entropy(stat1[select1][key1], None)
                                print("Entropy(S-" + key1 + ") =", self.eS1)

                                if abs(self.eS1) != 0:
                                    newV1 = []
                                    for i in newV:
                                        if i[ind1] == key1:
                                            newV1.append(i)

                                    stat11 = self.statistics(newV1, self.attributes)
                                    gain11 = self.gain(self.eS1, stat11)
                                    print(gain11)
                                    if gain11:
                                        select11 = (max(gain11, key=gain11.get))
                                        self.visted.append(select11)
                                        print("selected:", select11)
                                    else:
                                        break
                                else:
                                    for d in stat1[select1][key1]:
                                        if d != 'total':
                                            print("Play: ", d)

                else:
                    for d in self.stat[select][key].keys():
                        if d != 'total':
                            print("Play: ", d)


    def statistics(self, votes, attributes):
        data = {}

        for attr in attributes:
            data[attr] = {}
            data[attr]['total'] = 0

        for vote in votes:
            for j in attributes:
                if j not in self.visted:
                    key = attributes.index(j)
                    if vote[key] in data[attributes[key]]:
                        if vote[0] in data[attributes[key]][vote[key]]:
                            data[attributes[key]][vote[key]][vote[0]] += 1
                        else:
                            data[attributes[key]][vote[key]][vote[0]] = 1
                        data[attributes[key]][vote[key]]['total'] += 1
                    else:
                        data[attributes[key]][vote[key]] = {}
                        data[attributes[key]][vote[key]]['total'] = 1
                        data[attributes[key]][vote[key]][vote[0]] = 1
                    data[attributes[key]]['total'] += 1
        print(len(data.keys()),data)
        return  data


    def entropy(self, data, attr):
        entropy = 0
        if attr == self.attributes[0]:
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


    def gain(self, S, data):
        gain = {}
        for col in data:
            if col != 'Class' and col not in self.visted:
                gain[col] = S
                for key in data[col]:
                    if key != 'total':
                        ent = self.entropy(data[col][key], None)
                        gain[col] -= (data[col][key]['total']/ data[col]['total']) * ent

        return gain



test = ID3()
