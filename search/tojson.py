import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser
import jieba
from jieba.analyse import ChineseAnalyzer
import json
from gensim.models import word2vec
from gensim.models import KeyedVectors
import logging
import numpy as np

def embedding(query):
    #print("em in")
    model = KeyedVectors.load_word2vec_format('sample_test_embd.vec', encoding='utf-8', unicode_errors='ignore')
    # 計算某個詞的相關詞列表
    y2 = model.most_similar(query, topn=50)  # 20個最相關的
    vocab = list()
    print ("和【"+str(query)+"】最相關的詞有：\n")
    for item in y2:
        vocab.append(item[0])
        print (item[0], item[1])
    print ("--------\n")
    return (vocab)

#建立schema
schema = Schema(vid = TEXT(stored=True),
                author = TEXT(stored=True,analyzer=ChineseAnalyzer()),
                comment = TEXT(stored=True,analyzer=ChineseAnalyzer()),
                vote = TEXT(stored=True,analyzer=ChineseAnalyzer())
                )
#start
vid = ['6YQaXRzyTPk','Cf4A50LT3AQ','R0UBOYWEu28','UfwdDIzarW0'
,'V9aCCPDVZhA','b-eI7_litjw','cdHqrIce_bU','cfKdekQdOAQ','lZRNg2wjmRY','lkwycS8QUyE'] 
dic1 = dict()
video = list()

# 讀取並解析 .csv 檔案
for k in range(1,10):
    res = list()
    dic2 = dict()
    with open('data/video'+ str(k) +'.csv', 'r', encoding='utf-8') as f:
        texts = [_.strip().split(',') for _ in f.readlines() if len(_.strip().split(',')) == 4]

    # 儲存schema資訊至indexdir目錄
    indexdir = 'indexdir/'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)

    # 按照schema定義資訊，增加需要建立索引的文件
    writer = ix.writer()
    for i in range(1, len(texts)):
        vid, author, comment, vote = texts[i]
        writer.add_document(vid = vid, author = author, comment = comment, vote = vote)
    writer.commit()

    # 建立一個檢索器
    searcher = ix.searcher()
    emresult = embedding(vid[k])
    file = open('word'+str(k)+'.txt','w')
    file.write(str(emresult))
    file.close()

    for i in range(0,len(emresult)):
        results = searcher.find("comment", emresult[i], limit=1000)

        for j in range(0,len(results)):
            res.append(results[j].fields())
    print(vid[k-1])
    dic2["vid"] = vid[k-1]
    dic2["comments"] = res
    video.append(dic2)

dic1["channel"] = "伯恩夜夜秀"
dic1["videos"] = video

#filename = "res"+str(k)+".json" # 指定要把numbers串列存到number.json檔中
filename = "resall.json" # 指定要把numbers串列存到number.json檔中
with open(filename,"w",encoding = 'utf-8') as file: # 以寫入模式開啟檔案才可以將資料儲存進去
    json.dump(dic1,file,ensure_ascii=False) # 將numbers串列存到number.json檔


#print(dic1)

