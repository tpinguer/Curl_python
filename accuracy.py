import pandas as pd
pd.set_option('display.max_colwidth', 1000)
df = pd.read_csv("out2.csv")

vp = 0
vn = 0
fn = 0
fp = 0
vp_2 = 0

df["Client Name"] = df["Client Name"].fillna("0")
df["nlu_client_name"] = df["nlu_client_name"].fillna("0")

file = pd.DataFrame()
file['Client Name'] = df["Client Name"]
file['nlu_client_name'] = df["nlu_client_name"]
file.to_csv("valid.csv")

for index, row in df[2:104].iterrows():

    # Verdadeiro Positivo: quando falo que tem, e o NLU encontra igual
    if row["Client Name"] == row["nlu_client_name"]:
        vp = vp + 1
    # Falso positivo: quando falo que nao tem, e o NLU diz que tem
    elif row["Client Name"] == "0" and row["nlu_client_name"] != "0":
        fp = fp + 1

        print("False Positive on file {0}\n".format(row["Name"]))
        print("Actual: {1}\nExpected: {0}\n".format(row["Client Name"], row["nlu_client_name"]))

    # False negativo: quando falo que tem, e o NLU diz que nao tem
    elif row["Client Name"] != "0" and row["nlu_client_name"] == "0":
        fn = fn + 1

        print("False Negative on file {0}\n".format(row["Name"]))
        print("Actual: {1}\nExpected: {0}\n".format(row["Client Name"], row["nlu_client_name"]))

    elif row["nlu_client_name"] in row["Client Name"]:
        vp = vp + 1
    # Verdadeiro negativo: quando eu falo que tem, e o NLU diz outro nome (erro)
    elif row["Client Name"] != row["nlu_client_name"]:
        vn = vn + 1

print("vp ", vp)
print("vn ", vn)
print("fp ", fp)
print("fn ", fn)

def accuracy(vp, vn, fn, fp):
     acc = (vp + vn) / (vp + vn + fp + fn)
     return acc

accuracy = accuracy(vp, vn, fn, fp)
print("Accuracy: {0}".format(accuracy))