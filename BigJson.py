import os
import json
import math
Big = dict()
Data = dict()
Cid = dict()
Title = dict()

Wcloud = dict()
Info = dict()
Discuss = dict()
geng = list()
cloud = list()
info = list()
discuss = list()
lost = list()
count2 = 0

tMp_list = []
view_count = 0
like_count = 0
comment_count = 0


f = open("../search/data/1000_ver/video_IDs.csv","r")

geng_CounT = open("../search/data/1000_ver/geng_count.table","r")
for line in f:
    geng_count = 0
    line = line.strip()
    Word_Cloud = list()

    table = open("/Users/charleshuang0730/Desktop/1092專題測試/django-whoosh-test/testproject/search/data/1000_ver/sort_sim_text_time_table_merged_v1/"+line+"_text_time_sim.table","r")
    fff = open("../search/data/1000_ver/bsic_data_ver1000-new.tsv","r")
    ffff = open("../search/data/1000_ver/discuss_volume.tsv","r")
    fffff = open("../search/data/1000_ver/info.table","r")

    time = list()
    time_to_geng = dict()
    word_counter = 4
    for data in table:
        geng_tuple = list()
        data = data.strip().split("\t")
        Word_Cloud.append(data[0])
        geng_count = geng_count+1
        geng_tuple.append(data[0])
        geng_tuple.append(word_counter)
        geng_tuple_2 = tuple(geng_tuple)
        time.append(float(data[1]))
        time_to_geng[data[1]] = geng_tuple_2
        word_counter-=1
    time.sort()
    for t in time:
        Geng = dict()
        temp = dict()
        t = ' '+str(t)
        temp["time"] = t
        temp["weight"] = time_to_geng[t][1]
        Geng[time_to_geng[t][0]] = temp
        geng.append(Geng)
    
    Data["Geng"] = geng
    geng = list()
    
    with open("./data/1000_ver/sort_by_vote_vid_geng_comment.json") as in_json:
        commentjson = json.load(in_json)
    tmp = []
    print(Word_Cloud)
    for wc in Word_Cloud:
        wcc = list()
        wcc = wc.strip().split(',')
        print(wcc)
        for everywcc in wcc:
            comment_counter = 0
            for everyauthor in commentjson[line][everywcc]:
                if comment_counter == 3:
                    break
                else:
                    comment_counter += 1
                    Geng_clou = dict()
                    Geng_clou["group"] = wc
                    Geng_clou["name"] = everyauthor["text"]
                    Geng_clou["value"] = str(int(everyauthor["vote"])+60)
                    Geng_clou["author"] = everyauthor["author"]
                    Geng_clou["photo"] = everyauthor["photo"]
                    tmp.append(Geng_clou)
    Data["Word_Cloud"]=tmp

    for data3 in fff:
        data3 = data3.strip().split("\t")
        if data3[0] == line:
            Info["id"] = data3[0]
            Info["viewCount"] = data3[4]
            view_count = int(data3[4])
            Info["likeCount"] = data3[5]
            like_count = int(data3[5])
            Info["dislikeCount"] = data3[6]
            Info["favoriteCount"] = data3[7]
            Info["commentCount"] = data3[8]
            comment_count = int(data3[8])
            Cid[line] = data3[1]
            Title[line] = data3[2]
            info.append(Info)
            Data["Info"] = Info
            Info = dict()
            break
        else:
            Info["id"] = line
            Info["viewCount"] = None
            Info["likeCount"] = None
            Info["dislikeCount"] = None
            Info["favoriteCount"] = None
            Info["commentCount"] = None
            Cid[line] = None
            Title[line] = None
            Info = dict()
            
    ratio = open("./data/1000_ver/video_ratio.csv")
    for r in ratio:
        r = r.strip().split('\t')
        if r[0] == line:
            comment_ratio = r[1]
            break
   


    print(line)
    for data4 in ffff:
        data4 = data4.strip().split("\t")
        if data4[0] == line:
            Discuss["Entertainment_Value"] = math.sqrt(float(data4[1]))
            #Discuss["Gravity"] = 1 - float(data4[1])
            Discuss["Connectivity"] = math.sqrt(float(data4[2]))
            Discuss["Metrics"] = math.sqrt(0.4*(view_count/172179271)+0.3*(like_count/309775)+0.3*(comment_count/59037))
 
            tEmp=float(geng_CounT.readline().strip())

            Discuss["Geng_Ratio"] = tEmp + geng_count/10

            print(Discuss["Geng_Ratio"])
            Discuss["Comment_Ratio"] = math.sqrt(float(comment_ratio))

            total = 0
            for i in Discuss:
                total += ((1/5)*float(Discuss[i]))
            Discuss_list = [Discuss[k] for k in Discuss]
            Discuss["Value_List"] = Discuss_list
            Discuss["Overall"] = total
            Data["Discuss"] = Discuss
            Discuss = dict()
            break
        else:
            Discuss["Entertainment_Value"] = None
            Discuss["Connectivity"] = None
            Discuss = dict()

    Data["Title"] = Title[line]
    Data["Cid"] = Cid[line]
    
    Big[line] = Data
    Data = dict()
print(Big)

f.close()
fff.close()
ffff.close()
fffff.close()
table.close()
filename = "resall2.json" # 指定要把numbers串列存到number.json檔中
with open(filename,"w",encoding = 'utf-8') as file: # 以寫入模式開啟檔案才可以將資料儲存進去
    json.dump(Big,file,ensure_ascii=False) # 將numbers串列存到number.json檔


















      



