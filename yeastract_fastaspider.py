import pandas as pd
import requests

def FASTA_requester(u):
    url = requests.post(u)
    return url.text

def FASTA_parser(x):

    fasta = FASTA_requester(x)

    fasta_split = fasta.split("\n")

    if fasta_split[1].startswith(">"):
        del fasta_split[0]

    names = fasta_split[0].replace(">", "").split()

    try:
        sysname = names[0]
    except:
        sysname = " "

    try:
        protname = names[1]
    except:
        protname = " "

    try:
        protein = "".join(fasta_split[1:])
    except:
        protein = " "

    return (sysname, protname, protein)

data = pd.read_csv("gene_data.csv", usecols=["proteinname"])

data = data["proteinname"].tolist()

prot_data = [] #
for g in data:
    url = f"http://www.yeastract.com/download.php?type=aminoacid&id={g}"
    d = FASTA_parser(url)
    prot_data.append(d)
    print(d)

df = pd.DataFrame(prot_data, columns=['sysname', 'proteinname', 'prot_sequence'])

df.to_csv(r"/Users/willettr/NYCDSA/scrapy/yeastract/gene_seq.csv", index=None, header=True)
