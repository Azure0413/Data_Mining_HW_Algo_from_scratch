# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 23:00:40 2023

@author: Eric
"""

import numpy as np #匯入模組以製作array

filename = 'input.txt' #匯入檔案

#讀取檔案
elements = []
with open(filename) as file:
    for line in file:
        line = line.strip().split()
        elements.append(line)

#處理資料製作多維array
data = np.array(elements,dtype=object)
print('%s\nshape is %s' % (type(data), data.shape)) #資料結構與大小
print(data)

file.close()

init = [] #紀錄每一種資料
for i in data:
    for j in i:
        if(j not in init):
            init.append(j)
init = sorted(init) #排序資料，增加易讀性
print(init)

min_supp = eval(input("請輸入min support(0-1)："))
sup = int(min_supp*len(init))
print(sup)  #最小出現次數

from collections import Counter #匯入一種dict的子類別 存放資料
c = Counter()
for i in init:
    for d in data:
        if(i in d):
            c[i]+=1
print("C1:") #每種資料個紀錄一次(出現次數)
for i in c:
    print(str([i])+": "+str(c[i])) #出現次數
print()

l = Counter() #另建立一個counter紀錄符合min support的資料
for i in c:
    if(c[i] >= sup): #需大於min support
        l[frozenset([i])]+=c[i] #凍結集合 無法更改之集合
print("L1:") #篩選後的資料
for i in l:
    print(str(list(i))+": "+str(l[i])) #出現次數
print()

all =[] #用於記錄除了單元組合以外，2元素組合以上符合min support的資料組合
pl = l #用於紀錄最大資料組合
pos = 1 #用於紀錄最大資料組合之回合數
for count in range (2,1000): #迭代次數/回合數(round)
    nc = set() #紀錄資料組合
    temp = list(l) #暫存上一步經過篩選後的集合
    for i in range(0,len(temp)): #將L1中的元素排列組合 組合成新的集合
        for j in range(i+1,len(temp)):
            t = temp[i].union(temp[j])
            if(len(t) == count):
                nc.add(temp[i].union(temp[j])) #連結
    nc = list(nc)
    c = Counter()
    for i in nc:
        c[i] = 0 #INIT集合
        for j in data:
            temp = set(j)
            if(i.issubset(temp)):
                c[i]+=1
    print("C"+str(count)+":") #第幾次的組合
    for i in c:
        print(str(list(i))+": "+str(c[i])) #顯示每一組資料組合的出現頻率
    print()
    
    l = Counter() #紀錄篩選後符合min support的組合
    for i in c:
        if(c[i] >= sup):
            l[i]+=c[i]
    print("L"+str(count)+":") #第幾次篩選後的組合
    for i in l:
        print(str(list(i))+": "+str(l[i])) #print篩選後的組合
    all.append(l)
    print()
    if(len(l) == 0): #停止點(若篩選後的組合數為0代表後續組合無法搭於min support)
        break
    pl = l #最多元素之組合
    pos = count #第幾回合(round)
print("The Max combination: ") #print最大組合之資料
print("L"+str(pos)+":")
for i in pl:
    print(str(list(i))+": "+str(pl[i]))
print()

from itertools import combinations #用於做排列組合之模組
confident = eval(input("請輸入min confidence(0-1)：")) #使用者設定min confidence
con = [] #用於紀錄符合strong rule的組合

path = 'output.txt'
f = open(path, 'w')
f.write("交管系112 H54084010 陳冠言\n")
f.write('\n')
for p in all:
    for l in p:  #找上述最多組合內兩兩之間的關聯性(strong rule)
        c = [frozenset(q) for q in combinations(l,len(l)-1)] #將上述符合min supoort且具兩個元素以上之組合內的元素進行排列組合
        mmax = confident
        for a in c:  #找出資料組合內各自的組合(或單元)的個數 公式為Prob.(AUB/A)orProb.(AUB/B) 因此計算A、B與AUB的個數
            b = l-a
            ab = l
            sab = 0
            sa = 0
            sb = 0
            for q in data:
                temp = set(q) #每一筆(列)資料
                if(a.issubset(temp)): #a出現的次數
                    sa+=1
                if(b.issubset(temp)): #b出現的次數
                    sb+=1
                if(ab.issubset(temp)): #ab同時出現之次數
                    sab+=1
            temp = sab/sa*100
            if(temp > mmax):
                mmax = temp
            temp = sab/sb*100
            if(temp > mmax):
                mmax = temp
            if len(l) == 2: #由於函式combinations再判斷兩元素時會重複搜尋，因此獨立出來
                print(str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%")
                f.write(str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%\n")
                
            else: #大於兩元素之組合
                print(str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%")
                print(str(list(b))+" -> "+str(list(a))+" = "+str(sab/sb*100)+"%")
                f.write(str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%\n")
                f.write(str(list(b))+" -> "+str(list(a))+" = "+str(sab/sb*100)+"%\n")
        curr = 1
        print("choosing:", end=' ')
        print("choosing:", end=' ',file=f)
        for a in c:
            b = l-a
            ab = l
            sab = 0
            sa = 0
            sb = 0
            for q in data:
                temp = set(q)
                if(a.issubset(temp)): #a出現的次數
                    sa+=1
                if(b.issubset(temp)): #b出現的次數
                    sb+=1
                if(ab.issubset(temp)): #ab同時出現之次數
                    sab+=1
            if len(l) == 2: #由於函式combinations再判斷兩元素時會重複搜尋，因此獨立出來
                if curr <= 2:
                    mmax = confident
                    temp = sab/sa
                    if(temp >= mmax): #判斷是否大於min confidence
                        print(curr, end = ' ') #找出符合min confidence之組合(計數)
                        print(curr, end = ' ',file=f)
                        con.append(str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%\n")
                    curr += 1
                    temp = sab/sb
                    if(temp >= mmax): #判斷是否大於min confidence
                        print(curr, end = ' ') #找出符合min confidence之組合(計數)
                        print(curr, end = ' ',file=f)
                        con.append(str(list(b))+" -> "+str(list(a))+" = "+str(sab/sb*100)+"%\n")
                    curr += 1
                print("\n",file=f)
            else:  #大於兩元素之組合
                mmax = confident 
                temp = sab/sa
                if(temp >= mmax): #判斷是否大於min confidence
                    print(curr, end = ' ') #找出符合min confidence之組合(計數)
                    print(curr, end = ' ',file=f)
                    con.append(str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%\n")
                curr += 1
                temp = sab/sb
                if(temp >= mmax): #判斷是否大於min confidence
                    print(curr, end = ' ') #找出符合min confidence之組合(計數)
                    print(curr, end = ' ',file=f)
                    con.append(str(list(b))+" -> "+str(list(a))+" = "+str(sab/sb*100)+"%\n")
                curr += 1
        print('\n',file=f)
        print()
        print()
print("符合strong rule的組合：")
print("符合strong rule的組合：\n",file=f)
for i in con: #print符合strong rule的組合
    print(i)
    print(i,end='\n',file=f)
f.close()