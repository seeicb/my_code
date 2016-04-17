#html解析器
from bs4 import BeautifulSoup
import re
import urllib.parse
class html_parser(object):
    def _get_new_urls(self, page_url,soup):
    #函数得到所有新url
        new_urls=set()
        links=soup.find_all('a',href=re.compile(r"/view/\d+\.htm"))
        #取得页面中所有百科链接,形式为 /view/123456789.htm
        # print('打印links',links)
        for link in links:
            # print("打印每个link",link)
            # 结果为 <a href="/view/2828.htm" target="_blank">天津</a>
            new_url=link['href']  #取得链接中href内容
            #print('打印new_url',new_url) 结果:打印new_url /view/325108.htm
            #urljoin将相对路径转换为绝对路径
            new_full_url=urllib.parse.urljoin(page_url,new_url)
            # print('打印new_full_url',new_full_url) 将路径补全
            new_urls.add(new_full_url)
            #添加到new_urls中
        return new_urls
    def _get_new_data(self, page_url,soup):
        res_data={}
        res_data['url']=page_url
        #<dd class="lemmaWgt-lemmaTitle-title">
        title_node=soup.find('dd',class_="lemmaWgt-lemmaTitle-title").find('h1')
        res_data['title']=title_node.get_text()
        #<div label-module="lemmaSummary" class="lemma-summary">
        summary_node=soup.find('div',class_="lemma-summary")
        res_data['summary']=summary_node.get_text()
        # print(res_data)  res_data={url,标题,简介}
        return res_data

    def parse(self,page_url,html_cont):
    #self.parser.parse(new_url,html_cont)  page_url=new_url
        if page_url is None or html_cont is None:
            return
        soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf_8')
        # 解析html页面 print(soup)
        new_urls=self._get_new_urls(page_url,soup)
        # 得到页面中的所有新urls
        #print(new_urls)
        new_data=self._get_new_data(page_url,soup)
        #得到页面的url,标题,简介
        return new_urls,new_data
