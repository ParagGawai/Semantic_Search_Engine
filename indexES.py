import json
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import tensorflow as tf
import tensorflow_hub as hub

import warnings
warnings.filterwarnings('ignore') 


# connect to ES on localhost on port 9200
es = Elasticsearch("http://localhost:9200")
if es.ping():
	print('Connected to ES!')
else:
	print('Could not connect!')
	sys.exit()

print("*********************************************************************************")


# creating an index in ES is similar to creating a DB in an RDBMS
# Read each question and index into an index called questions
# Indexing only titles for this example to improve speed. In practice, its good to index CONCATENATE(title+body)
# Define the index


#Refer: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
# Mapping: Structure of the index
# Property/Field: name and type . These are like columns in RDBMS
# it is json
b = {"mappings": {
  	"properties": {
    		"title": {
      			"type": "text"
    		},
    		"title_vector": {
      			"type": "dense_vector",
      			"dims": 512
		}
	}
     }
   }       


ret = es.indices.create(index='questions-index', ignore=400, body=b) #400 caused by IndexAlreadyExistsException, 
# print(json.dumps(ret,indent=4))
print(ret)

# TRY this in browser: http://localhost:9200/questions-index

print("*********************************************************************************")

# sys.exit()

#load USE4 model

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")




# CONSTANTS
NUM_QUESTIONS_INDEXED = 200000   # we will only take 200000 questions and not all the questions just for faster computation


# it is what we saw in readData.py

# the column names of the question csv is as follows
# Col-Names: Id,OwnerUserId,CreationDate,ClosedDate,Score,Title,Body

# elastic search wants the documents format.
# doc_id means unique id for the question taken from row[0] ie id column
# title is the fifth column
cnt=0

with open(r'usr/share/elasticsearch/searchqa/data/Questions.csv', encoding="latin1") as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',' )
	next(readCSV, None)  # skip the headers 
	for row in readCSV:
		#print(row[0], row[5])
		doc_id = row[0]
		title = row[5]
		vec = tf.make_ndarray(tf.make_tensor_proto(embed([title]))).tolist()[0]	# 512 dimensional, floating values	
		
		b = {"title":title,
			"title_vector":vec,
			}	
		# it is nothing but the 512 diemensional vector for the corresponding text
		
		res = es.index(index="questions-index", id=doc_id, body=b)  # id is the unique id, here we are using doc_id as the unique id
		#print(res)
		

		# keep count of # rows processed
		cnt += 1
		if cnt%100==0:
			print(cnt)
		
		if cnt == NUM_QUESTIONS_INDEXED:
			break

	print("Completed indexing....")

	print("*********************************************************************************")
	




