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