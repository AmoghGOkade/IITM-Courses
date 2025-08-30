#different because it stores the unread messages and (decently) handles cases when the user you are talking to is sending messages
#problems - user is a string in some places and an int in others, it gets very bad at times

from socket import *
import asyncio
import websockets
import struct
import time
import urllib.parse

client_id = 71
serverPort = 8080
prev = 0
unread = {}
show = 0    #0 for shown no new, 1 for not shown no new, 2 for same page open as sender

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1) #One connection, others dropped

print("Server is listening on port", serverPort)

basic_page = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Messenger App</title>
</head>
<body>
    
    <!-- Sidebar -->
    <div>
        <div>
            <h2>Chats</h2>
            <ul>
                {chat_list_str}
            </ul>
        </div>

        <!-- To receive -->
        <div>
            <h2>Receive</h2>
            <form method="POST" action="/recv">
                <input type='submit' value='Fetch unread messages'>
            </form>
            <ul>
                {message_list}
            </ul>
        </div>
        
        <!-- New User -->
        <div>
            <h2>Send</h2>
            <form method="POST" action="/sendmsg">
                <input type="number" min="0" max="255" name="user_id" placeholder="Type User ID..." style="width: 162px;" value="{user_id}"><br>
                <input type="text" name="message" placeholder="Type a message..."><br>
                <input type='submit' value='Send'>
            </form>
        </div>
    </div>
    
    <!-- Chat Section -->
    <div style="display: {display};">
        
        <!-- Chat Header -->
        <div>
            <h3>Chat with {user_id} </h3>
        </div>
        
        <!-- Chat Messages -->
        <div>
            {user_file}
        </div>
        
    </div>
    
</body>
</html>
'''

async def client():
    while True:
        try:
            async with websockets.connect("ws://localhost:12345") as websocket:     #replace localhost with a.b.c.d server host's IP
                message = struct.pack("!BBB", 0, 0, client_id)  #associating
                await websocket.send(message)
                recv = await websocket.recv()
                if recv[0]==0 and recv[1]==1:
                    print("Associated successfully")
                elif recv[0]==0 and recv[1]==3:     #if ass done twice
                    print("Association already there")
                
                while True:
                    try:
                        #print("In while loop")
                        #print(chat_list)
                        clientSocket, clientAddress = serverSocket.accept()
                        #print(clientAddress, clientSocket)
                        #print(1)
                        data_temp = clientSocket.recv(1024).decode('utf-8')      #gets stuck here till something is done on the website
                        request = urllib.parse.unquote_plus(data_temp)
                        #print(request)
                        headers, _, body = request.partition('\r\n\r\n')
                        lines = headers.split('\r\n')
                        #print(body)
                        request_line = lines[0]
                        method, path, _ = request_line.split()
                        #print(method, path)
                        if method == 'GET' and path == '/':     #when page is re-loaded or accessed for the first time
                            #print(3)
                            home_page(clientSocket)
                        elif method == 'GET' and path.startswith('/chat?user') and path.split('=',1)[-1] in chat_list:      #2nd param of split() - max no. of splits to do     #when a user is clicked
                            #print(3)
                            user = path.split('=',1)[-1]
                            user_page(user, clientSocket)
                            #print(user+' clicked')
                        elif method == 'POST' and path == '/sendmsg':       #when enter is hit on the message box
                            params = dict(param.split('=') for param in body.split('&'))    #params is a dict having user_id and message as keys and their values as values
                            #print(params)
                            
                            sender_id = int(params["user_id"])      #limit between 0 and 255 using html features
                            data = bytes(params['message'], "utf-8")
                            message = struct.pack("!BBBBB", 2, 1, client_id, sender_id, len(data)) + data   #can only send bytes as websocket.send()    #the length is the number of bytes of the datatype
                            await websocket.send(message)
                            recv = await websocket.recv()
                            if recv[0]==1 and recv[1]==2 and message:
                                print("Sent nicely.")
                                sendmsg(params['user_id'],params['message'], clientSocket)
                            elif recv[0]==1 and recv[1]==3:
                                print(str(sender_id)+ "\'s buffer is full. Try later.")
                                response = 'HTTP/1.1 303 See Other\r\nLocation: /chat?user='+str(sender_id)
                                clientSocket.sendall(response.encode())
                                clientSocket.close()
                            else:
                                print("Failed for some reason")
                                return
                        elif method == "POST" and path == "/recv":
                            message = struct.pack("!BBB", 1, 0, client_id)
                            await websocket.send(message)
                            recv = await websocket.recv()
                            while recv[0]==2 and recv[1]==0:
                                sender = recv[3]
                                leng = recv[4]
                                data = recv[5::]
                                add_mess(sender, str(data))
                                
                                message = struct.pack("!BBB", 1, 0, client_id)
                                await websocket.send(message)
                                recv = await websocket.recv()
                                
                            if recv[0]==1 and recv[1]==1:
                                print("No messages for you. Try later")
                                show_unread(clientSocket, "")
                            else:
                                print("Failed for some reason")
                                return
                        else:
                            nack_resp(clientSocket,"404 Not Found")
                    except websockets.exceptions.ConnectionClosedError:
                        print("Timout happened. Going back to home page.")
                        nack_resp(clientSocket,"Latest action was lost due to server timeout.\nPlease go back (<-) and try again.")
                        break
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
            how_much_time = 10
            print("Sir's server is not running. Will try running in", how_much_time,"seconds")
            time.sleep(how_much_time)

def nack_resp(clientSocket,show_err):
    response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>"+show_err+"</h1>"
    clientSocket.sendall(response.encode())
    clientSocket.close()

def home_page(clientSocket):
    global prev
    global unread
    global show
    # Inititate association, if success
    temp='\r\n'.join(['<li><a href="/chat?user='+str(s)+'">'+str(s)+'</a></li>\r\n' for s in chat_list])
    if unread=={}:
        mess_lis = ""
    else:
        mess_lis = '\r\n'.join(['<li>'+str(unread[i])+" unread from "+str(i)+'</li>\r\n' for i in unread])
    if show > 0:
        mess_lis += "No new messages"
        show = 0
    response = ('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'+basic_page).format(chat_list_str=temp,display="none",message_list=mess_lis,user_id='',user_file='')
    #check new messages and append messages to the file corresponding user. If user not in chat_list, add to user_list.txt and update chat_list
    #response = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n Association failed' #If failed respond with association failed
    prev = 0
    clientSocket.sendall(response.encode())
    clientSocket.close()

def user_page(user, clientSocket):
    global prev
    global unread
    global show
    # Inititate association, if success
    # check new messages and append messages to the file corresponding user. If user not in chat_list, add to user_list.txt and update chat_list
    try:    #to create a new file if not existant
        file = open(user+'.txt','r')
    except FileNotFoundError:
        file = open(user+'.txt','a+')
    #print("show",show)
    if show != 2:
        if int(user) in unread:
            unread.pop(int(user))
    if unread=={}:
        mess_lis = ""
    else:
        mess_lis = '\r\n'.join(['<li>'+str(unread[i])+" unread from "+str(i)+'</li>\r\n' for i in unread])
    if show > 0:
        mess_lis += "No new messages"
        show = 0
        
    temp='\r\n'.join(['<li><a href="/chat?user='+str(s)+'">'+str(s)+'</a></li>\r\n' for s in chat_list])
    response = ('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'+basic_page).format(chat_list_str=temp,display="block",message_list=mess_lis,user_id=user,user_file=file.read())
    file.close()
    prev = user
    clientSocket.sendall(response.encode())
    clientSocket.close()

def sendmsg(user_id,message, clientSocket):
    if user_id not in chat_list:
        with open('user_list.txt','a+') as file:
            file.write(user_id+'\n')
            chat_list.append(user_id)
        #print(chat_list)
    if message:     #if message is not None
        with open(user_id+'.txt','a+') as file:
            file.write('<p>You: '+message+'</p>')
    response = 'HTTP/1.1 303 See Other\r\nLocation: /chat?user='+user_id
    clientSocket.sendall(response.encode())
    clientSocket.close()

def show_unread(clientSocket, sender):  #sender is int
    global prev
    global unread
    global show
    
    if show != 2:
        show = 1
    #print(0)
    if prev==0:
        response = 'HTTP/1.1 303 See Other\r\nLocation: /'
    else:
        response = 'HTTP/1.1 303 See Other\r\nLocation: /chat?user='+prev
    #print(2)
    clientSocket.sendall(response.encode())
    clientSocket.close()

def add_mess(sender, data):
    global unread
    global show
    global prev
    #print(1)
    if sender in unread:
        unread[sender] += 1
    else:
        unread[sender] = 1
    if str(sender) == prev:  #prev is str
        show = 2
    
    user_id = str(sender)
    if user_id not in chat_list:
        with open('user_list.txt','a+') as file:
            file.write(user_id+'\n')
            chat_list.append(user_id)
    with open(user_id+'.txt','a+') as file:
        file.write('<p>' + user_id + ": " + data[2::] + '</p>')

try:
    file = open('user_list.txt','r')
    chat_list = file.read().split('\n')
    file.close()
    if chat_list[-1] == '':
        chat_list.pop()
except FileNotFoundError:
    chat_list = []

asyncio.run(client())
