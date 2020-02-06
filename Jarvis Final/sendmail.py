import smtplib
import pandas as pd
import tkinter
from tkinter import *
def qmail(x,sub,msg):
    df=pd.read_csv("email.csv")
    idx = pd.Index(df['Name'])
    d=dict({})
    for i in range(len(df)):
        d[i]=df['Emailid'][i],df['Password'][i]
        
#print("#########################################################")
    #x=x.split()
    x=[word for word in x if word not in ["to","a","an","it","and","mail","email","also","including","include","in","that","this","send"]]
    
    mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
    mailServer.starttls()
#msg = input("What is your message? \n ")
    msg = 'Subject: {}\n\n{}'.format(sub, msg)
    print()
    if "from" in x:
        if "all" in x:
            for i in range(len(x)):
                if x[i]=="from":
                    from_ad=idx.get_loc(x[i+1])
            mailServer.login(d[from_ad][0] ,d[from_ad][1])
            for i in range(len(df)):
                mailServer.sendmail(d[from_ad][0], d[i][0] , msg)
                print("Sent Mail to",d[i][0])
        else:
            for i in range(len(x)):
                if x[i]=="from":
                    from_ad=idx.get_loc(x[i+1])
            
            mailServer.login(d[from_ad][0] ,d[from_ad][1])
            for i in range(from_ad+1,len(x)):
            
                mailServer.sendmail(d[from_ad][0], d[idx.get_loc(x[i])][0] , msg)
                print("Sent Mail to",d[idx.get_loc(x[i])][0])
    elif "all" in x:
        mailServer.login(d[0][0] ,d[0][1])

        for i in range(len(df)):
            mailServer.sendmail(d[0][0], d[i][0] , msg)
            print("Sent Mail to",d[i][0])
        
    
    else:
   # print("#",x)
        mailServer.login(d[0][0] ,d[0][1])
    
        for i in range(len(x)):
            mailServer.sendmail(d[0][0], d[idx.get_loc(x[i])][0] , msg)
            print("Sent Mail to",d[idx.get_loc(x[i])][0])
        
    

    print(" \n The Message has been Delivered")
    mailServer.quit()
