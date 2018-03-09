#Python script to create an object-based data structure to store the CSV data
#includes a demonstration of basic ways to query the dataset, with a txt file output

import csv

#-----------VARIABLES TO CHANGE------------

#new CSV filepath (created from "generate_csv.py"
input_file = r"C:\Users\hanna\Desktop\OpenNorth\Python\Output_Files\Biennial\Biennial_1.csv"
#title of original dataset
dataset = "Open Government Action Plan (Individual Comments)"
#output txt file name
fileoutput = "OG_ActionPlan_describe_8.txt"
#sample ID number from the file (demonstration of query capabilities)
id_no = 43
#sample date from the file (demonstration of query capabilities
date_query = "16/05/2016"
#sample event from the file (demonstration of query capabilities
event_query = "Edmonton"
#------------------------------------------

#read in the data from the standardized CSV file
with open(input_file, encoding='cp1252') as csvfile:
    id = []
    comment = []
    userinfo = []
    date = []
    event = []

    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        id_ = row[0]
        comment_ = row[1]
        userinfo_ = row[2]
        date_ = row[3]
        event_ = row[4]

        id.append(id_)
        comment.append(comment_)
        userinfo.append(userinfo_)
        date.append(date_)
        event.append(event_)

#Entry class to effectively store the information relating to each data entry
class Entry(object):
    id_ = 0
    comment_ = ""
    userinfo = ""
    date_ = ""
    event_ = ""

    def __init__(self, id_, comment_, userinfo_, date_, event_):
        self.id = id_
        self.comment = comment_
        self.userinfo = userinfo_
        self.date = date_
        self.event = event_

def make_entry(id_, comment_, userinfo_, date_, event_):
        entry = Entry(id_, comment_, userinfo_, date_, event_)
        return entry

#list to store each of the "Entry" objects
entry_list = []

def buildentries():
    for x in range(len(id)):
        current_entry = make_entry(id[x], comment[x], userinfo[x], date[x], event[x])
        entry_list.append(current_entry)

buildentries()

#find the comment associated with a certain ID number
def find_comment(id_no):
    for x in range(1, len(entry_list)):
        if int(entry_list[x].id) == id_no:
            return entry_list[x].comment
        else:
            return "No response"
#find the number of dates that are from a certain event
def find_dates(date):
    count = 0
    for x in range(0, len(entry_list)):
        if date in entry_list[x].date:
            count = count + 1
    return count

#find the number of comments that are from a certain event
def find_events(event):
    count = 0
    for x in range(0, len(entry_list)):
        if event in entry_list[x].event:
            count = count + 1
    return count

#function to generate a text file with a basic description of the dataset
def describe():
    file = open(fileoutput, "w")
    file.write('This data is from the ' + dataset + '  dataset.\n\n')
    file.write("Qualitative responses reflect answers to the question: " + entry_list[0].comment + "\n\n")
    file.write("Information collected about the respondents: " + entry_list[0].userinfo + "\n\n")
    file.write('---------- This dataset has ' + str(len(entry_list)) + ' entries\n\n')
    file.write("---------- Here is an example of the information contained within each entry: " + "\n\n")
    file.write("ID: " + entry_list[5].id + "\n")
    file.write("COMMENT: " + entry_list[5].comment + "\n")
    file.write("DATE: " + entry_list[5].date + "\n")
    file.write("RESPONDENT INFO: " + entry_list[5].userinfo + "\n\n")
    file.write("---------- Here are some examples of basic queries that can be performed: " + "\n\n")
    file.write("1. What is the comment associated with respondent #" + str(id_no) + "?" + "\n\n")
    file.write(find_comment(id_no) + "\n\n")
    file.write("2. How many responses were posted on 16/05/2016?\n\n")
    file.write("There were " + str(find_dates(date_query)) + " posted on that date.\n\n")
    file.write("3. How many responses are from the Edmonton consultation?\n\n")
    file.write("There were " + str(find_events(event_query)) + " responses posted from that event.")
    file.close()

describe()
