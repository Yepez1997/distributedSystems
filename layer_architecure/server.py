from socket import *
s = socket(AF_INET, SOCK_STREAM)
(conn, addr) = s.accept()
while True:
    data = conn.recv(1024) # receive 1024 bytes
    if not data: break
    conn.send(str(data) + "*")
conn.close()
