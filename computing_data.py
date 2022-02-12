from email.policy import strict
import re
import json
import os

file = open('plants.txt', 'r')
"""
str_lines = file.readlines()
'''str_lines.replace(';', '')
str_lines.splitlines()'''

'''
    Deleting *\n in the strings

list_without_end_char = []
for el in str_lines:
    list_without_end_char.append(el[:len(el) - 3])

print(list_without_end_char)
'''

while '\n' in str_lines:
    str_lines.remove('\n')

while '\n' in str_lines:
    str_lines.remove('\n')


elements_list = [el.split('=') for el in str_lines]

print(elements_list)
'''
for i in range(0, len(elements_list), 2):
    elements_list[i][1] = elements_list[i][1].splitlines()
print(elements_list)
'''
"""

string = file.read().replace('\n', '@')
without_numerical = ''.join([i for i in string if not i.isdigit() and i != '-']).split('@@')
#print(without_numerical)

liste = [el.split('=') for el in without_numerical]

final_list = []
for el in liste:
    dico = {}
    dico["ewe_name"] = el[0]
    if len(el) > 2:
        dico["french_name"] = el[1]
    dico["sci_name"] = el[len(el) - 1]

    final_list.append(dico)

#print(final_list)

file.close()

if os.path.exists('json_data'):
    os.remove('json_data')

json_file = open('json_data', 'a')

for json_ in final_list:
    json_file.write(str(json_))
    json_file.write('\n')

json_file.close