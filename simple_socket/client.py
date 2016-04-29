import socket

host = '127.0.0.1'
port = 12345
# 172.18.63.42
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
while True:
    try:
        cdata = input('输入:')
        client.send(cdata.encode('utf8'))
        if cdata == 'exit':
            print('断开连接')
            break
        sdata = client.recv(2048)
        print("B:", sdata.decode('utf8'))
        if sdata.decode('utf8') == 'exit':
            print('断开连接')
            break
    except:
        print("错误")
        break

client.close()
