import random
from neural_network import NeuralNetwork

def read_data(filename):
    # read data from file
    data = []
    label = []
    with open(filename) as f:
        for line in f:
            row = line[:-1].split(',')
            data.append(row[1:])
            label_row = [0] * 5
            label_row[int(row[0])] = 1
            label.append(label_row)

    return data, label


def run():
    # create a neural network with 784 input neuron, 16 hidden neuron and 5 output
    nn = NeuralNetwork(784, 50, 5)

    # get the train and test data
    train_data, train_label = read_data("train_data.csv")
    test_data, test_label = read_data("test_data.csv")

    # Number of training iterations
    for x in range(10):
        print("#### Iteration", x+1,"####")
        # randomly shuffle the data before training
        train = list(zip(train_data, train_label))
        random.shuffle(train)
        train_data, train_label = zip(*train)

        for i in range(len(train_data)):
            nn.train(train_data[i], train_label[i])

        count = 0
        for i in range(len(test_data)):
            predict_label = nn.predict(test_data[i])[1].tolist()
            predict_label = predict_label.index(max(predict_label))
            # print(predict_label, test_label[i].index(1))
            if predict_label == test_label[i].index(1):
                count += 1

            accuracy = count / len(test_label)

        print("Accuracy: ", accuracy)


if __name__ == "__main__":
    run()
