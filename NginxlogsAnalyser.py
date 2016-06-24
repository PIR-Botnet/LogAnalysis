import time
import re
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import datetime

class Nginx(object):
    filename = 'Nginxaccess.log'
    botmasterResource = ['/','/abc','/cca','/bac/acb/abc/?abc=2','/cba/abc/abc/?bca=0','/presentations/','/blog','/twiki/bin']
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
        try:
            f=open(self.filename, 'r')
        except IOError:
            print ('\n!!file %s does not exits' % nginx.filename)
            exit(0)
        data = f.readlines()
        for line in data:
            linedata = line.split(' ')
            #print (linedata[6])
            ip = linedata[0]
            str1 = re.split('[[:/]',linedata[3])
            temps = str1[3]+ '-' + str(self.getMonth(str1[2])).zfill(2)+ '-'+ str1[1]+ ' ' +str1[4]+':'
            minute = int(str1[5])
            temps = self.getTemps(temps,minute)
            temps = time.mktime(time.strptime(temps,'%Y-%m-%d %H:%M'))
            if (temps in self.totalActivity):
                self.totalActivity[temps] += 1
            else:
                self.totalActivity[temps] = 1
                
            if (ip in self.botIP):
                str1 = re.split('[[:/]',linedata[3])
                temps = str1[3]+ '-' + str(self.getMonth(str1[2])).zfill(2)+ '-'+ str1[1]+ ' ' +str1[4]+':'
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
            
        print (self.totalBotNumber)
        lastnum = 0
        firstStamp = sorted(self.botDictionary.keys())[0]
        lastStamp = sorted(self.botDictionary.keys())[-1]
        stamp = firstStamp
        while(stamp != lastStamp):
            if stamp not in self.botDictionary:
                self.botDictionary[stamp] = 0
            if stamp not in self.botActivity:
                self.botActivity[stamp] = 0
            if stamp not in self.totalActivity:
                self.totalActivity[stamp] = 0
            stamp = time.strftime('%Y-%m-%d %H:%M',time.localtime(stamp))
            stamp = datetime.datetime.strptime(stamp,'%Y-%m-%d %H:%M')
            stamp += datetime.timedelta(minutes = 5)
            stamp = time.mktime(stamp.timetuple())

        firstStamp = sorted(self.botsNumberIn30Minutes.keys())[0]
        lastStamp = sorted(self.botsNumberIn30Minutes.keys())[-1]
        stamp = firstStamp
        while(stamp != lastStamp):
            if stamp not in self.botsNumberIn30Minutes:
                self.botsNumberIn30Minutes[stamp] = []
            stamp = time.strftime('%Y-%m-%d %H:%M',time.localtime(stamp))
            stamp = datetime.datetime.strptime(stamp,'%Y-%m-%d %H:%M')
            stamp += datetime.timedelta(minutes = 30)
            stamp = time.mktime(stamp.timetuple())
        timelist = []
        anothertimelist = []
        for k in sorted(self.botDictionary.keys()):
            self.botDictionary[k] += lastnum
            timelist.append(time.strftime('%Y-%m-%d %H:%M',time.localtime(k)))
            print (time.strftime('%Y-%m-%d %H:%M',time.localtime(k))+'------ %d' % self.botDictionary[k])
            lastnum = self.botDictionary[k]
            self.bots.append(self.botDictionary[k])
            
        for k in sorted(self.botActivity.keys()):
            print (time.strftime('%Y-%m-%d %H:%M',time.localtime(k))+'------Activities------ %d' % self.botActivity[k])
            self.botsactivity.append(self.botActivity[k])
            
        for k in sorted(self.botsNumberIn30Minutes.keys()):
            anothertimelist.append(time.strftime('%Y-%m-%d %H:%M',time.localtime(k)))
            print (time.strftime('%Y-%m-%d %H:%M',time.localtime(k))+'------30minutes------ %d' % len(self.botsNumberIn30Minutes[k]))
            self.botsNumber.append(len(self.botsNumberIn30Minutes[k]))

        totalactivity = []
        for k in sorted(self.totalActivity.keys()):
            totalactivity.append(self.totalActivity[k])
        self.paint(self.bots,self.botsactivity,self.botsNumber,totalactivity,timelist,anothertimelist)
       
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
        elif(minute <60):
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
    
    def paint(self,bots,botsalive,botsNumber,totalactivity,temps,temps30minutes):
        plt.figure('number of bots')
        plt.xlabel(u'time/5minute')
        plt.ylabel(u'number of bots')
        plt.plot(bots)
        plt.figure('number of bots activity')
        plt.xlabel(u'time/5minute')
        plt.ylabel(u'number of bot activities')
        plt.plot(totalactivity,label = "total activity")
        plt.plot(botsalive,label = "bot activity")
        pl.legend()
        plt.figure('number of bots within 30 minutes')
        plt.xlabel(u'time/30minute')
        plt.ylabel(u'number of bots within 30 minutes')
        plt.plot(botsNumber)
        plt.show()
        
if __name__ == '__main__':
    nginx = Nginx()
    nginx.analysis()
