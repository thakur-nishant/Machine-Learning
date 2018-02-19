import math, json

class ID3:
    def __init__(self):
        self.votes = []
        with open('tic-attr.txt') as f:
            for line in f:
                self.attributes = line[:-1].split(',')
        # print(self.attributes)
        with open('tic-tac-toe.data') as f:
            for line in f:
                data = line[:-1].split(',')
                self.votes.append(data)
        self.draw = {}
        self.visited = []
        self.stat = {}
        self.queue = []

        self.start()


    def start(self):
        self.stat = self.statistics(self.votes, self.attributes)

        self.eS = self.entropy(self.stat, attr = "Class")
        print("\nEntropy(S) =", self.eS)

        gain = self.gain(self.eS, self.stat)
        print("Gain:", gain)

        select = (max(gain, key=gain.get))
        print("Selected:",select)
        self.draw[select] = {}

        g = self.recursive_select(self.stat[select], select)
        self.draw[select] = g

        while self.queue:
            current = self.queue.pop(0)
            g = self.recursive_select(current[0], current[1])
            self.make_graph(current[1], g, self.draw)

        print(self.draw)
        print(json.dumps(self.draw))


    def make_graph(self, current, g, draw):
        if current in draw:
            draw[current] = g
        else:
            if type(draw) is dict:
                for key in draw.keys():
                    self.make_graph(current, g, draw[key])


    def recursive_select(self,stat, select):

        ind = self.attributes.index(select)
        self.visited.append(select)
        graph = {}
        for key in stat:
            if key != 'total':
                eS = self.entropy(stat[key], None)
                print("\nEntropy(S-"+select, key+") =", eS)

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
                        selected_attr = (max(gain1, key = gain1.get))
                        print("selected:", selected_attr)
                        self.visited.append(selected_attr)
                        self.queue.append([stat1[selected_attr], selected_attr])
                        graph[key][selected_attr] = {}
                    else:
                        major = -1
                        for k in stat1['Class']:
                            print(k)
                            if k != 'total':
                                if stat1['Class'][k]['total'] > major:
                                    graph[key] = k
                                    major = stat1['Class'][k]['total']
                else:
                    for d in stat[key]:
                        if d != 'total':
                            print("Play: ",key, d)
                            print()
                            graph.update({key : d})
        return graph


    def statistics(self, votes, attributes):
        data = {}
        i = attributes.index("Class")
        for attr in attributes:
            if attr not in self.visited:
                data[attr] = {}
                data[attr]['total'] = 0

        for vote in votes:
            for j in attributes:
                if j not in self.visited:
                    key = attributes.index(j)
                    if vote[key] in data[attributes[key]]:
                        if vote[i] in data[attributes[key]][vote[key]]:
                            data[attributes[key]][vote[key]][vote[i]] += 1
                        else:
                            data[attributes[key]][vote[key]][vote[i]] = 1
                        data[attributes[key]][vote[key]]['total'] += 1
                    else:
                        data[attributes[key]][vote[key]] = {}
                        data[attributes[key]][vote[key]]['total'] = 1
                        data[attributes[key]][vote[key]][vote[i]] = 1
                    data[attributes[key]]['total'] += 1
        print("Stats:", len(data.keys()),data)
        return  data


    def entropy(self, data, attr):
        entropy = 0
        if attr == "Class":
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
            if col != 'Class' and col not in self.visited:
                gain[col] = S
                for key in data[col]:
                    if key != 'total':
                        ent = self.entropy(data[col][key], None)
                        gain[col] -= (data[col][key]['total']/ data[col]['total']) * ent

        return gain



test = ID3()
