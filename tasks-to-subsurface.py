import json
import csv
from dateutil import parser


class Dive:
    def __init__(self, task_data):
        self.data = task_data
        self.dive_num = ''
        self.date = ''
        self.time = ''
        self.location = ''
        self.max_depth = ''
        self.avg_depth = ''
        self.duration = ''
        self.visibility = ''
        self.water_temp = ''
        self.weight = ''
        self.suit = ''
        self.tags = ''
        self.start_pressure = ''
        self.end_pressure = ''
        self.notes = ''
        self.cyl_size = 'AL80'
        self.o2 = '21'
        self.row = [self.dive_num, self.date, self.time, self.location, self.max_depth,
                    self.avg_depth, self.duration, self.visibility, self.water_temp,
                    self.weight, self.suit, self.tags, self.start_pressure, self.end_pressure,
                    self.notes, self.cyl_size, self.o2]
        self.process_data()

    def process_data(self):
        if self.data.get('notes', False):
            dive_notes = self.data['notes']
        else:
            return
        dive_notes = dive_notes.replace("Bottom time:", "Duration:")
        dive_notes = dive_notes.replace("Temperature", "Water temp")
        dive_notes = dive_notes.replace("Exposure protection:", "Suit:")
        dive_notes = dive_notes.replace("Conditions:", "Tags:")
        dive_notes = dive_notes.replace("Comments:", "Notes:")
        split_dive = dive_notes.split('\n')

        properties = {}
        remove_chars = '+'
        for item in split_dive:
            item = item.replace(remove_chars, '')
            split_items = ' '.join(item.split()).split(': ')
            if len(split_items) > 1:
                if 'temps' in split_items[0]:
                    split_items[0] = split_items[0].replace('s', '')
                properties.update({split_items[0]: split_items[1]})

        if properties.get('Depth', False):
            properties['Max Depth'] = properties.pop('Depth')
            properties['Max Depth'] = properties['Max Depth'].split(' ')[0]
        if properties.get('Location', False) == False:
            if properties.get('Dive site', False) == False:
                properties['Location'] = self.data['title']
            else:
                properties['Location'] = properties['Dive site']
        properties['Location'] = self.data['title'] + ', ' + properties['Location']
        if properties.get('Time', False):
            if len(properties['Time'].split(' ')) > 1:
                properties['Time'] = properties['Time'].split(' ')[0] + ' ' + properties['Time'].split(' ')[1]
        if properties.get('Avg Depth', False):
            properties['Avg Depth'] = properties['Avg Depth'].split(' ')[0]
        if properties.get('Duration', False):
            properties['Duration'] = properties['Duration'].split(' ')[0]
        if properties.get('Visibility', False):
            properties['Visibility'] = properties['Visibility'].split(' ')[0]
        if properties.get('Water temp', False):
            properties['Water temp'] = properties['Water temp'].split(' ')[0]
        if properties.get('Weight', False):
            properties['Weight'] = properties['Weight'].split(' ')[0]
        if properties.get('Air', False):
            if len(properties['Air'].split(' ')) > 2:
                properties['Start Pressure'] = properties['Air'].split(' ')[0]
                properties['End Pressure'] = properties['Air'].split(' ')[2]
            #del properties['Air']

        self.dive_num = None
        if properties.get('Date', False):
            self.date = properties['Date']
        if properties.get('Time', False):
            self.time = properties['Time']
        if properties.get('Location', False):
            self.location = properties['Location']
        if properties.get('Max Depth', False):
            self.max_depth = properties['Max Depth']
        if properties.get('Avg Depth', False):
            self.avg_depth = properties['Avg Depth']
        if properties.get('Duration', False):
            self.duration = properties['Duration']
        if properties.get('Visibility', False):
            if int(properties["Visibility"]) <= 10:
                self.visibility = 1
            elif 10 < int(properties["Visibility"]) <= 30:
                self.visibility = 2
            elif 30 < int(properties["Visibility"]) <= 60:
                self.visibility = 3
            elif 60 < int(properties["Visibility"]) <= 100:
                self.visibility = 4
            elif 100 < int(properties["Visibility"]):
                self.visibility = 5
            else:
                self.visibility = 0
            #self.visibility = properties['Visibility']
        if properties.get('Water temp', False):
            self.water_temp = properties['Water temp']
        if properties.get('Weight', False):
            self.weight = properties['Weight']
        if properties.get('Suit', False):
            self.suit = properties['Suit']
        if properties.get('Tags', False):
            self.tags = properties['Tags']
        if properties.get('Start Pressure', False):
            self.start_pressure = properties['Start Pressure']
        if properties.get('Start Pressure', False):
            self.end_pressure = properties['End Pressure']
        if properties.get('Notes', False):
            self.notes = properties['Notes']

    def generate_row(self):
        self.row = [self.dive_num, self.date, self.time, self.location, self.max_depth,
                    self.avg_depth, self.duration, self.visibility, self.water_temp,
                    self.weight, self.suit, self.tags, self.start_pressure, self.end_pressure,
                    self.notes, self.cyl_size, self.o2]


with open('Tasks.json') as file:
    data = json.load(file)

dive_data = data['items'][0]['items']
processed_dives = []
counter = 0
for item in dive_data:
    if item['status'] != 'completed':
        counter += 1
for item in dive_data:
    if item['status'] != 'completed':
        processed_dives.append(Dive(item))


def sort_func(item):
    if item.date != '':
        date_obj = parser.parse(item.date)
        return date_obj
    else:
        return parser.parse("01/01/1990")


processed_dives.sort(key=sort_func, reverse=True)

counter = 5
for i in range(len(processed_dives)-1,0, -1):
    counter += 1
    processed_dives[i].dive_num = counter
    processed_dives[i].generate_row()


def rejoin(string_list):
    for i in range(2, len(string_list)):
        string_list[1] = string_list[1] + ' ' + string_list[i]
    return string_list


headers = ['Dive #', 'Date', 'Time', 'Location', 'Max Depth', 'Avg Depth', 'Duration',
           'Visibility', 'Water temp', 'Weight', 'Suit', 'Tags', 'Start Pressure',
           'End Pressure', 'Notes', 'Cyl. size', 'O2']

filename = 'divelog.csv'
with open(filename, 'w', newline='\n') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='\t')
    csvwriter.writerow(headers)
    for dive in processed_dives:
        csvwriter.writerow(dive.row)
