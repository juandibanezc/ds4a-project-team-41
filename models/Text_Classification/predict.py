import unidecode
import pickle
import re

"""
This function classifies the PQRS according to its topic into 3 major categories: Peticion, Solicitud and QRD (which stands for Quejas, reclamos and denuncias)
The function applies preliminary data cleaning and formatting and then transform the data using vectorization.
The resulting vector is feed into the model which is based on the Multinomial Naive Bayes Classifier.
    Input: an string containig the topic of the PQR
    
    Output: it returns the kind of requirement which can fall into the following categories: Peticion, Solicitud and QRD
"""

vect = pickle.load(open("vector.pkl","rb"))
model = pickle.load(open("naive_bayes.pkl","rb"))

def predict_request_kind(s, model = model, vectorizer = vect):
    s = re.sub('[^\w\s]','',unidecode.unidecode(s)).lower()
    s = [re.sub('[0123456789]','',s)]
    return print(model.predict(vect.transform(s)))
