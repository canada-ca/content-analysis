# Python script to create a CSV file of standardized format to facilitate future content analysis
# output is a CSV file
import csv

# -----------VARIABLES TO CHANGE------------

# the input csv file path
# RESTRICTIONS: needs to have extension ".csv", String
input_file = r"CHANGE THIS"

# the row in the csv file where appropriate data is located
# RESTRICTIONS: integer, if the data is missing, then assign "N/A"
id_field = 0
comment_field = 13
user_info_field = 9
date_field = "N/A"
event_field = 1

# output csv file name
# RESTRICTIONS: needs to have extension ".csv", String
output_file = r"CHANGE THIS"
# ------------------------------------------

# read data from input file
with open(input_file, encoding='cp1252') as csvfile:
    id = []
    comment = []
    userinfo = []
    date = []
    event = []

    readCSV = csv.reader(csvfile, delimiter=',')
    counter = 0
    for row in readCSV:

        if id_field == "N/A":
            id_= counter
            counter = counter+1
        else:
            id_ = row[id_field]

        if comment_field == "N/A":
            comment_ = "N/A"
        else:
            comment_ = row[comment_field]

        if user_info_field == "N/A":
            userinfo_ = "N/A"
        else:
            userinfo_ = row[user_info_field]

        if date_field == "N/A":
            date_ = "N/A"
        else:
            date_ = row[date_field]

        if event_field == "N/A":
            event_ = "N/A"
        else:
            event_ = row[event_field]

        if id_ == "" or comment_ == "" or userinfo_ == "" or date_ == "" or event_ == "":
            x = 1
        else:
            id.append(id_)
            comment.append(comment_)
            userinfo.append(userinfo_)
            date.append(date_)
            event.append(event_)


# create the new csv file
def write_csv():
    rows = zip(id, comment, userinfo, date, event)
    myFile = open(output_file, 'w', newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(rows)


write_csv()
