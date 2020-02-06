import JiraForJarvis as lib

url="https://jarvissih2020.atlassian.net"
uname="shobitpuri.sih@gmail.com"
passToken="Vy5H1diG8D3F6mDhQBeoAC68"

lib.Initalize(url,uname,passToken)

print("Please enter your command : ")
x = input()
lib.SetCommand(x)
