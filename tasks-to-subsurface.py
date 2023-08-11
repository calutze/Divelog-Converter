import json
import csv


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
        if properties.get('Avg Depth', False) != False:
            properties['Avg Depth'] = properties['Avg Depth'].split(' ')[0]

        if properties.get('Duration', False) != False:
            properties['Duration'] = properties['Duration'].split(' ')[0]
        if properties.get('Visibility', False) != False:
            properties['Visibility'] = properties['Visibility'].split(' ')[0]
        if properties.get('Water temp', False) != False:
            properties['Water temp'] = properties['Water temp'].split(' ')[0]
        if properties.get('Weight', False) != False:
            properties['Weight'] = properties['Weight'].split(' ')[0]
        if properties.get('Air', False) != False:
            if properties.get('Start Pressure', False) != False:
                properties['Start Pressure'] = properties['Air'].split(' ')[0]
            if properties.get('End Pressure', False) != False:
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
        if properties.get('Avg Depth', False):
            self.duration = properties['Duration']
        if properties.get('Visibility', False):
            self.visibility = properties['Visibility']
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

        self.row = [self.dive_num, self.date, self.time, self.location, self.max_depth,
                    self.avg_depth, self.duration, self.visibility, self.water_temp,
                    self.weight, self.suit, self.tags, self.start_pressure, self.end_pressure,
                    self.notes, self.cyl_size, self.o2]


with open('Tasks.json') as file:
    data = json.load(file)

dive_data = data['items'][3]['items']
processed_dives = []
counter = 0
for item in dive_data:
    if item['status'] != 'completed':
        counter += 1
for item in dive_data:
    if item['status'] != 'completed':
        processed_dives.append(Dive(item))


def rejoin(string_list):
    for i in range(2, len(string_list)):
        string_list[1] = string_list[1] + ' ' + string_list[i]
    return string_list


headers = ['Dive #', 'Date', 'Time', 'Location', 'Max Depth', 'Avg Depth', 'Duration',
           'Visibility', 'Water temps', 'Weight', 'Suit', 'Tags', 'Start Pressure',
           'End Pressure', 'Notes', 'Cyl. size', 'O2']

filename = 'divelog.csv'
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)
    for dive in processed_dives:
        csvwriter.writerow(dive.row)



# convert visibility to between 0-5
# strip + from visiblity


# make dive object or list
# sort dives by date and then by time
# add dive number


# if 'Time' in split_items[0]:
# split_items[1] = split_items[1] + ' ' + split_items[2]
# Location formatting
# if 'Location' in split_items[0]:
# for i in range(2, len(split_items)):
# split_items[1] = split_items[1] + ' ' + split_items[i]
# split_items = rejoin(split_items)
# if "Avg" in split_items[0]:
# split_items[0] = split_items[0] + ' ' + split_items[1]
# split_items.pop(1)
# x=1
# if "Depth" in split_items[0] and "Avg" not in split_items[0]:
# x=1


'''
# TODO: operation notes here, move into class
current_dive = dive_data[0]
dive_notes = current_dive['notes']
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
    if 'temp' in split_items[0]:
        split_items[0] = split_items[0].replace('s', '')
    properties.update({split_items[0]: split_items[1]})

properties['Max Depth'] = properties.pop('Depth')
properties['Location'] = current_dive['title'] + ', ' + properties['Location']
properties['Time'] = properties['Time'].split(' ')[0] + ' ' + properties['Time'].split(' ')[1]
properties['Avg Depth'] = properties['Avg Depth'].split(' ')[0]
properties['Max Depth'] = properties['Max Depth'].split(' ')[0]
properties['Duration'] = properties['Duration'].split(' ')[0]
properties['Visibility'] = properties['Visibility'].split(' ')[0]
properties['Water temp'] = properties['Water temp'].split(' ')[0]
properties['Weight'] = properties['Weight'].split(' ')[0]
properties['Start Pressure'] = properties['Air'].split(' ')[0]
properties['End Pressure'] = properties['Air'].split(' ')[2]
del properties['Air']
'''