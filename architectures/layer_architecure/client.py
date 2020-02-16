# clien socket tcp
from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
s.send("hello world")
data = s.recv(1024) # receive the response
print(data)
s.close()
# connection oriented service
