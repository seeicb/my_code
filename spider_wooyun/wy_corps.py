import requests
import re
from bs4 import BeautifulSoup

spider = requests.session()
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36',
          }


def get_allurl()
:
    allurl = []
    tempurl = []
    for i in range(1, 45):
        url = 'http://www.wooyun.org/corps/page/' + str(i)
        html = spider.get(url, headers=header)
        soup = BeautifulSoup(html.text, 'html.parser')
        links = soup.find_all('a', href=re.compile("/corps/.*"))
        for link in links:
            ahref = 'http://www.wooyun.org' + link.get('href')
            tempurl.append(ahref)
    for element in tempurl:
        if ('http://www.wooyun.org/corps/page/' not in element) and ('http://www.wooyun.org/corps/' != element):
            allurl.append(element)
    return allurl


def get_data(allurl):
    all_corps_home = []
    all_corps_record = []
    for url in allurl:
        html = spider.get(url, headers=header)
        re_corps_home = re.search("主页：http:.*?</h3>", html.text)
        try:
            temp_home = re_corps_home.group()[3:-5]
        except:
            temp_home = "没有获取主页"
        all_corps_home.append(temp_home)
        re_corps_record = re.search("\d+ 条纪录", html.text)
        record_temp = int(re_corps_record.group()[:-4])
        all_corps_record.append(record_temp)
    return(all_corps_home, all_corps_record)


def sort_by_record(allurl,  all_corps_home, all_corps_record):
    count = len(allurl)
    for i in range(0, count):
        for j in range(i + 1, count):
            if all_corps_record[i] < all_corps_record[j]:
                all_corps_record[i], all_corps_record[j] = all_corps_record[j], all_corps_record[i]
                all_corps_home[i], all_corps_home[j] = all_corps_home[j], all_corps_home[i]
                allurl[i], allurl[j] = allurl[j], allurl[i]
    return (allurl, all_corps_home, all_corps_record)


def file_out(allurl, all_corps_home, all_corps_record):
    fout = open('corps.html', 'w', )
    fout.write("<html>")
    fout.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
    fout.write("<body>")
    fout.write("<table>")
    for i in range(0, len(allurl)):
        fout.write("<tr>")
        fout.write("<td><a href=\" %s \" target=\"_blank\">%s</a></td>" %
                   (allurl[i], allurl[i][28:]))
        fout.write("<td>记录:%s&nbsp;</td>" % all_corps_record[i])
        fout.write("<td><a href=%s target=\"_blank\">%s</a></td>" %
                   (all_corps_home[i], all_corps_home[i]))
        fout.write("</tr>")
    fout.write("</table>")
    fout.write("</body>")
    fout.write("</html>")

    fout.close()


def main():
    print("获取厂商链接中...")
    allurl = get_allurl()
    print("获取厂商数据...")
    all_corps_home, all_corps_record = get_data(allurl)
    print("排序在...")
    allurl, all_corps_home, all_corps_record = sort_by_record(
        allurl,  all_corps_home, all_corps_record)
    print("写入文件中...")
    file_out(allurl, all_corps_home, all_corps_record)


if __name__ == '__main__':
    main()
