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
        self.draw = {}
        self.visted = []
        self.stat = self.statistics(self.votes, self.attributes)

        self.eS = self.entropy(self.stat, attr = self.attributes[-1])
        print("\nEntropy(S) =", self.eS)
        # for i in self.votes:
        #     print(i)
        self.stat = self.statistics(self.votes, self.attributes)
        gain = self.gain(self.eS, self.stat)
        print("Gain:", gain)

        select = (max(gain, key=gain.get))
        print("Selected:",select)
        # self.draw[select] = {}
        g = self.recursive_select(self.stat[select], select)
        self.draw[select] = g
        print(self.draw)


    def recursive_select(self,stat, select):

        ind = self.attributes.index(select)
        self.visted.append(select)
        graph = {}
        for key in stat:
            # print(self.stat)

            if key != 'total':

                eS = self.entropy(stat[key], None)
                print("\nEntropy(S-"+select, key+") =", self.eS)

                if abs(eS) != 0:
                    newV = []
                    for i in self.votes:
                        if i[ind] == key:
                            newV.append(i)

                    stat1 = self.statistics(newV, self.attributes)
                    gain1 = self.gain(eS, stat1)
                    print("Gain:", gain1)
                    if gain1:
                        graph[key] = {}
                        select1 = (max(gain1, key = gain1.get))
                        print("selected:", select1)
                        self.visted.append(select1)

                        graph[key][select1] = self.recursive_select(stat1[select1], select1)
                    else:
                        break
                else:
                    for d in stat[key]:
                        if d != 'total':
                            print("Play: ",key, d)
                            print()
                            graph.update({key : d})
        return graph


    def statistics(self, votes, attributes):
        data = {}

        for attr in attributes:
            if attr not in self.visted:
                data[attr] = {}
                data[attr]['total'] = 0

        for vote in votes:
            for j in attributes:
                if j not in self.visted:
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
        print("Stats:", len(data.keys()),data)
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
            if col != 'Class' and col not in self.visted:
                gain[col] = S
                for key in data[col]:
                    if key != 'total':
                        ent = self.entropy(data[col][key], None)
                        gain[col] -= (data[col][key]['total']/ data[col]['total']) * ent

        return gain



test = ID3()
