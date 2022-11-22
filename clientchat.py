import socket
import threading


#establish connection

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port = ("143.47.184.219", 5378)
sock.connect(host_port)


#handshake
my_username = input("Please enter your username:")
string_bytes = "HELLO-FROM " + my_username +  "\n"
complete_input = string_bytes.encode()
sock.sendall(complete_input)
data = sock.recv(4)
data = data.decode()
while data[-1] != "\n":
    newdata = sock.recv(4)
    newdata = newdata.decode()
    data +=newdata
    servermsg = data
    

from_server = servermsg.rstrip() 
from_server = servermsg.split()[0]


#make sure the user logins correctly:

while from_server == "IN-USE":

    my_username = input("Username already exists, try another one:\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_port = ("143.47.184.219", 5378)
    sock.connect(host_port)
    string_bytes = "HELLO-FROM " + my_username +  "\n"
    
    complete_input = string_bytes.encode()
    sock.sendall(complete_input)
    data = sock.recv(4)
    data = data.decode()
    servermsg = data
    while data[-1] != "\n":
        newdata = sock.recv(4)
        newdata = newdata.decode()
        data +=newdata
        servermsg = data

    from_server = servermsg.rstrip() 
    from_server = servermsg.split()[0]
    

name = servermsg.split()[1]
print("Welcome, " + name + "!")


#function to receive input and send data to the server
def take_receive():
    user_message = ""
    
    print(" Type \"!quit\" if you want to exit the program. \n Type \"!who\" to see the list of logged in users. \n Type \"@username_message\" to send a message.\n ")
    while user_message != "!quit":
        user_message = input()
        if user_message == "!who":
            string_bytes = "WHO\n"
            sock.sendall(string_bytes.encode())
            
        if user_message[0] == "@":
            data_array = user_message.split()
            receiver = data_array[0][1:]
            message = data_array[1:]
            message = ' '.join(message)

            string_bytes = "SEND " + receiver + " " + message + "\n" 
            sock.sendall(string_bytes.encode())
            
#function to receive from server and print
# function to receive from server and print
def recv_print():
    while True:
        try:
            data = sock.recv(4)
            data = data.decode()
            servermsg = data
            while data[-1] != "\n":
                newdata = sock.recv(4)
                newdata = newdata.decode()
                data +=newdata
                servermsg = data

        except OSError:
            break
        
        servermsg = servermsg.strip()
        servermsg = servermsg.split()
        if servermsg[0] == "WHO-OK": 
            print("Here are all curent users: \n" + servermsg[1])
        if servermsg[0] == "UNKNOWN": 
            print("You are trying to send a messsage to a user that doesn't exist. Please try again.\n")
        if servermsg[0] == "SEND-OK": 
            print("The message was successfully sent.\n")
        if servermsg[0] == "DELIVERY": 
            print("Message from " + servermsg[1] + ": " + " ".join(servermsg[2:]))
        if servermsg[0] == "BAD-RQST-BODY": 
            print("There is an error in the message's body. Try again.")
        if servermsg[0] == "BAD-RQST-HDR": 
            print("There is an error in the message's header. Try again.")
        if servermsg[0] == "BUSY": 
            print("Too many users on the server. Try again.")
        
        
        



t2 = threading.Thread(target=recv_print)
t2.start()
take_receive()
sock.close()
t2.join()
