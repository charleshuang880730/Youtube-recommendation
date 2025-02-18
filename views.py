from django.shortcuts import render,HttpResponse

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

from django.contrib.auth.models import User, Group
from search.models import Charles
from rest_framework import viewsets
from rest_framework import permissions
from search.serializers import UserSerializer, GroupSerializer, CharlesSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

vid = list()
r = dict()    
a = dict()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class CharlesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Charles.objects.all()
    serializer_class = CharlesSerializer
    permission_classes = [permissions.IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        response = {1,2,3}
        if request.method == 'POST':
            #return JsonResponse({'status': 'Get posts succeed', 'posts': _get_all_posts()})
            return Response

#API ViewSet -- for geng to comment
class MyOwnView(APIView):
    #@csrf_exempt
    def get(self, request):
        print("in")
        queryname = request.GET['queryname']
        jieba.cut(queryname)
        if ' ' in queryname:
            queryname.remove(' ')
        print(queryname)
        #result = emsearch2json(embedding(queryname),vid)
        result = commentsearch(embedding(queryname),vid)
        #print(result)
        return Response(result)

#API ViewSet -- for search engine
class MyOwnView2(APIView):
    #@csrf_exempt
    def get(self, request):

        number_of_result = 0
        r = dict() # final return 
        result = list() #list result
        res2 = dict() #dict result for priority
        list__result_data = list() #new result return

        queryname = request.GET['queryname'] #get query
        queryname = jieba.lcut(queryname) #cut the query by jieba
        if ' ' in queryname:
            queryname.remove(' ')

        print(queryname)
        jsonfile = open("/Users/charleshuang0730/Desktop/1092專題測試/django-whoosh-test/testproject/search/data_new_2.json","r")
        alldata = json.load(jsonfile) #all data in json file

        #title_search
        res2 = findtitle(queryname) #title result
        res2 = sorted(res2.items(), key=lambda x:x[1], reverse = True) #sorted by priority
        result = [ item[0] for item in res2 ] #take vid into list
        number_of_result += len(result)
        print(len(result),"keyresult")
        print(result)
        for www in result:
            newdata = dict()
            newdata = alldata[www]
            newdata["Tags"] = "title_result"
            list__result_data.append(newdata)
            
        #caption_search
        res2 = dict()
        caption_time_temp = dict()
        for data in queryname:
            temp = find_caption(data)
            caption_time_temp.update(find_caption_for_time(data))
            res2.update(temp)
            temp = dict()
        print("captionresult")
        res2 = sorted(res2.items(), key=lambda x:x[1], reverse = True)
        res2 = [ item[0] for item in res2 ]

        for r in result:
            if r in res2:
                res2.remove(r)
        print(res2)

        result = res2
        number_of_result += len(result)
        for www in result:
            newdata = dict()
            newdata = alldata[www]
            if "Tags" not in newdata:
                newdata["Tags"] = "caption_result"
                newdata["Tags_time"] = caption_time_temp[www]
            list__result_data.append(newdata)
        #print(list__result_data)


        #embedding_search
        embedding_res = list()
        em_word_counter = 0
        if number_of_result < 10:
            print("Less than 50")
            all_word = embedding(queryname) 
            print(all_word)
            for x in all_word:
                print(x)
                string_to_list = list()
                string_to_list.append(x)
                temp = list()
                temp = findtitle(string_to_list)        
                temp = sorted(temp.items(), key=lambda x:x[1], reverse = True) #sorted by priority
                temp2 = [ item[0] for item in temp ] #take vid into list
                print("this is temp2:",temp2)
                embedding_res += temp2
                if temp2 != []:
                    for r in result:
                        if r in temp2:
                            temp2.remove(r)

                    for www in temp2:
                        newdata = dict()
                        newdata = alldata[www]
                        what_word = x
                        if "Tags" not in newdata:
                            newdata["Tags"] = "embedding_result"
                            newdata["Word"] = what_word
                        list__result_data.append(newdata)
            print("embedresult")
            print(embedding_res)
            number_of_result += len(embedding_res)
        #result = embedding_res

        em_word_counter+=1
       # print(list__result_data)
        return Response(list__result_data)

#API ViewSet -- for popularity range
class MyOwnView3(APIView):

    def get(self, request):
        print("popularity range")
        popularity_result = dict()
        pop = request.GET['popularity']
        vid = popularitys(pop)
        for i in range(0,len(vid)):
            popularity_result[vid[i]] = vidQuery(vid[i])
        print("popularity finish")
        #print(e)    
        return Response(popularity_result)

#API ViewSet -- for keyword recommended
class MyOwnView4(APIView):

    def get(self, request):
        print("keyword recommended")
        keyword_result = dict()
        key = request.GET['keyword']
        vid = keyword(key)
        for i in range(0,len(vid)):
            keyword_result[vid[i]] = vidQuery(vid[i])
        print("keyword finish")
        return Response(keyword_result)

def keyword(key):
    jsonfile = open('search/data/1000_ver/keyword_to_vid_list.json')
    data = json.load(jsonfile)
    jsonfile.close()
    return data[key]

def popularitys(pop):
    jsonfile = open('search/data/1000_ver/popularity_class.json')
    data = json.load(jsonfile)
    jsonfile.close()
    return data[pop]

def findtitle(queryname):
    title_result = dict()
    f = open('search/data/1000_ver/info.table')
    for data in f:
        data = data.strip().split("\t")
        counter2 = 0
        for query in queryname:
            if (query in data[1]) or (query in data[2]) or (query in data[0]):
                vid = data[0]
                counter2 += 1
        if counter2 != 0:
            title_result[vid] = counter2
    return title_result

def vidQuery(vid):
    print("vidQuery been called !!!")
    jsonfile = open("/Users/charleshuang0730/Desktop/1092專題測試/django-whoosh-test/testproject/search/data_new_2.json","r")
    data = json.load(jsonfile)
    jsonfile.close()
    #print(data[vid])
    return data[vid]
 
def hello_world(request):
    print("basic page!!!")
    return render(request, 'main_page.html')

#Whoosh - Search video title
def titlesearch(query):
    #建立schema
    schema = Schema(Vid = TEXT(stored=True),
                    Title = TEXT(stored=True,analyzer=ChineseAnalyzer()),
                    Channel = TEXT(stored=True,analyzer=ChineseAnalyzer())
                   )

     # 讀取並解析 .csv 檔案
    with open('/Users/charleshuang0730/Desktop/1092專題測試/django-whoosh-test/testproject/search/data/1000_ver/info.table', 'r', encoding='utf-8') as f:
        texts = [_.strip().split(',') for _ in f.readlines() if len(_.strip().split('\t')) == 4]

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

    results = searcher.find("Title", query, limit=1000)
    print(results)
    print(len(results))
    for j in range(0,len(results)):
        print(results[j].Vid.fields())
        res.append(results[j].Vid.fields())
    print("----------next")

    return (res)

#Embedding - Search top 10 title
def embedding(querylist):
    vocab = list()
    model = KeyedVectors.load_word2vec_format('search/data/1000_ver/content_vid_text.graph_hpe.embd', encoding='utf-8', unicode_errors='ignore')
    for query in querylist:
        if query in model:
            # 計算某個詞的相關詞列表
            y2 = model.most_similar(query, topn=5)  # 20個最相關的
            print ("和【",query,"】最相關的詞有：\n")
            for item in y2:
                vocab.append(item[0])
                print (item[0], item[1])
            print ("--------\n")
        else:
            print("not in model!!!")
    return (vocab)

#Whoosh - Search comment by keyword and return .json
def emsearch2json(emresult,vid):
    #建立schema
    schema = Schema(Vid = TEXT(stored=True),
                    Author = TEXT(stored=True,analyzer=ChineseAnalyzer()),
                    Comment = TEXT(stored=True,analyzer=ChineseAnalyzer()),
                    Vote = TEXT(stored=True,analyzer=ChineseAnalyzer())
                   )
    #start
    dic1 = dict()
    video = list()

    # 讀取並解析 .csv 檔案
    for k in range(1,2):
        res = list()
        dic2 = dict()
        #with open('search/data/video'+ str(k) +'.csv', 'r', encoding='utf-8') as f:
        with open('./data/1000_ver/commentnew.table', 'r', encoding='utf-8') as f:
            texts = [_.strip().split('\t') for _ in f.readlines() if len(_.strip().split('\t')) == 4]
            print(texts)

        # 儲存schema資訊至indexdir目錄
        indexdir = 'indexdir/'
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
        ix = create_in(indexdir, schema)

        # 按照schema定義資訊，增加需要建立索引的文件
        writer = ix.writer()
        for i in range(1, len(texts)):
            Vid, Author, Comment, Vote = texts[i]
            writer.add_document(Vid = Vid, Author = Author, Comment = Comment, Vote = Vote)
        writer.commit()
        # 建立一個檢索器
        searcher = ix.searcher()
        #emresult = embedding(vid[k])

        #file = open('word'+str(k)+'.txt','w')
        #file.write(str(emresult))
        #file.close()

        for i in range(0,len(emresult)):
            results = searcher.find("Comment", emresult[i], limit=1000)

            for j in range(0,len(results)):
                res.append(results[j].fields())
        #print(vid[k-1])
        #print("search finish")
        dic2["vid"] = vid[k-1]
        dic2["comments"] = res
        video.append(dic2)

    dic1["channel"] = "伯恩夜夜秀"
    dic1["videos"] = video
    #print(dic1)

    filename = "resall.json" # 指定要把numbers串列存到number.json檔中
    with open(filename,"w",encoding = 'utf-8') as file: # 以寫入模式開啟檔案才可以將資料儲存進去
        json.dump(dic1,file,ensure_ascii=False) # 將numbers串列存到number.json檔


    return dic1

def commentsearch(emresult,vid):
    counter=0
    comment_result = list()
    f = open('./data/1000_ver/comment-2.table')
    for i in range(0,len(emresult)):
        for data in f:
            print(counter)
            counter+=1
            data = data.strip().split("\t")
            try:
                print(data[2])
                if emresult[i] in data[2]:
                    comment_result.append(data[2])
            except:
                print(data,counter)
        return comment_result

def find_caption(query):
    caption_result = dict()
    f = open("search/data/1000_ver/video_IDs.csv","r")
    for vid in f:
        vid = vid.strip()

        table = open("search/data/1000_ver/caption/"+vid+"_text_time.table")
        priority = 0
        for data in table:
            data = data.strip().split("\t")
            if data[0] == query:
                priority+=1
        if priority!=0:
            caption_result[vid]=priority
    return caption_result

def find_caption_for_time(query):
    caption_result_time = dict()
    f = open("search/data/1000_ver/video_IDs.csv","r")
    for vid in f:
        vid = vid.strip()
        table = open("search/data/1000_ver/caption/"+vid+"_text_time.table")
        for data in table:
            data = data.strip().split("\t")
            if data[0] == query:
                caption_result_time[vid] = data[1] 
    return caption_result_time

#刪除重複的元素並排序過
def deleteDuplicated(listA):
    return sorted(set(listA), key = listA.index)




