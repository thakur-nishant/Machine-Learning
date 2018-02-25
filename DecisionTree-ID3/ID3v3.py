"""
Name: Nishant Thakur
ID: 1001544591

References: https://en.wikipedia.org/wiki/ID3_algorithm
            http://www.onlamp.com/pub/a/python/2006/02/09/ai_decision_trees.html
"""
import math, json
import random
import jsbeautifier

# class that implements ID3 algorithm
class ID3:
    # Initialize function is used to format the data and to split the data into training and testing dataset
    def __init__(self):
        self.data = []
        #load attributes of dataset
        with open('tic-attr.txt') as f:
            for line in f:
                self.attributes = line[:-1].split(',')

        #load the data as list from the dataset
        with open('tic-tac-toe.data') as f:
            for line in f:
                data = line[:-1].split(',')
                self.data.append(data)

        #perform a random shuffle on dataset to mix the data
        random.shuffle(self.data)

        #split data in 80:20 partition
        n = len(self.data)
        len_train = math.floor(n * 0.8)
        train_dataset = self.data[:len_train]
        test_dataset = self.data[len_train:]

        self.target_attribute = "Class"
        #Training and testing with cross validation
        tree = self.cross_validation(10, train_dataset)

        # jsbeautifier is used to print the generated decision tree in tree format
        print("Tree:")
        print(jsbeautifier.beautify(json.dumps(tree)))

        # calculate accuracy by runing test on test dataset
        accuracy = self.test_decision_tree(test_dataset, tree)
        print("Accuracy:", accuracy)

    # this function is used for K-fold cross validation on the training dataset
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
            print("############## Iteration", i+1, "################")
            self.stats = self.statistics(train, self.attributes)

            tree = self.create_decision_tree(train, self.target_attribute, self.attributes)
            # print("Tree:", tree)

            accuracy = self.test_decision_tree(test, tree)
            print("Accuracy:", accuracy)
            print()
            tree_list.append(tree)
            accuracy_list.append(accuracy)

        print("Cross-validation Average Accuracy:", sum(accuracy_list)/k)
        print()
        best_tree = accuracy_list.index(max(accuracy_list))

        return tree_list[best_tree]


    # this function is used to build the decision tree
    # this function is called recursively to construct the entire tree
    # it returns the tree
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

                next_attrinures = [attr for attr in attributes if attr != best_gain]

                subtree = self.create_decision_tree(new_data, target_attribute, next_attrinures)
                tree[best_gain][key] = subtree

        return tree


    #this function is used to caluculate the entropy
    # returns entropy
    def entropy(self, data, target_attribute):

        stat = {}
        entropy = 0.0
        i = self.attributes.index(target_attribute)

        for row in data:
            if row[i] in stat:
                stat[row[i]] += 1.0
            else:
                stat[row[i]] = 1.0

        for key in stat.values():
            entropy += (-key / len(data)) * math.log2(key / len(data))

        return entropy


    # this fucntion is used to calculate gain for the given attribute
    # it returns the gain for the attribute
    def gain(self, data, attr, target_attribute):

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
            subset_entropy += key_stat * self.entropy(new_data, target_attribute)

        return (self.entropy(data, target_attribute) - subset_entropy)


    # this function is used to select the attribute with maximum gain
    # returns the attribute with maximum gain
    def select_attribute(self, data, attributes, target_attribute):
        gain = {}
        for attr in attributes:
            if attr != target_attribute:
                gain[attr] = self.gain(data, attr, target_attribute)

        return (max(gain, key = gain.get))


    # this function is used to track the statistics of each attribute in data
    # returns a dictionary for statistic of each attribute
    def statistics(self, votes, attributes):
        data = {}
        i = self.attributes.index(self.target_attribute)
        for attr in attributes:
            data[attr] = {}
            data[attr]['total'] = 0

        for vote in votes:
            for j in attributes:
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
        # print("Stats:", data)
        return  data


    # this function is used to test the generated tree and calculate the accuracy
    # returns accuracy
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

        accuracy = count / len(data)
        return accuracy


# start the algorithm by making the onject of the class
test = ID3()

