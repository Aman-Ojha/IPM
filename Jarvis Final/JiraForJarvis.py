import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
from bs4 import BeautifulSoup 
import webbrowser 

df=pd.read_csv("cmdlist.csv")
url = ""
username = ""
passToken = ""
auth1 = ""
cmdList=['get','create','delete','search','assign','notify']
objectList=['issue','project','user']
subobjectlist=['link']
headers1 = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
headers2 = {
    "Accept": "application/json",
}

#Setting The url,username and password
def Initalize(uname):
    x="https://jarvissih2020.atlassian.net"
    pas=pd.read_csv("Tokens.csv")
#print(pas)
    d=dict({})
    for i in range(len(pas)):
      d[i]=pas['USERNAME'][i],pas['TOKEN'][i]
    idx = pd.Index(pas['USER'])
#print(d)
#uname="shobitpuri.sih@gmail.com"
#passToken="Vy5H1diG8D3F6mDhQBeoAC68"
    
    uname=uname.split()
    uname=[word for word in uname if word not in ["user"," "]]
    print(uname)
    uname=d[idx.get_loc(uname[0])]
    print(uname)
    y =uname[1]
    uname=uname[0]
  
    global url,username,passToken,auth1
    url=x
    username=uname
    passToken=y
    auth1 = HTTPBasicAuth(uname,y)
    print("The Data passed is: ")
    print(x,uname,y)

def printCmd():
    print(df)
    
def DisplayIssueLinkType():
    api=url+"/rest/api/3/issueLinkType"
    response = requests.request(
      "GET",
      api,
      headers=headers2,
      auth=auth1
    )
    dict = json.loads(response.text)
    list = dict['issueLinkTypes']
    names=[]
    retval=""
    print("Choose your Link Type:")
    for i in range(len(list)):
        names.append(list[i]['name'])
        retval += " " + str(i+1) + ')'+ names[i] + "\n"
    return retval

def DisplayIssue():
  gpi=url+"/rest/api/3/issue/picker"
  #que=input("Enter your query: ")
  query = {
   'query': ''
 }

  response = requests.request(
     "GET",
     gpi,
     headers=headers2,
     params=query,
     auth=auth1
  )

  #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  li = json.loads(response.text)
  #print(list)
  names=[]
  print("Choose your issue(Type num)")
  retval=""
  for i in range(len(li["sections"][0]["issues"])):

    names.append(li["sections"][0]["issues"][i]["key"])
    soup=BeautifulSoup(li["sections"][0]["issues"][i]["summary"],"html.parser")
    text=soup.get_text()
    retval+=str(i+1)+')'+li["sections"][0]["issues"][i]["key"] + " : " + text+"\n"
  return retval



def SetCommand(cmd):
      if cmd=="get issue":

        GetIssue()
      elif cmd=="create issue":
        CreateIssue()
      elif cmd=="delete issue":
        DeleteIssue()
      elif cmd=="assign issue":
        AssignIssue()
      elif cmd=="notify issue":
        NotifyIssue()
      elif cmd=="create issue link":
        CreateIssueLink()
      elif cmd=="get issue link":
        GetIssueLink()
      elif cmd=="delete issue link":
        DeleteIssueLink()
      elif cmd=="create issue link type":
        CreateIssueLinkType()
      elif cmd=="delete issue link type":
        DeleteIssueLinkType()
      elif cmd=="get issue link type":
        GetIssueLinkType()
      elif cmd=="search issue":
        SearchIssue()
      elif cmd=="get watchers":
        GetWatcher()
      elif cmd=="add watchers":
        AddWatcher()
      elif cmd=="get projects":
        GetProject()
      elif cmd=="delete project":
        DeleteProject()
      elif cmd=="create project":
        CreateProject()
      elif cmd=="get comments":
        GetComments()
      else:
        print("Enter valid command")
li=[]
def SearchProject():
    api = url + "/rest/api/3/project"
    print(api)
    response = requests.request(
        "GET",
        api,
        headers=headers2,
        auth=auth1
    )
    global li
    li = json.loads(response.text)
    # print(list)
    names = []
    z="Choose your project(Type num):\n"
    for i in range(len(li)):
        names.append(li[i]["name"])
        z+=str(i + 1)+ ')'+ " "+ str(li[i]["name"])+"\n"
    return z
key=""
def SearchProjectChoice(choice):
    global key
    key = li[int(choice) - 1]["key"]
    

def DeleteProject():

    key=SearchProject()
    api = url+"/rest/api/3/project/"+key

    response = requests.request(
        "DELETE",
        api,
        auth=auth1
    )

    print(response.text)

def CreateProject():
    webbrowser.open_new("https://jarvissih2020.atlassian.net/secure/BrowseProjects.jspa?=&selectedProjectType=software")

    
summary=""
def CreateIssueSummary(s):
    global summary
    summary = s
    print("Enter your Description:-")
def CreateIssueDescrip(s):
    api=url+"/rest/api/3/issue"
    description = s
    global summary,key
    dict={
       "fields": {
          "project":
           {
              "key": key
           },
           "summary": summary,
           "description": {
              "type": "doc",
              "version": 1,
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "type": "text",
                      "text": description
                    }
                  ]
                }
              ]
            },

           "issuetype": {
              "name": "Task"
           }
       }
    }
    payload = json.dumps(dict)
    response = requests.request(
       "POST",
       api,
       data=payload,
       headers=headers1,
       auth=auth1
    )
    response = json.loads(response.text)
    
    s="A new issue "+str(response["key"])+" is created."
    return s
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

def GetIssue(key):
    #key = SearchIssue()
    #print(key)
    api=url+"/rest/api/3/issue/"+key
    response = requests.request(
      "GET",
      api,
      headers=headers2,
      auth=auth1
    )
    di = json.loads(response.text)
    retval = di['id']+'  '+di['key']+'  '+di['fields']['summary']+'  '+di['fields']['description']['content'][0]['content'][0]['text']
    return retval
def DeleteIssue():
  key=SearchIssue()
  api=url+"/rest/api/3/issue/"+key
  response = requests.request(
     "DELETE",
     api,
     auth=auth1
  )
def ChooseIssue(num):
  gpi=url+"/rest/api/3/issue/picker"
  #que=input("Enter your query: ")
  query = {
   'query': ''
 }

  response = requests.request(
     "GET",
     gpi,
     headers=headers2,
     params=query,
     auth=auth1
  )

  #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  list = json.loads(response.text)
  #print(list)
  names=[]
  print("Choose your issue(Type num)")

  choice = num
  key = list["sections"][0]["issues"][choice-1]["key"]
  return key

def SearchIssue():
  gpi=url+"/rest/api/3/issue/picker"
  que=input("Enter your query: ")
  query = {
   'query': que
 }

  response = requests.request(
     "GET",
     gpi,
     headers=headers2,
     params=query,
     auth=auth1
  )

  #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  list = json.loads(response.text)
  #print(list)
  names=[]
  print("Choose your project(Type num)")
  for i in range(len(list["sections"][0]["issues"])):

    names.append(list["sections"][0]["issues"][i]["key"])
    soup=BeautifulSoup(list["sections"][0]["issues"][i]["summary"],"html.parser")
    text=soup.get_text()
    print(i+1,')',list["sections"][0]["issues"][i]["key"] + " : " + text, end="")
    print("")
  choice = int(input())
  key = list["sections"][0]["issues"][choice-1]["key"]
  return key
def UserID(x):
  x=x.title()
  api=url+"/rest/api/3/users/search"
  response = requests.request(
   "GET",
   api,
   headers=headers2,
   auth=auth1
  )
  list=json.loads(response.text)
  #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  #print(list)
  for i in range(len(list)):
    if(list[i]["displayName"]==x):
      userid=list[i]["accountId"]
  return userid
def AssignIssue(key,userid):
  #key=SearchIssue()
  #userid=UserID()
  api= url+"/rest/api/3/issue/"+key+"/assignee"
  dict={
      "accountId": userid
    }

  payload = json.dumps(dict)

  response = requests.request(
     "PUT",
     api,
     data=payload,
     headers=headers1,
     auth=auth1
  )
  retval="Assigned"
  return retval
def AssignIssueUI(x):
  userid=UserID(x)
  global key
  api= url+"/rest/api/3/issue/"+key+"/assignee"
  dict={
      "accountId": userid
    }

  payload = json.dumps(dict)

  response = requests.request(
     "PUT",
     api,
     data=payload,
     headers=headers1,
     auth=auth1
  )
  return "Assigned to "+userid+"!"


def NotifyIssue(key,userid):
  #key=SearchIssue()
  #userid=UserID()
  api=url+"/rest/api/3/issue/"+key+"/notify"
  dict={
  "htmlBody": "The <strong>latest</strong> test results for this ticket are now available.",
  "subject": "Latest test results",
  "textBody": "The latest test results for this ticket are now available.",
  "to": {
    "voters": True,
    "watchers": True,
    "groups": [
      {
        "name": "jira-software-users"
      }
    ],
    "reporter": False,
    "assignee": False,
    "users": [
      {
        "accountId": userid,
        "active": False
      }
    ]
  },
  "restrict": {
    "permissions": [
      {
        "key": "BROWSE"
      }
    ],
    "groups": [
      {
        "name": "jira-software-users"
      }
    ]
  }
  }
  payload = json.dumps( dict )

  response = requests.request(
     "POST",
     api,
     data=payload,
     headers=headers1,
     auth=auth1
  )
  return "Notified"

  #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
def CreateIssueLink(key1,key2,type_link):
    api=url+"/rest/api/3/issueLink"
    print("Please find the outward issue:-")
    #key1 = SearchIssue()
    print("Please find the inward issue:-")
    #key2= SearchIssue()
    #type= GetIssueLinkType()
    dict = {
    "outwardIssue": {
    "key": key1
    },
    "comment": {
        "visibility": {
            "type": "group",
            "value": "jira-software-users"
        },
    "body": {
        "type": "doc",
        "version": 1,
        "content": [
                {
                    "type": "paragraph",
                    "content": [
                    {
                        "text": "Linked related issue!",
                        "type": "text"
                    }
                    ]
                }
                ]
            }
            },
    "inwardIssue": {
        "key": key2
        },
    "type": {
        "name": type_link
        }
    }
    payload = json.dumps(dict)
    response = requests.request(
    "POST",
    api,
    data=payload,
    headers=headers1,
    auth=auth1
    )

    #msg = json.loads(response.text)
    #print(msg)  #UNCOMMENT IF YOU ARE FACING ISSUES IN THIS BLOCK
    print("Link Created Successfully")
    return "Link Created Successfully"

def GetIssueLink(key):
    #key = SearchIssue()
    #print(key)
    api=url+"/rest/api/3/issue/"+key
    response = requests.request(
      "GET",
      api,
      headers=headers2,
      auth=auth1
    )
    data = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    data_json = json.loads(data)
    issuelinks = data_json['fields']['issuelinks']
    retval= ""
    for i in range (len(issuelinks)):
      retval += "\n" + key + " " + issuelinks[i]['type']['inward'] + " " + issuelinks[i]['inwardIssue']['key']

    return retval

def ShowLinks(key):
  api = url + "/rest/api/3/issue/" + key
  response = requests.request(
      "GET",
      api,
      headers=headers2,
      auth=auth1
  )
  data = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
  data_json = json.loads(data)
  issuelinks = data_json['fields']['issuelinks']
  retval = ""
  for j in range (len(issuelinks)):
    retval += " " + str(j+1) + " ) " +  key + " " + issuelinks[j]['type']['inward'] + " " + issuelinks[j]['inwardIssue']['key']

  return retval

def GetIssueLinkD(num,key):
  api = url + "/rest/api/3/issue/" + key
  response = requests.request(
      "GET",
      api,
      headers=headers2,
      auth=auth1
  )
  data = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
  data_json = json.loads(data)
  issuelinks = data_json['fields']['issuelinks']
  list_issueLinks = []
  for j in range (len(issuelinks)):
    list_issueLinks.append(issuelinks[j]['id'])

  return list_issueLinks[num-1]


def DeleteIssueLink(key):
  api1 = url+"/rest/api/3/issueLink/" + key
  response = requests.request(
    "DELETE",
    api1,
    auth=auth1
  )
  print("Issues has been deleted")
  return "Issues has been deleted"
def CreateIssueLink(key1,key2,type_link):
    api=url+"/rest/api/3/issueLink"
    print("Please find the outward issue:-")
    #key1 = SearchIssue()
    print("Please find the inward issue:-")
    #key2= SearchIssue()
    #type= GetIssueLinkType()
    dict = {
    "outwardIssue": {
    "key": key1
    },
    "comment": {
        "visibility": {
            "type": "group",
            "value": "jira-software-users"
        },
    "body": {
        "type": "doc",
        "version": 1,
        "content": [
                {
                    "type": "paragraph",
                    "content": [
                    {
                        "text": "Linked related issue!",
                        "type": "text"
                    }
                    ]
                }
                ]
            }
            },
    "inwardIssue": {
        "key": key2
        },
    "type": {
        "name": type_link
        }
    }
    payload = json.dumps(dict)
    response = requests.request(
    "POST",
    api,
    data=payload,
    headers=headers1,
    auth=auth1
    )

    #msg = json.loads(response.text)
    #print(msg)  #UNCOMMENT IF YOU ARE FACING ISSUES IN THIS BLOCK
    print("Link Created Successfully")
    return "Link Created Successfully"


def DeleteIssueLinkType():
    key=GetIssueLinkType()
    api = url+"/rest/api/3/issueLinkType/"+key

    #auth = HTTPBasicAuth("email@example.com", "<api_token>")

    response = requests.request(
        "DELETE",
        api,
        auth=auth1
    )

    print(response.text)




def AddWatcher(userid,key):
  #userid=UserID()
  #key=SearchIssue()
  payload = json.dumps(userid)
  api=url+"/rest/api/3/issue/"+key+"/watchers"
  response = requests.request(
     "POST",
     api,
     data=payload,
     headers=headers1,
     auth=auth1
  )
  #dict=json.loads(response.text)
  #print(json.dumps(dict, sort_keys=True, indent=4, separators=(",", ": ")))
  return "Watcher added"

def GetWatcher(key):
  #key=SearchIssue()
  api=url+"/rest/api/3/issue/"+key+"/watchers"

  response = requests.request(
   "GET",
   api,
   headers=headers2,
   auth=auth1
  )
  dict=json.loads(response.text)
  for i in range(len(dict["watchers"])):
    retval=dict["watchers"][i]["displayName"]
  return retval
 
def GetComments(key):
  #key=SearchIssue()
  api=url+"/rest/api/3/issue/"+key+"/comment"
  response = requests.request(
   "GET",
   api,
   headers=headers2,
   auth=auth1
  )
  list=json.loads(response.text)
  print(len(list["comments"]))
  retval=""
  for i in range(len(list["comments"])):
    retval+=list["comments"][i]["author"]["displayName"]+" : "+list["comments"][i]["body"]["content"][0]["content"][0]["text"]+" : " +list["comments"][i]["created"]+"\n"
  return retval

def GetProject():
  api=url +"/rest/api/3/project"
  response = requests.request(
   "GET",
   api,
   headers=headers2,
   auth=auth1
  )
  dic=json.loads(response.text)
  return str(json.dumps(dic, sort_keys=True, indent=4, separators=(",", ": ")))
  #return json.dumps(dict, sort_keys=True, indent=4, separators=(",", ": "))

def CreateIssueLinkType(inward,name,outward):
    api = url+"/rest/api/3/issueLinkType"
    # inward = input("Enter Inward\n")
    # name = input("Enter Name\n")
    # outward = input("Enter ")
    payload = json.dumps( {
      "inward": inward,
      "name": name,
      "outward": outward
    } )

    response = requests.request(
      "POST",
      api,
      data=payload,
      headers=headers1,
      auth=auth1
    )
    response = json.loads(response.text)
    return "A issue link type of id "+response['id']+" has been created"
    print("A issue link type of id "+response['id']+" has been created")

def GetIssueLinkType():
  api=url+"/rest/api/3/issueLinkType"
  response = requests.request(
    "GET",
    api,
    headers=headers2,
    auth=auth1
  )
  dict = json.loads(response.text)
  #list = dict['issueLinkTypes']
  retval=""
  print("Choose your Link Type:")
  for i in range(len(dict["issueLinkTypes"])):
    retval+="\n"+dict["issueLinkTypes"][i]["id"]+" : "+dict["issueLinkTypes"][i]["name"]
      

  return retval

def SearchIssue(query):
    gpi=url+"/rest/api/3/issue/picker"
    #que=input("Enter your query: ")
    query = {
     'query': query
   }

    response = requests.request(
       "GET",
       gpi,
       headers=headers2,
       params=query,
       auth=auth1
    )

    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    list = json.loads(response.text)
    #print(list)
    names=[]
    print("Choose your issue(Type num)")
    retval=""
    for i in range(len(list["sections"][0]["issues"])):

      names.append(list["sections"][0]["issues"][i]["key"])
      soup=BeautifulSoup(list["sections"][0]["issues"][i]["summary"],"html.parser")
      text=soup.get_text()
      retval+="  "+str(i+1)+')'+"  "+list["sections"][0]["issues"][i]["key"] + " : " + text+"\n"
    return retval