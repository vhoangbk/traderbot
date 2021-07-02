import csv

in_csv = 'AdditionIT.csv'

name_file = "AdditionIT"

row_size = 990
line_count = 0
data = []

header = ""

with open(in_csv, encoding="utf8", errors='ignore') as f:
  csv_reader = csv.reader(f, delimiter=',')

  for row in csv_reader:
      if line_count == 0:
        header = row
      else:
        row[0] = ""
        row[1] = "Task"
        row[3] = ""
        row[4] = "To Do"

      line_count += 1
      data.append(row)

  for i in range(0,line_count,row_size):
    out_csv = name_file + "_" + str(int(i/row_size)) + '.csv'
    print(out_csv)

    with open(out_csv, 'w', encoding='UTF8') as f:
      writer = csv.writer(f)

      # write the data
      print("start {}".format(i))
      end = row_size
      if i > 1:
        # write the header
        writer.writerow(header)
        end = row_size + i
        if end > line_count:
          end = line_count
      print("end {}".format(end))
      writer.writerows(data[i:end:1])
