# python 简单端口扫描
import threading
import time
import socket
import sys
import getopt


def Usage():
    print('usage:\n port_scan -t 127.0.0.1 -c')
    print(' port_scan -t 127.0.0.1 -a')
    print(' -c: scan common port')
    print(' -a: scan all port')
    sys.exit(0)

# 扫描指定端口


def scan_port(IP, PORT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((IP, PORT))
        if result == 0:
            print("**", IP, ":", PORT)
        # else:
        #     print(PORT,'未开放')
        s.close()
    except:
        print("扫描错误")

# 扫描常见端口


def scan_common(IP):
    print("Begin time:", time.ctime())
    port_list = (21, 22, 23, 25, 69, 80, 110, 443, 1080, 1158, 1433,
                 1521, 2100, 3128, 3389, 7001, 8080, 8081, 9080, 9090)
    for PORT in port_list:
        scan = threading.Thread(target=scan_port, args=(IP, PORT))
        scan.start()
    sys.exit(0)
# 扫描所有端口


def scan_all(IP):
    print("begin time:", time.ctime())
    for PORT in range(1, 65536):
        scan = threading.Thread(target=scan_port, args=(IP, PORT))
        scan.start()

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ht:ca')
    except:
        print('error')
        Usage()
    for o, a in opts:
        if o in ('-h'):
            Usage()
        elif o in ('-t'):
            IP = a
        elif o in ('-c'):
            scan_common(IP)
        elif o in ('-a'):
            scan_all(IP)
        else:
            print('参数错误')
