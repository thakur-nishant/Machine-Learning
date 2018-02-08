class ID3:
    def __init__(self):
        self.votes = []
        with open('playball-attr.txt') as f:
            for line in f:
                self.attributes = line.split(',')
        # print(self.attributes)
        with open('playball.txt') as f:
            for line in f:
                data = line[:-1].split(',')
                self.votes.append(data)


        self.data = self.statistics(self.votes, self.attributes)
        # for i in self.votes:
        #     print(i)

    def statistics(self, votes, attributes):
        data = {}

        for attr in attributes:
            data[attr] = {}
            data[attr]['total'] = 0

        for vote in votes:
            for j in range(len(attributes)):
                if vote[j] in data[attributes[j]]:
                    data[attributes[j]][vote[j]] += 1
                else:
                    data[attributes[j]][vote[j]] = 1
                data[attributes[j]]['total'] += 1
        print(data)
        return  data

test = ID3()
