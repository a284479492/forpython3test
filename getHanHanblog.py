#!/usr/bin/env python3

import urllib.request
import re

page=1
while page <= 7:
    mainhtml=r'http://blog.sina.com.cn/s/articlelist_1191258123_0_'+str(page)+'.html'
    print(mainhtml)
    page += 1
    maincontent=urllib.request.urlopen(mainhtml).read().decode()
    listtitle=re.findall("<a title.*?span>", maincontent)
    for str0 in listtitle:
        html=re.search('.*href=\"([^\"]+)\".*',str0).group(1)
        i=0
        while i < 5:
            try:
                content=urllib.request.urlopen(html).read().decode()
                filename=html[-26:]
                fobj=open(filename,'w')
                fobj.write(content)
                fobj.close()
                print("%s:===> Download %dst success!" %(html, i+1))
                i=5
            except Exception :
                print("%s:===> Download %dst FAILED" %(html, i+1))
                i += 1
