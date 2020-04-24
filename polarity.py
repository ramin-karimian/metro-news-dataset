from utils import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

data_version = "V02"
datapath=f"data/output_data/preprocessed_data_tagged_{data_version}.pkl"
df = load_data(datapath)

if __name__=="__main__":
    sentiment=SentimentIntensityAnalyzer()
    df["total_compound_polarity"]=None
    df["pos_polarity"]=None
    df["neg_polarity"]=None
    df["neu_polarity"]=None
    for i in range(len(df)):
        score=sentiment.polarity_scores(" ".join(df["tokens"][i]))
        df["neg_polarity"][i],df["neu_polarity"][i], df["pos_polarity"][i],df["total_compound_polarity"][i]= score.values()
    # df["polarity"] = df["tokens"].apply(lambda x: sentiment.polarity_scores(" ".join(x)))
    df.to_excel(f"data/output_data/preprocessed_data_tagged_{data_version}_(polarity_added).xlsx")
    save_data(f"data/output_data/preprocessed_data_tagged_{data_version}_(polarity_added).pkl",df)

