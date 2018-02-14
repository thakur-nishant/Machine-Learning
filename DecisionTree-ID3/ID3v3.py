import math, json
import random

class ID3:
    def __init__(self):
        self.data = []
        with open('tic-attr.txt') as f:
            for line in f:
                self.attributes = line[:-1].split(',')
        # print(self.attributes)
        with open('tic-tac-toe.data') as f:
            for line in f:
                data = line[:-1].split(',')
                self.data.append(data)

        random.shuffle(self.data)
        n = len(self.data)
        len_train = math.floor(n * 0.8)

        train = self.data[:len_train]
        test = self.data[len_train:]

        tree = self.cross_validation(20, train)
        # self.stats = self.statistics(train, self.attributes)
        #
        # tree = self.create_decision_tree(train, "Class", self.attributes)
        # # print(z)
        # print(json.dumps(tree))
        #
        accuracy = self.test_decision_tree(test, tree)
        print("Accuracy:", accuracy)


    def cross_validation(self, k, data):
        n = len(data)
        len_k = n//k
        accuracy_list = []
        tree_list = []
        for i in range(k):
            start = i*len_k
            end = (i+1) * len_k
            test = data[start:end]
            train = [x for x in data if x not in test]

            self.stats = self.statistics(train, self.attributes)

            tree = self.create_decision_tree(train, "Class", self.attributes)
            # print(z)
            print(json.dumps(tree))

            accuracy = self.test_decision_tree(test, tree)
            print("Accuracy:", accuracy)
            tree_list.append(tree)
            accuracy_list.append(accuracy)

        print("Cross-validation Average Accuracy:", sum(accuracy_list)/k)
        best_tree = accuracy_list.index(max(accuracy_list))

        return tree_list[best_tree]



    def create_decision_tree(self, data, target_attribute, attributes):
        data = data[:]
        tree = {}
        vals = []
        for record in data:
            vals.append(record[-1])

        if len(attributes) - 1 <= 0 or not vals:
            return self.data[0][-1]

        if vals.count(vals[0]) == len(data):
            return vals[0]

        best_gain = self.select_attribute(data, attributes, target_attribute)
        # print(best_gain)
        tree[best_gain] = {}

        for key in self.stats[best_gain]:
            if key != 'total':
                new_data = []
                i = self.attributes.index(best_gain)
                for row in data:
                    if row[i] == key:
                        new_data.append(row)

                new_attrinures = [attr for attr in attributes if attr != best_gain]

                subtree = self.create_decision_tree(new_data, target_attribute, new_attrinures)
                tree[best_gain][key] = subtree

        return tree


    def entropy(self, data, target_attr):

        stat = {}
        entropy = 0.0
        i = self.attributes.index(target_attr)

        for row in data:
            if row[i] in stat:
                stat[row[i]] += 1.0
            else:
                stat[row[i]] = 1.0

        for key in stat.values():
            entropy += (-key / len(data)) * math.log2(key / len(data))

        return entropy


    def gain(self, data, attr, target_attr):

        stats = {}
        subset_entropy = 0.0
        i = self.attributes.index(attr)

        for row in data:
            if row[i] in stats:
                stats[row[i]] += 1.0
            else:
                stats[row[i]] = 1.0


        for key in stats.keys():
            key_stat = stats[key] / sum(stats.values())
            new_data = [record for record in data if record[i] == key]
            subset_entropy += key_stat * self.entropy(new_data, target_attr)

        return (self.entropy(data, target_attr) - subset_entropy)


    def select_attribute(self, data, attributes, target_attribute):
        gain = {}
        for attr in attributes:
            if attr != target_attribute:
                gain[attr] = self.gain(data, attr, target_attribute)

        return (max(gain, key = gain.get))


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
        print("Stats:", len(data.keys()),data)
        return  data


    def test_decision_tree(self, data, tree):
        count = 0

        for row in data:
            decision = tree
            while True:
                for key in decision:
                    node = key
                i = self.attributes.index(node)
                result = row[i]
                decision = decision[node][result]
                if type(decision) is not dict:
                    break
            if decision == row[-1]:
                count += 1


        return (count / len(data))


test = ID3()

