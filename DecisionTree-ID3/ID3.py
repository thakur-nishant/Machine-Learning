import math

class ID3:
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


        self.stat = self.statistics(self.votes, self.attributes)

        self.eS = self.entropy(self.stat, attr = self.attributes[-1])
        print("Entropy(S) =", self.eS)
        # for i in self.votes:
        #     print(i)
        self.stat = self.statistics(self.votes, self.attributes)
        gain = self.gain(self.eS, self.stat)
        print(gain)

        select = (max(gain, key=gain.get))
        print("selected:",select)
        for key in self.stat[select].keys():
            # print(self.stat)
            if key != 'total':
                self.eS = self.entropy(self.stat[select][key], None)
                print("Entropy(S-"+key+") =", self.eS)

                if self.eS != 0:
                    newV = []
                    for i in self.votes:
                        if i[0] == key:
                            newV.append(i)

                    stat1 = self.statistics(newV, self.attributes)
                    gain1 = self.gain(self.eS, stat1)
                    print(gain1)

                    select1 = (max(gain1, key=gain1.get))
                    print("selected:", select1)

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


    def gain(self, S, data):
        gain = {}
        for col in data:
            if col != 'Play':
                gain[col] = S
                for key in data[col]:
                    if key != 'total':
                        ent = self.entropy(data[col][key], None)
                        gain[col] -= (data[col][key]['total']/ data[col]['total']) * ent

        return gain



test = ID3()
