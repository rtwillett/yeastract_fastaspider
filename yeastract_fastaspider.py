import pandas as pd
import requests

def get_sequences(sysname):

    url_gene = f"http://www.yeastract.com/download.php?type=gene&id={sysname}"
    url_promoter = f"http://www.yeastract.com/download.php?type=promoter&id={sysname}"
    url_protein = f"http://www.yeastract.com/download.php?type=aminoacid&id={sysname}"

    print(f"Requesting sequence data for .... {sysname}:")

    gene = FASTA_parser(url_gene)
    promoter = FASTA_parser(url_promoter)
    protein = FASTA_parser(url_protein)

    print(gene)
    print(promoter)
    print(protein)

    print("="*60)

    df_gene = pd.DataFrame([(sysname, gene[2])], columns = ['sysname', 'gene'])
    df_promoter = pd.DataFrame([(sysname, promoter[2])], columns = ['sysname', 'promoter'])
    df_protein = pd.DataFrame([(sysname, protein[2])], columns = ['sysname', 'protein'])

    df_all = df_gene.merge(df_promoter, on='sysname').merge(df_protein, on = 'sysname')
    return df_all

def FASTA_parser(x):
    '''
    Takes the text returned by FASTA_requester() and returns the sysname, protein name and protein sequence for the protein.
    '''

#     fasta = FASTA_requester(x)

    fasta = requests.post(x)

    fasta_split = fasta.text.split("\n")

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
data = pd.read_csv(r'./gene_data_locus.csv')
sysnames = data.loc[data.stdname != 'Uncharacterized'].sysname.tolist()

# Building url and scraping the data from each webpage entry.
seq_data = [get_sequences(s) for s in sysnames]

# prot_data = []
# for g in data:
#     url = f"http://www.yeastract.com/download.php?type=aminoacid&id={g}"
#     d = FASTA_parser(url)
#     prot_data.append(d)
#     print(d)

# Data export into a CSV
df_seq_data = pd.concat(seq_data)
# df = pd.DataFrame(prot_data, columns=['sysname', 'proteinname', 'prot_sequence'])
df_seq_data.to_csv(r"./gene_seq.csv", index=None, header=True)
