import requests
import re
from bs4 import BeautifulSoup

spider = requests.session()
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
          }


def get_allurl():
    allurl = []
    tempurl = []
    for i in range(1, 5):
        url = 'http://www.wooyun.org/whitehats/do/1/page/' + str(i)
        html = spider.get(url, headers=header)
        soup = BeautifulSoup(html.text, 'html.parser')
        links = soup.find_all('a', href=re.compile("/whitehats/.*"))
        for link in links:
            ahref = 'http://www.wooyun.org' + link.get('href')
            tempurl.append(ahref)
    for element in tempurl:
        if ('http://www.wooyun.org/whitehats/do/' not in element) and ('http://www.wooyun.org/whitehats/' != element):
            allurl.append(element)
    return allurl


def get_data(allurl):
    # rank 帽子等级 个人主页
    all_hat_rank = []
    all_hat_level = []
    all_hat_page = []
    for url in allurl:
        html = spider.get(url, headers=header)
        soup = BeautifulSoup(html.text, 'html.parser')
        for tag in soup.find_all('ul', class_="time"):
            string = tag.get_text(strip=True)
        re_hat_level = re.search("\w{2}白帽子", string)
        all_hat_level.append(re_hat_level.group())
        re_rank_num = re.search("Rank:\s\d+", string)
        rank_temp = re_rank_num.group()
        rank_temp = int(rank_temp[6:])
        all_hat_rank.append(rank_temp)
        re_page = str(soup.find_all("a", rel="nofollow"))
        re_hat_page = re.search("href=\".+?rel", re_page, re.IGNORECASE)
        try:
            re_hat_page = re_hat_page.group()[6:-5]
        except:
            # print('错误页面:', url)
            re_hat_page = '没有获得主页'
        all_hat_page.append(re_hat_page)
        # 正则写的太烂了
    return(all_hat_rank, all_hat_level, all_hat_page)


def sort_by_rank(allurl, all_hat_rank, all_hat_level, all_hat_page):
    count = len(allurl)
    for i in range(0, count):
        for j in range(i + 1, count):
            if all_hat_level[i] < all_hat_level[j]:
                all_hat_level[i], all_hat_level[j] = all_hat_level[j], all_hat_level[i]
                allurl[i], allurl[j] = allurl[j], allurl[i]
                all_hat_rank[i], all_hat_rank[j] = all_hat_rank[j], all_hat_rank[i]
                all_hat_page[i], all_hat_page[j] = all_hat_page[j], all_hat_page[i]
    return (allurl, all_hat_rank, all_hat_level, all_hat_page)


def file_out(allurl, all_hat_rank, all_hat_level, all_hat_page):
    fout = open('out.html', 'w', )
    fout.write("<html>")
    fout.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
    fout.write("<body>")
    fout.write("<table>")
    for i in range(0, len(allurl)):
        fout.write("<tr>")
        fout.write("<td><a href=\" %s \" target=\"_blank\">%s</a></td>" %
                   (allurl[i], allurl[i][32:]))
        fout.write("<td>%s&nbsp;</td>" % all_hat_level[i])
        fout.write("<td>Rank:%d&nbsp;</td>" % all_hat_rank[i])
        fout.write("<td><a href=%s target=\"_blank\">%s</a></td>" %
                   (all_hat_page[i], all_hat_page[i]))
        fout.write("</tr>")
    fout.write("</table>")
    fout.write("</body>")
    fout.write("</html>")

    fout.close()


def main():
    print('获取所有白帽子链接中...')
    allurl = get_allurl()
    print('获取所有白帽子数据中...')
    all_hat_rank, all_hat_level, all_hat_page = get_data(allurl)
    print('排序中...')
    allurl, all_hat_rank, all_hat_level, all_hat_page = sort_by_rank(
        allurl, all_hat_rank, all_hat_level, all_hat_page)
    print('写入文件中...')
    file_out(allurl, all_hat_rank, all_hat_level, all_hat_page)
    print('一共得到%d个白帽子数据' % len(allurl))
    print('完成')
if __name__ == '__main__':
    main()
