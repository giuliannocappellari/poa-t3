import json
from time import sleep
list_data =json.load(open('data.json', 'r'))
set_data =json.load(open('data2.json', 'r'))

# print(list_data)
for i in list_data:
    if i not in set_data:
        print(i)
        sleep(20)