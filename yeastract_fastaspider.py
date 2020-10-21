import pandas as pd
import requests

def FASTA_requester(u):
    '''
    Extracts and returns the text from within the txt file the target URL.
    '''
    url = requests.post(u)
    return url.text

def FASTA_parser(x):
    '''
    Takes the text returned by FASTA_requester() and returns the sysname, protein name and protein sequence for the protein.
    '''

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

# Extracting the list of protein names from a CSV file for which to scrape the entries.
data = pd.read_csv("gene_data.csv", usecols=["proteinname"])
data = data["proteinname"].tolist()

# Building url and scraping the data from each webpage entry.
prot_data = []
for g in data:
    url = f"http://www.yeastract.com/download.php?type=aminoacid&id={g}"
    d = FASTA_parser(url)
    prot_data.append(d)
    print(d)

# Data export into a CSV
df = pd.DataFrame(prot_data, columns=['sysname', 'proteinname', 'prot_sequence'])
df.to_csv(r"/Users/willettr/NYCDSA/scrapy/yeastract/gene_seq2.csv", index=None, header=True)
