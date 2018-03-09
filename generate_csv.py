#Python script to create a CSV file of standardized format to facilitate future content analysis
#outout is a CSV file

import csv

#-----------VARIABLES TO CHANGE------------
#the input csv file path
input_file = r"C:\Users\hanna\Desktop\OpenNorth\Data\forAnalysis\Same\Biennial\individualComments.csv"
#the row in the csv file where appropriate data is located
#if a data field is missing in the initial dataset, assign "N/A"
id_field = 0
comment_field = 18
user_info_field = 7
date_field = "N/A"
event_field = 1
#output csv file name
output_file = 'Biennial_8.csv'
#------------------------------------------

#read data from input file
with open(input_file, encoding='cp1252') as csvfile:
    id = []
    comment = []
    userinfo = []
    date = []
    event = []

    readCSV = csv.reader(csvfile, delimiter=',')
    counter = 0
    for row in readCSV:

        #comment out the appropriate variable if its data is missing
        id_ = row[id_field]
        comment_ = row[comment_field]
        userinfo_ = row[user_info_field]
        #date_ = row[1]
        event_ = row[event_field]

        #***IF NO USER INFO --> uncomment this line and comment out the previous
        #*** ADD CUSTOM INFO IF NECESSARY
        #userinfo_ = "N/A"

        # ***IF NO DATE --> uncomment this line and comment out the previous
        # *** ADD CUSTOM INFO IF NECESSARY
        date_ = "N/A"

        # ***IF NO EVENT --> uncomment this line and comment out the previous
        # *** ADD CUSTOM INFO IF NECESSARY
        #event_ = "N/A"

        #***IF NO ID --> uncomment this line and comment out the previous
        #id_= counter
        #counter = counter+1

        if id_ == "" or comment_ == "" or userinfo_ == "" or date_ == "" or event_ == "":
            x = 1
        else:
            id.append(id_)
            comment.append(comment_)
            userinfo.append(userinfo_)
            date.append(date_)
            event.append(event_)

#create the new csv file
def write_csv():
    rows = zip(id, comment, userinfo, date, event)
    myFile = open(output_file, 'w', newline = '')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(rows)

write_csv()
