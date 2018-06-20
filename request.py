import requests
import json
import os



def call_watson_nlu(text):
    url = 'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-03-16&features=keywords,entities'
    auth = ('2bd08d6f-7010-4d3e-bc36-1fc07af8ce4f', 'LgCXadW4WWvk')
    headers = {'Content-Type' : 'text/plain'}
    body = text
    body = body.encode("utf-8")
    

    r = requests.post(url, auth=auth, headers=headers, data = body )
    obj = json.loads(r.content)
    
    return obj
 
root_folder = os.path.dirname(__file__)

contracts_folder = os.path.join(root_folder, 'DataSet') 
nlu_responses_folder = os.path.join(root_folder, 'nlu_responses') 

file_list = []


for dirpath, dirnames, filenames in os.walk(contracts_folder):
    file_list = filenames

file_name = file_list[0]

for file_name in file_list:

    with open(os.path.join(contracts_folder, file_name), 'r', encoding='utf-8') as arq:
        texto = arq.read()
        resposta_nlu = call_watson_nlu(texto)


    with open(os.path.join(nlu_responses_folder, file_name + ".json"), 'w') as fp:
        json.dump(resposta_nlu, fp, indent=4)
    


