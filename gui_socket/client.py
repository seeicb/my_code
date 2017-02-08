from tkinter import *
from encrypt import *
import socket,os,struct,threading,base64
from  tkinter.filedialog import *

def gui_tk():
    client=socket_init()
    window=Tk()
    window.title("Client")

    root=Frame(window)
    root.pack()

    chat=Text(root)
    chat.bind("<KeyPress>", lambda e : "break")
    chat.grid()

    sr_label=Label(root,text="输入：")
    sr_label.grid(sticky=W+S)

    msg=StringVar()
    input_box=Entry(root,width=80,textvariable=msg)
    input_box.grid(row=1,sticky=E)

    fs_button=Button(root,text="发送",command=lambda: send_to(chat,client,msg,input_box))
    fs_button.grid(row=2,sticky=W+S)

    file_button=Button(root,text="文件传输",command=lambda: tk_askopenfile(chat,client))
    file_button.grid(row=2,column=0,sticky=E+S)

    t = threading.Thread(target=accept_msg, args=(client,chat))
    t.start()
    window.mainloop()
def socket_init():
    host = socket.gethostname()
    port = 12345
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client

def tk_askopenfile(chat,client):
    file_flag="sendfileflag"
    filepath=askopenfilename()
    if os.path.isfile(filepath):
        print("准备发送文件")
        client.send(DesEncrypt(file_flag))
        fhead = struct.pack('128sl',os.path.basename(filepath).encode('utf-8'),os.stat(filepath).st_size)
        client.send(fileEncrypt(fhead))
        fo = open(filepath,'rb')
        while True:
            filedata = fo.read(20480)
            if not filedata:
                break
            client.send(fileEncrypt(filedata))
        fo.close()
        print("发送完成")
        chat.insert(END,"Clinet:已发送文件:%s\n"% filepath)
def send_to(chat,client,msg,input_box):
    cdata=msg.get()
    print("加密前：",cdata,"\n")
    cdata=DesEncrypt(cdata)
    print("加密后：",cdata,"\n")
    client.send(cdata)
    if cdata:
        chat.insert(END,"Client:"+msg.get()+"\n")
    input_box.delete(0,END)

def accept_msg(client,chat):

    while True:
        cdata=client.recv(65535)
        print("接受加密后字符：",cdata,"\n")
        cdata=DesDecrypt(cdata)
        print("解密后：",cdata,"\n")
        cdata=cdata.decode()
        if cdata=="sendfileflag":
            print("准备接受文件")
            buf = client.recv(65535)
            if buf:
                buf=DesDecrypt(buf)
                filename,filesize =struct.unpack('128sl',buf)
                filename_f = filename.strip(b"\00").decode('utf-8')
                filenewname = os.path.join('./',('new_'+ filename_f))
                print("文件名",filename_f,"文件大小",filesize)
                recvd_size = 0
                fo = open(filenewname,'wb')
                print("开始接受")
                while not recvd_size == filesize:
                    if filesize - recvd_size > 20488:
                        rdata = client.recv(20488)
                        rdata=DesDecrypt(rdata)
                        recvd_size += len(rdata)
                    else:
                        rdata = client.recv(20488)
                        rdata=DesDecrypt(rdata)
                        recvd_size = filesize
                    fo.write(rdata)
                fo.close()
                print("接受完成")
                cdata="已接受到文件:"+filename_f
        if cdata:
            chat.insert(END,"Server:"+cdata+"\n")



def main():
    gui_tk()
if __name__ == '__main__':
    main()
