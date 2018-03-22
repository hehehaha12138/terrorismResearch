import scrapy
import time
import json
import execjs
#import jieba
from bs4 import BeautifulSoup
from lxml import etree
from scrapy import Spider, Request
from mgTest.items import MgItem
import logging


class TwitterSpider(Spider):
    name = "twitter"
    allowed_domains = ["http://twitter.com"]
    search_url = 'https://twitter.com/search?l=&q={Query}%20until%3A{Until}&src=typd'
    search_url_pages = 'https://twitter.com/i/search/timeline?vertical=default&q={Query}&src=typd&include_available_features=1&include_entities=1&max_position=TWEET-{TweetEnd}-{TweetFirst}-BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA&reset_error_state=false'
    translate_url = 'https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=6&tsel=3&kc=0&tk={Tk}&q={Query}'
                  # 'https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=1&tk={Tk}&q={Query}'
                  # 'https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=6&tsel=3&kc=0&tk={Tk}&q={Query}'
                  # 'https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=1&tk=906272.763700&q=%E4%BD%A0%E5%A5%BD'
    count = 0
    tweetFirst = 0
    result = []
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


    def tk(self, text):
        return self.ctx.call("tk", text)

    def start_requests(self):
        #yield Request(self.search_url_pages.format(Query='terrorism', TweetEnd=self.tweetEnd, TweetFirst=self.tweetFirst),callback=self.parse,dont_filter=True)
        yield Request(
            self.search_url.format(Query='terrorism',Until='2017-07-14'),
            callback=self.parse, dont_filter=True)



    def parse(self, response):
        print('---------first request---------')
        selector = scrapy.Selector(response)
        tweets = selector.xpath('//li[@class = "js-stream-item stream-item stream-item\n"]')
        tweet_size = len(tweets)
        if tweet_size != 0:
            self.tweetFirst = tweets[0].xpath('@data-item-id')[0].extract()
            # while True:
            #     print(self.tweetFirst)

        # tarfile = "../info/tweet/isis.txt"
        # s = ""
        # with open(tarfile, "a") as tar:
        for tweet in tweets:
            tweetText = tweet.xpath('.//div[@class = "js-tweet-text-container"]/p')[0].extract()
            tweetTime = tweet.xpath('.//div[@class = "stream-item-header"]/small')[0].extract()
            soup = BeautifulSoup(tweetText)
            soupTime = BeautifulSoup(tweetTime)
            self.count += 1
            # print('-------twitter' + str(self.count) + '--------')
            # s += soup.text
            # s += "\r\n"
            if soup.text == "":
                continue
            else:
                tkValue = self.tk(soup.text)

            yield Request(url=self.translate_url.format(Query=(str)(soup.text), Tk=tkValue),
                          callback=self.parse_translate, dont_filter=True)
                # tar.write(soup.text.encode('utf-8'))
                # tar.write(b"\r\n")
        i=1
        while(True):
            i+=1
            currentEnd = int(self.tweetFirst) - 500000000000000*i
            # print(i)
            if currentEnd<0:
                break
            yield Request(
                url=self.search_url_pages.format(Query='terrorism', TweetEnd=str(currentEnd),
                                                 TweetFirst=self.tweetFirst), callback=self.parse_json,dont_filter=True)


    def parse_json(self,response):
        updateData = json.loads(response.text)
        html = updateData["items_html"]
        updateSoup = BeautifulSoup(html)
        # print("different page!")
        for entry in updateSoup.find_all('div',class_='js-tweet-text-container'):
            self.count+=1
            twitterEntry = MgItem()
            twitterEntry['id'] = self.count
            twitterEntry['text'] = entry.get_text()
            self.result.append(twitterEntry)
            # print(type(entry.get_text()))
            print(entry.get_text())

            if entry.get_text() == "":
                continue
            else:
                tkValue = self.tk(entry.get_text())

            yield Request(self.translate_url.format(Query=(str)(entry.get_text()), Tk=tkValue),
                          callback=self.parse_translate, dont_filter=True)

    def parse_translate(self, response):
        print("我进来了！！！！")
        transData = json.loads(response.text)
        content = ""
        for data in transData[0]:
            if (isinstance(data[0], str)):
                content += data[0]
        # content = transData[0][0][0]
        print("translation:" + content)

        with open('../../info/tweet/terrorism.txt', 'ab') as tar:
            # self.translate_count += 1
            # tar.write('-------video' + str(self.translate_count) + '--------\n')
            tar.write(content.encode('utf-8'))
            tar.write(b'\r\n')









