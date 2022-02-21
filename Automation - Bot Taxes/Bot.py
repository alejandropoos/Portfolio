from numpy import string_
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB

import pandas as pd
import pickle


def tokenize(sentence):
  tokens=[]  # Declaramos un array tokens

  for i in range(len(sentence)):
    tokens.append(sentence[i]) 
  return tokens

def bot(sentences,classNb,Tv):
    text1 = sentences
    
    
    examples = [
        text1
    ]
 
    examples_X = Tv.transform(examples)
    # print(Tv.get_feature_names())
   
    predict = classNb.predict(examples_X)
 
    result = []
    for text, label in zip(sentences, predict):
       result ={
           
           label:sentences
                
        }
    return result  


def main():
    Data = pd.read_csv(r"./datasetnotas.csv", error_bad_lines=False)
    Data.applymap(str)


    train_text, test_text, train_labels, test_labels = train_test_split(Data["Campo"].astype(str),
                                                                    Data["Etiqueta"],
                                                                    random_state=85)
    
    
    Tv = TfidfVectorizer( min_df= 20, max_features=12242, strip_accents='unicode',analyzer='char',ngram_range=(1,16), tokenizer=tokenize)
    train_X = Tv.fit_transform(train_text).toarray()
    X_test = Tv.transform(test_text).toarray()

    train_X.shape
    
    classNb = MultinomialNB()
    classNb.fit(train_X, train_labels)
    
    
    predictionNB = classNb.predict(X_test)
 
    
    accuracyNB = accuracy_score(test_labels, predictionNB)
    print(f"Accuracy NB: {accuracyNB:.4%}")
    
    filenameTV = 'finalized_TVD.sav'
    
    pickle.dump(Tv, open(filenameTV, 'wb'))
    filename = 'finalized_ClassNBD.sav'
    
    pickle.dump(classNb, open(filename, 'wb'))

if __name__ == "__main__":
   main() 
