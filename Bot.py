import random
import time
import datetime
from faker import *

class Bot:
    awake = 1
    ip = '127.0.0.1'
    mrp = '\"METHODE /default PROTOCOL\"'
    time = '[Day/Month/Year:Hour:Minute:Second +Domain]'

    def __init__(self,localtime):
        self.time =  time.strftime('%d-%b-%Y %H:%M:%S',time.localtime(localtime))
        self.ip = self.generate_ip()
        self.mrp = self.generate_mrp(True)

    def change_ip(self):
        self.ip = self.generate_ip()

    def change_mrp(self):
        self.mrp = self.generate_mrp(True)
        
    def generate_ip(self):
        faker = Faker()
        ip = faker.ipv4()
        return ip
    
    def generate_mrp(self,bot):
        method_list = ['GET','HEAD','POST']
        botmasterResource = '/twitter/login/botmaster'
        notBotmasterResource = '/twitter/login/notbotmaster'
        parameterList = ['index','scm','acm','admin','guest']
        if (bot and random.random() < 0.5):
            method = method_list[random.randint(0, 1)]
            resource = '%s/?%s=%s' % (botmasterResource,parameterList[random.randint(0, 4)],random.randint(0,3))
            return '\"%s %s HTTP/1.1\"' % (method,resource)
        else:
            method = method_list[random.randint(0, 2)]
            resource = '%s/?%s=%s' % (notBotmasterResource,parameterList[random.randint(0, 4)],random.randint(0,3))
            return '\"%s %s HTTP/1.1\"' % (method,resource)
    
    def activity(self,global_time,filename,number):
        possibility = {'00':0.0273,'01':0.0166,'02':0.011,'03':0.008,'04':0.0066,'05':0.0065,'06':0.0091,'07':0.0164,'08':0.0332,'09':0.0481,'10':0.0556,'11':0.0564,'12':0.0553,'13':0.0575,'14':0.0583,'15':0.06,'16':0.0613,'17':0.0581,'18':0.0568,'19':0.0639,'20':0.0679,'21':0.0659,'22':0.0577,'23':0.0425}
        for k in possibility:
            possibility[k] = possibility[k]/2
        timeString = time.strftime('%d-%b-%Y:%H:%M:%S',time.localtime(global_time))
        hour = timeString.split(':')[1]
        possible = possibility[hour]
        if(random.random() < possible and number > 0):
            temp = []
            f=open(filename, 'a+')
            rand_num = random.random()
            if (rand_num < 0.01):
                self.change_ip()
            temp.append(self.ip)
            temp.append('- -')
            temp.append('['+time.strftime('%d/%b/%Y:%H:%M:%S',time.localtime(global_time))+' +0200]')
            new_mrp = self.generate_mrp(True)
            temp.append(new_mrp)
            temp.append(str(100 * random.randint(1, 3)))
            temp.append(str(random.randint(0, 2000)))
            if(number > 1):
                f.write(' '.join(temp) + '\n')
            else:
                f.write(' '.join(temp))
            f.close()
            number = number -1
            #print (hour)
            if(random.random() < 0.333 and number > 0):
                number = self.activity(global_time,filename,number)
            return number
        #print (number)
        return number
