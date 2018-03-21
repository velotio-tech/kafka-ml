#__author__ = "vaibhawvipul"
from __future__ import division,print_function, absolute_import
from sklearn.datasets import fetch_20newsgroups #built-in dataset 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import pickle
from kafka import KafkaConsumer

#Defining model and training it
categories = ["talk.politics.misc","misc.forsale","rec.motorcycles","comp.sys.mac.hardware","sci.med","talk.religion.misc"] #http://qwone.com/~jason/20Newsgroups/ for reference

def fetch_train_dataset(categories):
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
    return twenty_train

def bag_of_words(categories):
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(fetch_train_dataset(categories).data)
    pickle.dump(count_vect.vocabulary_, open("vocab.pickle", 'wb'))
    return X_train_counts

def tf_idf(categories):
    tf_transformer = TfidfTransformer()
    return (tf_transformer,tf_transformer.fit_transform(bag_of_words(categories)))

def model(categories):
    clf = MultinomialNB().fit(tf_idf(categories)[1], fetch_train_dataset(categories).target)
    return clf

#Uncomment the following lines to re-train the model
#model = model(categories)
#pickle.dump(model,open("model.pickle", 'wb'))
#print("Training Finished!")
#Training Finished Here

#Loading model and vocab
print("Loading pre-trained model")
vocabulary_to_load = pickle.load(open("vocab.pickle", 'rb'))
count_vect = CountVectorizer(vocabulary=vocabulary_to_load)
load_model = pickle.load(open("model.pickle", 'rb'))
#docs_new = ['I love bikes', 'My computer is for sale','I own a mac','I love Hinduism']
#docs_new = [open("test_bike_doc.txt",'r').read(),open("test_med_doc.txt",'r').read(),open("test_mac_doc.txt",'r').read()]
count_vect._validate_vocabulary()
count_vect._validate_vocabulary()
tfidf_transformer = tf_idf(categories)[0]

#predicting the streaming kafka messages
consumer = KafkaConsumer('twitter-stream',bootstrap_servers=['localhost:9092'])

print("Starting ML predictions.")

for message in consumer:
    X_new_counts = count_vect.transform([message.value])

    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    predicted = load_model.predict(X_new_tfidf)
    
    print(message.value+" => "+fetch_train_dataset(categories).target_names[predicted[0]])


