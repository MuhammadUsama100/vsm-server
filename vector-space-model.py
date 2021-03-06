import math
import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle
from nltk.stem import PorterStemmer
import copy


array: list = []
for i in range(1, 51):
    file1 = open(
        "G:/University/SEMESTER/SIXSEMESTER/IR/assignment/ass2/ShortStories/" + str(i) + ".txt", 'r',  encoding='utf8')
    Lines = file1.readlines()
    array.append(Lines)

file2 = open(
    "G:/University/SEMESTER/SIXSEMESTER/IR/assignment/ass2/stopwords.txt", 'r',  encoding='utf8')
lines = file2.readlines()
# creating a list of stop word each word is strip before adding to stop word list
stopwords = []

for i in lines:
    if(i.rstrip("\n") != ""):
        stopwords.append(i.rstrip("\n").strip())
print(stopwords)


lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
# breaking the value to tokens


def preprocessing(sentence):
    sentence = sentence.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    # tokens = nltk.word_tokenize(sentence)
    tokens = tokenizer.tokenize(sentence)
    lema_tokens = []
    for token in tokens:
        lema_tokens.append(lemmatizer.lemmatize(token))
    filtered_tokens = [word for word in lema_tokens if not word in stopwords]
    return filtered_tokens


processed_array: list = []
for doc in array:
    processed_doc: list = []
    for lines in doc:
        processed_doc.extend(preprocessing(lines))
    processed_doc.sort()
    processed_array.append(processed_doc)

# print(len(processed_array))

# calculating tf score
term_frequency_matrix: dict = {}

for doc_number in range(0, 50):
    term_frequency_matrix[doc_number]: dict = {}
    term_count_initialize: dict = {}
    for doc in processed_array:
        for term in doc:
            if term not in term_count_initialize:
                term_count_initialize[term] = 0
    term_frequency_matrix[doc_number] = term_count_initialize


for doc_number in range(0, len(processed_array)):
    for term in processed_array[doc_number]:
        if term in term_frequency_matrix[doc_number]:
            term_frequency_matrix[doc_number][term] = term_frequency_matrix[doc_number][term] + 1

# TF = log(1 + tf)
# for doc_number in term_frequency_matrix:
#     for term in term_frequency_matrix[doc_number]:
#         term_frequency_matrix[doc_number][term] = math.log10(
#             1 + term_frequency_matrix[doc_number][term])

#TF = 1 + ln(tf)
# for doc_number in term_frequency_matrix:
#     for term in term_frequency_matrix[doc_number]:
#         term_frequency_matrix[doc_number][term] = 1 + (0 if term_frequency_matrix[doc_number][term] == 0 else math.log10(
#             term_frequency_matrix[doc_number][term]))

# TF = 0.5 + 0.5*log(tf)/max(tf)
# max_val = -1
# for doc_number in term_frequency_matrix:
#     for term in term_frequency_matrix[doc_number]:
#         if term_frequency_matrix[doc_number][term] > max_val:
#             max_val = term_frequency_matrix[doc_number][term]
#     for term in term_frequency_matrix[doc_number]:
#         term_frequency_matrix[doc_number][term] = 0.5 + ((
#             0.5*term_frequency_matrix[doc_number][term])/max_val)
#     max_val = -1

# calculating idf score
inverse_doc_frequency: dict = {}
for doc in processed_array:
    for term in doc:
        if term not in inverse_doc_frequency:
            inverse_doc_frequency[term] = 0


for doc in processed_array:
    for term in inverse_doc_frequency:
        if term in doc:
            inverse_doc_frequency[term] = inverse_doc_frequency[term] + 1

# formula for idf  =  log(df)/N
for term in inverse_doc_frequency:
    inverse_doc_frequency[term] = math.log10(inverse_doc_frequency[term])/50


# calculating tf-idf formula = tf * idf calculated above

tf_idf_matrix: dict = copy.deepcopy(term_frequency_matrix)

for doc_number in tf_idf_matrix:
    for term in inverse_doc_frequency:
        if term in tf_idf_matrix[doc_number]:
            tf_idf_matrix[doc_number][term] = tf_idf_matrix[doc_number][term] * \
                inverse_doc_frequency[term]

# calculate angle between query and doc
# normalize length of the matrix
for doc_number in tf_idf_matrix:
    length_doc: list = []
    for term in tf_idf_matrix[doc_number]:
        length_doc.append(
            tf_idf_matrix[doc_number][term] * tf_idf_matrix[doc_number][term])
    for term in tf_idf_matrix[doc_number]:
        tf_idf_matrix[doc_number][term] = tf_idf_matrix[doc_number][term] / \
            math.sqrt(sum(length_doc))

# print(tf_idf_matrix)
f = open("tf.txt", "w")
f.write(str(term_frequency_matrix))
f.close()

f = open("idf.txt", "w")
f.write(str(inverse_doc_frequency))
f.close()

f = open("tfidf-matrix.txt", "w")
f.write(str(tf_idf_matrix))
f.close()

with open('tfidf-matrx.p', 'wb') as fp:
    pickle.dump(tf_idf_matrix, fp, protocol=pickle.HIGHEST_PROTOCOL)

with open('doc-dictionary.p', 'wb') as fp:
    pickle.dump(processed_array, fp, protocol=pickle.HIGHEST_PROTOCOL)

with open('inverse-doc.p', 'wb') as fp:
    pickle.dump(inverse_doc_frequency, fp, protocol=pickle.HIGHEST_PROTOCOL)
