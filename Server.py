import ssl
import os
import socket
import multiprocessing
from multiprocessing import Process
import threading
from thread import*
import hashlib
import hashlib
import random
import datetime

username_file_name = "username.txt"
password_file_name = "password.txt"
group_file_name = "groups.txt"
Salt = "kHSoJQYsLMIOTX6yI5HPDsMV7KJHed8vmhCCAsljRTqSsQ1brBRKr2JoVR2Oggpa"



LOCAL_HOST = socket.gethostname()

def writeToFile(info,nameofile):
    file = open(nameofile,"a+")
    file.write("{}\n".format(info))
    file.close

def validateInfo(info,nameofile):
    with open(nameofile,"a+") as f:
        for line in f:

            hashofinfo = hashlib.sha512(Salt+info).hexdigest()
            if hashofinfo + "\n" == line:
                return True
    file.close
    return False

def getGroups(nameofile,groups_file_name):
    groups_file_names = []
    with open(nameofile, "a+") as f:
        for line in f:
            #print(line)
            groups_file_names.append(line)
    file.close
    return groups_file_names

def getMessages(nameoffile):
    messages = []
    with open(nameoffile, "a+") as f:
        for line in f:
            messages.append(line)
    file.close
    return messages




def sendallGroups(allgroups,conn):
    for  i in range(len(allgroups)):
        # print(allgroups[i])
        conn.send(allgroups[i])
def CheckifGroupExists(group):

    with open(group_file_name, "a+") as f:
        for line in f:
            if group + "\n" == line:
                return True
    return False

def POST(group,message,username):
    s = group + ".txt"
    signedmessage = '%s %s' %(message,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    writeToFile(signedmessage,s)


def clientreset(conn):
    groups_file_names = []
    username = conn.recv(1024)
    flag = validateInfo(username, username_file_name)
    message = 'True'
    if (flag == False):
        Hashed_UN = hashlib.sha512(Salt + username).hexdigest()
        # print(Hashed_UN)
        # Checking for user name, if not there write new user name
        writeToFile(Hashed_UN, username_file_name)
        message = 'False'

    password = conn.recv(1024)
    if (flag == False):
        Hashed_PW = hashlib.sha512(Salt + password).hexdigest()
        # print(Hashed_UN)
        # Checking for user name, if not there write new user name
        writeToFile(Hashed_PW, password_file_name)
    flag2 = validateInfo(password, password_file_name)

    if (flag2 == False):
        conn.send('Invalid')
        while ResetLoginInfo(conn) == False:
            a = 6




    else:
        conn.send(message)

    while True:
        groups_file_names = []
        allgroups = getGroups(group_file_name, groups_file_names)
        sss = str(len(allgroups))
        conn.send(sss)
        # print(len(allgroups))
        if len(allgroups) != 0:
            # print(len(allgroups))
            sendallGroups(allgroups, conn)
            groups_file_names = []
        command = conn.recv(1024)
        if command == 'POST':
            group = conn.recv(1024)
            message = conn.recv(1024)
            POST(group, message, username)
            if CheckifGroupExists(group) == False:
                writeToFile(group, group_file_name)
                a = 5
            conn.send('Message has been written successfully to group %s' % group)

        elif command == 'GET':
            group = conn.recv(1024)
            groupfilename = group + ".txt"
            messages = getMessages(groupfilename)
            conn.send(str(len(messages)))
            sendallGroups(messages, conn)
        elif command == 'END':
            clientreset(conn)
            break
        elif command == 'CLOSE':
            break

def ResetLoginInfo(conn):
    username = conn.recv(1024)
    flag = validateInfo(username, username_file_name)
    message = 'True'
    if (flag == False):
        Hashed_UN = hashlib.sha512(Salt + username).hexdigest()
        # print(Hashed_UN)
        # Checking for user name, if not there write new user name
        writeToFile(Hashed_UN, username_file_name)
        message = 'False'

    password = conn.recv(1024)
    if (flag == False):
        Hashed_PW = hashlib.sha512(Salt + password).hexdigest()
        # print(Hashed_UN)
        # Checking for user name, if not there write new user name
        writeToFile(Hashed_PW, password_file_name)
    flag2 = validateInfo(password, password_file_name)
    if(flag2 == False):
        conn.send('Invalid')
        return False
    else:
        if(flag == False):
         conn.send('False')
        else:
            conn.send('True')
        return True








def clienthread(conn,Totalnumberofclients):

    groups_file_names = []
    username = conn.recv(1024)
    flag = validateInfo(username,username_file_name)
    message = 'True'
    if(flag == False):
     Hashed_UN = hashlib.sha512(Salt+username).hexdigest()
    #print(Hashed_UN)
    #Checking for user name, if not there write new user name
     writeToFile(Hashed_UN,username_file_name)
     message = 'False'

    password = conn.recv(1024)
    if(flag == False):
        Hashed_PW = hashlib.sha512(Salt + password).hexdigest()
        # print(Hashed_UN)
        # Checking for user name, if not there write new user name
        writeToFile(Hashed_PW, password_file_name)
    flag2 = validateInfo(password, password_file_name)

    if (flag2 == False):
        conn.send('Invalid')
        while ResetLoginInfo(conn) == False:
            a = 6




    else:
        conn.send(message)


    while True:
        groups_file_names = []
        allgroups = getGroups(group_file_name,groups_file_names)
        sss = str(len(allgroups))
        conn.send(sss)
        # print(len(allgroups))
        if len(allgroups) != 0:
            #print(len(allgroups))
            sendallGroups(allgroups, conn)
            groups_file_names = []
        command = conn.recv(1024)
        if command == 'POST':
            group = conn.recv(1024)
            message = conn.recv(1024)
            POST(group,message,username)
            if CheckifGroupExists(group) == False:
              writeToFile(group,group_file_name)
              a = 5
            conn.send('Message has been written successfully to group %s' % group)

        elif command == 'GET':
            group = conn.recv(1024)
            groupfilename = group + ".txt"
            messages = getMessages(groupfilename)
            conn.send(str(len(messages)))
            sendallGroups(messages,conn)
        elif command == 'END':
            clientreset(conn)
            break
        elif command == 'CLOSE':
            break



    conn.close()



def main():
    #Basic code to set up an openssl socket for encryption of communications between server and socket

    Totalnumberofclients = 0
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    dirname = os.path.dirname(__file__)
    filename1 = os.path.join(dirname, 'domain.crt')
    filename2 = os.path.join(dirname, 'domain.key')
    context.load_cert_chain(certfile=filename1, keyfile=filename2)

    bindsocket = socket.socket()
    bindsocket.bind((LOCAL_HOST,8000))
    bindsocket.listen(5)
    print('Server is up and listening!')
    while True:
     newsocket, fromaddr = bindsocket.accept()
     conn = context.wrap_socket(newsocket, server_side=True)
     Totalnumberofclients += 1
     start_new_thread(clienthread, (conn,Totalnumberofclients))




if __name__ == "__main__":
    main()
