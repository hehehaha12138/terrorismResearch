import scrapy
import time
import json
import execjs
#import jieba
from bs4 import BeautifulSoup
from lxml import etree
from scrapy import Spider, Request
from mgTest.mgTest.items import MgItem
import gzip
from io import  StringIO

import logging


class DarkNetSpider(Spider):
    name = "darkNet"
    allowed_domains = ["http://twitter.com"]
    #search_url = 'https://twitter.com/search?l=&q={Query}%20until%3A{Until}&src=typd'
    search_url = 'http://wpcxzq4ykmsxpacm.onion/archives.html'
    search_url_pages = 'https://twitter.com/i/search/timeline?vertical=default&q={Query}&src=typd&include_available_features=1&include_entities=1&max_position=TWEET-{TweetEnd}-{TweetFirst}-BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA&reset_error_state=false'
    translate_url = 'https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=6&tsel=3&kc=0&tk={Tk}&q={Query}'
    test_url = 'https://translate.google.cn/#auto/en/{Query}'
    count = 0
    tweetFirst = 0
    result = []
    translate_count = 0;
    ctx = execjs.compile(""" 
           function tk(a) 
            {var TKK = ((function() 
            {var a = 561666268;
             var b = 1526272306;
             return 406398 + '.' + (a + b); })());
              function b(a, b) 
              { for (var d = 0; d < b.length - 2; d += 3) 
                { var c = b.charAt(d + 2), c = 'a' <= c ? c.charCodeAt(0) - 87 : Number(c), c = '+' == b.charAt(d + 1) ? a >>> c : a << c; a = '+' == b.charAt(d) ? a + c & 4294967295 : a ^ c } return a } for (var e = TKK.split('.'), h = Number(e[0]) || 0, g = [], d = 0, f = 0; f < a.length; f++) {var c = a.charCodeAt(f);128 > c ? g[d++] = c : (2048 > c ? g[d++] = c >> 6 | 192 : (55296 == (c & 64512) && f + 1 < a.length && 56320 == (a.charCodeAt(f + 1) & 64512) ? (c = 65536 + ((c & 1023) << 10) + (a.charCodeAt(++f) & 1023), g[d++] = c >> 18 | 240, g[d++] = c >> 12 & 63 | 128) : g[d++] = c >> 12 | 224, g[d++] = c >> 6 & 63 | 128), g[d++] = c & 63 | 128)}a = h;for (d = 0; d < g.length; d++) a += g[d], a = b(a, '+-a^+6');a = b(a, '+-3^+b+-f');a ^= Number(e[1]) || 0;0 > a && (a = (a & 2147483647) + 2147483648);a %= 1E6;return a.toString() + '.' + (a ^ h) }
        """)

    def tk(self,a):
        # 获取google翻译内容的tk值
        # a：要翻译的内容，以字符串指定
        # 注意：要翻译的内容只能是英文，即只能是包含ASCII码的英文字符串
        TKK = (lambda a=561666268, b=1526272306: str(406398) + '.' + str(a + b))()

        def b(a, b):
            for d in range(0, len(b) - 2, 3):
                c = b[d + 2]
                c = ord(c[0]) - 87 if 'a' <= c else int(c)
                c = a >> c if '+' == b[d + 1] else a << c
                a = a + c & 4294967295 if '+' == b[d] else a ^ c
            return a

        e = TKK.split('.')
        h = int(e[0]) or 0
        g = []
        d = 0
        f = 0
        while f < len(a):
            c = ord(a[f])
            if 128 > c:
                g.insert(d, c)
                d += 1
            else:
                if 2048 > c:
                    g[d] = c >> 6 | 192
                    d += 1
                else:
                    if (55296 == (c & 64512)) and (f + 1 < len(a)) and (56320 == (ord(a[f + 1]) & 64512)):
                        f += 1
                        c = 65536 + ((c & 1023) << 10) + (ord(a[f]) & 1023)
                        g[d] = c >> 18 | 240
                        d += 1
                        g[d] = c >> 12 & 63 | 128
                        d += 1
                    else:
                        g[d] = c >> 12 | 224
                        d += 1
                        g[d] = c >> 6 & 63 | 128
                        d += 1
                    g[d] = c & 63 | 128
                    d += 1
            f += 1
        a = h
        for d in range(len(g)):
            a += g[d]
            a = b(a, '+-a^+6')
        a = b(a, '+-3^+b+-f')
        a ^= int(e[1]) or 0
        if 0 > a: a = (a & 2147483647) + 2147483648
        a %= 1E6
        return str(int(a)) + '.' + str(int(a) ^ h)

    def start_requests(self):
        yield Request(self.search_url.format(Query='terrorism', Until = '2017-07-14'),callback=self.parse,dont_filter=True)



    def parse(self, response):
        print('---------first request---------')
        selector = scrapy.Selector(response = response)
        #tweets = selector.xpath('//li[@class = "js-stream-item stream-item stream-item\n"]')
        videoTotal = selector.xpath('//div[@class = "entry-content"]')
        videoTimeList = videoTotal.xpath('./dl/dt');
        videoList = videoTotal.xpath('./dl/dd')
        result = open("isisResult.txt","wb")
        #self.tweetFirst = tweets[0].xpath('@data-item-id')[0].extract()\
        for index in range(len(videoList)):
            videoText = videoList[index].xpath('./a')[0].extract()
            videoTime = videoTimeList[index].xpath('.')[0].extract()

            # tweetText = tweet.xpath('.//div[@class = "js-tweet-text-container"]/p')[0].extract()
            # tweetTime = tweet.xpath('.//div[@class = "stream-item-header"]/small')[0].extract()
            soup = BeautifulSoup(videoText)
            timeSoup = BeautifulSoup(videoTime)
            # soupTime = BeautifulSoup(tweetTime)
            # time = dict(soup.a.attrs)
            # print(time)
            self.count += 1

            head = '-------video' + str(self.count) + '--------\n'
            result.write(head.encode("utf-8"))
            result.write((timeSoup.dt.text+"\n").encode("utf-8"))

            result.write((soup.a.text + "\n").encode("utf-8"))

            '''
            gzipStr = soup.a.text
            gzipFile = StringIO(gzipStr)
            gzipper = gzip.GzipFile(fileobj=gzipFile)
            data = gzipper.read()
         '''

            #result.write(data + "\n")
            '''
             print('-------video' + str(self.count) + '--------')
            #print(soup.p)
            print(timeSoup.dt.text)
            print(soup.a.text)
          '''
            if soup.a.text == "":
                continue
            else:
                tkValue = self.ctx.call("tk",soup.a.text)

            #print(soup.a.text)

            #yield Request(self.translate_url.format(Query=(str)(soup.a.text), Tk = tkValue),callback=self.parse_translate,dont_filter=True)
            yield Request(self.translate_url.format(Query=(str)(soup.a.text),Tk = tkValue),callback=self.parse_translate, dont_filter=True)

        #for video in videoList:






        i=1

        '''
        while(True):
            i+=1 
            currentEnd = int(self.tweetFirst) - 500000000000000*i
            if currentEnd<0:
                break
            yield Request(
                url=self.search_url_pages.format(Query='terrorism', TweetEnd=str(int(self.tweetFirst) - 500000000000000*i),
                                                 TweetFirst=self.tweetFirst), callback=self.parse_json,dont_filter=True)
        '''

    def parse_json(self,response):
        updateData = json.loads(response.text)
        html = updateData["items_html"]
        updateSoup = BeautifulSoup(html)
        for entry in updateSoup.find_all('div',class_='js-tweet-text-container'):
            self.count+=1
            twitterEntry = MgItem()
            twitterEntry['id'] = self.count
            twitterEntry['text'] = entry.get_text()
            self.result.append(twitterEntry)
                #f.write(str(entry.get_text().encode('utf-8','ignore'))[2:])
                #f.write('\n')
                #f.close()

    def parse_translate(self,response):

        transData = json.loads(response.text)
        content = ""
        for data in transData[0]:
            if(isinstance(data[0],str)):
                content += data[0]
        #content = transData[0][0][0]
        print("translation:"+content)



        with open('isisTranslate.txt', 'a') as f:
            self.translate_count += 1
            f.write('-------video' + str(self.translate_count) + '--------\n')
            f.write(content)
            f.write('\n')
            f.close()












