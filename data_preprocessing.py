#encoding:utf-8

import nltk
import re
from urllib.parse import unquote
from gensim.models.word2vec import Word2Vec
import os
import numpy as np
import multiprocessing
import keras
from keras.utils import np_utils
import time,random,json

datadir="./data"

train_normal="data/train_normal.txt"
train_sql="data/train_sql.txt"
valid_normal="data/real_normal.txt"
valid_sql="data/real_sql.txt"
model_dir="file/word2model"
files="file"

max_features=16

#逐行获取文件内容
class MySentences(object): 
    def __init__(self,dirname):
        self.dirname=dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname,fname),encoding="utf-8"):
                if len(line.strip()):#判断是否是空行
                    yield URLDECODE(line) #yield让函数变为生成器，在下次调用函数时直接从最后一个for执行

#对每条数据的每个字段向量化
class getVecs(object):
    def __init__(self,filename,model,classes=None):
        self.filename=filename
        self.model=model
        self.classes=classes
        self.f_len=0
        self.max_len=0
    def __iter__(self):
        for line in open(self.filename,encoding="utf-8"):
            if len(line.strip()):#判断是否是空行
                self.f_len+=1
                xx=[]
                for text in unquote(line) :
                    try:

                        xx.append(self.model[text])
                    except KeyError:
                        continue
                xx=np.array(xx, dtype='float')
                if self.max_len< len(xx):
                    self.max_len=len(xx)
                yield xx

#urldecode解码
def URLDECODE(payload):
    payload = payload.lower()
    while True:
        test = payload
        payload = unquote(payload)
        if test == payload:
            break
        else:
            continue
    # 数字泛化为"0"
    payload, num = re.subn(r'\d+', "0", payload)
    # 替换url为”http://u
    payload, num = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?]+', "http://u", payload)
    # 分词
    r = '''
        (?x)[\w\.]+?\(
        |\)
        |"\w+?"
        |'\w+?'
        |http://\w
        |</\w+>
        |<\w+>
        |<\w+
        |\w+=
        |>
        |[\w\.]+
    '''
    return nltk.regexp_tokenize(payload, r)

#逐行写入数据（特征+标记）
def save_data(text,filename):
    with open(filename,'a') as f:
        for line in text:
            f.write(str(line.tolist())+"|"+str(text.classes)+"\n")

#记录训练总数据量（正常+恶意）
def save_len(normal,sql):
    with open("./file/train_len",'w') as f:
            f.write(str(normal.f_len+sql.f_len))
            
def maxlen(normal,sql):
    max=0
    if normal.max_len<sql.max_len:
        max=sql.max_len
    else:
        max=normal.max_len
    return max

#将训练数据从文件中读取出来并向量化处理
def predata():
    startime=time.time()
    model=Word2Vec.load(model_dir)
    x_normal=getVecs(train_normal,model,0)
    x_sql=getVecs(train_sql,model,1)
    save_data(x_normal,"./file/x_train")
    save_data(x_sql,"./file/x_train")
    save_len(x_normal,x_sql)
    with open("./file/INPUT_SHAPE","w") as f:
        f.write(str(max_features*maxlen(x_normal,x_sql)))
    print("save complete!")

#将验证数据从文件中读取出来并向量化处理
def valid_data():
    startime=time.time()
    model=Word2Vec.load(model_dir)
    x_normal=getVecs(valid_normal,model,0)
    x_sql=getVecs(valid_sql,model,1)
    save_data(x_normal,"./file/x_valid")
    save_data(x_sql,"./file/x_valid")
    with open("./file/valid_len",'w') as f:
            f.write(str(x_normal.f_len+x_sql.f_len))

#训练word2vec模型
def train_word2vec():
    sentences=MySentences(datadir)

    cores=multiprocessing.cpu_count() #判断是否多核，在Word2Vec()方法中增加效率

    if os.path.exists(model_dir):
        print ("Find cache file %s" % model_dir)
        model=Word2Vec.load(model_dir)
    else:
        model=Word2Vec(size=max_features, window=5, min_count=10, iter=10, workers=cores)

        model.build_vocab(sentences)

        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
        model.save(model_dir)
        print("save model complete!")

def read_file(filename):
    for line in open(filename):
        if len(line.strip()):
            yield line

#打乱数据顺序
def upset_data(filename,len):
    X=[]
    for line in open(filename):
        X.append(line)
    a=[]
    for i in range(int(len)):
        a.append(i)
    random.shuffle(a)  
    with open(filename,'w') as f:
        for i in a:
            f.write(str(X[i]))
    print("save complete!")




def data_generator(batch_size,input_shape,filename):
    while True:
        cnt=0
        X=[]
        Y=[]
        for line in open(filename):
            [x,y]=line.split("|")
            x=json.loads(x)
            y=json.loads(y)
            X.append(x)
            Y.append(y)
            cnt+=1
            if cnt==batch_size:
                cnt=0
                X=np.array(X)
                Y=np.array(Y)
                X=keras.preprocessing.sequence.pad_sequences(X,
                    maxlen=input_shape, dtype='float32')
                
                Y=np_utils.to_categorical(Y,2)

                yield (X,Y)
                X=[]
                Y=[]

def batch_generator(next_batch,data_size):
    while True:
            X,Y=next(next_batch)
            yield (X,Y)
            
if __name__=="__main__":
    #save_data(files)
    train_word2vec()
    predata()
    for i in open("./file/train_len"):
        upset_data("./file/x_train",i)
    valid_data()
    for i in open("./file/valid_len"):
        upset_data("./file/x_valid",i)

