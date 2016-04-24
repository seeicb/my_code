import socket
host='127.0.0.1'
port=12345
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)
client,addr=server.accept()
print("**Accepted connection from:%s:%d" % (addr[0],addr[1]) )
while True:
    try:
        cdata=client.recv(2048)
        if cdata.decode('utf8')=='exit':
            print('断开连接')
            break
        print('A:',cdata.decode('utf8'))
        sdata=input("输入:")
        client.send(sdata.encode('utf8'))
        if sdata=='exit':
            print('断开连接')
            break

    except:
        print('错误')
        break



client.close()
