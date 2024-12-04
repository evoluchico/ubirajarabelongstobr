import networkx as nx
import pandas as pd
from operator import itemgetter

def compute_bridging_coefficient(G):
    bridging_coeff = {}
    for node in G:
        neighbors_degrees = [G.degree(neighbor) for neighbor in G.neighbors(node)]
        try:
            bridging_coeff[node] = 1 / sum(1 / deg for deg in neighbors_degrees if deg != 0)
        except ZeroDivisionError:
            bridging_coeff[node] = -1
        
    return bridging_coeff

# 1. Load the edge list
edges = pd.read_csv('User_Edge.csv')
G = nx.from_pandas_edgelist(edges, 'Source', 'Target')

# 2. Load the node ID list (assuming it's just a list of node IDs)
node_ids = pd.read_csv('User_ID.csv')
G.add_nodes_from(node_ids['Id'])

# 3. Compute the top 10 users according to centrality measures
print("calculating degree_centrality")
degree_centrality = nx.degree_centrality(G)
print("calculating betweenness_centrality")
betweenness_centrality = nx.betweenness_centrality(G)
print("calculating eigenvector_centrality")
eigenvector_centrality = nx.eigenvector_centrality(G)
print("calculating bridging_centrality")

bridging_coeff = compute_bridging_coefficient(G)
bridging_centrality = {node: betweenness_centrality[node] * bridging_coeff[node] for node in G}

top_degree = sorted(degree_centrality.items(), key=itemgetter(1), reverse=True)[:10]
top_betweenness = sorted(betweenness_centrality.items(), key=itemgetter(1), reverse=True)[:10]
top_eigenvector = sorted(eigenvector_centrality.items(), key=itemgetter(1), reverse=True)[:10]
top_bridging = sorted(bridging_centrality.items(), key=itemgetter(1), reverse=True)[:10]

print("# Top 10 users by degree centrality:", [user[0] for user in top_degree])
print("# Top 10 users by betweenness centrality:", [user[0] for user in top_betweenness])
print("# Top 10 users by eigenvector centrality:", [user[0] for user in top_eigenvector])
print("# Top 10 users by bridging centrality:", [user[0] for user in top_bridging])

# Top 10 users by degree centrality: [7601, 1286, 9407, 5207, 8965, 1827, 995, 9722, 1796, 5245]
# Top 10 users by betweenness centrality: [7601, 1286, 5207, 9407, 8965, 1796, 1827, 995, 9722, 11107]
# Top 10 users by eigenvector centrality: [7601, 9407, 1796, 1286, 1827, 11107, 995, 7042, 9273, 5245]
# Top 10 users by bridging centrality: [9631, 1721, 395, 1852, 7106, 10252, 10127, 6637, 11982, 8199]

nodeId_to_username = { row['Id']:row['Label'] for _, row in node_ids.iterrows() }

print("# Top 10 users by degree centrality:",      [nodeId_to_username[user[0]] for user in top_degree])
print("# Top 10 users by betweenness centrality:", [nodeId_to_username[user[0]] for user in top_betweenness])
print("# Top 10 users by eigenvector centrality:", [nodeId_to_username[user[0]] for user in top_eigenvector])
print("# Top 10 users by bridging centrality:",    [nodeId_to_username[user[0]] for user in top_bridging])

# Top 10 users by degree centrality: ['alinemghilardi', 'BiodiversidadeB', 'PaleoCisneros', 'mikannn', 'pansybeast', 'oTroianoleo', 'FeliPinheir', 'WryCritic', 'MMarcosaurus', 'ProjetoCiencia']
# Top 10 users by betweenness centrality: ['alinemghilardi', 'BiodiversidadeB', 'mikannn', 'PaleoCisneros', 'pansybeast', 'MMarcosaurus', 'oTroianoleo', 'FeliPinheir', 'WryCritic', 'antoniopedroalb']
# Top 10 users by eigenvector centrality: ['alinemghilardi', 'PaleoCisneros', 'MMarcosaurus', 'BiodiversidadeB', 'oTroianoleo', 'antoniopedroalb', 'FeliPinheir', 'Suspended_User', 'tito_aureliano', 'ProjetoCiencia']
# Top 10 users by bridging centrality: ['Suspended_User', 'bloodyWrst', 'DuroLocus', 'lazabipo', 'D4rkWzd', 'cinamogirl', 'TVManiaco_tvps2', 'whoistaoana', 'nyazkywalker', 'targaryengrrr']

# 4. Community detection using the Louvain method
import community as community_louvain

partition = community_louvain.best_partition(G)

# 5. Print the top 10 users per community
communities = {}
for node, comm_id in partition.items():
    if comm_id not in communities:
        communities[comm_id] = []
    communities[comm_id].append(node)

for comm_id, members in communities.items():
    members_by_degree = sorted(members, key=lambda x: degree_centrality[x], reverse=True)
    members_by_degree = [ nodeId_to_username[i] for i in members_by_degree ]
    print(f"Community {comm_id} top 10 users by degree centrality:", members_by_degree[:10])


Community 0 top 10 users by degree centrality: ['alinemghilardi', 'PlantaSim', 'willibrunow', 'MaximusSpino', 'schrarstzhaupt', 'JoanaOrfao', 'TewBlack', 'SerpInFormes', 'kimim01', 'pedrowisq']
Community 1 top 10 users by degree centrality: ['boringsuchus', 'paleoeddye', 'Suspended_User', 'catalina_leite', 'pilgrimcetus_', 'luizacaires3', 'MatheusKnothe', 'BRodriguesOhana', 'o_weverton', 'MarinesWitzke']
Community 2 top 10 users by degree centrality: ['WryCritic', 'MF_gadelha', 'PPaleoartist', 'DiAmador4', 'JuliotheArtist', 'sadtheropod', 'Suspended_User', '_PaleoGeek_', 'PalaeoVsRacism', 'LionsDenArtwork']
Community 3 top 10 users by degree centrality: ['ProjetoCiencia', 'tito_aureliano', 'dpaulocarvalho', 'kalebmelkor', 'ruzzibarbara', 'Pirulla25', 'bioriderjr', 'RabelloAnderson', 'eosauria', 'paleopirata']
Community 4 top 10 users by degree centrality: ['PaleoCisneros', 'Machado_DSc', 'mauritiantales', 'mathchaos', 'palaeodaniel', 'rpocisv', 'paleoTsimoes', 'PStewens', 'Yara_Haridy', 'RenanBantim']
Community 5 top 10 users by degree centrality: ['Colecionadores2', '_themingau', 'Joseane_sf', 'Albertossauro', 'nishi_kazue', 'tainancia', 'PedroHTunes', 'ArqueoPreHist', 'CoelhoPre', 'nigthstrange']
Community 6 top 10 users by degree centrality: ['FlavianaJorge', 'JornalOGlobo', 'xicosa', 'elis_sntn', 'Suspended_User', 'VenomaniaKou', 'revistapiaui', 'mwk__bw', 'wolverinegeo', 'NatGeo']
Community 7 top 10 users by degree centrality: ['smcarvalho42', 'giordaness', 'GabrielBritozz', 'portsmouthuni', 'Suspended_User', 'sr_kenway', 'ikessauro', 'poeirinhadoalem', 'capetaman', 'pauloal97618063']
Community 8 top 10 users by degree centrality: ['mikannn', 'PrazerCambraia', 'Sybylla_', 'rogandopraga', 'CamaradaHidalgo', '_ohcrab', 'lentevermelha', 'pifalcao', 'DiegoCrux', 'analesnovski']
Community 9 top 10 users by degree centrality: ['oTroianoleo', 'dwnews', 'R0dr1got3', 'paleorocha', 'Camila_18FJ', 'vleonelss', 'mponcci', 'LutzLeo', 'AmbBrasilia', 'dw_brasil']
Community 10 top 10 users by degree centrality: ['antoniopedroalb', 'lucaskias', 'PaleoBlogBR', 'MarcosTeo2', 'marciolcastro', 'pteroana', 'saradrawspaleo', 'Hypnos_art', 'Vinsevla1', 'THSpike']
Community 11 top 10 users by degree centrality: ['FeliPinheir', 'jutyrannus', 'tylerstoneart', 'tupaguerra', 'JersonTatu', 'DimetroDude', 'o_eco', 'almeidacm3', 'victor_debrito', 'allen_pancake']
Community 12 top 10 users by degree centrality: ['DaltonPinheiro1', 'nenel_leonam', 'MeioDeCultura', 'casavoguebrasil', 'MarcusRibeiroM2', 'saturns005', 'Brenin_m_b', 'rosecoloredjoca', 'C4iman15', 'jbubadue']
Community 13 top 10 users by degree centrality: ['MMarcosaurus', 'ValeriaRoman', 'luc14nobio', 'sgufmg', 'rrafaelbio', 'beccarivictor', 'Rafa_paleo', 'ramonsiilvaas', 'iMalvikaGaur', 'TomHoltzPaleo']
Community 14 top 10 users by degree centrality: ['brunobittar91', 'viadescendens', 'fadelandia', 'HaruJiggly', 'ratgroundpear', 'Nido_Quing', 'Lillyywho', 'badwitchmaris', 'subjetividdfeia', 'jinkitopia']
Community 15 top 10 users by degree centrality: ['BiodiversidadeB', 'PerboniRenato', 'MarjorieMbeller', 'Akamezinha', 'galileufanacc', 'LUNAtichenr', 'paulamariane27', 'rozzz_zz', 'folha_ciencia', 'PetraDeQuartzo']
Community 16 top 10 users by degree centrality: ['InsetoLand', 'isisrnd', 'Leo_Tusi', 'ttluao', 'ClelsonFraga', 'brunojose_', 'Luigi0131', 'LyraSid', '_themonie_', 'Bugseelf']
Community 18 top 10 users by degree centrality: ['PesquisaFapesp', 'AllBrPolitics', 'Fenix_glacialis', '2XVIINI', 'LuanMoldanMotta', 'hummyeonbird', 'anai_pari_', 'Rabiaandrea', 'robsongfreire', 'anabee']
Community 19 top 10 users by degree centrality: ['KerberLeonardo', 'PsychoAna_xD', 'PaleoCameron', 'Jorllyrey', 'doralcoelho', 'Suspended_User', 'MosaFabim', 'sasimarie', 'edvardvallek', 'saurianboy']
Community 20 top 10 users by degree centrality: ['fedkukso', 'adagamante', 'HenriqueRandom', 'peregrino0788', 'Suspended_User', 'stephanevw', 'balsedie', 'centaurus_crux', 'barroso2501', 'gustavoburin']
