import ssl
import os
import socket
import datetime
import time
LOCAL_HOST = socket.gethostname()
##Basic code to set up Client connecting to Server, and verifying the certificate, certificate name had to be Hostmachine name




def printallGroups(allgroups):
    print('Here is all the groups currently in the message boards')
    for i in range(len(allgroups)):
        myString = allgroups[i].replace("\n", "");
        print(myString)


def printCommands():
    print("\n POST - Post a message to a group under your username")
    print("\n GET - Get all of the messages of a group ")
    print("\n END - Log out of your account")
    print("\n CLOSE - Close the connection")
    print("\n NON - Do nothing")


def END(conn):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'domain.crt')
    context.load_verify_locations(filename)
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=socket.gethostname())
    # print(filename)

    conn.connect((LOCAL_HOST, 8000))
    cert = conn.getpeercert()
    # Code to obtain account information from user

    allgroups = []
    username = raw_input(
        'Enter your username, if you do not have an account; this will become your new account username(max length is 1023 characters)\n')
    conn.send(username)
    print('User name has been verified\n')
    password = raw_input('Enter your password->(max length is 1023 characters)')
    conn.send(password)
    flag = conn.recv(1024)

    if (flag == 'Invalid'):
        iv = 0
        print('Invalid user name or password, enter a new login username or correct password')
        while ResetLoginInfo(conn) == False:

            iv += 1
            if (iv == 3):
                print('Client is timed out due to numerous password failures, try again in 5 mins')
                time.sleep(300)

            print('Invalid user name or password, enter a new login username or correct password')
    else:
        if (flag == 'True'):
            print('Welcome back %s' % username)
        else:
            print('Welcome to the boards %s' % username)

    # makenewaccountpassword = raw_input('Enter your new password(max length is 1023 characters)')
    while True:
        sizeofallgroups = conn.recv(1024)
        if int(sizeofallgroups) == 0:
            print('There are currently No groups, if you would like to make one, use the POST command')
        else:
            i = 0
            # print(sizeofallgroups)
            while i < int(sizeofallgroups):
                data = conn.recv(1024)
                allgroups.append(data)
                i = i + 1

        printallGroups(allgroups)
        allgroups = []
        input = raw_input('Enter one of the following commands, GET;POST;END;CLOSE;HELP;NON\n')

        conn.send(input)
        if (input == 'POST'):

            group = raw_input('Enter the group you wish to post a message to \n')
            message = raw_input('Enter the message you wish to post \n')
            while len(message) == 0 or len(group) == 0:
                print('Blank input is not allowed, try again')
                group = raw_input('Enter the group you wish to post a message to \n')
                message = raw_input('Enter the message you wish to post \n')
            conn.send(group)
            conn.send(message)
            print(conn.recv(1024))

        elif input == 'GET':
            group = raw_input('Enter the group you wish to retrieve messages from \n')
            while len(group) == 0:
                print('Blank input is not allowed, try again')
                group = raw_input('Enter the group you wish to post a message to \n')
            conn.send(group)
            sizeofmessages = int(conn.recv(1024))
            messages = 10000 * [None]
            if sizeofmessages == 0:
                print("There are no messages in this group, perhaps you like to POST")
            else:
                i = 0
                while i < sizeofmessages:
                    data = conn.recv(1024)
                    myString = data.replace("\n", "");
                    if data != '\n':
                        print(myString)
                    i = i + 1
        elif input == 'END':
            print('You are now logged out,if you wish to sign back, go through the steps once again')
            END(conn)
            break;
        elif input == 'CLOSE':
            break;
        elif input == 'HELP':
            printCommands()
        elif input == 'NON':
            continue;
        else:
            print('No valid command entered')


def ResetLoginInfo(conn):
    username = raw_input(
    'Enter your username, if you do not have an account; this will become your new account username(max length is 1023 characters)\n')
    conn.send(username)
    print('User name has been verified\n')
    password = raw_input('Enter your password->(max length is 1023 characters)')
    conn.send(password)
    flag = conn.recv(1024)
    if(flag == 'Invalid'):
     return False
    else:
        if (flag == 'True'):
            print('Welcome back %s' % username)
        else:
            print('Welcome to the boards %s' % username)
        return True


def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'domain.crt')
    context.load_verify_locations(filename)
    conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname = socket.gethostname())
    #print(filename)

    conn.connect((LOCAL_HOST, 8000))
    cert = conn.getpeercert()
    #Code to obtain account information from user


    allgroups = []
    username = raw_input(
        'Enter your username, if you do not have an account; this will become your new account username(max length is 1023 characters)\n')
    conn.send(username)
    print('User name has been verified\n')
    password = raw_input('Enter your password->(max length is 1023 characters)')
    conn.send(password)
    flag = conn.recv(1024)

    if (flag == 'Invalid'):
        iv = 0
        print('Invalid user name or password, enter a new login username or correct password')
        while ResetLoginInfo(conn) == False:

            iv += 1
            if (iv == 3):
                print('Client is timed out due to numerous password failures, try again in 5 mins')
                time.sleep(300)

            print('Invalid user name or password, enter a new login username or correct password')
    else:
        if (flag == 'True'):
            print('Welcome back %s' % username)
        else:
            print('Welcome to the boards %s' % username)

    # makenewaccountpassword = raw_input('Enter your new password(max length is 1023 characters)')
    while True:
        sizeofallgroups = conn.recv(1024)
        if int(sizeofallgroups) == 0:
            print('There are currently No groups, if you would like to make one, use the POST command')
        else:
            i = 0
            # print(sizeofallgroups)
            while i < int(sizeofallgroups):
                data = conn.recv(1024)
                allgroups.append(data)
                i = i + 1

        printallGroups(allgroups)
        allgroups = []
        input = raw_input('Enter one of the following commands, GET;POST;END;CLOSE;HELP;NON\n')

        conn.send(input)
        if (input == 'POST'):

            group = raw_input('Enter the group you wish to post a message to \n')
            message = raw_input('Enter the message you wish to post \n')
            while len(message) == 0 or len(group) == 0:
                print('Blank input is not allowed, try again')
                group = raw_input('Enter the group you wish to post a message to \n')
                message = raw_input('Enter the message you wish to post \n')
            conn.send(group)
            conn.send(message)
            print(conn.recv(1024))

        elif input == 'GET':
            group = raw_input('Enter the group you wish to retrieve messages from \n')
            while  len(group) == 0:
                print('Blank input is not allowed, try again')
                group = raw_input('Enter the group you wish to post a message to \n')
            conn.send(group)
            sizeofmessages = int(conn.recv(1024))
            messages = 10000 * [None]
            if sizeofmessages == 0:
                print("There are no messages in this group, perhaps you like to POST")
            else:
                i = 0
                while i < sizeofmessages:
                    data = conn.recv(1024)
                    myString = data.replace("\n", "");
                    if data != '\n':
                        print(myString)
                    i = i + 1
        elif input == 'END':
            print('You are now logged out,if you wish to sign back, go through the steps once again')
            END(conn)
            break;
        elif input == 'CLOSE':
            break;
        elif input == 'HELP':
            printCommands()
        elif input == 'NON':
            continue;
        else:
            print('No valid command entered')







    conn.close();



if __name__ == "__main__":
    main()


