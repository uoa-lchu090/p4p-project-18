import csv

def format(filename):

    fields = ['id', 'filename', 'text']
    rows = []

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        id = 0
        for row in csv_reader:
            row.insert(0, id)
            id += 1
            rows.append(row)

    with open('new' + filename, 'w') as new_file:

        csv_writer = csv.writer(new_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(rows)

if __name__ == "__main__":
    format('JL_output_speechbrain.csv')