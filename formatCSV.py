import csv


updated_rows = []
with open('Data/loginids.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        row.append('')
        row.append('')
        row.append('')
        updated_rows.append(row)

with open('Data/loginids.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(updated_rows)