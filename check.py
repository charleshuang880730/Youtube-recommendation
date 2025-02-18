import os

file = open('./data/1000_ver/comment-2.table', "r")
fileWrite  = open('./data/1000_ver/commentnew.table', "a") 
counter = 0
for line in file:
   print(counter)
   counter+=1
   print(line)
   try:
       fileWrite.write(line)
   except:
       print(line)
