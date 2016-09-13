import socket
import sys
import getopt


def  client_start(target,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))
    while True:
        cdata = input(target+':~ #')
        client.send(cdata.encode('utf8'))
        sdata=client.recv(2048)
        print(sdata.decode('utf-8'))

    client.close()
def usage():
    print("Usage: \npython shell-client.py -t 127.0.0.1 -p 12345")
    print("-h,--help")
    print("-t,--target  target ip")
    print("-p,--port    target port")
    sys.exit(0)
def main():
    global target
    global port
    args = sys.argv[1:]
    if not len(sys.argv[1:]):
        usage()

    try:
        opts,args=getopt.getopt(sys.argv[1:],"ht:p:",["help","target=","port="])
    except getopt.GetoptError as err:
        # print(str(err))
        usage()
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-t","--target"):
            target=a
        elif o in ("-p","--port"):
            port=a
        else:
            print("参数错误")
    if target is not None and port is not None:
        client_start(target,port)
    else:
        usage()
if __name__ == '__main__':
    main()
