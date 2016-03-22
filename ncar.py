#coding=utf-8

import urllib, urllib2, time, socket, sys, re, tempfile, os, threading

global Site
global SiteWP
global AllInfo
abc = 0   #counter
Spyder = [0,0,0,0,0]
Data = []

AllInfo = [[],[],[],[],[]]

Site = lines = tuple(open(sys.path[0]+'/SiteList.txt', 'r'))
SiteWP = Site[0]
    #EpisodeSpider is a method to get the information in webpage, two re.findall can be change to other function. 
    #LinkSaver is a function to save all link. it can be change to spy other webpage.
class Spider:

    def EpisodeSpider(self):
        global abc
        global AllInfo
        global Spyder
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        values = {'name' : 'WHY',    
	    	      'location' : 'SDU',    
		          'language' : 'Python' }    

        headers = { 'User-Agent' : user_agent }  #As a browser

        data = urllib.urlencode(values)
        req = urllib2.Request(SiteWP, data, headers)

        try:
            result = urllib2.urlopen(req , timeout = 25)
        except urllib2.URLError, e:
            if isinstance(e.reason , socket.timeout):
                print "Time out"
            else:
                Spyder = 1
                print e
                exit()

        content = result.read()  #Get Content
        content = content.decode('gbk')

        RawUpdate = re.findall("S\d\dE\d\d",content)  #find episode
        update = []  #Define Now Update Episode List
        for x in RawUpdate:
            if x not in update:
                update.append(x)  #update is unique list

        match = re.findall('target="_blank">(.*?).chs(.*?)eng(.*?).srt',content)  #match Chinese srt files
        if match:
            for x in range(len(match)):
                match[x] = match[x][0]
        match2 = re.findall('target="_blank">(.*?).chs(.*?)eng(.*?).ass',content)
        if match2:
            for x in range(len(match2)):
                match2[x] = match2[x][0]
        match.extend(match2)         #?????????????????????????????
        
        
        tittle = re.findall('<meta name="description" content="(.*?),',content)  #episode's name
        
        AllInfo[abc].extend(['Mark'])
        AllInfo[abc].extend(tittle)
        AllInfo[abc].extend(update)
        AllInfo[abc].extend(match)
        Spyder[abc] = 1
        abc = abc + 1
        
        print '线程',abc,'运行完毕！'

Model = Spider()
abc = 0

for x in range (5):
    SiteWP = Site[x-1]
    t = threading.Thread( target = Model.EpisodeSpider, args = ())
    t.start()
for x in range (70):
    time.sleep(1)
    if 0 not in Spyder:
        for x in range (abc):
            for k in AllInfo[x]:
                    Data.append(k)
        break

for x in Data:
    print x