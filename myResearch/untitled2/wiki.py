#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pan Yang (panyangnlp@gmail.com)
# Copyright 2017 @ Yu Zhen
import gensim
import logging
import multiprocessing
import os
import re
import sys
import matplotlib.pyplot as plt
import numpy as np


from nltk import word_tokenize
from time import time
from sklearn.cluster import KMeans
from gensim.models import Word2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def Show2dCorpora(corpus):
    nodes = list(corpus)
    ax0 = [x[0][1] for x in nodes] # 绘制各个doc代表的点
    ax1 = [x[1][1] for x in nodes]
    # print(ax0)
    # print(ax1)
    plt.plot(ax0,ax1,'o')
    plt.show()

def get_stop_words_set(file_name):
    with open(file_name,'r') as file:
        return set([line.strip() for line in file])


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleanrn = re.compile('\n')
    cleantext = re.sub(cleanr, ' ', raw_html)
    cleantext = re.sub(cleanrn,'',cleantext)
    return cleantext


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
        self.stop_list = get_stop_words_set('C:/Users/Administrator/PycharmProjects/untitled2/stopword.txt')

    def __iter__(self):
        for root, dirs, files in os.walk(self.dirname):
            for filename in files:
                file_path = (root + '/' + filename)
                for line in open(file_path,encoding='utf-8'):
                    sline = line.strip()
                    if sline == "":
                        continue
                    rline = cleanhtml(sline)
                    tokenized_line = ' '.join(word_tokenize(rline))
                    is_alpha_word_line = [word for word in
                                          tokenized_line.lower().split()
                                          if (word.isalpha() and word not in self.stop_list)]
                    yield is_alpha_word_line


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print
        "Please use python train_with_gensim.py data_path"
        exit()
    data_path = sys.argv[1]
    begin = time()
    sentences = MySentences(data_path)
    dictionary = gensim.corpora.Dictionary(sentences)
    corpus = [dictionary.doc2bow(text) for text in sentences]



    '''
    model = gensim.models.Word2Vec(sentences,
                                   size=100,
                                   window=5,
                                   min_count=5,
                                   workers=multiprocessing.cpu_count())

    model.save("data/model/word2vec_gensim")
    model.wv.save_word2vec_format("data/model/word2vec_org",
                                  "data/model/vocabulary",
                                  binary=False)

    end = time()
    print
    "Total procesing time: %d seconds" % (end - begin)
    '''


    doc2 = MySentences('C:/Users/Administrator/PycharmProjects/untitled2/testContent.txt')
    copDoc2 = dictionary.doc2bow(doc2)

    tfidf_model = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf_model[corpus]
    lda = gensim.models.LdaModel(corpus_tfidf, num_topics=50, id2word=dictionary)
    corpus_lda = lda[corpus_tfidf]
    Show2dCorpora(corpus_lda)



    '''
    tfidf_model = gensim.models.TfidfModel(corpus)
    tfidf_m = tfidf_model[corpus]
    '''

    '''
    from sklearn.decomposition import PCA

    weight = lda_csc_matrix.toArray()
    pca = PCA(n_components=2)  # 输出两维
    newData = pca.fit_transform(weight)  # 载入N维
    print(newData)

    # 5A景区
    x1 = []
    y1 = []
    i = 0
    while i < 400:
        x1.append(newData[i][0])
        y1.append(newData[i][1])
        i += 1

        # 动物
    x2 = []
    y2 = []
    i = 400
    while i < 600:
        x2.append(newData[i][0])
        y2.append(newData[i][1])
        i += 1

        # 人物
    x3 = []
    y3 = []
    i = 600
    while i < 800:
        x3.append(newData[i][0])
        y3.append(newData[i][1])
        i += 1

        # 国家
    x4 = []
    y4 = []
    i = 800
    while i < 1000:
        x4.append(newData[i][0])
        y4.append(newData[i][1])
        i += 1

        # 四种颜色 红 绿 蓝 黑
    PCA.plt.plot(x1, y1, 'or')
    PCA.plt.plot(x2, y2, 'og')
    PCA.plt.plot(x3, y3, 'ob')
    PCA.plt.plot(x4, y4, 'ok')
    PCA.plt.show()

    '''
