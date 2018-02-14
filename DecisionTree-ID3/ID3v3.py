import math

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

        self.create_decision_tree(self.votes, "Class", self.attributes)


    def create_decision_tree(self, data, target_attribute, attributes):
        data = data[:]
        vals = [record[target_attribute] for record in data]
        tree = {}
        if vals.count(vals[0]) == len(data):
            return vals[0]

        if len(attributes) - 1 <= 0:
            return tree

        






