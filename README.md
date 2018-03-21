# Bag of Words and tf-idf implementation in scikit-learn   

This project is a simple implementation of bag of words and tf-idf. It does document classification using the following dataset -
### [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/)

##  Categories for classification

1. talk.politics.misc
2. misc.forsale
3. rec.motorcycles
4. comp.sys.mac.hardware
5. sci.med
6. talk.religion.misc

## Requirements - 

1. scikit-learn
2. pickle
3. Kafka

## Install Kafka

1. `wget http://www-us.apache.org/dist/kafka/1.0.0/kafka_2.11-1.0.0.tgz`
2. `tar -xvf kafka_2.11-1.0.0.tgz`

## Test Documents -

1. [test_bike_doc.txt](https://auto.ndtv.com/news/hero-electric-unveils-two-new-e-bikes-and-a-new-e-scoter-in-india-1807728)
2. [test_med_doc.txt](https://med.stanford.edu/news/all-news/2018/01/cancer-vaccine-eliminates-tumors-in-mice.html)
3. [test_mac_doc.txt](https://techcrunch.com/2018/01/31/apple-could-let-you-run-ipad-apps-on-your-mac/)

## How to run the project - 

Start Kafka

1. `bin/zookeeper-server-start.sh config/zookeeper.properties`
2. `bin/kafka-server-start.sh config/server.properties`
3. `bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic velotio`

Start kafka producer
4. `python twitter_kafka_prodcer.py`

Start message classifier
5. `python doc_classifier.py`

## Understanding the output -

"message" => category

### NOTE - This project is under development. Help it grow by opening issues and pull requests! :) 
