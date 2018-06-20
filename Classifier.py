import pandas as pd
import requests
import json
import math
import numpy as np
import re


df = pd.read_csv("out.csv")
with open("nlu_dump.json", 'r', encoding='utf-8') as arq:
    nlu_dump = arq.read()  
    nlu_dump = json.loads(nlu_dump)     


def call_watson_nlu(text):
    url = 'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-03-16&features=keywords,entities'
    auth = ('2bd08d6f-7010-4d3e-bc36-1fc07af8ce4f', 'LgCXadW4WWvk')
    headers = {'Content-Type' : 'text/plain'}
    body = text
    body = body.encode("utf-8")
    
    r = requests.post(url, auth=auth, headers=headers, data = body )
    obj = json.loads(r.content)
    
    return obj
   

text = "IBM is an American multinational technology company headquartered in Armonk, New York, United States, with operations in over 170 countries."

company_black_list = ['International Business Machines Corporation','IBM', 'Batch Management' ,'IBM Company', 'IBM Services', 'IBM Machines',
    'IBM Products and Services', 'SOW', 'Relocation Services', 'International Business Machines', 'Services','Customer',
    'The Cloud Service','IBM Corporation', 'IBM Confidential', 'MRC', 
    'PBL', 'Reinstallation Services', 'ITD', 'Guardium Steady State Operations', 'PBL TCV', 'Project Management Services', 
    'Range Motion Detector', 'Guardium', 'IBM Security Services', 'TCV', 'Lessor', 'IBM Business Partners', 'Global Agreement',
    'Chalan Santo Papa St', 'Mainframe Services', 'IBM Security Guardium', 'IBM Global Services', 'Disco-Certify-Reinstall Services',
    'theft', 'Physical Planning Services', '$200.000', 'Business Partners', 'BANA', 'Supply Chain Management Signature',
    'IBM Consultants', 'WW Transactional', 'IBM Security Operations Center', 'IBM Subcontractor', 'lelliott@bankofguam.com', 'Materials IBM',
    'Equipment Modification Services', 'Decommission Services', 'Brocade','IMI Steady State MRC', 'Early Adopter Program',
    'IBM PMR', 'METRA', 'IBM GTS', 'WW Accounting', 'TSS', 'Cloud Management', 'ATA Confidential', 'Project Management',
    'Designated Location', 'Brocade Support', 'AECI', '$200.00', 'tmarshal@us.ibm.com', 'zOS Cloud Complex', 'WW Accounting', 'RACI', 'Recovery Management',
    'LPARs', 'Texas Government', '30 days', 'Total Capital', 'SBC', 'PTI', 'IMI Steady State MRC Total', 'Mac', 'CSD','IBM Consolidated Capital', 'IBM Network Management Services',
    'Edge Delivery Services', 'Brocade Supplemental Support', 'IBM Global Technology Services', 'cagena Support', 'IMI', 'Ion Services', '#', 'Client']


type_white_list = ["Company", "Facility", "Organization"]

def get_client_name(file_name):
    
    # text = file.read()
    nlu_response = nlu_dump[file_name]
    # return entity with max relevance
    for entity in nlu_response["entities"]:

        match = re.search(r"IBM", entity["text"])
        if match != None:
            print("Found IBM Related stuff: {0}".format(match))
            continue
        if entity["type"] not in type_white_list:
            print("Type is " + entity["type"] + " continuing...")
            continue
        if entity["text"] in company_black_list:
            print("Entity is " + entity["text"] + " continuing...")
            continue
        
        else: 
            print("Found client: {0} Type is {1}".format(entity["text"], entity["type"]))
            
            print('\n')
            return entity["text"]

gts_non_so_file_names = df.loc[df["Tipo"] == "GTS non-SO"]["Name"].tolist()

column_index = df.columns.get_loc("nlu_client_name")

for file_name in gts_non_so_file_names:

    row_index = df.index[df["Name"] == file_name][0]

    item = df.iloc[row_index,column_index]

    if np.isnan(item) == False:
    # and len(item) != 0:
        print("exists: " + item + "")
        continue

    client_name = get_client_name(file_name)

    row_index = df.index[df["Name"] == file_name]
    column_index = df.columns.get_loc("nlu_client_name")
    df.iloc[row_index,column_index] = client_name
    df.to_csv('out2.csv', index=False, encoding="utf-8")

vp = 0
vn = 0
fn = 0
fp = 0
vp_2 = 0

df["Client Name"] = df["Client Name"].fillna("0")
df["nlu_client_name"] = df["nlu_client_name"].fillna("0")

for index, row in df[2:104].iterrows():
    # Verdadeiro Positivo: quando falo que tem, e o NLU encontra igual
    if row["Client Name"] == row["nlu_client_name"]:
        vp = vp + 1
    # Falso positivo: quando falo que nao tem, e o NLU diz que tem
    elif row["Client Name"] == "0" and row["nlu_client_name"] != "0":
        fp = fp + 1
    # False negativo: quando falo que tem, e o NLU diz que nao tem
    elif row["Client Name"] != "0" and row["nlu_client_name"] == "0":
        fn = fn + 1
    elif row["nlu_client_name"] in row["Client Name"]:
        vp_2 = vp_2 + 1
    # Verdadeiro negativo: quando eu falo que tem, e o NLU diz outro nome (erro)
    elif row["Client Name"] != row["nlu_client_name"]:
        vn = vn + 1

print("vp ", vp)
print("vn ", vn)
print("fp ", fp)
print("fn ", fn)
print("vp_2 ", vp_2)

# accuracy = "vp" + "vn" / "vp" + "vn" + "fp" + "fn"
# def acc(client_name):
#     accuracy = get_client_name(file_name)

#     print(accuracy)
