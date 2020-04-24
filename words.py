import pandas as pd
import numpy as np
import networkx as nx
from utils import *


def extract_words(data):
    words = pd.Series()
    for i in range(len(data)):
        check_print(i)
        for j in range(len(data[i])):
            if data[i][j] not in words.keys(): words.loc[data[i][j]] = 1
            else:  words.loc[data[i][j]] = words.loc[data[i][j]] + 1
    return words

def extract_edges_and_words(data):
    edges_dict = {}
    # words_dict = {}
    words_dict = pd.Series()
    g = nx.Graph()
    for i in range(len(data)):
        check_print(i)
        for j in range(len(data[i])):
            # if data[i][j] in tags:
            if data[i][j] not in words_dict.keys(): words_dict.loc[data[i][j]] = 1
            else:  words_dict.loc[data[i][j]] = words_dict.loc[data[i][j]] + 1
            # if data[i][j] not in words_dict: words_dict[data[i][j]] = 1
            # else:  words_dict[data[i][j]] = words_dict[data[i][j]] + 1

            for k in range(len(data[i])):
                if j == k:continue
                # if data[i][k] in tags:

                if f"{data[i][j]}__{data[i][k]}" in edges_dict.keys():
                    edges_dict[f"{data[i][j]}__{data[i][k]}"] = edges_dict[f"{data[i][j]}__{data[i][k]}"] + 1
                    g[data[i][j]][data[i][k]]['count'] = g[data[i][j]][data[i][k]]['count'] +1
                elif f"{data[i][k]}__{data[i][j]}" in edges_dict.keys():
                    edges_dict[f"{data[i][k]}__{data[i][j]}"] = edges_dict[f"{data[i][k]}__{data[i][j]}"] + 1
                    g[data[i][k]][data[i][j]]['count'] = g[data[i][k]][data[i][j]]['count'] +1
                else:
                    edges_dict[f"{data[i][j]}__{data[i][k]}"] = 1
                    g.add_edge(data[i][j],data[i][k],count = 1)

    return edges_dict , words_dict , g

def create_edgeist(d):
    df = pd.DataFrame(columns=['node1','node2','count'])
    i=0
    for k,v in d.items():
        check_print(i)
        i = i + 1
        ks = k.split("__")
        df.loc[len(df)] = [ks[0],ks[1],v]
    return df


if __name__=="__main__":
    # tagspath =f"data/source_data/Top 300 words.xlsx"
    data_version = f"V04"
    # datapath = f"data/output_data/total/{data_version}/preprocessed_data_{data_version}_(polarity_added)_total.pkl"
    datapath = f"data/output_data/total/{data_version}/preprocessed_data_{data_version}_total.pkl"
    wordsist_savepath = f"data/output_data/total/{data_version}/wordsist_{data_version}.xlsx"
    edgeist_savepath = f"data/output_data/total/{data_version}/words_edgeist_{data_version}.xlsx"
    g_savepath = f"data/output_data/total/{data_version}/words_network_{data_version}.gexf"

    # tags_df = pd.read_excel(tagspath)
    # tags = tags_df['WORD'].values

    data = load_data(datapath)
    tokens = data['tokens'].values

    # dic , g = extract_edges(tokens)
    words_dict = extract_words(tokens)
    # edges_dict , words_dict , g = extract_edges_and_words(tokens)
    # df = create_edgeist(edges_dict)
    # df.to_excel(edgeist_savepath)
    words_dict.to_excel(wordsist_savepath)
    # nx.write_gexf(g,g_savepath)


