import threading
import queue
import socket
import time

port_queue=queue.Queue()
num_threads=100
global IP
IP='123.147.190.11'

def scan_port(IP,port_queue):
    while True:
        PORT=port_queue.get()
        # print(IP,PORT)
        # try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result=s.connect_ex((IP,PORT))
        if result == 0:
            print("**", IP,":",PORT)
        else:
            pass
        #     print(PORT,'未开放')
        s.close()
        port_queue.task_done()
def main():
    print("Begin time:", time.ctime())
    for i in range(1,65535):
        port_queue.put(i)
    for i in range(num_threads):
        scan=threading.Thread(target=scan_port,args=(IP,port_queue))
        scan.setDaemon(True)
        scan.start()
    port_queue.join()
    print("End time:", time.ctime())
if __name__ == '__main__':
    main()
