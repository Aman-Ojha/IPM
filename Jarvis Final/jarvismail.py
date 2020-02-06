import os
import email
import imaplib
import getpass
from bs4 import BeautifulSoup
import os
import mimetypes
import tkinter.simpledialog as simpledialogs
import tkinter
from tkinter import *


mail=""


def login():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    print(type(mail))
    #mail.login(username,getpass.getpass(prompt="Password: ",stream=None))
    mail.login(simpledialog.askstring(title="Fetch Mail",prompt="Enter User Name"),simpledialog.askstring(title="Fetch Mail",prompt="Enter Password"))
    mail.select("inbox")

    status,data = mail.list()
    if(status=='OK'):
        print(mail.list())
    return mail
'''
def listemail():

    result,data=mail.uid('search',None,"ALL")
    emaillist = data[0].split()
    print("This is your inbox :")
    for i in range(len(emaillist)):
        print(i+1,")",emaillist[i],end="")
        print("")
    print("Enter Choice :")
    choice = simpledialog.askstring(title="Fetch Mail",prompt="Enter choice")
    result2, email_data = mail.uid("fetch",emaillist[int(choice)-1],'(RFC822)')
    raw = email_data[0][1].decode("utf-8")
    msg = email.message_from_string(raw)
    print(dir())
'''
def choosemail(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    print(type(mail))
    #mail.login(username,getpass.getpass(prompt="Password: ",stream=None))
    mail.login(username,password)
    mail.select("inbox")

    status,data = mail.list()
    if(status=='OK'):
        print(mail.list())
    #mail.login(username,getpass.getpass(prompt="Password: ",stream=None))
    mail.select("inbox")

    status,data = mail.list()
    if(status=='OK'):
        print(mail.list())

    result,data=mail.uid('search',None,"ALL")
    emaillist = data[0].split()
    #print(emaillist)
    ss=""
    for i in range(len(emaillist)):
        result2, email_data = mail.uid("fetch",emaillist[i],'(RFC822)')
        raw = email_data[0][1].decode("utf-8")
        msg = email.message_from_string(raw)
        ss+=str(i+1)+")"+msg['FROM']+"  "+msg['SUBJECT']+'\n'

    choice = simpledialog.askstring(title="Fetch Mail",prompt=ss+"\nEnter your choice: ")
    choice = int(choice)
    result2, email_data = mail.uid("fetch",emaillist[choice-1],'(RFC822)')
    raw = email_data[0][1].decode("utf-8")
    msg = email.message_from_string(raw)
    from_=msg['FROM']
    subject_=msg['SUBJECT']
    date_=msg['DATE']
    ss=""
    ss+="\nFROM : "+from_
    ss+="\nSUBJECT: "+subject_
    ss+="\nDATE: "+date_
    ss
    ss+="\nBODY: "
    counter = 1
    for part in msg.walk():
        if part.get_content_maintype()=="multipart":
            continue
        content_type = part.get_content_type()
        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(content_type)
            if not ext:
                exit = ".bin"
            filename = 'msg-part-%08d%s'%(counter,ext)
        counter+=1
    #saving file
    save_path=os.path.join(os.getcwd(),"emails",date_,subject_)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(os.path.join(save_path, filename),'wb') as fp:
        fp.write(part.get_payload(decode=True))

    if "plain" in content_type:
        ss+=part.get_payload()
    elif "html" in content_type:
        html_=part.get_payload()
        soup = BeautifulSoup(html_,"html.parser")
        text = soup.get_text()
        ss+=text
    else:
        print(content_type)
    return ss
