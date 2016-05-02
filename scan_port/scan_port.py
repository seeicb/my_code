#python 简单端口扫描
import threading,time,socket

#扫描指定端口
def scan_port(IP,PORT):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result=s.connect_ex((IP,PORT))
        if result==0:
            print("**",IP,":",PORT)
        # else:
        #     print(PORT,'未开放')
        s.close()
    except:
        print("扫描错误")

#扫描常见端口
def scan_usual(IP):
    port_list=(21,22,23,25,69,80,110,443,1080,1158,1433,1521,2100,3128,3389,7001,8080,8081,9080,9090)
    for PORT in port_list:
        scan=threading.Thread(target=scan_port,args=(IP,PORT))
        scan.start()

#扫描所有端口
def scan_all(IP):
    for PORT in range(1,65534):
        scan=threading.Thread(target=scan_port,args=(IP,PORT))
        scan.start()

if __name__ == '__main__':
    print("begin time:",time.ctime())
    scan_all('202.202.43.125')
    # scan_usual('127.0.0.1')
    print("end time:",time.ctime())
