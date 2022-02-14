import os
import re

file = open('json_data', 'r')

plants = file.read()
data_without_claw = re.sub("'", '"', plants)

if os.path.exists('json_data_double_claws'):
    os.remove('json_data_double_claws')

f = open("json_data_double_claws", 'a')
f.writelines(data_without_claw)
f.close()

file.close

# Adding ',' in the json file
file = open('json_data_double_claws', 'r')

plants = file.read()

if os.path.exists('final_json_data.json'):
    os.remove('final_json_data.json')

f = open("final_json_data.json", 'a')
j = 1
f.write('{')
f.write('"{}" : \\"'.format(j))
for i in plants:
    f.write(i)
    if i == '}':
        j += 1
        f.write('\\",')
        f.write('\n"{}" : \\"'.format(j))
f.write('}')
f.close()