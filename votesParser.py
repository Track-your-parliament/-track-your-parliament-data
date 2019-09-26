import pandas as pd
import time

PATH_DIST = './data/SaliDBAanestysJakauma_result.csv'
PATH_VOTES = './data/SaliDBAanestys_result.csv'

dataVotesDist = pd.read_csv(
    PATH_DIST,
    delimiter=';', 
    dtype={'AanestysId': int, 'Ryhma': str, 'Jaa': int, 'Ei': int, 'Tyhjia': int, 'Poissa': int, 'Yhteensa': int, 'Tyyppi': str})
dataVoteInfos = pd.read_csv(
    PATH_VOTES, 
    delimiter=';', 
    dtype={'AanestysId': int, 'IstuntoVPVuosi': int, 'IstuntoPvm': str, 'AanestysMitatoity': int, 'KohtaKasittelyVaihe': str, 'AanestysValtiopaivaasia': str })

# Filter rows
filteredVoteInfos = dataVoteInfos[(
    dataVoteInfos.KieliId == 1) & (dataVoteInfos.IstuntoVPVuosi >= 2015) & (dataVoteInfos.AanestysValtiopaivaasia.str.startswith('HE'))]
filteredVotesDist = dataVotesDist[(dataVotesDist.Tyyppi == 'eduskuntaryhma') | (
    dataVotesDist.Tyyppi == 'hallitusoppositio')]

# Drop useless columns
filteredVoteInfos = filteredVoteInfos.drop(dataVoteInfos.columns.difference(
    ['AanestysId', 'IstuntoVPVuosi', 'IstuntoPvm', 'AanestysMitatoity', 'KohtaKasittelyVaihe', 'AanestysValtiopaivaasia']), axis=1)
filteredVotesDist = filteredVotesDist.drop(columns=['JakaumaId', 'Imported'])

# Filter rows from the first voting of the year 2015
filteredVotesDist = filteredVotesDist[filteredVotesDist.AanestysId >= 36087]

# Every other votingId refers to the previous voting på svenska
#print(filteredVotesDist[filteredVotesDist.AanestysId == 36088])

# Join the two tables with merge, remove rows with NaNs.
joined = filteredVotesDist.merge(filteredVoteInfos, how='left', on='AanestysId')
joined = joined.dropna(axis=0)
joined = joined[(joined.KohtaKasittelyVaihe == 'Ainoa käsittely') | (joined.KohtaKasittelyVaihe == 'Toinen käsittely')]

# Save file with timestamp
timestr = time.strftime("%Y%m%d_%H%M%S")
joined.to_csv(f"./data/{timestr}_voting_info.csv", sep=";")