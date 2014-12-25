#!/usr/bin/env python3

import urllib.request
import re, tempfile
import os, time

path=tempfile.gettempdir()+os.sep+'daomubiji'
if not os.path.exists(path):
    os.mkdir(path)
mainhtml=r'http://www.daomubiji.com'
maincontent=urllib.request.urlopen(mainhtml).read().decode()
#listtitle0=re.findall('\s*<td\s*colspan.*<h2>(.*)</h2></center>.*', maincontent)
#print(listtitle0)
listContent=re.split('\n', maincontent)
#创建一个名为downlog的文件，做简单的日至记录，记载网页下载失败的情况
with open(path+'/'+'downlog', 'a') as logobj:
    for j in listContent:
        if re.search('\s*<td\s*colspan.*<h2>(.*)</h2></center>.*', j):
            sectionName=re.search('\s*<td\s*colspan.*<h2>(.*)</h2></center>.*', j).groups()[0]
    #       print(sectionName)
            new_path=os.path.join(path, sectionName)
            if not os.path.isdir(new_path):
                os.makedirs(new_path)
        elif re.search('<td><a href="(.*)">(.*)</a></td>',j):
            url=re.search('<td><a href="(.*)">(.*)</a></td>',j).groups()[0]
            #为了方便网页下载后的文件进行排序，将标题中的中文数字转换为了阿拉伯数字。（数字十例外，在头部就是1，在尾部就是0，在中间什么都不是，偷懒就没有对它进行处理）
            def transRule(x):
                if x.group() == '一':return'1'
                elif x.group() == '二':return'2'
                elif x.group() == '三':return'3'
                elif x.group() == '四':return'4'
                elif x.group() == '五':return'5'
                elif x.group() == '六':return'6'
                elif x.group() == '七':return'7'
                elif x.group() == '八':return'8'
                elif x.group() == '九':return'9'
                else:return x.group()
            title=re.search('<td><a href="(.*)">(.*)</a></td>',j).groups()[1]
            try:
                title=re.split('["第""章"]', title)[0]+'第'+re.sub(r"['一''二''三''四''五''六''七''八''九''十']", transRule, re.split('["第""章"]', title)[1])+'章'+re.split('["第""章"]', title)[2]
            except Exception:
                pass
    #       print(sectionName, "\n", url, title)
            if not  os.path.exists(new_path+'/'+title) and not os.path.exists(new_path+'/'+title+'.txt'):
                fobj=open(new_path+'/'+title, 'w')
            else:
                continue
            k=0
            #有时候子网页由于网络或者其他原因，未能一次下载成功，便设置了重复尝试5次进行下载。具体次数会写入downlog中
            while k < 5:
                try:
                    content=urllib.request.urlopen(url).read().decode("UTF-8")
                except Exception:
                    content=''
                if content and title:
                    fobj.write(content)
                    print(time.strftime('%Y-%m-%d %H:%M:%S'),'SUCCESS download:===>', sectionName+r'@'+title)
                    logText=time.strftime('%Y-%m-%d %H:%M:%S')+' '+'SUCCESS download:===>'+' '+ sectionName+r'@'+title+'\n'
                    logobj.write(logText)
                    logobj.truncate()
                    break
                else:
                    k += 1
                    print(time.strftime('%Y-%m-%d %H:%M:%S'),'FAILED download %d th:===>' %(k), sectionName+r'@'+title)
                    logText=time.strftime('%Y-%m-%d %H:%M:%S')+' '+'FAILED download %d th:===>' %(k)+' '+ sectionName+r'@'+title+'\n'
                    logobj.write(logText)
                    logobj.truncate()
                    continue
            fobj.close()
        else:
            continue




#以下部分是将和html文件去掉多余的部分转换为txt文件。原html文件会被删除。
for i in  os.listdir(path):
    absDirPath=path+os.sep+i
    if os.path.isdir(absDirPath):
        #print(absDirPath)
        for j in os.listdir(absDirPath):
            if not os.path.splitext(j)[1]:
                absFilePath=absDirPath+os.sep+j
            else:
                continue
            if os.path.isfile(absFilePath):
                #print(absFilePath)
                with open(absFilePath+'.txt', 'w') as txtObj:
                    with open(absFilePath) as fobj:
                        txtContent=fobj.readlines()
                        for k in txtContent:
                            rightTitle=re.search('.*<h[12]>(.*)</h[12]>.*', k)
                            rightContent=re.search(".*<p>(.*)</p>.*", k)
                            rightEnd=re.match(".*<!-- You can start editing here. -->.*", k)
                            if rightTitle:
                                txtObj.write(rightTitle.groups()[0].center(200))
                                txtObj.write("\n")
                                #print(rightTitle.groups()[0])
                                continue
                            if rightContent:
                                txtObj.write("  ")
                                txtObj.write(rightContent.groups()[0].ljust(80))
                                txtObj.write("\n")
                                #print(rightContent.groups()[0])
                                continue
                            if rightEnd:
                                break
                    print(absFilePath,"===>转换成功")
                os.remove(absFilePath)
