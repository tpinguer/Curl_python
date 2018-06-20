import requests
import json
import os
import re

 
root_folder = os.path.dirname(__file__)

contracts_folder = os.path.join(root_folder, 'DataSet') 
nlu_responses_folder = os.path.join(root_folder, 'nlu_responses') 

file_list = []


for dirpath, dirnames, filenames in os.walk(nlu_responses_folder):
    file_list = filenames

file_name = file_list[0]

list_file = {}
json_data = []

for file_name in file_list:

    with open(os.path.join(nlu_responses_folder, file_name), 'r', encoding='utf-8') as arq:
        texto = arq.read()
    word = re.sub(r'.txt.json$', '', file_name)

    #CALL WATSON NLU
    try:
        nlu_response = json.loads(texto)
    except:
        print("deu erro no " + file_name)

    list_file[word] = nlu_response
   
    pass

    
with open("nlu_dump"  + ".json", 'w') as fp:
    json.dump(list_file, fp,indent=4)




