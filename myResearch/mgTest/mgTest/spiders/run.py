# -*- coding: utf-8 -*-
# @Time     : 2018/3/21 18:56
# @Author   : chen qian


from scrapy import cmdline


name = 'twitter'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())