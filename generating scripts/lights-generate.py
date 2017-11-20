import csv
import time
readin = csv.DictReader(open('lights.csv', "rb"))
input_list = []
item_list = []
output_file = open('lights.yaml', 'w')

for line in readin:
    input_list.append(line)

for x in range(0, len(input_list)):
    entry = ""
    entry += "- platform: " + input_list[x]['platform']
    entry += "\n  name: \"" + input_list[x]['name'] + "\""
    entry += "\n  state_topic: \"" + input_list[x]['state_topic'] + "\""
    entry += "\n  command_topic: \"" + input_list[x]['command_topic'] + "\""
    entry += "\n  payload_on: \"" + input_list[x]['payload_on'] + "\""
    entry += "\n  payload_off: \"" + input_list[x]['payload_off'] + "\""
    item_list.append(entry)

output_file.write("# Generated on " + time.strftime("%c") + "\n")
output_file.write("# by " + __file__ + "\n\n")
for item in item_list:
    output_file.write(item + "\n\n")
