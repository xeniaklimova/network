#optional group 58
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 8000

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = []
nicknames = []


def handle(client):
    while True:

        message = client.recv(2048).decode()
        
        if not message:
            index = clients.index(client) #remove the client and its nickname off the list
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
        
        elif message[0:10] == "HELLO-FROM":
            if len(nicknames) >=1:
                client.send("BUSY\n".encode())
                return


            message = message.split()
            if(len(message) == 1):
                client.send("BAD-RQST-BODY\n".encode())

            nickname = message[1]

            
                
            while nickname in nicknames:
                client.send("IN-USE\n".encode())

            nicknames.append(nickname)
            clients.append(client)

        

            client.send("HELLO {}\n".format(nickname).encode())


            

        elif message == "WHO":
            clientstring = "WHO-OK " + ",".join(nicknames) + "\n"
            client.send(clientstring.encode())
            
        elif message[0:4] == "SEND":
            message = message.split()
            receiver = message[1]

            if len(message) < 3:
                client.send("BAD-RQST-BODY\n".encode())
                return

            statement = " ".join(message[2:])


            if(receiver in nicknames):
                
                index_receiver = nicknames.index(receiver)
                tobesent = clients[index_receiver]
                sender_index = clients.index(client)
                sender = nicknames[sender_index]

                servermsg = "DELIVERY " + "".join(sender)  + " " + statement + "\n"
                client.send("SEND-OK\n".encode())
                tobesent.send(servermsg.encode())


            else:
                client.send("UNKNOWN\n".encode())


        else:
            client.send("BAD-RQST-HDR\n".encode())
        
        
def receive():
    while True:
        # accept connection
        client, address = server.accept()


        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

        

print("Server is listening...")
receive()