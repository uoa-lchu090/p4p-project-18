import codecs
import csv
import os
import matplotlib as plt


def getList(filename):
    data = []
    with open(filename) as file:
        print(file)
        reader = csv.reader(file)
        for row in reader:
            try:
                data.append(row)
            except:
                print(row)

    print(data)
    return data


def graph(filelist, labels):
    data = []
    fileset = []
    for filename in filelist:
        fileset.append(getList(filename))

    for results in fileset:
        total = 0
        for row in results:
            total += row[4]
        ave = total / len(results)
        data.append(ave)

    fig = plt.figure(figsize=(10, 5))
    plt.bar(labels, data, color='maroon',
            width=0.4)

    plt.xlabel("Dataset")
    plt.ylabel("MER")
    plt.title("MER of new model on different datasets")
    plt.show()


def reencode(filename):
    import codecs
    BLOCKSIZE = 1048576  # or some other, desired size in bytes
    with codecs.open(filename, "r", "cp1252") as sourceFile:
        with codecs.open(filename, "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)


if __name__ == '__main__':
    directory = 'Model_All'
    filenames = []
    labels = ['JL', 'MansField', 'Mozilla']
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        filenames.append(f)

    graph(filenames, labels)
