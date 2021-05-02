from flask_cors import CORS, cross_origin
from flask import Flask, request
import math
import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import pickle
from nltk.stem import PorterStemmer
ps = PorterStemmer()
nltk.download()

with open('tfidf-matrx.p', 'rb') as fp:
    tf_idf_matrix = pickle.load(fp)


with open('doc-dictionary.p', 'rb') as fp:
    processed_array = pickle.load(fp)


# with open('inverse-doc.p', 'rb') as fp:
#     inverse_doc_frequency = pickle.load(fp)

lemmatizer = WordNetLemmatizer()
file2 = open(
    "stopwords.txt", 'r',  encoding='utf8')

lines = file2.readlines()
# creating a list of stop word each word is strip before adding to stop word list
stopwords = []

for i in lines:
    if(i.rstrip("\n") != ""):
        stopwords.append(i.rstrip("\n").strip())
print(stopwords)


def process_query(queryString):
    # queryprocessing
    query_frequency: dict = {}
    for doc in processed_array:
        for term in doc:
            if term not in query_frequency:
                query_frequency[term] = 0

    query = queryString

    # tokenizer = RegexpTokenizer(r'\w+')
    query = query.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(query)
    # tokens = nltk.word_tokenize(query)
    lema_tokens = []
    for token in tokens:
        lema_tokens.append(lemmatizer.lemmatize(token))
    filtered_query_tokens = [
        word for word in lema_tokens if not word in stopwords]

    for term in query_frequency:
        if term in filtered_query_tokens:
            query_frequency[term] = query_frequency[term] + 1

    # for term in inverse_doc_frequency:
    #     query_frequency[term] = query_frequency[term] * \
    #         inverse_doc_frequency[term]

    print(len(query_frequency))

    #TF = log(1+tf)
    # for term in query_frequency:
    #     query_frequency[term] = math.log10(1+query_frequency[term])

    #TF = 1+log(tf)
    # for term in query_frequency:
    #     query_frequency[term] = 1 + (0 if query_frequency[term]
    #                                  == 0 else math.log10(query_frequency[term]))

    #TF = 0.5 + 0.5*log(tf)/max(tf)
    # max_val = -1
    # for term in query_frequency:
    #     if max_val < query_frequency[term]:
    #         max_val = query_frequency[term]
    # print(max_val)
    # for term in query_frequency:
    #     query_frequency[term] = 0.5 + (0.5*(0 if query_frequency[term]
    #                                           == 0 else math.log10(query_frequency[term])) / max_val)

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

    result = dict(sorted(result.items(), key=lambda val: val[1], reverse=True))

    result_set: list = []
    for i in result:
        if result[i] > 0:
            result_set.append((i+1, result[i]))

    print(result_set[0][1] - result_set[1][1])
    count = 0

    finalresult = {}
    finalresult["result-doc-set"] = []
    finalresult["result-set"] = []
    for index in range(0, len(result_set)-1):
        if(index+1 == len(result_set)):
            continue
        if result_set[index][1] >= 0.005 or index == 0:
            print("result doc # {} => {} , test=> {}".format(
                result_set[index][0], result_set[index][1], abs(result_set[index][1]-result_set[0][1])))
            count = count + 1
            finalresult["result-set"].append(
                {result_set[index][0]: result_set[index][1]})
            finalresult["result-doc-set"].append(result_set[index][0])

    finalresult["total-doc-retrived"] = count
    finalresult["result-doc-set"].sort()
    return finalresult


questions:  list = [
    "sent due",  # 1
    "walked quickly",  # 2
    "face of agony",  # 3
    "little unsteadily",  # 4
    "across adventures",  # 5
    "several nervous neighbourhood",  # 6
    "master jacket",  # 7
    "really love painter",  # 8
    "french pine herbs",  # 9
    "picked news phrases"  # 10
]

# process_query(questions[7-1])


app = Flask(__name__)

CORS(app, support_credentials=True)
app.debug = True
# this is a flask route which takes a query and returns a value that is used in the frontend to display the user the result
@app.route('/process-query', methods=['POST'])
@cross_origin(supports_credentials=True)
def process():
    try:
        if request.method == 'POST':
            q = str(request.get_json()["query"]).lower().strip()
            print(q)
            result = process_query(q)
            return {"resultset": result}
    except:
        return {"err": str("ERROR DUE TO INVALID QUERY")}
