import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import tkinter.simpledialog as simpledialogs
import tkinter
from tkinter import *
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
import sendmail as smail
import JiraForJarvis as Ji
import travel_directions as tdir

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list



def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])+"#####"
            break
    #result=
    return result
def model(input_question):
    
    input_question=" ".join([word for word in input_question if word not in ["as","jira","on","in","please","to","a","an","it","and","mail","email","also","including","include","in","that","this","send"]])
    return input_question
def chatbot_response(msg):
    
    msg=msg.split()
    '''
    if "jira" in msg and "login" in msg:
        msg=[word for word in msg if word not in ["as","in","into"]]
        print(msg)
        
        #lid = simpledialog.askstring(title="Jira",prompt="Login in as?")
        Ji.Initalize(msg[2])
    #if "jira" in msg or "issue" in msg or "watchers" in msg or "projects" in msg or "comments" in msg:
        z=model(msg)
        print(z)
        
        #us = EntryBox.get("1.0",'end-1c').strip()
       # print("#######",us,"###########")
       # Ji.Initalize(us)             
       # Ji.SetCommand(z)
       
        us = EntryBox.get("1.0",'end-1c').strip()
        print("$",us)
        EntryBox.delete("0.0",END)
        
        if us == '':
            ChatLog.insert(END, "You: " + us+"#" + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 18 ))

            
            #ChatLog.insert(END, "Jarvis: " + res + '\n\n')
            #hatLog.config(state=DISABLED)
            #ChatLog.yview(END)
        
        
        
        
        
    '''    
    if "email" in msg or "mail" in msg:
        
        w = Tk()
        w.withdraw()
        sub = simpledialog.askstring(title="Mail",prompt="What is the Subject?")
        cont = simpledialog.askstring(title="Mail",prompt="What is your message?")

        smail.qmail(msg,sub,cont)
        #ChatLog.insert(END, "Jarvis: " + "The Message has been Delivered!"+ '\n\n')
        
        
        res="The Message has been Delivered!"
    else:
        res="".join(msg)
        '''
        msg="".join(msg)
        ints = predict_class(msg, model)
        print(msg,model,ints)
        res = getResponse(ints, intents)
        '''
    return res
d="lol"
def shob(msg):
    global d
    ChatLog.config(state=NORMAL)
    ChatLog.insert(END, "You: " + msg + '\n\n')
    ChatLog.config(foreground="#442265", font=("Verdana", 18 ))
    msg=msg.split()
    if "exit" in msg or "bye" in msg or "quit" in msg or "goodbye" in msg:
        exit()
        
    if "jira" in d:
        if d=="jira AIUI":
            res=Ji.AssignIssueUI(msg[0])
            d="lol"
        if d=="jira CICP":
            Ji.SearchProjectChoice(msg[0])
            res="Enter your summary:"
            d="jira CIS"
        elif d=="jira CIS":
            Ji.CreateIssueSummary("".join(msg))
            res="Enter your Description:"
            d="jira CID"
        elif d=="jira CID":
            res=Ji.CreateIssueDescrip("".join(msg))
            d="lol"
            
                
                
                
        if "jira" in msg or "issue" in msg or "watchers" in msg or "projects" in msg or "comments" in msg:
            z=model(msg)
            print(z)
            if z=="get issue":
                l1 = Ji.DisplayIssue()
                res=l1
                        #ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please:-\n"+res)
                num = int(num)
                key=Ji.ChooseIssue(num)
                res = Ji.GetIssue(key)
                    
                    
            elif z=="create issue":
                res=Ji.SearchProject()
                d="jira CICP"
            elif z=="delete issue":
                res = Ji.DisplayIssue()
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please:-\n"+res)
                num = int(num)
                key=Ji.ChooseIssue(num)
                res ="\n"+ Ji.DeleteIssue(key)
            elif z=="assign issue":
                res = Ji.DisplayIssue()
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please(NUM):-\n"+res)
                num = int(num)
                key=Ji.ChooseIssue(num)
                uname = simpledialog.askstring(title="Enter Username",prompt="Enter full name:-\n")
                uid = Ji.UserID(uname)
                res="\n"+Ji.AssignIssue(key,uid)
            elif z=="notify issue":
                res = Ji.DisplayIssue()
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please(NUM):-\n"+res)
                num = int(num)
                key=Ji.ChooseIssue(num)
                uname = simpledialog.askstring(title="Enter Username",prompt="Enter full name:-\n")
                uid = Ji.UserID(uname)
                res ="\n"+ Ji.NotifyIssue(key,uid)
            elif z=="create issue link":
                l1 = Ji.DisplayIssue()
                res=l1
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Outward Issue",prompt="Enter you choice please:-\n"+res)
                num = int(num)
                num2 = simpledialog.askstring(title="Choose Inward Issue",prompt="Enter you choice please:-\n"+res)
                num2 = int(num2)
                l2 = Ji.DisplayIssueLinkType()
                res = l2
                num3 = simpledialog.askstring(title="Choose Issue Link Type",prompt="Enter you choice please:-\n"+res)
                num3 = int(num3)
                outward_key = Ji.ChooseIssue(num)
                inward_key = Ji.ChooseIssue(num2)
                type_link = Ji.GetIssueLinkType(num3)
                res = Ji.CreateIssueLink(outward_key,inward_key,type_link)

            elif z=="get issue link":
                l1 = Ji.DisplayIssue()
                res=l1
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please:-\n"+res)
                num = int(num)
                key = Ji.ChooseIssue(num)
                res = Ji.GetIssueLink(key)
            elif z=="delete issue link":
                l1 = Ji.DisplayIssue()
                res=l1
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please:-\n"+res)
                num = int(num)
                key = Ji.ChooseIssue(num)
                l2 = Ji.ShowLinks(key)
                res = l2
                num2 = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please:-\n"+res)
                num2 = int(num2)
                key2 = Ji.GetIssueLinkD(num2,key)
                res = Ji.DeleteIssueLink(key2)
            elif z=="create issue link type":
                inward=simpledialog.askstring(title="Inward",prompt="Enter Inward:-\n")
                name=simpledialog.askstring(title="Name",prompt="Enter Name:-\n")
                outward=simpledialog.askstring(title="Outward",prompt="Enter outward:-\n")
                res = Ji.CreateIssueLinkType(inward,name,outward)
            elif z=="delete issue link type":
                d="jira delete issue link type"
            elif z=="get issue link type":
                res="\n"+Ji.GetIssueLinkType()
                
            elif z=="search issue":
                query = simpledialog.askstring(title="Enter Query",prompt="Enter your Query:-\n")
                res="\n"+Ji.SearchIssue(query)
            elif z=="get watchers":
                l1 = Ji.DisplayIssue()
                res=l1
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please(NUM):-\n"+res)
                num = int(num)
                key=Ji.ChooseIssue(num)
                res="\n"+Ji.GetWatcher(key)
                    
            elif z=="add watchers":
                l1 = Ji.DisplayIssue()
                res=l1
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please(NUM):-\n"+res)
                num = int(num)
                key=Ji.ChooseIssue(num)
                uname = simpledialog.askstring(title="Enter Username",prompt="Enter full name:-\n")
                uid = Ji.UserID(uname)
                res="\n"+Ji.AddWatcher(uid,key)
            elif z=="get projects":
                l1 = Ji.GetProject()
                res = l1
                ChatLog.insert(END, "Project : " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Project",prompt="Enter you choice please:-\n"+res)
                num = int(num)
                key = Ji.ChooseProject(num)
                res = Ji.GetProjectDet(key)  
            elif z=="delete project":
                d="jira delete project"
            elif z=="create project":
                d="jira create project"
            elif z=="get comments":
                l1 = Ji.DisplayIssue()
                res=l1
                ChatLog.insert(END, "Jarvis: " + res + '\n\n')
                num = simpledialog.askstring(title="Choose Issue",prompt="Enter you choice please(NUM):-\n"+res)
                num = int(num)
                key=Ji.ChooseIssue(num)
                res="\n"+Ji.GetComments(key)
            else:
                res="Please enter valid command!"
    elif "jira" in msg and "login" in msg:
            
        print(msg)
        
            
            
        #lid = simpledialog.askstring(title="Jira",prompt="Login in as?")
        Ji.Initalize(msg[2])
    #if "jira" in msg or "issue" in msg or "watchers" in msg or "projects" in msg or "comments" in msg:
        z=model(msg)
        print(z)
        d="jira"
        res="Specify Task"
        
            
            
        #us = EntryBox.get("1.0",'end-1c').strip()
       # print("#######",us,"###########")
       # Ji.Initalize(us)             
       # Ji.SetCommand(z)
        #res=jfj()
      #  res = chatbot_response(msg)
    elif "search" in msg:
        msg=[word for word in msg if word not in ["jarvis","this","for","search","google"]]
        msg=" ".join(msg)
        import webbrowser
        from googlesearch import search 
        for j in search(msg, tld="co.in", num=10, stop=1, pause=0):
            res="Related Link:\n "+j
        webbrowser.open_new("https://www.google.co.in/search?q=" +(str(msg))+ "&oq="+(str(msg))+"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU")
    elif ("send" in msg and"email" in msg) or ("send" in msg and "mail" in msg):
        w = Tk()
        w.withdraw()
        sub = simpledialog.askstring(title="Mail",prompt="What is the Subject?")
        cont = simpledialog.askstring(title="Mail",prompt="What is your message?")

        smail.qmail(msg,sub,cont)
        res="The Message has been Delivered!"   
    elif "time" in msg or "date" in msg or "day" in msg:
        import datetime
        today = datetime.datetime.now()
        day_ind=today.isoweekday()
            #today=today.strftime("%Y-%m-%d %H:%M:%S").split()
        today=today.strftime("%d-%m-%Y %H:%M:%S").split()
        today.append([
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ])      
        if "time" in msg:
            res="\nTime: "+today[1]
        elif "date" in msg:
            res="\nDate: "+today[0]
        elif "day" in msg:
            res="\nDay: "+today[2][day_ind-1]
        else:
            res="\nDate: "+today[0]+"\n"+"Time: "+today[1]+"\n"+"Day: "+today[2][day_ind-1]
            
    elif "country" in msg:
        import requests
        def get_country(country):
          #  print("@##$%^&")
            url = "https://restcountries.eu/rest/v2/name/%s?fullText=true" % country
            r = requests.get(url)
            if isinstance(r.json(), dict):
                res="Country not found."
            else:
                return r.json()
        def country_info(country_fetch):
          #  print("@##$%^&")
            capital = country_fetch[0]["capital"]
            calling_code = country_fetch[0]["callingCodes"][0]
            population = country_fetch[0]["population"]
            region = country_fetch[0]["region"]
            currency = country_fetch[0]["currencies"][0]["name"]
            currency_symbol = country_fetch[0]["currencies"][0]["symbol"]
            time_zone = country_fetch[0]["timezones"][0]
            print("\nCapital: " + str(capital)+"\nCalling Code: " + str(calling_code)+"\nCurrency: " + str(currency)+"\nCurrency Symbol: " + str(currency_symbol)+"\nPopulation: " + str(population)+"\nRegion: " + str(region)+"\nTime Zone: " + str(time_zone))
            return "\nCapital: " + str(capital)+"\nCalling Code: " + str(calling_code)+"\nCurrency: " + str(currency)+"\nCurrency Symbol: " + str(currency_symbol)+"\nPopulation: " + str(population)+"\nRegion: " + str(region)+"\nTime Zone: " + str(time_zone)
        country=[word for word in msg if word not in ["country","info","information","about","this","that","tell","load","get","obtain","me","the"]]
            #print("$$$$$$$$  ",country[0])
        country_fetch = get_country(country[0])
        if country_fetch is not None:
            res=country_info(country_fetch)
        else:
            res="how may I help u?"
                
    elif "directions" in msg or "direction" in msg:
        msg=[word for word in msg if word not in ["direction","directions","from","here","office","college","to","there","that","the","city","nearest","closest","nearby"]]
        print(msg)
        tdir.main(" ".join(msg))
        res="Follow the direction"
            
    elif ("fetch" in msg and "mail" in msg )or ("fetch" in msg and "email" in msg )or("get" in msg and "mail" in msg )or ("get" in msg and "email" in msg )or("retrieve" in msg and "mail" in msg )or ("retrieve" in msg and "email" in msg ):
        import jarvismail as jm
        a=simpledialog.askstring(title="Fetch Mail",prompt="Enter User Name")
        b=simpledialog.askstring(title="Fetch Mail",prompt="Enter Password")

        res=jm.choosemail(a,b)
             
        
    else:
        res="how may I help u?"
    ChatLog.insert(END, "Jarvis: " + res + '\n\n')
    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)
#Creating GUI with tkinter

import os
import sys
d="lol"
def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    #print (sys._getframe().f_back.f_code.co_name)
    
    #X = os.path.realpath(sys.argv[0])
    #print(X)
    global d
    print("#",msg,"$",d,"$")
     
        
        
        
    EntryBox.delete("0.0",END)
    
    if msg != '':
        shob(msg)

def Speak():
    import speech_recognition as sr;
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk");
        audio=r.listen(source);
        print("Enough")
    try:
        msg=r.recognize_google(audio);
        msg=msg.lower()
    except:
        pass
    print("#",msg)
    if msg != '':
        shob(msg)
     
base = Tk()
base.title("J.A.R.V.I.S.")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",14,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter speech command
SpeakButton = Button(base, font=("Verdana",14,'bold'), text="Speak", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= Speak)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)

SendButton.place(x=255, y=401, height=45)
SpeakButton.place(x=255,y=445,height=45)
EntryBox.place(x=6, y=401, height=90, width=265)

'''root = tkinter.Tk()
root.title("I'm Listening")
label = tkinter.Label(root, fg="dark green")
label.pack()
#counter_label(label)
button = tkinter.Button(root, text='Speak', width=25, )
button.pack()
root.mainloop()'''


base.mainloop()
