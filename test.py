from sklearn.ensemble import RandomForestClassifier
import numpy as np
import math

class Domain:
    def __init__(self, _name, _label, _length, _num, _yuanyin, _shang):
        self.name = _name
        self.label = _label
        self.length = _length
        self.num = _num
        self.yuanyin = _yuanyin
        self.shang = _shang
    
    def returnData(self):
        return [self.length, self.num, self.yuanyin, self.shang]
 
    def returnLabel(self):
        if self.label == "dga":
            return 0
        else:
            return 1

#count the number of basic num
def number_num(url_dns):
    n=0
    for i in url_dns:
        if i in "0123456789":
            n=n+1;
    return n

#count the number of basic num
def number_yuanyin(url_dns):
    n=0
    for i in url_dns:
        if i in "aeiou":
            n=n+1;
    return 0

#calculate the shang
def cal_shang(url_dns):
    h = 0.0
    sumLetter = 0
    letter = [0] * 26
    url_dns = url_dns.lower()
    for i in range(len(url_dns)):
        if url_dns[i].isalpha():
            letter[ord(url_dns[i]) - ord('a')] += 1
            sumLetter += 1
    for i in range(26):
        p = 1.0 * letter[i] / sumLetter
        if p > 0:
            h += -(p * math.log(p, 2))
    return h


def initData(filename, domainlist):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "":
                 continue
            tokens = line.split(",")
            name = tokens[0]
            if(len(tokens)==1):
                label=' '
            else:
                label = tokens[1]
            length=len(name)
            num=number_num(name)
            yuanyin=number_yuanyin(name)
            shang=cal_shang(name)
            domainlist.append(Domain(name, label, length, num, yuanyin, shang))


def main():
    train_list = []
    test_list=[]
    initData("train.txt",train_list)
    initData("test.txt",test_list)
    featureMatrix = []
    labelList = []
    for item in train_list:
         featureMatrix.append(item.returnData())
         labelList.append(item.returnLabel())

    clf = RandomForestClassifier(random_state = 0)
    clf.fit(featureMatrix,labelList)
    
    with open("result.txt","w") as f:
        for i in test_list:
            f.write(i.name)
            f.write(",")
            if clf.predict([i.returnData()])[0] == 0:
                f.write("notdga")
            else:
                f.write("dga")
            f.write("\n")            
           
if __name__ == '__main__':
    main()
