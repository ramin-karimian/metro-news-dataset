import numpy as np
import pandas as pd
from utils import *
import os

def pfcm(data, c, expo=2, max_iter=1000, min_impro=0.005, a=1, b=4, nc=3):
    """
    <h3>Possiblistic Fuzzy C-Means Clustering Algorithm</h3>
    <b>Parameters :</b><ul>
    <li><u>data</u>: Dataset to be clustered, with size M-by-N,
    where M is the number of data points
    and N is the number of coordinates for each data point.</li>
    <li><u>c</u> : Number of clusters</li>
    <li><u>expo</u> : exponent for the U matrix (default = 2)</li>
    <li><u>max_iter</u> : Maximum number of iterations (default = 1000)</li>
    <li><u>min_impor</u> : Minimum amount of imporvement (default = 0.005)</li>
    <li><u>a</u> : User-defined constant a (default = 1)</li>
    <li><u>b</u> : User-defined constant b that should be
    greater than a (default = 4)</li>
    <li><u>nc</u> : User-defined constant nc (default = 2)</li>
    </ul>
    The clustering process stops when the maximum number of iterations is
    reached, or when objective function improvement or the maximum centers
    imporvement between two consecutive iterations is less
     than the minimum amount specified.<br><br>
    <b>Return values :</b><ul>
    <li><u>cntr</u> : The clusters centers</li>
    <li><u>U</u> : The C-Partionned Matrix (used in FCM)</li>
    <li><u>T</u> : The Typicality Matrix (used in PCM)</li>
    <li><u>obj_fcn</u> : The objective function for U and T</li>
    </ul>
    """
    obj_fcn = np.zeros(shape=(max_iter, 1))
    ni = np.zeros(shape=(c, data.shape[0]))
    U = initf(c, data.shape[0])
    T = initf(c, data.shape[0])
    cntr = np.random.uniform(low=np.min(data), high=np.max(data), size=(
        c, data.shape[1]))
    for i in range(max_iter):
        current_cntr = cntr
        U, T, cntr, obj_fcn[i], ni = pstepfcm(
                data, cntr, U, T, expo, a, b, nc, ni)
        if i > 1:
            if abs(obj_fcn[i] - obj_fcn[i-1]) < min_impro:
                break
            elif np.max(abs(cntr - current_cntr)) < min_impro:
                break
    return cntr, U, T, obj_fcn


def pstepfcm(data, cntr, U, T, expo, a, b, nc, ni):
    mf = np.power(U, expo)
    tf = np.power(T, nc)
    tfo = np.power((1-T), nc)
    cntr = (np.dot(a*mf+b*tf, data).T/np.sum(
        a*mf+b*tf, axis=1).T).T
    dist = pdistfcm(cntr, data)
    obj_fcn = np.sum(np.sum(np.power(dist, 2)*(a*mf+b*tf), axis=0)) + np.sum(
        ni*np.sum(tfo, axis=0))
    ni = mf*np.power(dist, 2)/(np.sum(mf, axis=0))
    tmp = np.power(dist, (-2/(nc-1)))
    U = tmp/(np.sum(tmp, axis=0))
    tmpt = np.power((b/ni)*np.power(dist, 2), (1/(nc-1)))
    T = 1/(1+tmpt)
    return U, T, cntr, obj_fcn, ni


def initf(c, data_n):
    A = np.random.random(size=(c, data_n))
    col_sum = np.sum(A, axis=0)
    return A/col_sum


def pdistfcm(cntr, data):
    out = np.zeros(shape=(cntr.shape[0], data.shape[0]))
    for k in range(cntr.shape[0]):
        out[k] = np.sqrt(np.sum((np.power(data-cntr[k], 2)).T, axis=0))
    return out


def pfcm_predict(data, cntr, expo=2, a=1, b=4, nc=3):
    """
    <h3>Possiblistic Fuzzy C-Means Clustering Prediction Algorithm</h3>
    <b>Parameters :</b><ul>
    <li><u>data</u>: Dataset to be clustered, with size M-by-N,
    where M is the number of data points
    and N is the number of coordinates for each data point.</li>
    <li><u>cntr</u> : centers of the dataset previoulsy calculated</li>
    <li><u>expo</u> : exponent for the U matrix (default = 2)</li>
    <li><u>a</u> : User-defined constant a (default = 1)</li>
    <li><u>b</u> : User-defined constant b that should be
    greater than a (default = 4)</li>
    <li><u>nc</u> : User-defined constant nc (default = 2)</li>
    </ul>
    The algortihm predicts which clusters the new dataset belongs to<br><br>
    <b>Return values :</b><ul>
    <li><u>new_cntr</u> : The new clusters centers</li>
    <li><u>U</u> : The C-Partionned Matrix (used in FCM)</li>
    <li><u>T</u> : The Typicality Matrix (used in PCM)</li>
    <li><u>obj_fcn</u> : The objective function for U and T</li>
    </ul>
    """
    dist = pdistfcm(cntr, data)
    tmp = np.power(dist, (-2/(nc-1)))
    U = tmp/(np.sum(tmp, axis=0))
    mf = np.power(U, expo)
    ni = mf*np.power(dist, 2)/(np.sum(mf, axis=0))
    tmpt = np.power((b/ni)*np.power(dist, 2), (1/(nc-1)))
    T = 1/(1+tmpt)
    tf = np.power(T, nc)
    tfo = np.power((1-T), nc)
    new_cntr = (np.dot(a*mf+b*tf, data).T/np.sum(
        a*mf+b*tf, axis=1).T).T
    obj_fcn = np.sum(np.sum(np.power(dist, 2)*(a*mf+b*tf), axis=0)) + np.sum(
        ni*np.sum(tfo, axis=0))
    return new_cntr, U, T, obj_fcn



if __name__=="__main__":
    oneOrTotal = ["one_article","total","total_one_article"][1]


    modelName = f"WNTM_V15_30"
    if modelName not in os.listdir(f'models'): os.mkdir(f'models/{modelName}')
    if oneOrTotal not in os.listdir(f'models/{modelName}'): os.mkdir(f'models/{modelName}/{oneOrTotal}')
    datapath = f"C:/Users/RAKA/Documents/NLP/topic modeling/STTM-master_java/report/(4._.2020)/report.pkl"

    # data, df_total = load(datapath,extention = "topics",article=oneOrTotal)[0]
    total_df = load_data(datapath)
    for i in range(len(total_df)-1,-1,-1):
        if total_df[f"topical_rep_{modelName}"][i] == None:
            # print(i)
            total_df = total_df.drop(index = i)
    # data = np.array(total_df[f"topical_rep_{modelName}"])
    data = np.array([x for x in total_df[f"topical_rep_{modelName}"]])


    # cf=[2,3,4,5,7,8,10,12,15]
    cf=[10]
    df = pd.DataFrame(columns=cf)
    df[cf[0]] = [None]*max(cf)

    # writer = pd.ExcelWriter(f'models/{modelName}/results.xlsx',
    #                         engine='xlsxwriter')
    for c in cf:
        print(c)
        confiq={"n_clusters":c}
        # datapath=f"models/{modelName}/{modelName}.pkl"
        cntr, U, T, obj_fcn = pfcm(data, c, expo=2, max_iter=1000, min_impro=0.005, a=1, b=4, nc=3)
        # res,df,df_total= model(confiq,df,data,df_total)
        # output_results(writer,c,df)

    # df.to_excel(f'models/{modelName}/{oneOrTotal}/{modelName}_multi_clustring_results.xlsx')
    # save_data(f'models/{modelName}/{oneOrTotal}/{modelName}.pkl',df_total)
    # df_total.to_csv(f'models/{modelName}/{oneOrTotal}/{modelName}.csv')
