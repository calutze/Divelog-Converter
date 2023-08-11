import json
import csv


class Dive:
    def __init__(self, task_data):
        self.data = task_data
        self.dive_num = None
        self.date = None
        self.time = None
        self.location = None
        self.max_depth = None
        self.avg_depth = None
        self.duration = None
        self.visibility = None
        self.water_temp = None
        self.weight = None
        self.suit = None
        self.tags = None
        self.start_pressure = None
        self.end_pressure = None
        self.notes = None
        self.cyl_size = 'AL80'
        self.o2 = '21'
        self.process_data()

    def process_data(self):
        x=1

    def location(self):
        self.location = 1


with open('Tasks.json') as file:
    data = json.load(file)

dive_data = data['items'][3]['items']
#processed_dives = []
#for item in dive_data:
    #processed_dives.append(Dive(item))

def rejoin(string_list):
    for i in range(2, len(string_list)):
        string_list[1] = string_list[1] + ' ' + string_list[i]
    return string_list
# TODO: operation notes here, move into class
current_dive = dive_data[0]
dive_notes = current_dive['notes']
dive_notes = dive_notes.replace("Bottom time:", "Duration:")
dive_notes = dive_notes.replace("Temperature:", "Water temp:")
dive_notes = dive_notes.replace("Exposure protection:", "Suit:")
dive_notes = dive_notes.replace("Conditions:", "Tags:")
dive_notes = dive_notes.replace("Comments:", "Notes:")
split_dive = dive_notes.split('\n')
properties = {}

# fix headers
# change bottom time to duration
#for item in split_dive:
    #if "Bottom time:" in item:
        #item = item.replace("Bottom time", "Duration")
        #split_dive
        #x=1


remove_chars = '+'
for item in split_dive:
    item = item.replace('+', '')
    split_items = ' '.join(item.split()).split(' ')
    if 'ime' in split_items[0]:
        split_items[1] = split_items[1] + ' ' + split_items[2]
    #Location formatting
    if 'ocation' in split_items[0]:
        #for i in range(2, len(split_items)):
            #split_items[1] = split_items[1] + ' ' + split_items[i]
        split_items = rejoin(split_items)
    properties.update({split_items[0]: split_items[1]})
location = current_dive['title']


dive_log_file = open('divelog.csv', 'w')
csv_writer = csv.writer(dive_log_file)
counter = 0

# convert visibility to between 0-5
# strip + from visiblity


    # make dive object or list
    # sort dives by date and then by time
    # add dive number