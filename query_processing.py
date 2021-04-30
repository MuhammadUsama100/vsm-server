
import math
import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle
from nltk.stem import PorterStemmer
ps = PorterStemmer()

with open('tfidf-matrx.p', 'rb') as fp:
    tf_idf_matrix = pickle.load(fp)


with open('doc-dictionary.p', 'rb') as fp:
    processed_array = pickle.load(fp)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# queryprocessing
query_frequency: dict = {}
for doc in processed_array:
    for term in doc:
        if term not in query_frequency:
            query_frequency[term] = 0

query = "picked news phrases"

# tokenizer = RegexpTokenizer(r'\w+')
query = query.lower()
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(query)
# tokens = nltk.word_tokenize(query)
lema_tokens = []
for token in tokens:
    lema_tokens.append(lemmatizer.lemmatize(token))
filtered_query_tokens = [
    word for word in lema_tokens if not word in stop_words]


for term in query_frequency:
    if term in filtered_query_tokens:
        query_frequency[term] = query_frequency[term] + 1

# length normalize
length_doc: list = []
for term in query_frequency:
    length_doc.append(
        query_frequency[term] * query_frequency[term])
for term in query_frequency:
    query_frequency[term] = query_frequency[term] / \
        math.sqrt(sum(length_doc))

print(filtered_query_tokens)


result: dict = {}
for doc_number in tf_idf_matrix:
    result[doc_number] = 0
    dot_product: list = []
    for term in tf_idf_matrix[doc_number]:
        dot_product.append(
            tf_idf_matrix[doc_number][term] * query_frequency[term])
    result[doc_number] = sum(dot_product)


# print(result)

for i in result:
    if result[i] > 0 and result[i] < 0.005:
        print(i+1)
        print(result[i])
