import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer
import json
from gensim.models import word2vec
from gensim.models import KeyedVectors
import logging
import numpy as np

vid = ['6YQaXRzyTPk','Cf4A50LT3AQ','R0UBOYWEu28','UfwdDIzarW0'
,'V9aCCPDVZhA','b-eI7_litjw','cdHqrIce_bU','cfKdekQdOAQ','lZRNg2wjmRY','lkwycS8QUyE']

#建立schema
schema = Schema(Vid = TEXT(stored=True),
                Title = TEXT(stored=True,analyzer=ChineseAnalyzer()),
                Channel = TEXT(stored=True,analyzer=ChineseAnalyzer())
                )

# 讀取並解析 .csv 檔案
with open('/Users/charleshuang0730/Desktop/1092專題測試/django-whoosh-test/testproject/search/data/60video2.csv', 'r', encoding='utf-8') as f:
    print(f)
    texts = [_.strip().split(',') for _ in f.readlines() if len(_.strip().split(',')) == 3]



print(len(texts))
# 儲存schema資訊至indexdir目錄
indexdir = 'indexdir/'
if not os.path.exists(indexdir):
    os.mkdir(indexdir)
ix = create_in(indexdir, schema)

# 按照schema定義資訊，增加需要建立索引的文件
writer = ix.writer()
for i in range(1, len(texts)):
    Vid, Title, Channel = texts[i]
    writer.add_document(Vid = Vid, Title = Title, Channel = Channel)
writer.commit()
# 建立一個檢索器
searcher = ix.searcher()


#dic = dict()
def embedding(query):
    vocab = list()
    model = KeyedVectors.load_word2vec_format('sample_test_embd.vec', encoding='utf-8', unicode_errors='ignore')
    # 計算某個詞的相關詞列表
    y2 = model.most_similar(query, topn=300)  # 20個最相關的
    vocab = list()
    #print ("和【"+str(query)+"】最相關的詞有：\n")
    for item in y2: 
        vocab.append(item[0])
        #dic[str(item[0])] = item[1]
        #print (item[0], item[1])
    #print ("--------\n")
    return (vocab)
    #return dic

def embedding2(query):
    model = KeyedVectors.load_word2vec_format('sample_test_embd.vec', encoding='utf-8', unicode_errors='ignore')
    y3 = model.similarity(query,"實價")
    return y3

def titlesearch(query):
    res = list()

    results = searcher.find("Title", query, limit=1000)
    print(results)
    print(len(results))
    for j in range(0,len(results)):
        print(results[j].fields())
        res.append(results[j].fields())
    print("----------next")

    return (res)

res = list()
#res1 = dict()
res2 = dict()

result = titlesearch("政治")

if(len(result)<5):
    for i in range(0,len(vid)-1):
        title = searcher.find("Vid", vid[i] ,limit=1)
        #res = res + embedding("非洲")
        res1 = embedding("政治")
        res2[str(vid[i])] = embedding2(vid[i])
        print (title[0].fields())
        print (embedding2(vid[i]))
    print (res2)
    print (sorted(res2.items(), key = lambda d: d[1]))
else:
    print (res)

#print (res1)







