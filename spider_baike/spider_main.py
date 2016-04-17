#爬虫主程序

import url_manager,html_parser,html_download,html_out
class SpiderMain(object):

    def __init__(self):
        self.urls=url_manager.UrlManager()
        self.downloader = html_download.Htmldownloader()
        self.parser=html_parser.html_parser()
        self.outputer=html_out.HtmlOutputer()

    def craw(self,root_url):
        count=1
        self.urls.add_new_url(root_url)
        #增加root_url
        while self.urls.has_new_url():
            try:
                new_url=self.urls.get_new_url()
                #第一次时new_url为root_url,此后从new_urls中取出
                print("这是第%d个url：%s"  % (count,new_url))
                html_cont=self.downloader.download(new_url)
                #下载new_url页面内容,赋值为html_cont
                new_urls,new_data=self.parser.parse(new_url,html_cont)
                # print(new_urls,new_data)  得到所有新urls,得到页面的url,标题,简介
                self.urls.add_new_urls(new_urls)
                #将new_urls加入到self.urls.new_urls中
                self.outputer.collect_data(new_data)
                if count==5:
                    break
                count=count+1
            except:
                print('爬取失败')
        self.outputer.output_html()
print("测试开始")
if __name__=='__main__':
    root_url="http://baike.baidu.com/view/3402860.htm"
    obj_spider=SpiderMain()
    obj_spider.craw(root_url)
