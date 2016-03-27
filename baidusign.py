# coding:utf-8

import time, urllib2, cookielib, re, urllib

path = ''
url_sign = "http://tieba.baidu.com/sign/add"
filename = path + 'CookieBaidu.txt'
cookie = cookielib.MozillaCookieJar()
cookie.load(filename, ignore_discard=True, ignore_expires=True)
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
for pn in range(2):
    url_like = "http://tieba.baidu.com/f/like/mylike?&pn=" + str(pn + 1)

    response_like = opener.open(url_like).read().decode('gbk')
    liked_tieba = re.findall(r'</tr><tr><td><a href="/f\?kw=(.*?)" title="(.*?)">', response_like)
    # tittle_tieba = re.findall(r'</tr><tr><td><a href=".*?" title="(.*?)">',response_like)


    for i in liked_tieba:
        print i[1].encode('utf-8')
        tieba_url = 'http://tieba.baidu.com/f?kw=' + i[0]
        response_tieba = opener.open(tieba_url).read()
        tbs = re.findall('tbs.{1,5}(?:=|:).{1,8}"(\w{26})"', response_tieba)
        if not tbs:
            continue
        print tbs[0]
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'tieba.baidu.com',
            'Origin': 'http://tieba.baidu.com',
            'Referer': tieba_url,
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
        }

        data = urllib.urlencode({
            'ie': 'utf-8',
            'tbs': tbs[0],
            'kw': i[1].encode('utf-8')
        })
        request_sign = urllib2.Request(url_sign, data, header)
        response = opener.open(request_sign).read()
