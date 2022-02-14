import requests
import json
import subprocess


#API details
url = "http://127.0.0.1:5000/plants"
headers = {'Content-Type': 'application/json'}

file = open('json_data_double_claws', 'r')

content = file.read()
data = ''
for i in content:
    data += i
    if i == '}':
        subprocess.Popen('curl -i -H "Content-Type: application/json" -X POST -d \'{}\' http://127.0.0.1:5000/plants'.format(str(data)), shell=True,  stdout=open('outputfile.json'))
        #body = json.dumps(dict(data))
        data = ''
        #Making http post request
        #response = requests.post(url, headers=headers, data=body, verify=False)
        
        #print(response.json())

file.close()


"""import requests
import json

#API details
url = "http://127.0.0.1:5000/plants"
body = dict({"ewe_name": " AHAMÉ en Éwé ", "sci_name": " *BASILIC OCYNIUM ou OCYNIUM BASILIUM ;*"})
print(body.get('ewe_name'))
headers = {'Content-Type': 'application/json'}

#Making http post request
response = requests.post(url, headers=headers, data=body, verify=False)

print(response.json())"""


"""
data = '{"ewe_name": " ÉHLIVI ", "sci_name": " *PHYLLANTHUS*"}'
subprocess.Popen('curl -i -H "Content-Type: application/json" -X POST -d \'{}\' http://127.0.0.1:5000/plants'.format(data), shell=True,  stdout=open('outputfile.json'))
"""