import random
from Bot import *
from notBot import *
import time
import datetime
import multiprocessing

global_time = time.time()
print ("start time : " + time.strftime('%d-%b-%Y:%H:%M:%S',time.localtime(global_time)))

def generate_mrp(bot):
    method_list = ['GET','HEAD','POST']
    botmasterResource = '/twitter/login/botmaster'
    notBotmasterResource = '/twitter/login/notbotmaster'
    parameterList = ['index','scm','acm','admin','guest']
    if (bot):
        method = method_list[random.randint(0, 1)]
        resource = '/%s/?%s=%s' % (botmasterResource,parameterList[random.randint(0, 4)],random.randint(0,3))
        return '\"%s %s HTTP/1.1\"' % (method,resource)
    else:
        method = method_list[random.randint(0, 2)]
        resource = '/%s/?%s=%s' % (notBotmasterResource,parameterList[random.randint(0, 4)],random.randint(0,3))
        return '\"%s %s HTTP/1.1\"' % (method,resource)

def generate_ip():
    ip = ''
    temp = []
    for i in range(4):
        id = random.randint(1, 255)
        temp.append(str(id))
    ip = '.'.join(temp)
    return ip

def generate_bot():
    Time = time.strftime('%d-%m-%Y:%H:%M:%S',time.localtime(globalTime))
    bot = Bot(Time)
    self.machineList.append(bot)

def generate_notBot():
    Time = time.strftime('%d-%m-%Y:%H:%M:%S',time.localtime(globalTime))
    notbot = notBot(Time)
    machineList.append(notbot)

def bot_loop(filename,botList,global_time):
    global number
    #print (number)
    for bot in botList:
        number = bot.activity(global_time,filename,number)
    
def notBot_loop(filename,notBotList,global_time):
    global number
    #print (number)
    for notBot in notBotList:
        number = notBot.activity(global_time,filename,number)

#start here
print ('please enter the number of log to generate')
while True:
    try:
        number = int(input())
    except NameError:
        print  ('please enter an number')
        continue
    if number <= 0:
        print ('please enter an possitive number')
        continue 
    break
print ('please enter the number of bots')
botNumber = int(input())
print ('please enter the number of notbots')
notBotNumber = int(input())
print ('please enter a filename to output the apache log data')
filename = input()
botList = []
notBotList = []
for i in range(botNumber):
    bot = Bot(global_time)
    botList.append(bot)
for i in range(botNumber):
    notbot = notBot(global_time)
    notBotList.append(notbot)

while number:
    if (random.randint(0,botNumber+notBotNumber)<botNumber):
        for bot in botList:
            number = bot.activity(global_time,filename,number)
    if (random.randint(0,botNumber+notBotNumber)<notBotNumber):
        for notbot in notBotList:
            number = notbot.activity(global_time,filename,number)
    global_time = time.strftime('%d-%b-%Y:%H:%M:%S',time.localtime(global_time))
    date_time = datetime.datetime.strptime(global_time,'%d-%b-%Y:%H:%M:%S')
    date_time = date_time + datetime.timedelta(seconds = random.randint(1,60))
    global_time = time.mktime(date_time.timetuple())

print('Fin')
