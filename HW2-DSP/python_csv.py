import csv

t = [] # column 0
data1 = [] # column 1
# data2 = [] # column 2

with open('sigB.csv') as f:
    # open the csv file
    reader = csv.reader(f)
    for row in reader:
        # read the rows 1 one by one
        t.append(float(row[0])) # leftmost column
        data1.append(float(row[1])) # second column
        # data2.append(float(row[2])) # third column

num_data_pts = 3

for i in range(len(t) - num_data_pts):

    time_start = t[0 + i]
    time_end = t[(num_data_pts - 1) + i]

    time_diff = time_end - time_start

    # print("Total sample time is " + str(time_diff) + " seconds")

    sample_rate = int(num_data_pts / time_diff)

    # print("The sample rate is " + str(sample_rate))

# for i in range(len(t)):
#     # print the data to verify it was read
#     # print(str(t[i]) + ", " + str(data1[i]) + ", " + str(data2[i]))
#     print(str(t[i]) + ", " + str(data1[i]))