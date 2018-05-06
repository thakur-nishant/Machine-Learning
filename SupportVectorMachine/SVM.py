import itertools

def read_pgm(pgmf):
    """Return a raster of integers from a PGM as a list of lists."""
    pgmf.readline()
    # assert pgmf.readline() == 'P5\n'
    (width, height) = [int(i) for i in pgmf.readline().split()]
    depth = int(pgmf.readline())
    assert depth <= 255

    raster = []
    for y in range(height):
        row = []
        for y in range(width):
            row.append(ord(pgmf.read(1)))
        raster.append(row)

    return list(itertools.chain.from_iterable(raster))


def read_data():

    X = []
    Y = []
    for dir in range(1,41):
        for file in range(1,11):
            pgmf = open('att_faces/s'+str(dir)+'/'+str(file)+'.pgm', 'rb')
            data = read_pgm(pgmf)
            Y.append(dir)
            X.append(data)

    return X, Y
    # print(X[0])

X,Y = read_data()