import pandas as pd 
import numpy as np
from sklearn import tree
from sklearn.linear_model import LogisticRegression
import math

alp={'a','e','i','o','u'}

def cal_data(s):
    d=np.zeros(6)
    d[0]=int(len(s))

    sumt=0
    for i in s:
        if(i.isdigit()):
            sumt+=1
    d[1]=int(sumt)
   
    h=0.0
    sumt=0
    letter=[0]*26
    for i in range(len(s)):
        if s[i].isalpha():
            letter[ord(s[i])-ord('a')]+=1
            sumt+=1
    if(sumt!=0):
        for i in range(26):
            p=1.0*letter[i]/sumt
            if p>0:
                h+=-(p*math.log(p,2))
    d[2]=h

    sumt=0
    for i in s:
        if(i=='.'):
            sumt+=1
    d[3]=int(sumt)

    h1=0
    h2=0
    h=0.0
    for i in range(int(len(s))):
        if(s[i]=='.'):
            break
        if(s[i].isalpha()):
            h1+=1
            for j in alp:
                if(s[i]==j):
                    h2+=1
    if(h1!=0):
        h=h2/h1
    else:
        h=0
    d[4]=h        
    #print(d)
    return d
    
data=np.loadtxt('train.txt',delimiter=',',dtype=str) 
name=data[:,0] 
label=data[:,-1]

df=np.zeros((len(name),6))

for i in range(len(name)):
    df[i]=cal_data(name[i])
    if(label[i]=='dga'):
        df[i][5]=1
    else:
        df[i][5]=0


X=df[:,0:5]
Y=df[:,-1]
Y=Y.astype('int')

clf=tree.DecisionTreeClassifier()
clf=clf.fit(X,Y)

testdata=np.loadtxt('test.txt',delimiter=',',dtype=str)
testname=testdata
if testname.shape:
    lenth=len(testname)
else:
    lenth=1
    testname=[str(testname)]
    
testdf=np.zeros((lenth,6))

for i in range(lenth):
    testdf[i]=cal_data(testname[i])

#result=linear_model.predict(testdf[0:900,0:4])
result=clf.predict(testdf[:,0:5])

f=open('result.txt','w')
for i in range(lenth):
    f.write(testname[i]+',')
    if(result[i]==0):
        f.write('notdga\n')
    else:
        f.write('dga\n')
f.close()
