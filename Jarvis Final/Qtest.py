import pandas as pd

url="https://jarvissih2020.atlassian.net"
pas=pd.read_csv("Tokens.csv")
#print(pas)
d=dict({})
for i in range(len(pas)):
    d[i]=pas['USERNAME'][i],pas['TOKEN'][i]
idx = pd.Index(pas['USER'])
#print(d)
#uname="shobitpuri.sih@gmail.com"
#passToken="Vy5H1diG8D3F6mDhQBeoAC68"
uname = input("Name:\n ")
uname=uname.split()
uname=[word for word in uname if word not in ["user"," "]]
print(uname[0])
uname=d[idx.get_loc(uname[0])]
print(uname)
passToken =uname[1]
uname=uname[0]


flag = 0

for i in range (len(pas['USERNAME'])):
    if(pas['USERNAME'][i] == uname and pas['TOKEN'][i] == passToken ):
        flag=1
        break
import JiraForJarvis as lib

if (flag):
    lib.Initalize(url,uname,passToken)
    print("Hello "+pas['USER'][i]+"\n")
    print("Please enter your command : ")
    lib.printCmd()
    x = input()
    lib.SetCommand(x)

else:
    print("Invalid Credentials")

