import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import unidecode
import re

# Read in the data
df = pd.read_csv("Modulo_PQR_Sector_Salud_V3.csv",encoding='latin-1', sep =";")
new_cat = {1.0:"Peticion", 2.0:"Queja", 3.0:"Reclamo", 4.0:"Solicitud", 5.0:"Denuncia"}
# Drop all Na values
df = df[["pqr_tipo_solicitud_id","asunto"]].dropna()
# Drop category 6.0
df = df[df["pqr_tipo_solicitud_id"].isin([1.0,2.0,3.0,4.0,5.0])]
# Changing the variable to categorical
df["pqr_tipo_solicitud_id"] = df["pqr_tipo_solicitud_id"].astype("category").replace(new_cat)

# Striping the punctuacion symbols
df["asunto"] = df["asunto"].astype("string").str.replace(r'[^\w\s]','')
# Removing numbers
df["asunto"] = df["asunto"].astype("string").str.replace(r'[0123456789]','')
df["asunto"] = df["asunto"].str.lower()
df.drop_duplicates(subset = ["asunto"], inplace = True)

# Striping the accents of words
df["asunto"] = df.apply(lambda x : unidecode.unidecode(x.asunto), axis = 1)

#loading list with stopwords in Spanish
stop = pd.read_csv("stop_words_spanish.txt", header = None, names = ["words"])
stop = stop["words"].values.tolist()

cat_tra = {"Denuncia":"QRD", "Queja":"QRD", "Reclamo":"QRD"}
df["pqr_tipo_solicitud_id"] = df["pqr_tipo_solicitud_id"].replace(cat_tra)

#--------------Data Modelling-----------------------------------------------------------

#Split into test and training set
df_train =  df.sample(frac = 0.9, random_state = 10)
df_test = df.drop(df_train.index)

#Vectorizing the variable asunto
vect = TfidfVectorizer(stop_words = stop, max_df = 0.8, min_df = 3, ngram_range = (1,2))
V = vect.fit_transform(df_train["asunto"])


# Fitting the model
model = MultinomialNB()
model.fit(V, df_train["pqr_tipo_solicitud_id"])


pickle.dump(model, open("naive_bayes.pkl","wb"))
pickle.dump(vect, open("vector.pkl","wb"))