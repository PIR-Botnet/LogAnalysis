import time
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pylab as pl
import datetime

class Apache(object):
    filename = 'final.log'
    botmasterResource = ['/abc','/cca','/bac/acb/abc/?abc=2','/cba/abc/abc/?bca=0','/presentations/','/blog','/twitter/login/botmaster']
    botIP = []
    totalBotNumber = 0
    botDictionary = {}
    botActivity = {}
    totalActivity = {}
    bots = []
    botsactivity = []
    botsNumberIn30Minutes = {}
    botsNumber = []
    
    def analysis(self):
        linedata = []
        with open(self.filename) as file:
            for line in file:
                linedata = line.split(' ')
                ip = linedata[0]
                str1 = re.split('[[:/]',linedata[3])
                temps = str1[3] + '-' + str(self.getMonth(str1[2])).zfill(2) + '-' + str1[1] + ' ' + str1[4] + ':'
                minute = int(str1[5])
                temps = self.getTemps(temps,minute)
                temps = time.mktime(time.strptime(temps,'%Y-%m-%d %H:%M'))
                if (temps in self.totalActivity):
                    self.totalActivity[temps] += 1
                else:
                    self.totalActivity[temps] = 1
                    
                if (ip in self.botIP):
                    str1 = re.split('[[:/]',linedata[3])
                    temps = str1[3] + '-' + str(self.getMonth(str1[2])).zfill(2) + '-' + str1[1] + ' ' + str1[4] + ':'
                    minute = int(str1[5])
                    temps = self.getTemps(temps,minute)
                    temps = time.mktime(time.strptime(temps,'%Y-%m-%d %H:%M'))
                    if (temps in self.botActivity):
                        self.botActivity[temps] += 1
                    else:
                        self.botActivity[temps] = 1

                
                try:
                    if (self.rightResource(linedata[6]) and ip not in self.botIP):
                        self.totalBotNumber += 1
                        self.botIP.append(ip)
                        self.botIP.append(linedata[0])
                        str1 = re.split('[[:/]',linedata[3])
                        temps = str1[3]+ '-' + str(self.getMonth(str1[2])).zfill(2)+ '-'+ str1[1]+ ' ' +str1[4]+':'
                        minute = int(str1[5])
                        temps = self.getTemps(temps,minute)
                        temps = time.mktime(time.strptime(temps,'%Y-%m-%d %H:%M'))
                        if (temps in self.botDictionary):
                            self.botDictionary[temps] += 1
                        else:
                            self.botDictionary[temps] = 1
                        if (temps in self.botActivity):
                            self.botActivity[temps] += 1
                        else:
                            self.botActivity[temps] = 1
                except IndexError:
                    continue

                if (ip in self.botIP):
                    str1 = re.split('[[:/]',linedata[3])
                    temps = str1[3]+ '-' + str(self.getMonth(str1[2])).zfill(2)+ '-'+ str1[1]+ ' ' +str1[4]+':'
                    minute = int(str1[5])
                    temps30Minutes = self.getTemps30Minutes(temps,minute)
                    temps30Minutes = time.mktime(time.strptime(temps30Minutes,'%Y-%m-%d %H:%M'))
                    if (temps30Minutes not in self.botsNumberIn30Minutes):
                        self.botsNumberIn30Minutes[temps30Minutes] = []
                    if(ip not in self.botsNumberIn30Minutes[temps30Minutes]):
                        self.botsNumberIn30Minutes[temps30Minutes].append(ip)
            
        print ("total bots number = ",self.totalBotNumber)
        lastnum = 0
        firstStamp = sorted(self.botDictionary.keys())[0]
        lastStamp = sorted(self.botDictionary.keys())[-1]
        stamp = firstStamp
        while(stamp <= lastStamp):
            if stamp not in self.botDictionary:
                self.botDictionary[stamp] = 0
            stamp = time.strftime('%Y-%m-%d %H:%M',time.localtime(stamp))
            stamp = datetime.datetime.strptime(stamp,'%Y-%m-%d %H:%M')
            stamp += datetime.timedelta(minutes = 5)
            stamp = time.mktime(stamp.timetuple())

        firstStamp = sorted(self.botActivity.keys())[0]
        lastStamp = sorted(self.botActivity.keys())[-1]
        stamp = firstStamp
        while(stamp <= lastStamp):
            if stamp not in self.botActivity:
                self.botActivity[stamp] = 0
            if stamp not in self.totalActivity:
                self.totalActivity[stamp] = 0
            #print (self.botActivity[stamp])
            stamp = time.strftime('%Y-%m-%d %H:%M',time.localtime(stamp))
            stamp = datetime.datetime.strptime(stamp,'%Y-%m-%d %H:%M')
            stamp += datetime.timedelta(minutes = 5)
            stamp = time.mktime(stamp.timetuple())
            
        firstStamp = sorted(self.botsNumberIn30Minutes.keys())[0]
        lastStamp = sorted(self.botsNumberIn30Minutes.keys())[-1]
        stamp = firstStamp
        while(stamp <= lastStamp):
            if stamp not in self.botsNumberIn30Minutes:
                self.botsNumberIn30Minutes[stamp] = []
            stamp = time.strftime('%Y-%m-%d %H:%M',time.localtime(stamp))
            stamp = datetime.datetime.strptime(stamp,'%Y-%m-%d %H:%M')
            stamp += datetime.timedelta(minutes = 30)
            stamp = time.mktime(stamp.timetuple())
        timelist = []
        anothertimelist = []
        justanothertimelist = []
        for k in sorted(self.botDictionary.keys()):
            self.botDictionary[k] += lastnum
            timelist.append(time.strftime('%Y-%m-%d %H:%M',time.localtime(k)))
            print (time.strftime('%Y-%m-%d %H:%M',time.localtime(k))+'------ %d' % self.botDictionary[k])
            lastnum = self.botDictionary[k]
            self.bots.append(self.botDictionary[k])
            
        for k in sorted(self.botActivity.keys()):
            justanothertimelist.append(time.strftime('%Y-%m-%d %H:%M',time.localtime(k)))
            print (time.strftime('%Y-%m-%d %H:%M',time.localtime(k))+'------Activities------ %d' % self.botActivity[k])
            self.botsactivity.append(self.botActivity[k])
            
        for k in sorted(self.botsNumberIn30Minutes.keys()):
            anothertimelist.append(time.strftime('%Y-%m-%d %H:%M',time.localtime(k)))
            print (time.strftime('%Y-%m-%d %H:%M',time.localtime(k))+'------30minutes------ %d' % len(self.botsNumberIn30Minutes[k]))
            self.botsNumber.append(len(self.botsNumberIn30Minutes[k]))

        totalactivity = []
        for k in sorted(self.totalActivity.keys()):
            totalactivity.append(self.totalActivity[k])

        #print (self.botActivity[sorted(self.botActivity.keys())[-2]])
        x1 = []
        x2 = []
        x3 = []
        #print(justanothertimelist)
        for stringTime in timelist:
            x1.append(datetime.datetime.strptime(stringTime, "%Y-%m-%d %H:%M"))
        for stringTime in anothertimelist:
            x2.append(datetime.datetime.strptime(stringTime, "%Y-%m-%d %H:%M"))
        for stringTime in justanothertimelist:
            x3.append(datetime.datetime.strptime(stringTime, "%Y-%m-%d %H:%M"))   
        self.paint(self.bots,self.botsactivity,self.botsNumber,totalactivity,timelist,anothertimelist,x1,x2,x3)
       
    def rightResource(self,string):
        for resource in self.botmasterResource:
            if (string.startswith(resource)):
                return True
        return False
        
    def getTemps(self,temps,minute):
        if(minute < 5):
            temps += '00'
        elif(minute <10):
            temps += '05'
        elif(minute <15):
            temps += '10'
        elif(minute <20):
            temps += '15'
        elif(minute <25):
            temps += '20'
        elif(minute <30):
            temps += '25'
        elif(minute <35):
            temps += '30'
        elif(minute <40):
            temps += '35'
        elif(minute <45):
            temps += '40'
        elif(minute <50):
            temps += '45'
        elif(minute <55):
            temps += '50'
        else:
            temps += '55'
        return temps

    def getTemps30Minutes(self,temps,minute):
        if(minute <= 30):
            temps += '00'
        else:
            temps += '30'
        return temps
    
    def getMonth(self,monthstr):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if (monthstr in months):
            month = months.index(monthstr) + 1
        else:
            month = 0
        return month
    
    def paint(self,bots,botsactivity,botsNumber,totalactivity,temps,temps30minutes,x1,x2,x3):
        plt.figure('number of bots')
        plt.xlabel(u'time/5minute')
        plt.ylabel(u'number of bots')
        plt.plot(x1,bots)
        plt.gcf().autofmt_xdate()
        plt.figure('number of bots activity')
        plt.xlabel(u'time/5minute')
        plt.ylabel(u'number of bot activities')
        plt.plot(x3,totalactivity,label = "total activity")
        plt.plot(x3,botsactivity,label = "bot activity")
        plt.gcf().autofmt_xdate()
        pl.legend()
        plt.figure('number of bots within 30 minutes')
        plt.xlabel(u'time/30minute')
        plt.ylabel(u'number of bots within 30 minutes')
        plt.plot(x2,botsNumber)
        plt.gcf().autofmt_xdate()
        plt.show()
        
if __name__ == '__main__':
    apache = Apache()
    apache.analysis()
#尽量真实地模拟出一个apache日志，每个bot和非bot独立运行
#30分钟的图像横坐标以时间输出
    '''
presentation:
    更多的讲讲自己干了啥
    用了什么语言 python，怎么做的
    代码流程用流程图简要描述一遍，bot和notBot的行为方式
    流程给你用summary,log，simulation，analyse，result，amelioration
    概率分布的介绍
    注意时间，这次用了12分钟
    server anaysis? 更详细的标题 botnet log 流量分析。。。
    ---------------------
    propo:
        逻辑连贯
        client 和 bot分开
        log 加在twitter 上
        介绍log format 太长了
        botmaster和bot在twitter上做了什么
        说明我知道bot怎么运行
        simulation更靠后
        analyse   然后  evaluation
        概率分布
        删除总bot数量
        概率分布曲线和traffic一起，证明我detect bien
        30000bots +
        所有人整个projet的conclusion
    
'''
    
    
