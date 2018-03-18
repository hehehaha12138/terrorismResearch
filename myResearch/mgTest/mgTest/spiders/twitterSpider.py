import scrapy
import time
import json
import execjs
#import jieba
from bs4 import BeautifulSoup
from lxml import etree
from scrapy import Spider, Request
from mgTest.mgTest.items import MgItem

import logging


class TwitterSpider(Spider):
    name = "twitter"
    allowed_domains = ["http://twitter.com"]
    search_url = 'https://twitter.com/search?l=&q={Query}%20until%3A{Until}&src=typd'
    search_url_pages = 'https://twitter.com/i/search/timeline?vertical=default&q={Query}&src=typd&include_available_features=1&include_entities=1&max_position=TWEET-{TweetEnd}-{TweetFirst}-BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA&reset_error_state=false'
    translate_url = 'https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=6&tsel=3&kc=0&tk={Tk}&q={Query}'
    count = 0
    tweetFirst = 0
    tweetEnd = 10000
    result = []
    ctx = execjs.compile(""" 
            function TL(a) { 
            var k = ""; 
            var b = 406644; 
            var b1 = 3293161072; 

            var jd = "."; 
            var $b = "+-a^+6"; 
            var Zb = "+-3^+b+-f"; 

            for (var e = [], f = 0, g = 0; g < a.length; g++) { 
                var m = a.charCodeAt(g); 
                128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
                e[f++] = m >> 18 | 240, 
                e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
                e[f++] = m >> 6 & 63 | 128), 
                e[f++] = m & 63 | 128) 
            } 
            a = b; 
            for (f = 0; f < e.length; f++) a += e[f], 
            a = RL(a, $b); 
            a = RL(a, Zb); 
            a ^= b1 || 0; 
            0 > a && (a = (a & 2147483647) + 2147483648); 
            a %= 1E6; 
            return a.toString() + jd + (a ^ b) 
        }; 

        function RL(a, b) { 
            var t = "a"; 
            var Yb = "+"; 
            for (var c = 0; c < b.length - 2; c += 3) { 
                var d = b.charAt(c + 2), 
                d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
                d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
                a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
            } 
            return a 
        } 
        """)
    def start_requests(self):
        self.tweetFirst = 0
        self.tweetEnd = 974650501387227136
        #yield Request(self.search_url_pages.format(Query='terrorism', TweetEnd=self.tweetEnd, TweetFirst=self.tweetFirst),callback=self.parse,dont_filter=True)
        yield Request(
            self.search_url.format(Query='terrorism',Until='2017-07-14'),
            callback=self.parse, dont_filter=True)



    def parse(self, response):
        # print("********************")
        # print(response.text)
        # print("********************")
        '''
        print("干正事了：")
        updateData = json.loads(response.text)
        html = updateData["items_html"]
        updateSoup = BeautifulSoup(html)
        tarfile = '../../info/html.txt'
        tar = open(tarfile, 'wb')
        tar.write(updateSoup.prettify().encode('utf-8'))
        tweets = updateSoup.find_all(name='li', attrs='js-stream-item stream-item stream-item ')
        print("tweets:")
        print("123456")
        # print(tweets)
        i = 0

        tweet_size = len(tweets)
        if tweet_size != 0:
            # items_id = tweets[0].find_all('li', class="js-")
            self.tweetFirst = tweets[0].attrs['data-item-id']
            # print('tweetFirst:')
            # print(tweets[0])
            self.tweetEnd -= 1000

        for tweet in tweets:
            tweet = tweet.find_all('p', 'TweetTextSize js-tweet-text tweet-text')
            print(i)
            print(tweet[0].get_text())
            i += 1
        '''
        print('---------first request---------')
        selector = scrapy.Selector(response)
        tweets = selector.xpath('//li[@class = "js-stream-item stream-item stream-item\n"]')
        tweet_size = len(tweets)
        # print('----------')
        # print(tweets)
        # print(tweet_size)
        # print('----------')
        if tweet_size != 0:
            self.tweetFirst = tweets[0].xpath('@data-item-id')[0].extract()
            self.tweetEnd -= 10000
            print(self.tweetFirst)
        #
        # tarfile = "../../info/terrorism.txt"
        #with open(tarfile, 'wb') as tar:
        for tweet in tweets:
            tweetText = tweet.xpath('.//div[@class = "js-tweet-text-container"]/p')[0].extract()
            tweetTime = tweet.xpath('.//div[@class = "stream-item-header"]/small')[0].extract()
            soup = BeautifulSoup(tweetText)
            soupTime = BeautifulSoup(tweetTime)
            #time = dict(soup.a.attrs)
        #         # print(time)
            self.count += 1
            print('-------twitter' + str(self.count) + '--------')
        #         # print(soupTime.text)
            print(soup.text)
        #         # print(tweetText)
        #
        #         s = soup.text.encode('utf-8')
        #         s += b'\r\n'
        #         # print("--------------------------------------------------")
        #         tar.write(s)
        #
        #         print(s)
        i=1
        while(True):
            i+=1
            currentEnd = int(self.tweetFirst) - 500000000000000*i
            if currentEnd<0:
                break
            yield Request(
                url=self.search_url_pages.format(Query='terrorism', TweetEnd=str(int(self.tweetFirst) - 500000000000000*i),
                                                 TweetFirst=self.tweetFirst), callback=self.parse_json,dont_filter=True)


    def parse_json(self,response):
        updateData = json.loads(response.text)
        html = updateData["items_html"]
        updateSoup = BeautifulSoup(html)
        print("different page!")
        for entry in updateSoup.find_all('div',class_='js-tweet-text-container'):
            self.count+=1
            twitterEntry = MgItem()
            twitterEntry['id'] = self.count
            twitterEntry['text'] = entry.get_text()
            self.result.append(twitterEntry)
            print(entry.get_text())
                #f.write(str(entry.get_text().encode('utf-8','ignore'))[2:])
                #f.write('\n')
                #f.close()

    def parse_translate(self,response):
        transData = json.loads(response.text)
        content = transData[0][0][1]
        with open('r3.txt', 'a') as f:
            f.write(content)
            f.write('\n')
            f.close()










