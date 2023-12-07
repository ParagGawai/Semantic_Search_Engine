import csv

# DONOT use pandas here as it laods all of data into RAM at once.


cnt=0

with open(r'E:\Placement\Semantic Search\data\Questions.csv', encoding="latin1") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',', )
        next(readCSV, None)  # skip the headers
        # for row in readCSV:
        #         # keep count of # rows processed
        #         cnt += 1
        #         #print(cnt)

# print(cnt,len(row))
# print(row)




# cnt=0

# with open(r'E:\Placement\Semantic Search\data\Answers.csv', encoding="latin1") as csvfile:
#         readCSV = csv.reader(csvfile, delimiter=',')
#         next(readCSV, None)  # skip the headers
#         for row in readCSV:
#                 # keep count of # rows processed
#                 cnt += 1

# print(cnt,len(row))
