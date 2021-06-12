import re

# msg = 'halo @user apa kabarnya'

# userName = 'user'

userName = 'userr'

sender = 'manusia'

msg = sender+' : halo @userr apa kabarnya'

# test = arrmsg[1].split('@')
# print('msg')
# print('arrmsg')
# print('tess parse @:',test)

def checkTag(msg):
    arrmsg = msg.split(' ')
    for i in range(len(arrmsg)):
        # print('check arrmsg:',arrmsg[i])
        if(re.search('@',arrmsg[i])):
            userMention = arrmsg[i].split('@')
            if(userMention[1]== userName):
                return(True)

def parseSender(msg):
    if(msg!=''):
        arrmsg = msg.split(' : ')
        return(arrmsg[0])

sender = parseSender(msg)
if (checkTag(msg)):
    print(sender,'is tagging you')
    print('(*) '+msg)
else:
    print('- '+msg)
