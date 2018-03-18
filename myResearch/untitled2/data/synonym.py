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

def draw(word,modelAdress):

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    en_wiki_word2vec_model = Word2Vec.load(modelAdress)
    similar = en_wiki_word2vec_model.most_similar(word)

    import numpy as np
    import matplotlib.pyplot as plt

    n = len(similar)
    content = []
    name = []
    for item in similar:
        content.append(item[1])
        name.append(item[0])
    print(content)

    fig, ax = plt.subplots()
    index = np.arange(n)
    bar_width = 0.35

    opacity = 0.4

    rects1 = plt.bar(index,content, bar_width, alpha=opacity, color='b')
    plt.xlabel('Synonym of the word '+word)
    plt.ylabel('Similarity')
    plt.xticks(index, name)

    plt.ylim(content[9]-0.01,content[0]+0.01)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    draw('halal','C:/Users/Administrator/data/model/word2vec_gensim')