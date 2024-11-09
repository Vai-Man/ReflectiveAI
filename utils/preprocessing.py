import sklearn
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


stop_words = stopwords.words('english') 
# better file handling needed
with open('utils/data.pkl', 'rb') as f:
    data = pickle.load(f)

def preprocess(inp):
    inp = inp.lower()
    inp = inp.replace(r'[^\w\s]+', '')
    inp = [word for word in inp.split() if word not in (stop_words)]

    ps = PorterStemmer()
    inp = ' '.join([ps.stem(i) for i in inp])
    inputToModel = data.transform([inp]).toarray()
    return inputToModel