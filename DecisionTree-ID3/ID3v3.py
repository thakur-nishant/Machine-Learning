import math, json
import random
from collections import defaultdict

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

        self.stats = self.statistics(train, self.attributes)

        tree = self.create_decision_tree(train, "Class", self.attributes)
        # print(z)
        print(json.dumps(tree))

        accuracy = self.test_decision_tree(test, tree)
        print("Accuracy:", accuracy)



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
        """
        Calculates the entropy of the given data set for the target attribute.
        """
        val_freq = {}
        data_entropy = 0.0
        i = self.attributes.index(target_attr)
        # Calculate the frequency of each of the values in the target attr
        for record in data:
            if record[i] in val_freq:
                val_freq[record[i]] += 1.0
            else:
                val_freq[record[i]] = 1.0

        # Calculate the entropy of the data for the target attribute
        for freq in val_freq.values():
            data_entropy += (-freq / len(data)) * math.log(freq / len(data), 2)

        return data_entropy


    def gain(self, data, attr, target_attr):
        """
        Calculates the information gain (reduction in entropy) that would
        result by splitting the data on the chosen attribute (attr).
        """
        val_freq = {}
        subset_entropy = 0.0
        i = self.attributes.index(attr)
        # Calculate the frequency of each of the values in the target attribute
        for record in data:
            if record[i] in val_freq:
                val_freq[record[i]] += 1.0
            else:
                val_freq[record[i]] = 1.0

        # Calculate the sum of the entropy for each subset of records weighted
        # by their probability of occuring in the training set.
        for val in val_freq.keys():
            val_prob = val_freq[val] / sum(val_freq.values())
            data_subset = [record for record in data if record[i] == val]
            subset_entropy += val_prob * self.entropy(data_subset, target_attr)

        # Subtract the entropy of the chosen attribute from the entropy of the
        # whole data set with respect to the target attribute (and return it)
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

